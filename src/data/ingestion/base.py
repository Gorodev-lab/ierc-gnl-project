"""
Base Ingestion Classes - IERC-GNL
==================================
Clases base para pipelines de ingesta con tracking y calidad.
"""

import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Iterator, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from contextlib import contextmanager
import json

import pandas as pd
import geopandas as gpd

from ..catalog.catalog import DataCatalog, IngestionRun, DatasetMetadata
from ..lakehouse.storage import LocalFileStorage, StorageConfig
from src.utils.h3 import (
    add_h3_column_vectorized, vector_to_h3_grid, netcdf_to_h3_parquet,
    create_temporal_partition_columns, get_gulf_h3_cells
)
from src.utils.logging import setup_logging

logger = setup_logging(__name__)


@dataclass
class IngestionConfig:
    """Configuración base para ingesta."""
    dataset_name: str
    layer: str = "silver"  # bronze, silver, gold
    partition_cols: List[str] = field(default_factory=lambda: ["h3_cell", "year", "month"])
    h3_resolution: int = 8
    bbox: Tuple[float, float, float, float] = (22.5, -115.0, 32.0, -108.0)
    compression: str = "zstd"
    batch_size: int = 100000
    validate: bool = True
    # CDC / exact-once deduplication
    cdc_key_column: str = ""           # columna clave única (ej. proyecto_id)
    cdc_hash_columns: List[str] = field(default_factory=list)  # columnas para hash de contenido


