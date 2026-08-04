"""
NASA OceanColor Ingester - IERC-GNL
====================================
Ingesta de datos NetCDF (clorofila-a, SST) → Parquet particionado H3.
"""

import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Iterator, Optional, List, Dict, Any
from datetime import datetime
import logging

from .base import BaseIngester, IngestionConfig
from src.utils.h3 import netcdf_to_h3_parquet
from src.utils.logging import setup_logging
from config import get_raw_dir

logger = setup_logging(__name__)


class NASAOceanColorIngester(BaseIngester):
    """
    Ingester para NASA OceanColor Level 3 Mapped Images.
    
    Fuentes:
    - Chlorophyll-a: https://oceandata.sci.gsfc.nasa.gov/opendap/MODISA/L3SMI/
    - SST: https://oceandata.sci.gsfc.nasa.gov/opendap/MODISA/L3SMI/
    
    Procesa archivos NetCDF diarios/mensuales y los convierte a Parquet
    particionado por H3 cell + año/mes.
    """
    
    def __init__(self, 
                 config: IngestionConfig,
                 catalog,
                 storage,
                 variable: str = "chlor_a",
                 source_dir: str = None,
                 chunk_size: Dict[str, int] = None):
        super().__init__(config, catalog, storage)
        self.variable = variable
        
        if source_dir is None:
            source_dir = str(get_raw_dir("nasa"))
        
        self.source_dir = Path(source_dir)
        self.chunk_size = chunk_size or {"time": 1, "lat": 500, "lon": 500}
        
        # Mapeo de variable a patrón de archivo
        self.file_patterns = {
            "chlor_a": "nasa_chlor_a_{year}_{month:02d}.nc",
            "sst": "nasa_sst_{year}_{month:02d}.nc"
        }
    
    def extract(self) -> Iterator[pd.DataFrame]:
        """
        Extrae datos de archivos NetCDF locales.
        
        Yields:
            DataFrame por archivo (día/mes) con columnas: time, lat, lon, value
        """
        pattern = self.file_patterns.get(self.variable)
        if not pattern:
            raise ValueError(f"Variable no soportada: {self.variable}")
        
        # Buscar archivos disponibles
        files = sorted(self.source_dir.glob(f"nasa_{self.variable}_*.nc"))
        
        if not files:
            logger.warning(f"No se encontraron archivos para {self.variable} en {self.source_dir}")
            return
        
        logger.info(f"Encontrados {len(files)} archivos para {self.variable}")
        
        for file_path in files:
            try:
                # Extraer año/mes del nombre
                # Formato: nasa_chlor_a_2020_01.nc
                stem = file_path.stem
                parts = stem.split('_')
                if len(parts) >= 4:
                    year = int(parts[-2])
                    month = int(parts[-1])
                else:
                    logger.warning(f"Nombre de archivo no reconocido: {file_path.name}")
                    continue
                
                # Procesar archivo
                df = self._process_netcdf_file(file_path, year, month)
                if not df.empty:
                    yield df
                    
            except Exception as e:
                logger.error(f"Error procesando {file_path}: {e}")
                self.errors.append(f"{file_path}: {e}")
                continue
    
    def _process_netcdf_file(self, file_path: Path, year: int, month: int) -> pd.DataFrame:
        """Procesa un archivo NetCDF individual y agrega por H3 cell."""
        
        # Abrir con chunking para memoria
        ds = xr.open_dataset(file_path, chunks=self.chunk_size, engine='netcdf4')
        
        # Verificar variable
        if self.variable not in ds.data_vars:
            logger.warning(f"Variable {self.variable} no encontrada en {file_path}")
            return pd.DataFrame()
        
        var_data = ds[self.variable]
        
        # Recortar a bbox del Golfo
        min_lat, min_lon, max_lat, max_lon = self.config.bbox
        if 'lat' in var_data.dims and 'lon' in var_data.dims:
            var_data = var_data.sel(
                lat=slice(max_lat, min_lat),  # xarray espera max primero para lat decreciente
                lon=slice(min_lon, max_lon)
            )
        
        # Convertir a DataFrame
        df = var_data.to_dataframe().reset_index()
        df = df.rename(columns={self.variable: 'value'})
        
        # Filtrar valores válidos (no fill_value)
        fill_value = var_data.attrs.get('_FillValue', -32767)
        df = df[df['value'] != fill_value]
        df = df.dropna(subset=['value'])
        
        if df.empty:
            return pd.DataFrame()
        
        # Añadir H3 cell ANTES de agregar
        df = self._add_h3_column(df)
        df = df.dropna(subset=['h3_cell'])
        
        if df.empty:
            return pd.DataFrame()
        
        # Agregar por H3 cell (mean, std, count)
        agg_df = df.groupby('h3_cell').agg(
            value_mean=('value', 'mean'),
            value_std=('value', 'std'),
            value_count=('value', 'count'),
            lat_mean=('lat', 'mean'),
            lon_mean=('lon', 'mean'),
        ).reset_index()
        
        # Añadir columnas temporales
        agg_df['year'] = year
        agg_df['month'] = month
        agg_df['time_partition'] = f"{year}-{month:02d}"
        agg_df['time'] = pd.Timestamp(f"{year}-{month:02d}-01")
        
        logger.debug(f"  {file_path.name}: {len(df)} píxeles → {len(agg_df)} celdas H3")
        return agg_df
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforma datos crudos a formato estandarizado con H3."""
        
        # df ya viene agregado por H3 cell desde _process_netcdf_file
        # Filtrar solo celdas válidas en el Golfo
        df = df.dropna(subset=['h3_cell'])
        
        # Renombrar columnas de valor agregado
        df = df.rename(columns={
            'value_mean': self.variable,
            'value_std': f'{self.variable}_std',
            'value_count': f'{self.variable}_count',
        })
        
        # Seleccionar y ordenar columnas finales
        output_cols = [
            'time', 'year', 'month', 'time_partition',
            'h3_cell', self.variable,
            f'{self.variable}_std', f'{self.variable}_count',
            'lat_mean', 'lon_mean'
        ]
        
        # Añadir quality_flag si existe
        if 'quality_flag' in df.columns:
            output_cols.append('quality_flag')
        
        # Solo incluir columnas que existan
        output_cols = [c for c in output_cols if c in df.columns]
        
        return df[output_cols]
    
    def _add_h3_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Añade columna H3 vectorizada."""
        return self._add_h3_vectorized(df, 'lat', 'lon', 'h3_cell', self.config.h3_resolution)
    
    def _add_h3_vectorized(self, df: pd.DataFrame, lat_col: str, lon_col: str, 
                           h3_col: str, resolution: int) -> pd.DataFrame:
        """Versión vectorizada para DataFrames grandes."""
        df = df.copy()
        
        valid_mask = df[lat_col].notna() & df[lon_col].notna()
        
        if valid_mask.any():
            lats = df.loc[valid_mask, lat_col].values
            lons = df.loc[valid_mask, lon_col].values
            
            # Batch H3 conversion
            import h3
            h3_cells = [h3.latlng_to_cell(lat, lon, resolution) for lat, lon in zip(lats, lons)]
            
            df.loc[valid_mask, h3_col] = h3_cells
        
        df.loc[~valid_mask, h3_col] = None
        return df
    
    def _get_partition_path(self, df: pd.DataFrame) -> str:
        """Genera ruta de partición: nasa_chlor_a/year=2024/month=01/"""
        if df.empty:
            return f"nasa/{self.variable}/"
        
        year = df['year'].iloc[0]
        month = df['month'].iloc[0]
        return f"nasa/{self.variable}/year={year}/month={month:02d}/"


class NASAOceanColorMonthlyIngester(NASAOceanColorIngester):
    """
    Ingester para promedios mensuales (archivos mensuales ya agregados).
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sobrescribir patrón para archivos mensuales
        self.file_patterns = {
            "chlor_a": "nasa_chlor_a_{year}_{month:02d}.nc",
            "sst": "nasa_sst_{year}_{month:02d}.nc"
        }


def create_nasa_ingester(variable: str, catalog, storage, config_overrides: Dict = None) -> NASAOceanColorIngester:
    """Factory para crear ingester NASA configurado."""
    
    base_config = IngestionConfig(
        dataset_name=f"nasa_{variable}",
        layer="silver",
        partition_cols=["year", "month"],  # Solo temporal, NO h3_cell
        h3_resolution=8,
        bbox=(22.5, -115.0, 32.0, -108.0),
        compression="zstd",
        batch_size=50000,
        validate=True
    )
    
    if config_overrides:
        for k, v in config_overrides.items():
            setattr(base_config, k, v)
    
    return NASAOceanColorIngester(
        config=base_config,
        catalog=catalog,
        storage=storage,
        variable=variable
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("NASA OceanColor Ingester module loaded")