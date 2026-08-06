"""
Shared Column Standardization - IERC-GNL
==========================================
Common column rename/standardize utilities for all ingesters.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import geopandas as gpd


# Standard column names across all datasets
STANDARD_COLUMNS = {
    'h3_cell': ['h3_cell', 'h3', 'h3_index', 'cell'],
    'lat': ['lat', 'latitud', 'latitude', 'y'],
    'lon': ['lon', 'longitud', 'longitude', 'x'],
    'year': ['year', 'yr', 'ano'],
    'month': ['month', 'mes', 'mo'],
    'time_partition': ['time_partition', 'time_part', 'partition'],
    'geometry': ['geometry', 'geom', 'shape'],
}


def standardize_columns(
    df: pd.DataFrame,
    column_map: Dict[str, List[str]],
    type_map: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """
    Estandariza nombres de columnas usando mapeo configurable.
    
    Args:
        df: DataFrame a estandarizar
        column_map: Dict {standard_name: [possible_names...]}
        type_map: Optional dict {column: dtype} para conversión de tipos
    
    Returns:
        DataFrame con columnas renombradas y tipos convertidos
    """
    df = df.copy()
    
    # Renombrar columnas
    for std_name, possible_names in column_map.items():
        for col in possible_names:
            if col in df.columns:
                df = df.rename(columns={col: std_name})
                break
    
    # Convertir tipos si se especifica
    if type_map:
        for col, dtype in type_map.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except Exception:
                    pass  # Silenciar errores de conversión
    
    return df


def standardize_gdf_columns(
    gdf: gpd.GeoDataFrame,
    column_map: Dict[str, List[str]],
    type_map: Optional[Dict[str, Any]] = None
) -> gpd.GeoDataFrame:
    """
    Estandariza nombres de columnas en GeoDataFrame.
    """
    df = standardize_columns(gdf, column_map, type_map)
    return gpd.GeoDataFrame(df, crs=gdf.crs)


def rename_depth_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renombra columnas de profundidad a estándar batimétrico."""
    rename_map = {}
    depth_mappings = {
        'depth_mean': 'bathymetry_mean',
        'depth_min': 'bathymetry_min',
        'depth_max': 'bathymetry_max',
        'depth_std': 'bathymetry_std',
        'depth_count': 'bathymetry_count',
        'depth_value': 'bathymetry_value',
    }
    for src, dst in depth_mappings.items():
        if src in df.columns:
            rename_map[src] = dst
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


if __name__ == "__main__":
    # Test
    import pandas as pd
    df = pd.DataFrame({'latitud': [1,2], 'longitud': [3,4], 'fecha': [5,6]})
    result = standardize_columns(df, {
        'lat': ['latitud', 'latitude'],
        'lon': ['longitud', 'longitude'],
        'date': ['fecha', 'time']
    })
    print(result.columns.tolist())  # ['lat', 'lon', 'date']