"""
Unit tests for GovernmentDataConnector - IERC-GNL
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
import xml.etree.ElementTree as ET
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data.connectors.government_api import (
    GovernmentDataConnector,
    create_government_connector,
)


class TestGovernmentDataConnector:
    """Test GovernmentDataConnector initialization and configuration."""
    
    def test_connector_initialization_default_timeout(self):
        """Test connector initializes with default timeout."""
        connector = GovernmentDataConnector()
        assert connector.timeout == 10
        assert connector._ssl_context is not None
    
    def test_connector_initialization_custom_timeout(self):
        """Test connector initializes with custom timeout."""
        connector = GovernmentDataConnector(timeout=20)
        assert connector.timeout == 20
    
    def test_factory_function(self):
        """Test factory function returns connector instance."""
        connector = create_government_connector(timeout=15)
        assert isinstance(connector, GovernmentDataConnector)
        assert connector.timeout == 15


class TestWMSCapabilitiesParsing:
    """Test WMS GetCapabilities XML parsing."""
    
    @pytest.fixture
    def sample_wms_capabilities(self):
        """Sample WMS 1.3.0 GetCapabilities XML response."""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<WMS_Capabilities version="1.3.0" xmlns="http://www.opengis.net/wms">
  <Service>
    <Name>WMS</Name>
    <Title>SENER Gas Infrastructure</Title>
  </Service>
  <Capability>
    <Layer>
      <Name>gas_pipelines</Name>
      <Title>Gas Natural Pipelines</Title>
      <Abstract>Active gas transportation pipelines in Mexico</Abstract>
      <EX_GeographicBoundingBox>
        <westBoundLongitude>-118.0</westBoundLongitude>
        <eastBoundLongitude>-86.0</eastBoundLongitude>
        <southBoundLatitude>14.0</southBoundLatitude>
        <northBoundLatitude>33.0</northBoundLatitude>
      </EX_GeographicBoundingBox>
    </Layer>
    <Layer>
      <Name>terminal_gnl</Name>
      <Title>GNL Terminals</Title>
      <Abstract>Liquefied Natural Gas terminals</Abstract>
      <EX_GeographicBoundingBox>
        <westBoundLongitude>-117.5</westBoundLongitude>
        <eastBoundLongitude>-87.0</eastBoundLongitude>
        <southBoundLatitude>15.0</southBoundLatitude>
        <northBoundLatitude>32.0</northBoundLatitude>
      </EX_GeographicBoundingBox>
    </Layer>
    <Layer>
      <Name>water_bodies</Name>
      <Title>Water Bodies</Title>
      <Abstract>Lakes and rivers</Abstract>
    </Layer>
  </Capability>
</WMS_Capabilities>'''
    
    def test_parse_wms_layers_extracts_all_layers(self, sample_wms_capabilities):
        """Test parsing extracts all layer metadata."""
        connector = GovernmentDataConnector()
        root = ET.fromstring(sample_wms_capabilities)
        layers = connector._parse_wms_layers(root)
        
        assert len(layers) == 3
        assert layers[0]['name'] == 'gas_pipelines'
        assert layers[0]['title'] == 'Gas Natural Pipelines'
        assert layers[0]['abstract'] == 'Active gas transportation pipelines in Mexico'
        assert layers[0]['bbox'] == [-118.0, 14.0, -86.0, 33.0]
        assert layers[0]['queryable'] == False  # default
        
    def test_parse_wms_layers_handles_missing_bbox(self, sample_wms_capabilities):
        """Test parsing handles layers without bounding box."""
        connector = GovernmentDataConnector()
        root = ET.fromstring(sample_wms_capabilities)
        layers = connector._parse_wms_layers(root)
        
        # Third layer has no bbox
        assert 'bbox' not in layers[2] or layers[2].get('bbox') is None
    
    def test_parse_wms_layers_empty_capabilities(self):
        """Test parsing empty capabilities returns empty list."""
        connector = GovernmentDataConnector()
        root = ET.fromstring('<WMS_Capabilities><Capability><Layer/></Capability></WMS_Capabilities>')
        layers = connector._parse_wms_layers(root)
        assert layers == []


class TestGovernmentAPIFetching:
    """Test live government API fetching with mocked responses."""
    
    @patch('src.data.connectors.government_api.urllib.request.urlopen')
    def test_fetch_sener_wms_success(self, mock_urlopen):
        """Test successful SENER WMS fetch returns filtered gas layers."""
        # Mock XML response
        mock_xml = '''<?xml version="1.0"?>
<WMS_Capabilities xmlns="http://www.opengis.net/wms">
  <Capability>
    <Layer>
      <Name>gas_pipeline_layer</Name>
      <Title>Gas Pipeline</Title>
      <Abstract>Main gas transportation pipeline</Abstract>
    </Layer>
    <Layer>
      <Name>water_layer</Name>
      <Title>Water</Title>
      <Abstract>Water bodies</Abstract>
    </Layer>
  </Capability>
</WMS_Capabilities>'''
        mock_response = MagicMock()
        mock_response.read.return_value = mock_xml.encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        connector = GovernmentDataConnector(timeout=5)
        layers = connector.fetch_sener_gas_wms_capabilities()
        
        assert len(layers) == 1
        assert layers[0]['name'] == 'gas_pipeline_layer'
        mock_urlopen.assert_called_once()
    
    @patch('src.data.connectors.government_api.urllib.request.urlopen')
    def test_fetch_sener_wms_timeout_returns_empty(self, mock_urlopen):
        """Test timeout returns empty list instead of raising."""
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("Timeout")
        
        connector = GovernmentDataConnector(timeout=5)
        layers = connector.fetch_sener_gas_wms_capabilities()
        
        assert layers == []
    
    @patch('src.data.connectors.government_api.urllib.request.urlopen')
    def test_fetch_asea_wms_success(self, mock_urlopen):
        """Test successful ASEA WMS fetch returns MIA layers."""
        mock_xml = '''<?xml version="1.0"?>
<WMS_Capabilities xmlns="http://www.opengis.net/wms">
  <Capability>
    <Layer>
      <Name>mia_hidrocarburos</Name>
      <Title>MIAs Hidrocarburos</Title>
      <Abstract>Manifestaciones de Impacto Ambiental</Abstract>
    </Layer>
  </Capability>
</WMS_Capabilities>'''
        mock_response = MagicMock()
        mock_response.read.return_value = mock_xml.encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        connector = GovernmentDataConnector(timeout=5)
        layers = connector.fetch_asea_mias_summary()
        
        assert len(layers) == 1
        assert 'mia' in layers[0]['name'].lower()


class TestLocalFallback:
    """Test local CSV fallback loading."""
    
    @patch('src.data.connectors.government_api.get_causanatura_dir')
    @patch('pandas.read_csv')
    def test_load_local_fallback_success(self, mock_read_csv, mock_get_dir):
        """Test loading local fallback CSV."""
        mock_path = Path("/fake/path")
        mock_get_dir.return_value = mock_path
        mock_df = pd.DataFrame({'proyecto_id': ['P1', 'P2'], 'nombre': ['Proj1', 'Proj2']})
        mock_read_csv.return_value = mock_df
        
        # Need to mock path.exists() to return True
        with patch.object(Path, 'exists', return_value=True):
            connector = GovernmentDataConnector()
            df = connector._load_local_fallback()
        
        assert len(df) == 2
        assert list(df.columns) == ['proyecto_id', 'nombre']
        mock_read_csv.assert_called_once()
    
    @patch('src.data.connectors.government_api.get_causanatura_dir')
    def test_load_local_fallback_missing_file(self, mock_get_dir):
        """Test missing fallback file returns empty DataFrame."""
        mock_get_dir.return_value = Path("/nonexistent")
        
        connector = GovernmentDataConnector()
        df = connector._load_local_fallback()
        
        assert df.empty


class TestConsolidatedProjects:
    """Test consolidated projects DataFrame generation."""
    
    @patch.object(GovernmentDataConnector, 'fetch_sener_gas_wms_capabilities')
    @patch.object(GovernmentDataConnector, 'fetch_asea_mias_summary')
    @patch.object(GovernmentDataConnector, '_load_local_fallback')
    def test_get_consolidated_projects_fallback_only(self, mock_fallback, mock_asea, mock_sener):
        """Test consolidated projects uses fallback when live APIs empty."""
        mock_sener.return_value = []
        mock_asea.return_value = []
        mock_fallback.return_value = pd.DataFrame({
            'proyecto_id': ['P1', 'P2'],
            'nombre': ['Project 1', 'Project 2'],
            'lat': [20.0, 21.0],
            'lon': [-100.0, -101.0],
        })
        
        connector = GovernmentDataConnector()
        df = connector.get_consolidated_projects_df()
        
        assert len(df) == 2
        assert 'live_sener_available' in df.columns
        assert 'live_asea_available' in df.columns
        assert df['live_sener_available'].iloc[0] == False
        assert df['live_asea_available'].iloc[0] == False
    
    @patch.object(GovernmentDataConnector, 'fetch_sener_gas_wms_capabilities')
    @patch.object(GovernmentDataConnector, 'fetch_asea_mias_summary')
    @patch.object(GovernmentDataConnector, '_load_local_fallback')
    def test_get_consolidated_projects_with_live_data(self, mock_fallback, mock_asea, mock_sener):
        """Test consolidated projects marks live data availability."""
        mock_sener.return_value = [{'name': 'layer1', 'title': 'Gas Layer', 'abstract': 'gas pipeline'}]
        mock_asea.return_value = [{'name': 'mia1', 'title': 'MIA Layer', 'abstract': 'impacto ambiental'}]
        mock_fallback.return_value = pd.DataFrame({
            'proyecto_id': ['P1'],
            'nombre': ['Project 1'],
        })
        
        connector = GovernmentDataConnector()
        df = connector.get_consolidated_projects_df()
        
        assert len(df) == 1
        assert df['live_sener_available'].iloc[0] == True
        assert df['live_asea_available'].iloc[0] == True


class TestStandardizeLiveData:
    """Test live WMS layer to DataFrame conversion."""
    
    def test_standardize_live_data_infers_types(self):
        """Test type inference from layer metadata."""
        connector = GovernmentDataConnector()
        
        layers = [
            {'name': 'terminal_gnl_altamira', 'title': 'Terminal GNL Altamira', 'abstract': 'LNG terminal'},
            {'name': 'gasoducto_transporte_norte', 'title': 'Gasoducto Norte', 'abstract': 'Transporte gas natural'},
            {'name': 'estacion_compresion_1', 'title': 'Estación Compresión', 'abstract': 'Compression station'},
            {'name': 'unknown_layer', 'title': 'Unknown', 'abstract': 'Some layer'},
        ]
        
        df = connector._standardize_live_data(layers, 'sener')
        
        assert len(df) == 4
        assert df.iloc[0]['tipo_proyecto'] == 'terminal_gnl'
        assert df.iloc[1]['tipo_proyecto'] == 'gasoducto_transporte'
        assert df.iloc[2]['tipo_proyecto'] == 'estacion_compresion'
        assert df.iloc[3]['tipo_proyecto'] == 'infraestructura_gas'
        assert all(df['fuente'] == 'sener')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])