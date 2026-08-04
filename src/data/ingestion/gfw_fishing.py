"""
Global Fishing Watch Ingester - IERC-GNL
=========================================
Ingesta de datos GFW (CSV/ZIP) → Parquet particionado H3.
"""

import pandas as pd
import zipfile
import glob
from pathlib import Path
from typing import Iterator, Optional, List, Dict, Any
import logging

from .base import BaseIngester, IngestionConfig
from src.utils.h3 import add_h3_column_vectorized
from src.utils.logging import setup_logging
from config import get_raw_dir

logger = setup_logging(__name__)


class GFWFishingEffortIngester(BaseIngester):
    """
    Ingester para Global Fishing Watch - Esfuerzo Pesquero Aparente v3.0.

    Fuente: Zenodo record 14982712
    - fishing-vessels-v3.csv: metadatos embarcaciones
    - fleet-daily-csvs-100-v3-YYYY.zip: esfuerzo diario por año

    Procesa archivos CSV comprimidos y convierte a Parquet particionado
    por H3 cell + año/mes.
    """

    def __init__(self,
                 config: IngestionConfig,
                 catalog,
                 storage,
                 source_dir: str = None,
                 target_years: List[int] = None,
                 vessels_file: str = "zenodo_global_fishing_watch_fishing-vessels-v3.csv"):
        super().__init__(config, catalog, storage)
        
        if source_dir is None:
            source_dir = str(get_raw_dir("gfw"))
        
        self.source_dir = Path(source_dir)
        self.target_years = target_years or [2020, 2021, 2022, 2023]
        self.vessels_file = vessels_file
        self._vessels_cache: Optional[pd.DataFrame] = None

    def extract(self) -> Iterator[pd.DataFrame]:
        """
        Extrae datos de esfuerzo pesquero por año.

        Yields:
            DataFrame por archivo ZIP (un año) con columnas estandarizadas
        """
        for year in self.target_years:
            zip_pattern = f"*fleet-daily-csvs-100-v3-{year}.zip"
            zip_files = list(self.source_dir.glob(zip_pattern))

            if not zip_files:
                logger.warning(f"No se encontró archivo para año {year}: {zip_pattern}")
                continue

            zip_path = zip_files[0]
            logger.info(f"Procesando {zip_path.name} ({zip_path.stat().st_size / 1e9:.2f} GB)")

            # Procesar ZIP en chunks
            yield from self._process_zip_year(zip_path, year)

    def _process_zip_year(self, zip_path: Path, year: int) -> Iterator[pd.DataFrame]:
        """Procesa un archivo ZIP anual en chunks."""

        with zipfile.ZipFile(zip_path, 'r') as zf:
            csv_files = [f for f in zf.namelist() if f.endswith('.csv')]
            logger.info(f"  {len(csv_files)} archivos CSV en {zip_path.name}")

            for csv_file in csv_files:
                try:
                    # Leer CSV en chunks
                    with zf.open(csv_file) as f:
                        # Primera pasada: detectar columnas
                        sample = pd.read_csv(f, nrows=5)
                        f.seek(0)

                        # Leer en chunks
                        chunk_iter = pd.read_csv(f, chunksize=self.config.batch_size)

                        for chunk_idx, chunk in enumerate(chunk_iter):
                            # Estandarizar columnas
                            chunk = self._standardize_columns(chunk)

                            # Filtrar a bbox Golfo
                            chunk = self._filter_gulf_bbox(chunk)

                            if not chunk.empty:
                                # Añadir metadatos temporales
                                chunk['year'] = year
                                if 'date' in chunk.columns:
                                    chunk['month'] = pd.to_datetime(chunk['date']).dt.month
                                    chunk['time_partition'] = pd.to_datetime(chunk['date']).dt.strftime('%Y-%m')
                                else:
                                    chunk['month'] = 1
                                    chunk['time_partition'] = f"{year}-01"

                                # Añadir H3 usando utilidad compartida
                                chunk = add_h3_column_vectorized(
                                    chunk, 'lat', 'lon', 'h3_cell', self.config.h3_resolution
                                )

                                yield chunk

                except Exception as e:
                    logger.error(f"Error procesando {csv_file} en {zip_path.name}: {e}")
                    self.errors.append(f"{zip_path.name}/{csv_file}: {e}")
                    continue

    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Estandariza nombres de columnas GFW."""
        # Mapeo de columnas comunes GFW
        column_map = {
            'lat': ['lat', 'latitude', 'Lat', 'Latitude'],
            'lon': ['lon', 'longitude', 'Lon', 'Longitude'],
            'fishing_hours': ['fishing_hours', 'hours', 'fishing_hours_100th', 'FishingHours'],
            'mmsi': ['mmsi', 'MMSI', 'vessel_mmsi'],
            'gear_type': ['gear_type', 'gear', 'GearType', 'gear_category'],
            'flag': ['flag', 'Flag', 'country', 'vessel_flag'],
            'date': ['date', 'Date', 'timestamp', 'time']
        }

        df = df.copy()
        for std_name, possible_names in column_map.items():
            for col in possible_names:
                if col in df.columns:
                    df = df.rename(columns={col: std_name})
                    break

        # Asegurar tipos
        if 'fishing_hours' in df.columns:
            df['fishing_hours'] = pd.to_numeric(df['fishing_hours'], errors='coerce')
        if 'mmsi' in df.columns:
            df['mmsi'] = df['mmsi'].astype(str)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        return df

    def _filter_gulf_bbox(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filtra filas dentro del bbox del Golfo de California."""
        if 'lat' not in df.columns or 'lon' not in df.columns:
            return df

        min_lat, min_lon, max_lat, max_lon = self.config.bbox
        mask = (
            (df['lat'] >= min_lat) & (df['lat'] <= max_lat) &
            (df['lon'] >= min_lon) & (df['lon'] <= max_lon)
        )
        return df[mask].copy()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforma a formato estandarizado con H3."""

        # Añadir H3 cell usando utilidad compartida
        df = add_h3_column_vectorized(df, 'lat', 'lon', 'h3_cell', self.config.h3_resolution)

        # Filtrar válidos
        df = df.dropna(subset=['h3_cell'])

        # Seleccionar columnas finales
        output_cols = [
            'date', 'year', 'month', 'time_partition',
            'h3_cell', 'fishing_hours', 'mmsi', 'gear_type', 'flag',
            'lat', 'lon'
        ]

        # Solo incluir columnas que existan
        output_cols = [c for c in output_cols if c in df.columns]

        return df[output_cols]

    def _get_partition_path(self, df: pd.DataFrame) -> str:
        if df.empty:
            return "gfw/fishing_effort/"

        year = df['year'].iloc[0]
        month = df['month'].iloc[0]
        return f"gfw/fishing_effort_h3/year={year}/month={month:02d}/"


class GFWVesselsIngester(BaseIngester):
    """Ingester para metadatos de embarcaciones GFW (archivo único CSV)."""

    def __init__(self, config: IngestionConfig, catalog, storage,
                 source_dir: str = None,
                 vessels_file: str = "zenodo_global_fishing_watch_fishing-vessels-v3.csv"):
        super().__init__(config, catalog, storage)
        if source_dir is None:
            source_dir = str(get_raw_dir("gfw"))
        self.source_path = Path(source_dir) / vessels_file

    def extract(self) -> Iterator[pd.DataFrame]:
        if not self.source_path.exists():
            logger.warning(f"Archivo embarcaciones no encontrado: {self.source_path}")
            return

        # Leer en chunks
        for chunk in pd.read_csv(self.source_path, chunksize=self.config.batch_size):
            yield chunk

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Estandariza metadatos de embarcaciones."""
        df = df.copy()

        # Mapeo columnas
        column_map = {
            'mmsi': ['mmsi', 'MMSI'],
            'vessel_name': ['vessel_name', 'name', 'ship_name'],
            'ship_type': ['ship_type', 'type', 'vessel_type'],
            'gear_type': ['gear_type', 'gear', 'fishing_gear'],
            'flag': ['flag', 'country', 'vessel_flag'],
            'length_m': ['length_m', 'length', 'loa'],
            'tonnage_gt': ['tonnage_gt', 'tonnage', 'gt']
        }

        for std_name, possible_names in column_map.items():
            for col in possible_names:
                if col in df.columns:
                    df = df.rename(columns={col: std_name})
                    break

        # Asegurar mmsi como string
        if 'mmsi' in df.columns:
            df['mmsi'] = df['mmsi'].astype(str)

        # Añadir timestamp de ingesta
        df['ingestion_timestamp'] = pd.Timestamp.utcnow()

        return df

    def _get_partition_path(self, df: pd.DataFrame) -> str:
        return "gfw/vessels/"


