#!/usr/bin/env python3
"""
Bathymetry Ingester - IERC-GNL
==============================
Procesa batimetría ETOPO1 (GeoTIFF) y GEBCO (GPKG) → H3 multi-resolución.
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Iterator, Optional, List, Dict, Any, Tuple
import logging

from .base import BaseIngester, IngestionConfig
from src.utils.h3 import vector_to_h3_grid
from src.utils.logging import setup_logging
from config import get_causanatura_dir

logger = setup_logging(__name__)

# Bounding box Golfo de California
MIN_LAT, MAX_LAT = 22.5, 32.0
MIN_LON, MAX_LON = -115.0, -108.0


class BathymetryIngester(BaseIngester):
    """
    Ingester para modelos batimétricos (ETOPO1, GEBCO).
    
    Extrae estadísticas por celda H3 a múltiples resoluciones.
    """
    
    def __init__(self, 
                 config: IngestionConfig,
                 catalog,
                 storage,
                 source_paths: Dict[str, str],
                 h3_resolutions: List[int] = None,
                 stats: List[str] = None):
        super().__init__(config, catalog, storage)
        self.source_paths = source_paths
        self.h3_resolutions = h3_resolutions or [8, 9, 10]
        self.stats = stats or ['mean', 'min', 'max', 'std', 'count']
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforma datos crudos a formato estandarizado."""
        df = df.copy()
        
        # Asegurar columnas temporales
        if 'year' not in df.columns:
            df['year'] = 2024
        if 'month' not in df.columns:
            df['month'] = 1
        if 'time_partition' not in df.columns:
            df['time_partition'] = '2024-01'
        
        # Renombrar columnas de profundidad
        rename_map = {}
        if 'depth_mean' in df.columns:
            rename_map['depth_mean'] = 'bathymetry_mean'
        if 'depth_min' in df.columns:
            rename_map['depth_min'] = 'bathymetry_min'
        if 'depth_max' in df.columns:
            rename_map['depth_max'] = 'bathymetry_max'
        if 'depth_std' in df.columns:
            rename_map['depth_std'] = 'bathymetry_std'
        if 'depth_count' in df.columns:
            rename_map['depth_count'] = 'bathymetry_count'
        if 'depth_value' in df.columns:
            rename_map['depth_value'] = 'bathymetry_value'
        
        if rename_map:
            df = df.rename(columns=rename_map)
        
        return df
    
    def extract(self) -> Iterator[pd.DataFrame]:
        """Extrae estadísticas de batimetría por H3 cell para cada fuente y resolución."""
        
        for source_name, source_path in self.source_paths.items():
            path = Path(source_path)
            if not path.exists():
                logger.warning(f"Archivo no encontrado: {path}")
                continue
            
            logger.info(f"Procesando batimetría: {source_name} desde {path.name}")
            
            if path.suffix.lower() in ['.tif', '.tiff']:
                yield from self._process_geotiff(source_name, path)
            elif path.suffix.lower() == '.gpkg':
                yield from self._process_gpkg(source_name, path)
            else:
                logger.warning(f"Formato no soportado: {path.suffix}")
    
    def _process_gpkg(self, source_name: str, path: Path) -> Iterator[pd.DataFrame]:
        """Procesa GeoPackage vectorizado (contornos batimétricos GEBCO)."""
        gdf = gpd.read_file(path)
        
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")
        
        # Filtrar solo líneas dentro del bbox del Golfo
        gdf = gdf.cx[MIN_LON:MAX_LON, MIN_LAT:MAX_LAT]
        
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")
        
        # Identificar columnas de profundidad
        depth_cols = [c for c in gdf.columns if 'depth' in c.lower() or 'elev' in c.lower() or 'bath' in c.lower()]
        if not depth_cols:
            numeric_cols = gdf.select_dtypes(include=[np.number]).columns.tolist()
            depth_cols = numeric_cols
        
        if not depth_cols:
            logger.warning(f"No se encontraron columnas de profundidad en {source_name}")
            return
        
        depth_col = depth_cols[0]
        logger.info(f"  Usando columna de profundidad: {depth_col}")
        
        # Solo procesar resolución 8 para evitar explosión de particiones
        for resolution in [8]:  # Solo resolución 8
            logger.info(f"  {source_name} res={resolution}: vector → H3 grid")
            
            gdf_work = gdf[[depth_col, 'geometry']].copy()
            gdf_work = gdf_work.rename(columns={depth_col: 'depth_value'})
            
            h3_grid = vector_to_h3_grid(gdf_work, resolution=resolution, area_weight=True)
            
            if h3_grid.empty:
                continue
            
            h3_grid['depth_weighted'] = h3_grid['depth_value'] * h3_grid['area_fraction']
            
            agg = h3_grid.groupby('h3_cell').agg(
                depth_mean=('depth_weighted', 'sum'),
                depth_min=('depth_value', 'min'),
                depth_max=('depth_value', 'max'),
                depth_count=('depth_value', 'count'),
                area_total=('area_fraction', 'sum'),
            ).reset_index()
            
            agg['resolution'] = resolution
            agg['year'] = 2024
            agg['month'] = 1
            agg['time_partition'] = '2024-01'
            agg['source'] = source_name
            
            yield agg


def create_bathymetry_ingester(catalog, storage, config_overrides: Dict = None):
    """Factory para crear ingester de batimetría (GEBCO)."""

    base_config = IngestionConfig(
        dataset_name="bathymetry_gebco",
        layer="silver",
        partition_cols=["resolution"],  # Solo por resolución (3 particiones)
        h3_resolution=8,
        bbox=(22.5, -115.0, 32.0, -108.0),
        compression="zstd",
        batch_size=50000,
        validate=True
    )

    if config_overrides:
        for k, v in config_overrides.items():
            setattr(base_config, k, v)

    return BathymetryIngester(
        config=base_config,
        catalog=catalog,
        storage=storage,
        source_paths={
            "gebco": str(get_causanatura_dir("output/GEBCO_Batimetria_Golfo.gpkg")),
        },
        h3_resolutions=[8, 9, 10],
        stats=['mean', 'min', 'max', 'std', 'count']
    )


if __name__ == "__main__":
    from src.utils.logging import setup_logging
    setup_logging("ierc_gnl.bathymetry")
    print("Bathymetry Ingester module loaded")