"""
Shared H3 Utilities - IERC-GNL
================================
Single source of truth for H3 operations. Used by all ingesters and engines.
"""

import h3
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from typing import List, Dict, Optional, Tuple, Union, Any
import logging

logger = logging.getLogger(__name__)

# ============================================================
# Bbox Filtering (Native geopandas)
# ============================================================

GULF_BBOX = (22.5, -115.0, 32.0, -108.0)


def filter_gdf_bbox(
    gdf: gpd.GeoDataFrame,
    bbox: Tuple[float, float, float, float] = GULF_BBOX
) -> gpd.GeoDataFrame:
    """
    Filtra GeoDataFrame por bbox usando geopandas .cx[] indexer (native, fast).
    
    Args:
        gdf: GeoDataFrame con geometría
        bbox: (min_lat, min_lon, max_lat, max_lon)
    
    Returns:
        GeoDataFrame filtrado
    """
    if gdf.empty:
        return gdf
    
    min_lat, min_lon, max_lat, max_lon = bbox
    # geopandas .cx[] expects (x, y) = (lon, lat)
    return gdf.cx[min_lon:max_lon, min_lat:max_lat]


def filter_df_bbox(
    df: pd.DataFrame,
    bbox: Tuple[float, float, float, float] = GULF_BBOX,
    lat_col: str = 'lat',
    lon_col: str = 'lon'
) -> pd.DataFrame:
    """
    Filtra DataFrame con lat/lon por bbox usando boolean indexing (vectorized).
    
    Args:
        df: DataFrame con columnas lat/lon
        bbox: (min_lat, min_lon, max_lat, max_lon)
        lat_col: nombre de columna latitud
        lon_col: nombre de columna longitud
    
    Returns:
        DataFrame filtrado
    """
    if df.empty or lat_col not in df.columns or lon_col not in df.columns:
        return df
    
    min_lat, min_lon, max_lat, max_lon = bbox
    mask = (
        (df[lat_col] >= min_lat) & (df[lat_col] <= max_lat) &
        (df[lon_col] >= min_lon) & (df[lon_col] <= max_lon)
    )
    return df[mask].copy()


# ============================================================
# H3 Cell Generation
# ============================================================

def get_gulf_h3_cells(
    resolution: int,
    bbox: Tuple[float, float, float, float] = GULF_BBOX
) -> List[str]:
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


# ============================================================
# H3 Column Addition (Vectorized)
# ============================================================

def add_h3_column_vectorized(
    df: pd.DataFrame,
    lat_col: str = 'lat',
    lon_col: str = 'lon',
    h3_col: str = 'h3_cell',
    resolution: int = 8
) -> pd.DataFrame:
    """
    Añade columna H3 a DataFrame con coordenadas lat/lon.
    Versión vectorizada usando numpy + h3 batch (más rápido para DataFrames grandes).
    """
    df = df.copy()

    # Filtrar válidos
    valid_mask = df[lat_col].notna() & df[lon_col].notna()

    if valid_mask.any():
        lats = df.loc[valid_mask, lat_col].values
        lons = df.loc[valid_mask, lon_col].values

        # h3 no tiene batch nativo, usar list comprehension optimizada
        h3_cells = [h3.latlng_to_cell(lat, lon, resolution) for lat, lon in zip(lats, lons)]

        df.loc[valid_mask, h3_col] = h3_cells

    df.loc[~valid_mask, h3_col] = None
    return df


# ============================================================
# Vector to H3 Grid Conversion
# ============================================================

def vector_to_h3_grid(
    gdf: gpd.GeoDataFrame,
    resolution: int = 8,
    area_weight: bool = True
) -> gpd.GeoDataFrame:
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
                cells = [h3.latlng_to_cell(geom.y, geom.x, resolution)]
            elif geom.geom_type in ('Polygon', 'MultiPolygon'):
                cells = h3.geo_to_cells(geom.__geo_interface__, resolution)
            elif geom.geom_type in ('LineString', 'MultiLineString'):
                # Buffer lines to create polygons for H3 conversion
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


# ============================================================
# Temporal Partition Columns
# ============================================================

def create_temporal_partition_columns(
    df: pd.DataFrame,
    time_col: str = 'time',
    freq: str = 'monthly'
) -> pd.DataFrame:
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


