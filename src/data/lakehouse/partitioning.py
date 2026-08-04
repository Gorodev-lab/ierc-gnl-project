"""
Lakehouse Partitioning - IERC-GNL
==================================
Utilidades de particionado espacial H3 y temporal.
"""

import h3
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point, shape
from typing import List, Dict, Optional, Tuple, Union, Any
import numpy as np
import logging

logger = logging.getLogger(__name__)


def get_gulf_h3_cells(resolution: int, 
                      bbox: Tuple[float, float, float, float] = (22.5, -115.0, 32.0, -108.0)) -> List[str]:
    """
    Obtiene todas las celdas H3 que intersectan el bounding box del Golfo.
    """
    min_lat, min_lon, max_lat, max_lon = bbox
    
    bbox_poly = Polygon([
        (min_lon, min_lat),
        (max_lon, min_lat),
        (max_lon, max_lat),
        (min_lon, max_lat),
        (min_lon, min_lat)
    ])
    
    cells = h3.geo_to_cells(bbox_poly.__geo_interface__, resolution)
    logger.debug(f"H3 resolución {resolution}: {len(cells)} celdas para bbox {bbox}")
    return list(cells)


def add_h3_column(df: pd.DataFrame,
                  lat_col: str = 'lat',
                  lon_col: str = 'lon',
                  h3_col: str = 'h3_cell',
                  resolution: int = 8) -> pd.DataFrame:
    """
    Añade columna H3 a DataFrame con coordenadas lat/lon.
    
    Vectorizado para performance.
    """
    df = df.copy()
    df[h3_col] = df.apply(
        lambda row: h3.geo_to_h3(row[lat_col], row[lon_col], resolution) 
        if pd.notna(row[lat_col]) and pd.notna(row[lon_col]) 
        else None, axis=1
    )
    return df


def add_h3_column_vectorized(df: pd.DataFrame,
                              lat_col: str = 'lat',
                              lon_col: str = 'lon',
                              h3_col: str = 'h3_cell',
                              resolution: int = 8) -> pd.DataFrame:
    """
    Versión vectorizada usando numpy + h3 batch (más rápido para DataFrames grandes).
    """
    df = df.copy()
    
    # Filtrar válidos
    valid_mask = df[lat_col].notna() & df[lon_col].notna()
    
    if valid_mask.any():
        lats = df.loc[valid_mask, lat_col].values
        lons = df.loc[valid_mask, lon_col].values
        
        # h3 no tiene batch nativo, usar list comprehension optimizada
        h3_cells = [h3.geo_to_h3(lat, lon, resolution) for lat, lon in zip(lats, lons)]
        
        df.loc[valid_mask, h3_col] = h3_cells
    
    df.loc[~valid_mask, h3_col] = None
    return df


def vector_to_h3_grid(gdf: gpd.GeoDataFrame,
                      resolution: int = 8,
                      area_weight: bool = True) -> gpd.GeoDataFrame:
    """
    Convierte geometrías vectoriales (Point, Polygon, MultiPolygon) a grid H3
    con pesos de área para joins espaciales precisos.
    
    Args:
        gdf: GeoDataFrame con geometrías
        resolution: Resolución H3 objetivo
        area_weight: Si True, calcula fracción de área por celda
    
    Returns:
        GeoDataFrame con una fila por (feature, h3_cell) con geometría de la celda H3
    """
    records = []
    
    for idx, row in gdf.iterrows():
        geom = row.geometry
        if geom is None or geom.is_empty:
            continue
        
        # Obtener celdas H3 que intersectan la geometría
        try:
            if geom.geom_type == 'Point':
                cells = [h3.geo_to_h3(geom.y, geom.x, resolution)]
            elif geom.geom_type in ('Polygon', 'MultiPolygon'):
                cells = h3.geo_to_cells(geom.__geo_interface__, resolution)
            elif geom.geom_type in ('LineString', 'MultiLineString'):
                # Buffer lines to create polygons for H3 conversion
                # Use a small buffer (e.g., 100m at equator ~0.001 deg)
                buffered = geom.buffer(0.001)
                if buffered.geom_type in ('Polygon', 'MultiPolygon'):
                    cells = h3.geo_to_cells(buffered.__geo_interface__, resolution)
                else:
                    logger.debug(f"Buffer no produjo polígono para {geom.geom_type} en índice {idx}")
                    continue
            else:
                logger.debug(f"Saltando geometría tipo {geom.geom_type} en índice {idx}")
                continue
        except Exception as e:
            logger.warning(f"Error procesando geometría {idx}: {e}")
            continue
        
        if not cells:
            continue
        
        # Calcular peso de área si es polígono
        if area_weight and geom.geom_type in ('Polygon', 'MultiPolygon'):
            total_area = geom.area
            for cell in cells:
                cell_boundary = h3.cell_to_boundary(cell)
                cell_poly = Polygon(cell_boundary)
                intersection = geom.intersection(cell_poly)
                area_frac = intersection.area / total_area if total_area > 0 else 1.0 / len(cells)
                
                records.append({
                    'h3_cell': cell,
                    'geometry': cell_poly,
                    'source_index': idx,
                    'area_fraction': area_frac,
                    **{k: v for k, v in row.items() if k != 'geometry'}
                })
        else:
            # Para puntos o sin peso de área
            for cell in cells:
                cell_boundary = h3.cell_to_boundary(cell)
                cell_poly = Polygon(cell_boundary)
                records.append({
                    'h3_cell': cell,
                    'geometry': cell_poly,
                    'source_index': idx,
                    'area_fraction': 1.0 / len(cells),
                    **{k: v for k, v in row.items() if k != 'geometry'}
                })
    
    if not records:
        return gpd.GeoDataFrame(columns=['h3_cell', 'geometry'], crs="EPSG:4326")
    
    result = gpd.GeoDataFrame(records, crs="EPSG:4326")
    logger.debug(f"Vector → H3 grid: {len(gdf)} features → {len(result)} celdas H3 (res={resolution})")
    return result


def create_temporal_partition_columns(df: pd.DataFrame,
                                       time_col: str = 'time',
                                       freq: str = 'monthly') -> pd.DataFrame:
    """
    Añade columnas de partición temporal estándar.
    
    Args:
        df: DataFrame con columna temporal
        time_col: Nombre de columna temporal
        freq: 'daily', 'monthly', 'yearly'
    
    Returns:
        DataFrame con columnas de partición añadidas
    """
    df = df.copy()
    dt = pd.to_datetime(df[time_col])
    
    df['year'] = dt.dt.year
    df['month'] = dt.dt.month
    df['day'] = dt.dt.day
    
    if freq == 'daily':
        df['time_partition'] = dt.dt.strftime('%Y-%m-%d')
    elif freq == 'monthly':
        df['time_partition'] = dt.dt.strftime('%Y-%m')
    elif freq == 'yearly':
        df['time_partition'] = dt.dt.strftime('%Y')
    else:
        df['time_partition'] = dt.dt.strftime('%Y-%m')
    
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test get_gulf_h3_cells
    cells_8 = get_gulf_h3_cells(8)
    cells_10 = get_gulf_h3_cells(10)
    print(f"H3_8 cells: {len(cells_8)}")
    print(f"H3_10 cells: {len(cells_10)}")
    print(f"Sample H3_8: {cells_8[:5]}")