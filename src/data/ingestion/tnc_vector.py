"""
TNC Vector Ingester - IERC-GNL
===============================
Ingesta de capas vectoriales TNC (Shapefile/GeoJSON) → H3 grid.
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from typing import Iterator, Optional, List, Dict, Any
import zipfile
import tempfile
import logging

from .base import BaseIngester, IngestionConfig
from src.utils.h3 import vector_to_h3_grid
from src.utils.logging import setup_logging
from config import get_raw_dir

logger = setup_logging(__name__)


class TNCVectorIngester(BaseIngester):
    """
    Ingester para capas vectoriales de The Nature Conservancy.
    
    Capas soportadas:
    - Bajos marinos (Polígonos)
    - Arrecifes de coral negro (Polígonos)
    - Otras capas vectoriales TNC
    
    Convierte geometrías a grid H3 con pesos de área para joins espaciales precisos.
    """
    
    def __init__(self, 
                 config: IngestionConfig,
                 catalog,
                 storage,
                 source_dir: str = None,
                 layers: List[str] = None,
                 h3_resolution: int = 8):
        super().__init__(config, catalog, storage)
        
        if source_dir is None:
            source_dir = str(get_raw_dir("tnc"))
        
        self.source_dir = Path(source_dir)
        self.layers = layers or ["bajos_marinos", "arrecifes_coral_negro"]
        self.h3_resolution = h3_resolution
        self._layer_files = self._discover_layer_files()
    
    def _discover_layer_files(self) -> Dict[str, Path]:
        """Descubre archivos de capas en el directorio fuente."""
        files = {}
        
        # Buscar archivos ZIP (shapefiles)
        for zip_file in self.source_dir.glob("*.zip"):
            name = zip_file.stem.lower()
            if 'bajos' in name or 'bajo' in name:
                files['bajos_marinos'] = zip_file
            elif 'arrecife' in name or 'coral' in name or 'negro' in name:
                files['arrecifes_coral_negro'] = zip_file
            else:
                # Usar nombre del archivo como clave
                files[name] = zip_file
        
        # Buscar GeoJSON sueltos
        for geojson_file in self.source_dir.glob("*.geojson"):
            name = geojson_file.stem.lower()
            if name not in files:
                files[name] = geojson_file
        
        logger.info(f"Capas TNC descubiertas: {list(files.keys())}")
        return files
    
    def extract(self) -> Iterator[pd.DataFrame]:
        """Extrae y convierte cada capa a H3 grid."""
        
        for layer_name in self.layers:
            if layer_name not in self._layer_files:
                logger.warning(f"Capa no encontrada: {layer_name}")
                continue
            
            file_path = self._layer_files[layer_name]
            logger.info(f"Procesando capa TNC: {layer_name} desde {file_path.name}")
            
            try:
                gdf = self._read_vector_file(file_path)
                if gdf is None or gdf.empty:
                    logger.warning(f"Capa vacía o error leyendo: {layer_name}")
                    continue
                
                # Añadir metadatos de capa
                gdf['tnc_layer'] = layer_name
                gdf['source_file'] = file_path.name
                
                # Convertir a H3 grid con pesos de área
                h3_grid = vector_to_h3_grid(gdf, resolution=self.h3_resolution, area_weight=True)
                
                if h3_grid.empty:
                    logger.warning(f"Capa {layer_name} no generó celdas H3")
                    continue
                
                # Añadir columnas de partición
                h3_grid['year'] = 2024  # Capas estáticas
                h3_grid['month'] = 1
                h3_grid['time_partition'] = '2024-01'
                
                # Convertir geometría a WKT para almacenamiento en Parquet
                h3_grid['h3_geometry_wkt'] = h3_grid['geometry'].apply(lambda g: g.wkt)
                h3_grid = h3_grid.drop(columns=['geometry'])
                
                yield h3_grid
                
            except Exception as e:
                logger.error(f"Error procesando capa {layer_name}: {e}")
                self.errors.append(f"{layer_name}: {e}")
                continue
    
    def _read_vector_file(self, file_path: Path) -> Optional[gpd.GeoDataFrame]:
        """Lee archivo vectorial (ZIP shapefile o GeoJSON)."""
        
        if file_path.suffix.lower() == '.zip':
            # Extraer shapefile de ZIP
            with tempfile.TemporaryDirectory() as tmpdir:
                with zipfile.ZipFile(file_path, 'r') as zf:
                    zf.extractall(tmpdir)
                
                # Buscar .shp
                shp_files = list(Path(tmpdir).rglob("*.shp"))
                if not shp_files:
                    logger.error(f"No se encontró .shp en {file_path}")
                    return None
                
                gdf = gpd.read_file(shp_files[0])
                
        elif file_path.suffix.lower() in ['.geojson', '.json']:
            gdf = gpd.read_file(file_path)
            
        else:
            logger.error(f"Formato no soportado: {file_path.suffix}")
            return None
        
        # Asegurar CRS WGS84
        if gdf.crs is None:
            logger.warning(f"CRS no definido en {file_path}, asumiendo EPSG:4326")
            gdf.set_crs("EPSG:4326", inplace=True)
        elif gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")
        
        # Validar geometrías
        gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty]
        
        logger.debug(f"  Leídas {len(gdf)} features de {file_path.name}")
        return gdf
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforma H3 grid a formato estandarizado."""
        
        # df ya viene como H3 grid desde extract()
        # Solo asegurar columnas estándar
        
        df = df.copy()
        
        # Renombrar h3_cell si viene con otro nombre
        if 'h3_cell' not in df.columns and 'h3' in df.columns:
            df = df.rename(columns={'h3': 'h3_cell'})
        
        # Seleccionar columnas finales
        # Mantener todas las propiedades originales + h3_cell + h3_geometry + time_partition
        standard_cols = ['h3_cell', 'h3_geometry', 'tnc_layer', 'source_file', 
                        'year', 'month', 'time_partition', 'area_fraction', 'source_index']
        
        # Añadir propiedades originales que existan
        extra_cols = [c for c in df.columns if c not in standard_cols]
        output_cols = standard_cols + extra_cols
        
        # Solo incluir columnas que existan
        output_cols = [c for c in output_cols if c in df.columns]
        
        return df[output_cols]
    
    def _get_partition_path(self, df: pd.DataFrame) -> str:
        if df.empty:
            return "tnc/unknown/"
        
        layer = df['tnc_layer'].iloc[0] if 'tnc_layer' in df.columns else 'unknown'
        return f"tnc/{layer}_h3/h3_{self.h3_resolution}={{h3_cell}}/"


def create_tnc_ingester(catalog, storage, layer_name: str, config_overrides: Dict = None) -> TNCVectorIngester:
    """Factory para crear ingester TNC para una capa específica."""
    
    dataset_map = {
        "bajos_marinos": "tnc_bajos_marinos",
        "arrecifes_coral_negro": "tnc_arrecifes_coral_negro"
    }
    
    dataset_name = dataset_map.get(layer_name, f"tnc_{layer_name}")
    
    base_config = IngestionConfig(
        dataset_name=dataset_name,
        layer="silver",
        partition_cols=["tnc_layer"],  # Solo por capa, NO por h3_cell
        h3_resolution=8,
        bbox=(22.5, -115.0, 32.0, -108.0),
        compression="zstd",
        batch_size=50000,
        validate=True
    )
    
    if config_overrides:
        for k, v in config_overrides.items():
            setattr(base_config, k, v)
    
    return TNCVectorIngester(
        config=base_config,
        catalog=catalog,
        storage=storage,
        layers=[layer_name]
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("TNC Vector Ingester module loaded")