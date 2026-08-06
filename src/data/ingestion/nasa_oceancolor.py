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
from src.utils.h3 import add_h3_column_vectorized, netcdf_to_h3_parquet
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
        df = add_h3_column_vectorized(df, 'lat', 'lon', 'h3_cell', self.config.h3_resolution)
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

    def _get_partition_path(self, df: pd.DataFrame) -> str:
        """Genera ruta de partición: nasa_chlor_a/year=2024/month=01/"""
        if df.empty:
            return f"nasa/{self.variable}/"

        year = df['year'].iloc[0]
        month = df['month'].iloc[0]
        return f"nasa/{self.variable}/year={year}/month={month:02d}/"


def create_nasa_ingester(variable: str, catalog, storage, **kwargs):
    """Factory para crear NASAOceanColorIngester."""
    from src.data.ingestion.factory import create_ingester
    dataset_map = {
        "chlor_a": "nasa_chlor_a",
        "sst": "nasa_sst",
    }
    dataset_name = dataset_map.get(variable, "nasa_chlor_a")
    return create_ingester(NASAOceanColorIngester, dataset_name, catalog, storage, variable=variable, **kwargs)


if __name__ == "__main__":
    from ..utils.logging import setup_logging
    setup_logging("ierc_gnl.nasa_oceancolor")
    print("NASA OceanColor Ingester module loaded")