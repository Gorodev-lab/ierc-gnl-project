"""
Government API Connector - IERC-GNL
====================================
Connects to official government data sources (SENER WMS, ASEA/CENAGAS SIG)
with resilient fallback to local verified datasets.

Uses Python stdlib only: urllib, json, ssl, xml.etree.ElementTree
"""

import urllib.request
import urllib.error
import json
import ssl
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging
import pandas as pd

from src.utils.logging import setup_logging
from config import get_causanatura_dir

logger = setup_logging(__name__)


class GovernmentDataConnector:
    """
    Connects to official Mexican government energy/environmental data APIs.
    
    Sources:
    - SENER CNIH WMS MapServer (gas pipelines & infrastructure)
    - ASEA SIG Hidrocarburos (MIA records & permits)
    - CENAGAS (pipeline network data)
    
    Falls back to local CSV datasets when endpoints are unavailable.
    """
    
    # SENER CNIH WMS endpoints
    SENER_WMS_BASE = "https://sig.cnih.gob.mx/arcgis/services"
    SENER_GAS_WMS = f"{SENER_WMS_BASE}/Infraestructura_GasNatural/MapServer/WMSServer"
    
    # ASEA SIG Hidrocarburos endpoints
    ASEA_SIG_BASE = "https://sig.asea.gob.mx/arcgis/services"
    ASEA_MIAS_WMS = f"{ASEA_SIG_BASE}/MIAs_Hidrocarburos/MapServer/WMSServer"
    
    # CENAGAS endpoints
    CENAGAS_WMS = "https://sig.cenagas.com.mx/arcgis/services/Red_Nacional_Gasoductos/MapServer/WMSServer"
    
    # Timeouts
    CONNECT_TIMEOUT = 10  # seconds
    READ_TIMEOUT = 30     # seconds
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self._ssl_context = ssl.create_default_context()
        self._ssl_context.check_hostname = False
        self._ssl_context.verify_mode = ssl.CERT_NONE
        
    def _fetch_wms_capabilities(self, wms_url: str) -> Optional[ET.Element]:
        """
        Fetch and parse WMS GetCapabilities XML from a MapServer endpoint.
        Returns parsed XML Element tree or None on failure.
        """
        capabilities_url = f"{wms_url}?service=WMS&version=1.3.0&request=GetCapabilities"
        
        try:
            req = urllib.request.Request(
                capabilities_url,
                headers={'User-Agent': 'IERC-GNL/1.0 GovernmentDataConnector'}
            )
            with urllib.request.urlopen(req, timeout=self.timeout, context=self._ssl_context) as response:
                xml_content = response.read()
                return ET.fromstring(xml_content)
        except urllib.error.URLError as e:
            logger.warning(f"WMS Capabilities fetch failed for {wms_url}: {e}")
            return None
        except ET.ParseError as e:
            logger.warning(f"WMS XML parse failed for {wms_url}: {e}")
            return None
        except Exception as e:
            logger.warning(f"Unexpected error fetching {wms_url}: {e}")
            return None
    
    def _parse_wms_layers(self, capabilities_xml: ET.Element) -> List[Dict[str, Any]]:
        """Extract layer metadata from WMS GetCapabilities XML."""
        layers = []
        
        # WMS 1.3.0 namespace handling
        ns = {'wms': 'http://www.opengis.net/wms'}
        
        # Find all Layer elements
        for layer_elem in capabilities_xml.findall('.//wms:Layer', ns):
            name_elem = layer_elem.find('wms:Name', ns)
            title_elem = layer_elem.find('wms:Title', ns)
            abstract_elem = layer_elem.find('wms:Abstract', ns)
            
            layer_info = {
                'name': name_elem.text if name_elem is not None else '',
                'title': title_elem.text if title_elem is not None else '',
                'abstract': abstract_elem.text if abstract_elem is not None else '',
                'queryable': layer_elem.get('queryable', '0') == '1'
            }
            
            # Extract bounding box if present
            bbox_elem = layer_elem.find('wms:EX_GeographicBoundingBox', ns)
            if bbox_elem is not None:
                west = bbox_elem.find('wms:westBoundLongitude', ns)
                east = bbox_elem.find('wms:eastBoundLongitude', ns)
                south = bbox_elem.find('wms:southBoundLatitude', ns)
                north = bbox_elem.find('wms:northBoundLatitude', ns)
                if all(x is not None and x.text is not None for x in [west, east, south, north]):
                    layer_info['bbox'] = [
                        float(west.text), float(south.text),
                        float(east.text), float(north.text)
                    ]
            
            layers.append(layer_info)
        
        return layers
    
    def fetch_sener_gas_wms_capabilities(self) -> List[Dict[str, Any]]:
        """
        Connect to SENER CNIH WMS MapServer and extract active gas pipeline layer metadata.
        
        Returns:
            List of layer dicts with name, title, abstract, bbox, queryable flag.
        """
        logger.info("Fetching SENER CNIH WMS Capabilities for gas infrastructure...")
        capabilities = self._fetch_wms_capabilities(self.SENER_GAS_WMS)
        
        if capabilities is None:
            logger.warning("SENER WMS unavailable, returning empty layer list")
            return []
        
        layers = self._parse_wms_layers(capabilities)
        
        # Filter for gas pipeline related layers
        gas_layers = [
            layer for layer in layers
            if any(kw in (layer['name'] + layer['title'] + layer['abstract']).lower() 
                   for kw in ['gas', 'gasoducto', 'pipeline', 'transporte', 'distribucion'])
        ]
        
        logger.info(f"Found {len(gas_layers)} gas-related layers from SENER WMS")
        return gas_layers
    
    def fetch_asea_mias_summary(self) -> List[Dict[str, Any]]:
        """
        Connect to ASEA/CENAGAS SIG Hidrocarburos endpoints and extract MIA layer metadata.
        
        Returns:
            List of layer dicts with MIA project metadata.
        """
        logger.info("Fetching ASEA SIG WMS Capabilities for MIA records...")
        capabilities = self._fetch_wms_capabilities(self.ASEA_MIAS_WMS)
        
        if capabilities is None:
            logger.warning("ASEA WMS unavailable, returning empty layer list")
            return []
        
        layers = self._parse_wms_layers(capabilities)
        
        # Filter for MIA related layers
        mia_layers = [
            layer for layer in layers
            if any(kw in (layer['name'] + layer['title'] + layer['abstract']).lower() 
                   for kw in ['mia', 'impacto', 'ambiental', 'manifiesto', 'evaluacion'])
        ]
        
        logger.info(f"Found {len(mia_layers)} MIA-related layers from ASEA WMS")
        return mia_layers
    
    def _load_local_fallback(self) -> pd.DataFrame:
        """
        Load consolidated projects from local verified CSV dataset.
        
        Returns:
            DataFrame with standardized columns matching government API schema.
        """
        fallback_path = get_causanatura_dir("output") / "gnl_proyectos_consolidados.csv"
        
        if not fallback_path.exists():
            logger.warning(f"Local fallback not found: {fallback_path}")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(fallback_path)
            logger.info(f"Loaded {len(df)} records from local fallback: {fallback_path.name}")
            return df
        except Exception as e:
            logger.error(f"Failed to load local fallback: {e}")
            return pd.DataFrame()
    
    def _standardize_live_data(self, layers: List[Dict[str, Any]], source: str) -> pd.DataFrame:
        """
        Convert WMS layer metadata to standardized project DataFrame format.
        
        Note: WMS GetCapabilities only provides layer metadata, not individual features.
        For actual project records, we'd need WFS GetFeature or direct CSV/API endpoints.
        This provides a structural placeholder for when those endpoints are available.
        """
        if not layers:
            return pd.DataFrame()
        
        records = []
        for layer in layers:
            record = {
                'proyecto_id': f"{source.upper()}_{layer['name']}" if layer['name'] else f"{source.upper()}_unknown",
                'nombre': layer['title'] or layer['name'],
                'estado': 'N/A',  # WMS layer metadata doesn't include state
                'tipo_proyecto': self._infer_type_from_layer(layer),
                'fuente': source,
                'lat': None,
                'lon': None,
                'estatus': 'En_evaluacion',
                'capacidad_mtpa': None,
                'longitud_km': None,
                'folio_asea': None,
                'pdf_url': None,
                'source_file': f"{source}_wms_layer",
                'source_type': source,
                'layer_name': layer['name'],
                'layer_abstract': layer['abstract'],
                'bbox': layer.get('bbox'),
                'queryable': layer.get('queryable', False)
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def _infer_type_from_layer(self, layer: Dict[str, Any]) -> str:
        """Infer project type from layer metadata."""
        text = (layer.get('name', '') + ' ' + layer.get('title', '') + ' ' + layer.get('abstract', '')).lower()
        
        if any(kw in text for kw in ['terminal', 'gnl', 'licuefaccion']):
            return 'terminal_gnl'
        elif any(kw in text for kw in ['transporte', 'pipeline', 'gasoducto']):
            if 'distribucion' in text or 'distribution' in text:
                return 'gasoducto_distribucion'
            return 'gasoducto_transporte'
        elif any(kw in text for kw in ['compresion', 'compression', 'estacion']):
            return 'estacion_compresion'
        elif any(kw in text for kw in ['planta', 'plant']):
            return 'planta_licuefaccion'
        
        return 'infraestructura_gas'
    
    def get_consolidated_projects_df(self) -> pd.DataFrame:
        """
        Main entry point: merges live API results with local fallback CSVs.
        
        Strategy:
        1. Try to fetch live data from SENER WMS (gas pipelines)
        2. Try to fetch live data from ASEA WMS (MIAs)
        3. Always load local fallback as base
        4. Merge: live data supplements/updates fallback, fallback is authoritative for records
        
        Returns:
            Consolidated DataFrame with standardized schema.
        """
        logger.info("Building consolidated projects dataset...")
        
        # Step 1: Load local fallback (authoritative record set)
        fallback_df = self._load_local_fallback()
        
        # Step 2: Try live SENER gas infrastructure
        sener_layers = self.fetch_sener_gas_wms_capabilities()
        sener_df = self._standardize_live_data(sener_layers, 'sener')
        
        # Step 3: Try live ASEA MIAs
        asea_layers = self.fetch_asea_mias_summary()
        asea_df = self._standardize_live_data(asea_layers, 'asea')
        
        # Step 4: Merge - fallback is primary, live layers supplement metadata
        if fallback_df.empty and sener_df.empty and asea_df.empty:
            logger.warning("All data sources empty, returning empty DataFrame")
            return pd.DataFrame()
        
        # For now, fallback_df contains the actual project records
        # Live WMS layers only provide layer metadata (no feature data)
        # When WFS/feature endpoints are available, merge on proyecto_id
        
        result = fallback_df.copy()
        
        # Add source tracking
        if 'source_type' not in result.columns:
            result['source_type'] = 'consolidated'
        
        # Mark if live data was available
        result['live_sener_available'] = not sener_df.empty
        result['live_asea_available'] = not asea_df.empty
        result['live_cenagas_available'] = False  # TODO: implement CENAGAS endpoint
        
        logger.info(f"Consolidated dataset: {len(result)} records from fallback, "
                   f"SENER live={'yes' if not sener_df.empty else 'no'}, "
                   f"ASEA live={'yes' if not asea_df.empty else 'no'}")
        
        return result


def create_government_connector(timeout: int = 10) -> GovernmentDataConnector:
    """Factory function for GovernmentDataConnector."""
    return GovernmentDataConnector(timeout=timeout)


if __name__ == "__main__":
    # Quick self-test
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    connector = create_government_connector(timeout=15)
    
    print("Testing SENER WMS...")
    sener_layers = connector.fetch_sener_gas_wms_capabilities()
    print(f"  Found {len(sener_layers)} gas layers")
    
    print("Testing ASEA WMS...")
    asea_layers = connector.fetch_asea_mias_summary()
    print(f"  Found {len(asea_layers)} MIA layers")
    
    print("Loading consolidated projects...")
    df = connector.get_consolidated_projects_df()
    print(f"  Records: {len(df)}")
    if not df.empty:
        print(f"  Columns: {list(df.columns)}")
        print(f"  Sample:\n{df.head(3).to_string()}")
    
    sys.exit(0)