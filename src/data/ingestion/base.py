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
        Validaciones básicas de calidad.

        Returns:
            Dict con resultados de validación
        """
        results = {
            "total_rows": len(df),
            "null_counts": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "h3_cells_unique": df['h3_cell'].nunique() if 'h3_cell' in df.columns else 0,
            "time_partitions": df['time_partition'].nunique() if 'time_partition' in df.columns else 0,
            "passed": True,
            "warnings": []
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
            out_of_bbox = (
                (df['lat'] < min_lat) | (df['lat'] > max_lat) |
                (df['lon'] < min_lon) | (df['lon'] > max_lon)
            ).sum()
            if out_of_bbox > 0:
                results["warnings"].append(f"{out_of_bbox} filas fuera del bbox del Golfo")

        return results

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

                # Finalizar con éxito
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


if __name__ == "__main__":
    # Test de imports
    print("Base ingester classes loaded successfully")