def create_gfw_ingester(dataset_type: str, catalog, storage, config_overrides: Dict = None) -> BaseIngester:
    """Factory para crear ingester GFW."""

    if dataset_type == "fishing_effort":
        base_config = IngestionConfig(
            dataset_name="gfw_fishing_effort",
            layer="silver",
            partition_cols=["h3_cell", "year", "month"],
            h3_resolution=8,
            bbox=(22.5, -115.0, 32.0, -108.0),
            compression="zstd",
            batch_size=100000,
            validate=True
        )
        ingester_class = GFWFishingEffortIngester
    elif dataset_type == "vessels":
        base_config = IngestionConfig(
            dataset_name="gfw_vessels",
            layer="silver",
            partition_cols=[],  # No particionar, tabla de referencia
            h3_resolution=8,
            bbox=(22.5, -115.0, 32.0, -108.0),
            compression="zstd",
            batch_size=50000,
            validate=True
        )
        ingester_class = GFWVesselsIngester
    else:
        raise ValueError(f"Tipo GFW desconocido: {dataset_type}")

    if config_overrides:
        for k, v in config_overrides.items():
            setattr(base_config, k, v)

    return ingester_class(config=base_config, catalog=catalog, storage=storage)


if __name__ == "__main__":
    from src.utils.logging import setup_logging
    setup_logging("ierc_gnl.gfw_fishing")
    print("GFW Ingester module loaded")