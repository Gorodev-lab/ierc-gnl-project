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
from dataclasses import dataclass
import numpy as np
import logging

logger = logging.getLogger(__name__)


@dataclass
class H3PartitionConfig:
    """Configuración de particionado H3."""
    resolution: int
    bbox: Tuple[float, float, float, float]  # min_lat, min_lon, max_lat, max_lon
    coastal_resolution: Optional[int] = None
    coastal_buffer_km: float = 10.0


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


def get_adaptive_gulf_h3_cells(port_hotspots: List[Tuple[float, float]] = None,
                                k_ring_res9: int = 15) -> List[Tuple[str, int]]:
    """
    Obtiene la grilla H3 adaptativa oficial para el Golfo de California:
    - H3_8 (~0.73 km²) para mar abierto y zonas pesqueras regionales.
    - H3_9 (~0.10 km²) para las zonas de interfaz portuaria/industrial
      (Puerto Libertad, Guaymas, Punta Chueca).
    
    Returns:
        Lista de tuplas (h3_cell, resolution)
    """
    if port_hotspots is None:
        port_hotspots = [
            (29.9107, -112.6835),  # Puerto Libertad
            (27.9179, -110.9039),  # Guaymas
            (28.9886, -112.1603)   # Punta Chueca Comca'ac
        ]
    
    adaptive_cells = []
    seen_cells = set()
    
    # 1. Celdas Res 9 para hotspots portuarios
    for lat, lon in port_hotspots:
        center_res9 = h3.latlng_to_cell(lat, lon, 9)
        ring_res9 = h3.grid_disk(center_res9, k_ring_res9)
        for cell in ring_res9:
            if cell not in seen_cells:
                seen_cells.add(cell)
                adaptive_cells.append((cell, 9))
    
    # 2. Celdas Res 8 regionales
    regional_res8 = get_gulf_h3_cells(8)
    for cell in regional_res8:
        if cell not in seen_cells:
            seen_cells.add(cell)
            adaptive_cells.append((cell, 8))
            
    logger.info(f"Grilla H3 Adaptativa generada: {len(adaptive_cells)} celdas totales")
    return adaptive_cells


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


def raster_to_h3_stats(raster_path: str,
                       resolution: int = 8,
                       stats: List[str] = None,
                       bbox: Tuple[float, float, float, float] = None,
                       nodata: float = None) -> pd.DataFrame:
    """
    Extrae estadísticas de raster por celda H3 usando exactextract.
    
    Args:
        raster_path: Ruta a GeoTIFF/NetCDF
        resolution: Resolución H3
        stats: Lista de estadísticas ['mean', 'min', 'max', 'std', 'count', 'sum']
        bbox: Bounding box opcional para recortar (min_lat, min_lon, max_lat, max_lon)
        nodata: Valor nodata a ignorar
    
    Returns:
        DataFrame con h3_cell y estadísticas
    """
    import rasterio
    from rasterio.windows import from_bounds
    import exactextract
    
    if stats is None:
        stats = ['mean', 'min', 'max', 'std', 'count']
    
    with rasterio.open(raster_path) as src:
        # Determinar bbox de trabajo
        if bbox is None:
            work_bbox = src.bounds
        else:
            min_lat, min_lon, max_lat, max_lon = bbox
            work_bbox = (min_lon, min_lat, max_lon, max_lat)
        
        # Obtener celdas H3 que cubren el bbox
        bbox_poly = Polygon([
            (work_bbox[0], work_bbox[1]),
            (work_bbox[2], work_bbox[1]),
            (work_bbox[2], work_bbox[3]),
            (work_bbox[0], work_bbox[3]),
            (work_bbox[0], work_bbox[1])
        ])
        h3_cells = h3.geo_to_cells(bbox_poly.__geo_interface__, resolution)
        
        logger.info(f"Procesando {len(h3_cells)} celdas H3 para raster {raster_path}")
        
        results = []
        for cell in h3_cells:
            cell_boundary = h3.cell_to_boundary(cell, geo_json=True)
            cell_poly = Polygon(cell_boundary)
            
            try:
                # exactextract espera geometría en CRS del raster
                cell_geom = cell_poly.__geo_interface__
                
                # Extraer estadísticas
                extracted = exactextract.exact_extract(
                    src, cell_geom, stats,
                    include_cols=['x', 'y'] if False else None
                )
                
                if extracted and len(extracted) > 0:
                    stat_vals = extracted[0]
                    record = {'h3_cell': cell}
                    for stat_name in stats:
                        record[f'value_{stat_name}'] = stat_vals.get(stat_name)
                    results.append(record)
            except Exception as e:
                logger.debug(f"Error extrayendo celda {cell}: {e}")
                continue
        
        df = pd.DataFrame(results)
        logger.info(f"Raster → H3 stats: {len(df)} celdas con datos válidos")
        return df


def netcdf_to_h3_parquet(netcdf_path: str,
                         variable: str,
                         resolution: int = 8,
                         time_dim: str = 'time',
                         lat_dim: str = 'lat',
                         lon_dim: str = 'lon',
                         bbox: Tuple[float, float, float, float] = None,
                         chunk_size: Dict[str, int] = None,
                         output_path: str = None) -> pd.DataFrame:
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
        import pyarrow as pa
        import pyarrow.parquet as pq
        table = pa.Table.from_pandas(result, preserve_index=False)
        pq.write_to_dataset(
            table,
            root_path=output_path,
            partition_cols=['h3_cell', 'year', 'month'],
            compression='zstd'
        )
        logger.info(f"Escrito a {output_path}")
    
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


def get_h3_parent_cell(h3_cell: str, target_resolution: int) -> str:
    """Obtiene celda padre a resolución objetivo."""
    current_res = h3.get_resolution(h3_cell)
    if current_res <= target_resolution:
        return h3_cell
    return h3.h3_to_parent(h3_cell, target_resolution)


def aggregate_h3_to_resolution(df: pd.DataFrame,
                                h3_col: str = 'h3_cell',
                                value_cols: List[str] = None,
                                agg_func: str = 'mean',
                                target_resolution: int = 7) -> pd.DataFrame:
    """
    Agrega DataFrame particionado por H3 a resolución más gruesa.
    """
    df = df.copy()
    df['h3_parent'] = df[h3_col].apply(lambda x: get_h3_parent_cell(x, target_resolution))
    
    if value_cols is None:
        value_cols = [c for c in df.columns if c not in [h3_col, 'h3_parent'] and df[c].dtype in ['float64', 'float32', 'int64', 'int32']]
    
    agg_dict = {col: agg_func for col in value_cols}
    agg_dict[h3_col] = 'first'  # mantener una celda hija representativa
    
    result = df.groupby('h3_parent').agg(agg_dict).reset_index()
    result = result.rename(columns={'h3_parent': h3_col})
    
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test get_gulf_h3_cells
    cells_8 = get_gulf_h3_cells(8)
    cells_10 = get_gulf_h3_cells(10)
    print(f"H3_8 cells: {len(cells_8)}")
    print(f"H3_10 cells: {len(cells_10)}")
    print(f"Sample H3_8: {cells_8[:5]}")