class BaseIngester:
    """
    Clase base para ingestores.

    Proporciona:
    - Tracking de ejecuciones en catálogo
    - Escritura particionada en lakehouse
    - Validación de calidad básica
    """

    def __init__(self,
                 config: IngestionConfig,
                 catalog: DataCatalog,
                 storage: LocalFileStorage):
        self.config = config
        self.catalog = catalog
        self.storage = storage
        self.run_id: Optional[str] = None
        self.records_processed = 0
        self.records_inserted = 0
        self.records_updated = 0
        self.records_failed = 0
        self.errors: List[str] = []

    def extract(self) -> Iterator[pd.DataFrame]:
        """
        Extrae datos de la fuente.

        Yields:
            DataFrames en batches para procesamiento streaming
        """
        raise NotImplementedError("Subclasses must implement extract()")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma datos crudos a formato estandarizado.

        Args:
            df: DataFrame crudo

        Returns:
            DataFrame transformado con columnas estándar (h3_cell, time_partition, etc.)
        """
        raise NotImplementedError("Subclasses must implement transform()")

    def load(self, df: pd.DataFrame, partition_path: str) -> Path:
        """
        Carga DataFrame transformado al lakehouse.

        Args:
            df: DataFrame transformado
            partition_path: Ruta relativa dentro de la capa

        Returns:
            Path escrito
        """
        return self.storage.write_parquet(
            df,
            layer=self.config.layer,
            relative_path=partition_path,
            partition_cols=self.config.partition_cols,
            compression=self.config.compression
        )

    def validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validaciones básicas de calidad + schema contract.

        Returns:
            Dict con resultados de validación
        """
        # --- Schema contract validation ---
        schema_results = self._validate_schema_contract(df)

        results = {
            "total_rows": len(df),
            "null_counts": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "h3_cells_unique": df['h3_cell'].nunique() if 'h3_cell' in df.columns else 0,
            "time_partitions": df['time_partition'].nunique() if 'time_partition' in df.columns else 0,
            "passed": schema_results["passed"],
            "warnings": schema_results["warnings"]
        }

        # Validaciones específicas
        if 'h3_cell' in df.columns:
            null_h3 = df['h3_cell'].isnull().sum()
            if null_h3 > 0:
                results["warnings"].append(f"{null_h3} filas sin h3_cell válido")
                results["passed"] = False

        if 'time_partition' in df.columns:
            null_time = df['time_partition'].isnull().sum()
            if null_time > 0:
                results["warnings"].append(f"{null_time} filas sin time_partition")

        # Validar bbox
        if 'lat' in df.columns and 'lon' in df.columns:
            min_lat, min_lon, max_lat, max_lon = self.config.bbox
            try:
                out_of_bbox = (
                    (df['lat'] < min_lat) | (df['lat'] > max_lat) |
                    (df['lon'] < min_lon) | (df['lon'] > max_lon)
                ).sum()
                if out_of_bbox > 0:
                    results["warnings"].append(f"{out_of_bbox} filas fuera del bbox del Golfo")
            except TypeError:
                # Columnas lat/lon no son numéricas - ya reportado por schema contract
                pass

        return results

    def _validate_schema_contract(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Valida DataFrame contra schema registrado en catálogo."""
        ds_meta = self.catalog.get_dataset(self.config.dataset_name)
        if not ds_meta or not ds_meta.schema.get("columns"):
            return {"passed": True, "warnings": []}

        # Solo validar columnas de negocio (no particiones técnicas ni derivadas)
        # Las columnas técnicas añadidas durante ingesta: h3_cell*, year, month, time_partition, ingestion_timestamp, _cdc_hash
        technical_cols = {'year', 'month', 'time_partition', 'ingestion_timestamp', '_cdc_hash'}
        h3_prefix = 'h3_cell'

        expected_cols = [
            c["name"] if isinstance(c, dict) else c 
            for c in ds_meta.schema["columns"]
        ]
        # Filtrar columnas técnicas del DataFrame para comparar
        business_cols = [c for c in df.columns if c not in technical_cols and not c.startswith(h3_prefix)]
        
        missing = set(expected_cols) - set(business_cols)
        extra = set(business_cols) - set(expected_cols)

        warnings = []
        if missing:
            warnings.append(f"Schema contract: columnas faltantes {missing}")
        if extra:
            warnings.append(f"Schema contract: columnas extra no declaradas {extra}")

        # Validar tipos si están definidos
        type_warnings = []
        for col_def in ds_meta.schema["columns"]:
            if isinstance(col_def, dict):
                expected_type = col_def.get("dtype") or col_def.get("type")
                if expected_type:
                    col_name = col_def["name"]
                    if col_name in df.columns:
                        actual_type = str(df[col_name].dtype)
                        # Mapeo pandas dtype -> schema type (incluyendo identidades)
                        type_map = {
                            "int64": "int64", "int32": "int32", "int16": "int16", "int8": "int8",
                            "float64": "float64", "float32": "float32",
                            "object": "string", "str": "string", "string": "string",
                            "datetime64[ns]": "timestamp", "datetime64[ns, UTC]": "timestamp",
                            "bool": "boolean"
                        }
                        actual_normalized = type_map.get(actual_type, actual_type).lower()
                        expected_normalized = expected_type.lower()
                        if actual_normalized != expected_normalized:
                            # Solo warn si son tipos fundamentalmente distintos (no float32 vs float64)
                            if not (expected_normalized in ("float32", "float64") and actual_normalized in ("float32", "float64")):
                                type_warnings.append(f"{col_name}: esperado {expected_type}, got {actual_type}")

        passed = len(missing) == 0 and len(type_warnings) == 0
        return {"passed": passed, "warnings": warnings + type_warnings}

    def run(self, input_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Ejecuta pipeline completo de ingesta.

        Returns:
            Dict con resumen de la ejecución
        """
        logger.info(f"Iniciando ingesta: {self.config.dataset_name}")

        # Iniciar tracking en catálogo
        self.run_id = self.catalog.start_ingestion_run(
            dataset_name=self.config.dataset_name,
            input_path=input_path
        )

        try:
            # Procesar cada batch
            batch_idx = -1
            for batch_idx, batch_df in enumerate(self.extract()):
                logger.debug(f"Procesando batch {batch_idx + 1}: {len(batch_df)} filas")

                # Transformar
                transformed = self.transform(batch_df)

                # CDC deduplication (exact-once)
                transformed = self._deduplicate_by_cdc_hash(transformed)

                # Validar
                quality_results = self.validate_data(transformed)

                if self.config.validate and not quality_results["passed"]:
                    logger.warning(f"Validación fallida batch {batch_idx}: {quality_results['warnings']}")
                    self.records_failed += len(transformed)
                    continue

                # Determinar ruta de partición
                partition_path = self._get_partition_path(transformed)

                # Cargar
                self.load(transformed, partition_path)

                self.records_processed += len(batch_df)
                self.records_inserted += len(transformed)

                # Registrar calidad en catálogo si el método existe
                for warning in quality_results.get("warnings", []):
                    pass

            # Finalizar con éxito (after ALL batches)
            self.catalog.finish_ingestion_run(
                run_id=self.run_id,
                status="success",
                records_processed=self.records_processed,
                records_inserted=self.records_inserted,
                records_updated=self.records_updated,
                records_failed=self.records_failed,
                quality_results={
                    "total_batches": batch_idx + 1,
                    "warnings_count": len(self.errors)
                }
            )

            logger.info(f"Ingesta completada: {self.config.dataset_name} - "
                       f"{self.records_inserted} registros insertados")

            return {
                "status": "success",
                "run_id": self.run_id,
                "records_processed": self.records_processed,
                "records_inserted": self.records_inserted,
                "records_updated": self.records_updated,
                "records_failed": self.records_failed
            }

        except Exception as e:
            logger.error(f"Error en ingesta {self.config.dataset_name}: {e}")
            self.catalog.finish_ingestion_run(
                run_id=self.run_id,
                status="failed",
                records_processed=self.records_processed,
                records_inserted=self.records_inserted,
                records_updated=self.records_updated,
                records_failed=self.records_failed,
                error_message=str(e)
            )
            return {
                "status": "failed",
                "run_id": self.run_id,
                "error_message": str(e)
            }

    def _get_partition_path(self, df: pd.DataFrame) -> str:
        """Genera ruta de partición basada en dataset y datos."""
        # Por defecto: dataset_name/
        return f"{self.config.dataset_name}/"

    # --- CDC / exact-once deduplication ---
    def _deduplicate_by_cdc_hash(self, df: pd.DataFrame) -> pd.DataFrame:
        """Elimina filas cuyo hash de contenido ya existe en el lakehouse."""
        if not self.config.cdc_hash_columns or not self.config.cdc_key_column:
            return df
        if df.empty:
            return df

        # Hash de contenido por fila (vectorizado con pandas)
        content = df[self.config.cdc_hash_columns].astype(str).agg('|'.join, axis=1)
        df = df.copy()
        df['_cdc_hash'] = content.apply(lambda x: hashlib.md5(x.encode()).hexdigest()[:16])

        # Leer hashes existentes del lakehouse (una vez por run)
        if not hasattr(self, '_existing_hashes'):
            try:
                existing = self.storage.read_parquet(
                    self.config.layer,
                    self._get_partition_path(df),
                    columns=[self.config.cdc_key_column, '_cdc_hash']
                )
                self._existing_hashes = set(existing['_cdc_hash'].tolist()) if not existing.empty else set()
            except Exception:
                self._existing_hashes = set()

        # Filtrar solo filas nuevas
        new_mask = ~df['_cdc_hash'].isin(list(self._existing_hashes))
        n_dups = len(df) - int(new_mask.sum())
        if n_dups:
            logger.info(f"CDC dedup: {len(df)} filas → {int(new_mask.sum())} nuevas ({n_dups} duplicados)")
        # Mantener _cdc_hash para persistencia en lakehouse
        return df.loc[new_mask].reset_index(drop=True)


if __name__ == "__main__":
    # Test de imports
    print("Base ingester classes loaded successfully")