# ============================================================
# NetCDF to H3 Parquet (moved here from partitioning.py)
# ============================================================

def netcdf_to_h3_parquet(
    netcdf_path: str,
    variable: str,
    resolution: int = 8,
    time_dim: str = 'time',
    lat_dim: str = 'lat',
    lon_dim: str = 'lon',
    bbox: Tuple[float, float, float, float] = None,
    chunk_size: Dict[str, int] = None,
    output_path: str = None
) -> pd.DataFrame:
    """
    Convierte variable NetCDF a DataFrame particionado por H3.
    Optimizado para memoria usando chunking.

    Args:
        netcdf_path: Ruta al archivo NetCDF
        variable: Nombre de la variable a extraer
        resolution: Resolución H3
        time_dim: Nombre de dimensión temporal
        lat_dim: Nombre de dimensión latitud
        lon_dim: Nombre de dimensión longitud
        bbox: Bounding box (min_lat, min_lon, max_lat, max_lon)
        chunk_size: Tamaño de chunks {time: 1, lat: 500, lon: 500}
        output_path: Si se proporciona, escribe directamente a Parquet particionado

    Returns:
        DataFrame con columnas [time, h3_cell, variable, ...]
    """
    import xarray as xr
    import pyarrow as pa
    import pyarrow.parquet as pq

    if chunk_size is None:
        chunk_size = {'time': 1, 'lat': 500, 'lon': 500}

    # Abrir con chunking para memoria eficiente
    ds = xr.open_dataset(netcdf_path, chunks=chunk_size)

    # Recortar a bbox si se proporciona
    if bbox:
        min_lat, min_lon, max_lat, max_lon = bbox
        ds = ds.sel({
            lat_dim: slice(min_lat, max_lat),
            lon_dim: slice(min_lon, max_lon)
        })

    # Obtener variable
    var_data = ds[variable]

    # Convertir a DataFrame por chunks de tiempo
    all_records = []

    for time_idx in range(var_data.sizes[time_dim]):
        time_slice = var_data.isel({time_dim: time_idx})
        time_val = time_slice[time_dim].values

        # Convertir slice a DataFrame
        df_slice = time_slice.to_dataframe().reset_index()
        df_slice = df_slice.rename(columns={variable: 'value'})

        # Añadir H3
        df_slice = add_h3_column_vectorized(df_slice, lat_dim, lon_dim, 'h3_cell', resolution)

        # Añadir partición temporal
        if hasattr(time_val, 'strftime'):
            df_slice['time_partition'] = pd.Timestamp(time_val).strftime('%Y-%m')
        else:
            df_slice['time_partition'] = str(time_val)[:7]  # YYYY-MM

        df_slice['year'] = pd.Timestamp(time_val).year
        df_slice['month'] = pd.Timestamp(time_val).month

        # Filtrar nulos
        df_slice = df_slice.dropna(subset=['h3_cell', 'value'])

        all_records.append(df_slice[['time', 'year', 'month', 'time_partition', 'h3_cell', 'value']])

        if time_idx % 10 == 0:
            logger.debug(f"Procesado {time_idx + 1}/{var_data.sizes[time_dim]} pasos temporales")

    result = pd.concat(all_records, ignore_index=True)
    result = result.rename(columns={'value': variable})

    logger.info(f"NetCDF → H3: {len(result)} registros, {result.h3_cell.nunique()} celdas H3")

    if output_path:
        # Escribir particionado
        table = pa.Table.from_pandas(result, preserve_index=False)
        pq.write_to_dataset(
            table,
            root_path=output_path,
            partition_cols=['h3_cell', 'year', 'month'],
            compression='zstd'
        )
        logger.info(f"Escrito a {output_path}")

    return result


# ============================================================
# If __name__ == "__main__"
# ============================================================

if __name__ == "__main__":
    from ..utils.logging import setup_logging
    setup_logging("ierc_gnl.h3")

    # Test get_gulf_h3_cells
    cells_8 = get_gulf_h3_cells(8)
    cells_10 = get_gulf_h3_cells(10)
    print(f"H3_8 cells: {len(cells_8)}")
    print(f"H3_10 cells: {len(cells_10)}")
    print(f"Sample H3_8: {cells_8[:5]}")