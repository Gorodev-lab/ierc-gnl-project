"""
Global Fishing Watch Ingester - IERC-GNL
=========================================
Ingesta de datos GFW (CSV/ZIP local + API) → Parquet particionado H3.
"""

import os
import pandas as pd
import zipfile
import glob
from pathlib import Path
from typing import Iterator, Optional, List, Dict, Any
import logging
import requests
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta

from .base import BaseIngester, IngestionConfig
from src.utils.h3 import add_h3_column_vectorized, filter_df_bbox
from src.utils.logging import setup_logging
from config import get_raw_dir

logger = setup_logging(__name__)


class GFWAPIError(Exception):
    """Excepción para errores de GFW API."""
    pass


class GFWFishingEffortIngester(BaseIngester):
    """
    Ingester para Global Fishing Watch - Esfuerzo Pesquero Aparente v3.0.

    Fuentes soportadas:
    - Local: Zenodo record 14982712 (CSV/ZIP descargados)
    - API: GFW Public API (eventos de pesca, encuentros, etc.)

    Procesa y convierte a Parquet particionado por H3 cell + año/mes.
    """

    def __init__(self,
                 config: IngestionConfig,
                 catalog,
                 storage,
                 source_dir: str = None,
                 target_years: List[int] = None,
                 vessels_file: str = "zenodo_global_fishing_watch_fishing-vessels-v3.csv",
                 api_token: str = None,
                 api_base_url: str = "https://gateway.api.globalfishingwatch.org/v3"):
        super().__init__(config, catalog, storage)

        if source_dir is None:
            source_dir = str(get_raw_dir("gfw"))

        self.source_dir = Path(source_dir)
        self.target_years = target_years or [2020, 2021, 2022, 2023]
        self.vessels_file = vessels_file
        self._vessels_cache: Optional[pd.DataFrame] = None

        # API configuration
        self.api_token = api_token or os.getenv("GFW_API_TOKEN")
        self.api_base_url = api_base_url.rstrip('/')
        self._session: Optional[requests.Session] = None

    def extract(self) -> Iterator[pd.DataFrame]:
        """
        Extrae datos de esfuerzo pesquero por año.

        Yields:
            DataFrame por archivo ZIP (un año) con columnas estandarizadas
        """
        # Si hay token de API, intentar API primero
        if self.api_token:
            logger.info("Token de API detectado, extrayendo desde GFW API...")
            yield from self._extract_from_api()
        else:
            logger.info("Sin token de API, extrayendo desde archivos locales...")
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
        return filter_df_bbox(df, self.config.bbox)

    def _extract_from_api(self) -> Iterator[pd.DataFrame]:
        """
        Extrae datos desde GFW Public API v3.

        NOTA: Los endpoints públicos de GFW API v3 pueden requerir:
        - Token con scopes específicos (ej: 'events:read', 'vessels:read')
        - URL base: https://gateway.api.globalfishingwatch.org/v3

        Endpoints v3:
        - /v3/events (eventos de pesca) - requiere dataset parameter
        - /v3/vessels/search (búsqueda de embarcaciones) - requiere dataset parameter

        Parámetros v3:
        - datasets[0]=public-global-fishing-events:latest
        - start-date, end-date
        - limit, offset (obligatorio para events)
        - bbox NO soportado en /v3/events (filtrado client-side)

        Yields:
            DataFrame con eventos de pesca o vessels estandarizados
        """
        if not self.api_token:
            logger.warning("No API token available, skipping API extraction")
            return

        # Determine endpoint based on dataset
        is_vessels = self.config.dataset_name == "gfw_vessels"
        endpoint = "/vessels/search" if is_vessels else "/events"

        # Lazy session initialization
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update({
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            })
            # Aggressive timeouts and connection settings
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=1,
                pool_maxsize=1,
                max_retries=0
            )
            self._session.mount('https://', adapter)
            self._session.mount('http://', adapter)
            # Disable keep-alive to avoid connection issues
            self._session.headers.update({"Connection": "close"})

        # Rango temporal por defecto: últimos 30 días
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)

        # Parámetros base
        params = {}

        if not is_vessels:
            # Parámetros para /v3/events
            params.update({
                "datasets[0]": "public-global-fishing-events:latest",
                "start-date": start_date.strftime("%Y-%m-%d"),
                "end-date": end_date.strftime("%Y-%m-%d"),
                "offset": 0,
                "limit": 1000,  # Reduced limit for faster response
            })
        else:
            # Parámetros para /v3/vessels/search - search by query
            # Note: requires 'vessels:read' scope and access to public-global-vessel-identity dataset
            # vessels/search does NOT accept offset/limit - uses 'since' token, max 50 results
            params.update({
                "query": "Mexico",
                "datasets[0]": "public-global-vessel-identity:latest",
                "includes[0]": "MATCH_CRITERIA",
                "includes[1]": "OWNERSHIP",
                "includes[2]": "AUTHORIZATIONS",
            })

        logger.info(f"Consultando GFW API v3: {endpoint}")

        total_fetched = 0
        while True:
            try:
                response = self._session.get(
                    f"{self.api_base_url}{endpoint}",
                    params=params,
                    timeout=(5, 15)  # (connect timeout, read timeout)
                )
                response.raise_for_status()
                data = response.json()

                entries = data.get("entries", [])
                if not entries:
                    break

                df = pd.DataFrame(entries)
                df = self._standardize_api_columns(df)

                # Para vessels, no hay lat/lon - omitir H3 y bbox
                if not is_vessels:
                    # Filtrar bbox del Golfo (client-side, ya que API no lo soporta)
                    df = self._filter_gulf_bbox(df)

                    if not df.empty:
                        df = add_h3_column_vectorized(
                            df, 'lat', 'lon', 'h3_cell', self.config.h3_resolution
                        )

                        if 'timestamp' in df.columns:
                            df['year'] = pd.to_datetime(df['timestamp']).dt.year
                            df['month'] = pd.to_datetime(df['timestamp']).dt.month
                            df['time_partition'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m')
                        else:
                            df['year'] = datetime.utcnow().year
                            df['month'] = datetime.utcnow().month
                            df['time_partition'] = datetime.utcnow().strftime('%Y-%m')
                else:
                    # Vessels: no positional data, just add time partition
                    df['year'] = datetime.utcnow().year
                    df['month'] = datetime.utcnow().month
                    df['time_partition'] = datetime.utcnow().strftime('%Y-%m')

                if not df.empty:
                    yield df

                total_fetched += len(entries)
                logger.debug(f"Fetched {len(entries)} entries (total: {total_fetched})")

                # Paginación - vessels search uses 'since' token, events uses offset
                if is_vessels:
                    since = data.get("since")
                    if not since:
                        break
                    params["since"] = since
                else:
                    if len(entries) < params["limit"]:
                        break
                    params["offset"] += params["limit"]

            except requests.exceptions.RequestException as e:
                logger.error(f"Error en paginación: {e}")
                # For vessels, fall back to local files if API fails
                if is_vessels:
                    logger.info("Falling back to local files for vessels dataset")
                    yield from self._extract_from_local_files()
                raise GFWAPIError(f"GFW API request failed: {e}")

        logger.info(f"GFW API v3 extraction complete: {total_fetched} total entries")
        return  # Success, exit after working endpoint

    def _extract_from_local_files(self) -> Iterator[pd.DataFrame]:
        """Fallback: extraer desde archivos ZIP locales (Zenodo)."""
        logger.info("Extrayendo desde archivos locales (Zenodo)...")
        for year in self.target_years:
            zip_pattern = f"*fleet-daily-csvs-100-v3-{year}.zip"
            zip_files = list(self.source_dir.glob(zip_pattern))

            if not zip_files:
                logger.warning(f"No se encontró archivo para año {year}: {zip_pattern}")
                continue

            zip_path = zip_files[0]
            logger.info(f"Procesando {zip_path.name} ({zip_path.stat().st_size / 1e9:.2f} GB)")
            yield from self._process_zip_year(zip_path, year)

    def _standardize_api_columns(self, df: pd.DataFrame) -> pd.DataFrame:
            """
            Estandariza columnas de la respuesta de la API GFW v3.

            Mapea campos de la API a nombres estándar del ingester.
            La API v3 usa estructura anidada: position.lat, position.lon
            Para vessels, los datos vienen en registryInfo y selfReportedInfo
            Para events, los datos vienen en position, vessel, fishing
            """
            df = df.copy()

            # Para vessels API: extraer datos de registryInfo y selfReportedInfo
            if 'registryInfo' in df.columns:
                # registryInfo es una lista de dicts
                registry_list = df['registryInfo'].tolist()
                if registry_list and registry_list[0]:
                    # Tomar el primer registro de registryInfo
                    registry_df = pd.json_normalize([r[0] if r else {} for r in registry_list])
                    for col in ['ssvid', 'flag', 'shipname', 'geartype', 'lengthM', 'tonnageGt', 'imo', 'callsign']:
                        if col in registry_df.columns:
                            df[col.lower()] = registry_df[col].values

            if 'selfReportedInfo' in df.columns:
                self_reported_list = df['selfReportedInfo'].tolist()
                if self_reported_list and self_reported_list[0]:
                    sri_df = pd.json_normalize([r[0] if r else {} for r in self_reported_list])
                    for col in ['ssvid', 'flag', 'shipname', 'imo', 'callsign']:
                        if col in sri_df.columns and col.lower() not in df.columns:
                            df[col.lower()] = sri_df[col].values

            # Para events API: extraer datos de vessel y fishing
            if 'vessel' in df.columns:
                vessel_list = df['vessel'].tolist()
                if vessel_list and vessel_list[0]:
                    vessel_df = pd.json_normalize(vessel_list)
                    for col in ['ssvid', 'flag', 'name', 'type', 'id']:
                        if col in vessel_df.columns:
                            if col == 'name':
                                df['vessel_name'] = vessel_df[col].values
                            elif col == 'type':
                                df['ship_type'] = vessel_df[col].values
                            else:
                                df[col.lower()] = vessel_df[col].values

            if 'fishing' in df.columns:
                fishing_list = df['fishing'].tolist()
                if fishing_list and fishing_list[0]:
                    fishing_df = pd.json_normalize(fishing_list)
                    for col in ['fishing_hours', 'totalDistanceKm', 'averageSpeedKnots', 'averageDurationHours']:
                        if col in fishing_df.columns:
                            if col == 'averageDurationHours':
                                df['fishing_hours'] = fishing_df[col].values
                            else:
                                df[col.lower()] = fishing_df[col].values

            # Extraer lat/lon desde position anidado si existe (para events)
            if 'position' in df.columns:
                # position es un dict con lat/lon
                position_series = df['position']
                # Convertir a lista de dicts para json_normalize
                position_list = position_series.tolist()
                position_df = pd.json_normalize(position_list)
                if 'lat' in position_df.columns:
                    df['lat'] = position_df['lat'].values
                if 'lon' in position_df.columns:
                    df['lon'] = position_df['lon'].values

            # Mapeo de campos de la API v3
            column_map = {
                'lat': ['lat', 'latitude', 'position_lat'],
                'lon': ['lon', 'longitude', 'position_lon'],
                'fishing_hours': ['fishing_hours', 'duration_hours', 'hours'],
                'mmsi': ['mmsi', 'ssvid', 'vessel_id'],
                'gear_type': ['gear_type', 'gear', 'vessel_class', 'geartype'],
                'flag': ['flag', 'flag_state', 'country'],
                'timestamp': ['timestamp', 'event_start', 'start_time', 'time'],
                'vessel_name': ['vessel_name', 'shipname'],
                'ship_type': ['ship_type', 'vessel_type', 'class'],
                'length_m': ['length_m', 'length', 'loa', 'lengthm'],
                'tonnage_gt': ['tonnage_gt', 'tonnage', 'gt', 'tonnagegt'],
            }

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
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

            return df

    def _filter_gulf_bbox(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filtra filas dentro del bbox del Golfo de California."""
        return filter_df_bbox(df, self.config.bbox)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforma a formato estandarizado con H3."""
        
        # Para vessels, no hay datos posicionales - no añadir H3
        is_vessels = self.config.dataset_name == "gfw_vessels"
        if not is_vessels:
            # Añadir H3 cell usando utilidad compartida
            df = add_h3_column_vectorized(df, 'lat', 'lon', 'h3_cell', self.config.h3_resolution)

            # Filtrar válidos
            df = df.dropna(subset=['h3_cell'])

        # Seleccionar columnas finales
        if is_vessels:
            output_cols = [
                'year', 'month', 'time_partition',
                'mmsi', 'gear_type', 'flag', 'vessel_name', 'imo', 'callsign',
                'ship_type', 'length_m', 'tonnage_gt'
            ]
        else:
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
            if self.config.dataset_name == "gfw_vessels":
                return "gfw/vessels/"
            return "gfw/fishing_effort/"

        year = df['year'].iloc[0]
        month = df['month'].iloc[0]
        
        if self.config.dataset_name == "gfw_vessels":
            return f"gfw/vessels/"
        
        return f"gfw/fishing_effort_h3/year={year}/month={month:02d}/"


def create_gfw_ingester(dataset_type: str, catalog, storage, **kwargs):
    """Factory para crear GFWFishingEffortIngester."""
    from src.data.ingestion.factory import create_ingester
    dataset_map = {
        "fishing_effort": "gfw_fishing_effort",
        "vessels": "gfw_vessels",
    }
    dataset_name = dataset_map.get(dataset_type, "gfw_fishing_effort")
    return create_ingester(GFWFishingEffortIngester, dataset_name, catalog, storage, **kwargs)


if __name__ == "__main__":
    from src.utils.logging import setup_logging
    setup_logging("ierc_gnl.gfw_fishing")
    print("GFW Ingester module loaded")