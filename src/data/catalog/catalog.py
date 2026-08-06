"""
Data Catalog — IERC-GNL (Simplified JSON-based)
================================================
Minimal metadata tracking. Replaces 556-line DuckDB version with ~80 lines of JSON.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid


logger = logging.getLogger(__name__)


@dataclass
class DatasetMetadata:
    """Metadatos de un dataset en el catálogo."""
    name: str
    description: str = ""
    source_type: str = "file"
    source_path: str = ""
    format: str = "parquet"
    crs: str = "EPSG:4326"
    temporal_frequency: str = "static"
    temporal_range: List[str] = None
    spatial_bbox: List[float] = None
    h3_resolution: int = 8
    schema: Dict[str, Any] = None
    lakehouse_paths: Dict[str, str] = None
    quality_expectations: List[str] = None
    priority: str = "medium"
    tags: List[str] = None
    status: str = "active"
    size_estimate_gb: Optional[float] = None
    cdc_enabled: bool = False
    cdc_key_column: Optional[str] = None
    cdc_hash_columns: Optional[List[str]] = None
    created_at: str = None
    updated_at: str = None

    def __post_init__(self):
        if self.temporal_range is None:
            self.temporal_range = ["", ""]
        if self.spatial_bbox is None:
            self.spatial_bbox = [22.5, -115.0, 32.0, -108.0]
        if self.schema is None:
            self.schema = {}
        if self.lakehouse_paths is None:
            self.lakehouse_paths = {}
        if self.quality_expectations is None:
            self.quality_expectations = []
        if self.tags is None:
            self.tags = []
        if self.cdc_hash_columns is None:
            self.cdc_hash_columns = []
        now = datetime.utcnow().isoformat()
        if self.created_at is None:
            self.created_at = now
        self.updated_at = now


@dataclass
class IngestionRun:
    """Registro de una ejecución de ingesta."""
    run_id: str
    dataset_name: str
    started_at: str
    finished_at: Optional[str] = None
    status: str = "running"  # running, success, failed, partial
    records_processed: int = 0
    records_inserted: int = 0
    records_updated: int = 0
    records_failed: int = 0
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    quality_results: Optional[Dict[str, Any]] = None


class DataCatalog:
    """
    Catálogo de datos basado en archivos JSON.

    Proporciona:
    - Registro de datasets y sus metadatos (datasets.json)
    - Tracking de ejecuciones de ingesta (runs.jsonl)
    - Consulta simple de metadatos
    """

    def __init__(self, catalog_dir: Union[str, Path] = None):
        if catalog_dir is None:
            from config import get_data_dir
            catalog_dir = get_data_dir("catalog")

        self.catalog_dir = Path(catalog_dir)
        self.catalog_dir.mkdir(parents=True, exist_ok=True)

        self.datasets_file = self.catalog_dir / "datasets.json"
        self.runs_file = self.catalog_dir / "runs.jsonl"

        # Initialize files if they don't exist
        if not self.datasets_file.exists():
            self.datasets_file.write_text("[]", encoding="utf-8")

        logger.info(f"DataCatalog inicializado en {self.catalog_dir}")

    def _load_datasets(self) -> List[Dict]:
        """Carga datasets desde JSON."""
        try:
            return json.loads(self.datasets_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_datasets(self, datasets: List[Dict]):
        """Guarda datasets a JSON."""
        self.datasets_file.write_text(
            json.dumps(datasets, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def _append_run(self, run: IngestionRun):
        """Añade una ejecución al log JSONL."""
        with self.runs_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(run), ensure_ascii=False) + "\n")

    # ============================================================
    # Dataset Management
    # ============================================================

    def register_dataset(self, metadata: DatasetMetadata) -> bool:
        """Registra o actualiza un dataset en el catálogo."""
        datasets = self._load_datasets()

        # Check if exists
        existing_idx = None
        for i, ds in enumerate(datasets):
            if ds["name"] == metadata.name:
                existing_idx = i
                break

        metadata.updated_at = datetime.utcnow().isoformat()
        data = asdict(metadata)

        if existing_idx is not None:
            # Update
            data["created_at"] = datasets[existing_idx].get("created_at", metadata.created_at)
            datasets[existing_idx] = data
            logger.info(f"Dataset actualizado: {metadata.name}")
        else:
            # Insert
            datasets.append(data)
            logger.info(f"Dataset registrado: {metadata.name}")

        self._save_datasets(datasets)
        return True

    def get_dataset(self, name: str) -> Optional[DatasetMetadata]:
        """Obtiene metadatos de un dataset."""
        datasets = self._load_datasets()
        for ds in datasets:
            if ds["name"] == name:
                return DatasetMetadata(**ds)
        return None

    def list_datasets(self,
                      status: Optional[str] = None,
                      priority: Optional[str] = None,
                      tags: Optional[List[str]] = None) -> List[DatasetMetadata]:
        """Lista datasets con filtros opcionales."""
        datasets = self._load_datasets()

        filtered = []
        for ds in datasets:
            if status and ds.get("status") != status:
                continue
            if priority and ds.get("priority") != priority:
                continue
            if tags:
                ds_tags = ds.get("tags", [])
                if not any(tag in ds_tags for tag in tags):
                    continue
            filtered.append(DatasetMetadata(**ds))

        # Sort by priority desc, then name
        priority_order = {"critical": 3, "high": 2, "medium": 1, "low": 0}
        filtered.sort(key=lambda d: (-priority_order.get(d.priority, 0), d.name))

        return filtered

    # ============================================================
    # Ingestion Run Tracking (Lineage)
    # ============================================================

    def start_ingestion_run(self,
                            dataset_name: str,
                            input_path: Optional[str] = None,
                            run_id: Optional[str] = None) -> str:
        """Inicia tracking de una ejecución de ingesta."""
        if run_id is None:
            run_id = f"{dataset_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        run = IngestionRun(
            run_id=run_id,
            dataset_name=dataset_name,
            started_at=datetime.utcnow().isoformat(),
            input_path=input_path,
            status="running"
        )

        self._append_run(run)
        logger.info(f"Ingestion run iniciado: {run_id}")
        return run_id

    def finish_ingestion_run(self,
                             run_id: str,
                             status: str,
                             records_processed: int = 0,
                             records_inserted: int = 0,
                             records_updated: int = 0,
                             records_failed: int = 0,
                             output_path: Optional[str] = None,
                             error_message: Optional[str] = None,
                             quality_results: Optional[Dict] = None):
        """Finaliza tracking de una ejecución de ingesta."""
        # Read all runs, find and update the matching one
        runs = []
        if self.runs_file.exists():
            with self.runs_file.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        runs.append(json.loads(line))

        # Update the matching run
        for run in runs:
            if run["run_id"] == run_id:
                run["finished_at"] = datetime.utcnow().isoformat()
                run["status"] = status
                run["records_processed"] = records_processed
                run["records_inserted"] = records_inserted
                run["records_updated"] = records_updated
                run["records_failed"] = records_failed
                run["output_path"] = output_path
                run["error_message"] = error_message
                run["quality_results"] = quality_results
                break

        # Rewrite the entire file
        with self.runs_file.open("w", encoding="utf-8") as f:
            for run in runs:
                f.write(json.dumps(run, ensure_ascii=False) + "\n")

        logger.info(f"Ingestion run finalizado: {run_id} - {status}")

    def get_ingestion_history(self,
                              dataset_name: Optional[str] = None,
                              limit: int = 50) -> List[IngestionRun]:
        """Obtiene historial de ejecuciones."""
        runs = []
        if self.runs_file.exists():
            with self.runs_file.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        run_data = json.loads(line)
                        if dataset_name is None or run_data.get("dataset_name") == dataset_name:
                            runs.append(IngestionRun(**run_data))

        # Sort by started_at desc
        runs.sort(key=lambda r: r.started_at, reverse=True)
        return runs[:limit]

    def register_derived_dataset(self,
                                 name: str,
                                 source_datasets: List[str],
                                 transform_logic_version: str,
                                 **metadata) -> DatasetMetadata:
        """Registra dataset derivado con lineage y versión de lógica."""
        tags = metadata.pop("tags", []) + ["derived"]
        # Embebir lineage en schema para trazabilidad
        schema = metadata.get("schema", {})
        schema["lineage"] = {
            "sources": source_datasets,
            "transform_version": transform_logic_version,
            "created_by": "pipeline_v1"
        }
        metadata["schema"] = schema
        metadata["tags"] = tags
        metadata["lakehouse_paths"] = metadata.get("lakehouse_paths", {"gold": f"curated/{name}/"})

        ds_meta = DatasetMetadata(name=name, **metadata)
        self.register_dataset(ds_meta)
        return ds_meta


def load_catalog_from_yaml(catalog_dir: Union[str, Path], yaml_path: str) -> DataCatalog:
    """Carga catálogo desde archivo YAML."""
    import yaml

    catalog = DataCatalog(catalog_dir)

    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    for name, ds_config in config.get('datasets', {}).items():
        if ds_config.get('status') == 'pending_access':
            continue

        source = ds_config.get('source', {})
        if source.get('type') == 'file':
            source_path = source.get('path', '')
        elif source.get('type') == 'zenodo':
            source_path = f"zenodo:{source.get('record_id')}"
        elif source.get('type') == 'api':
            source_path = source.get('url', '')
        elif source.get('type') == 'doi':
            source_path = source.get('url', '')
        else:
            source_path = source.get('path', '')

        schema_config = ds_config.get('schema', {})
        if 'columns' in schema_config:
            columns = schema_config['columns']
        elif 'variables' in schema_config:
            columns = schema_config['variables']
        elif 'properties' in schema_config:
            columns = schema_config['properties']
        else:
            columns = []

        metadata = DatasetMetadata(
            name=name,
            description=ds_config.get('description', ''),
            source_type=source.get('type', 'file'),
            source_path=source_path,
            format=ds_config.get('format', 'parquet'),
            crs=ds_config.get('crs', 'EPSG:4326'),
            temporal_frequency=ds_config.get('temporal', {}).get('frequency', 'static'),
            temporal_range=ds_config.get('temporal', {}).get('range', ['', '']),
            spatial_bbox=ds_config.get('spatial', {}).get('bbox', [22.5, -115.0, 32.0, -108.0]),
            h3_resolution=ds_config.get('spatial', {}).get('h3_resolution', 8),
            schema={"columns": columns, "derived": ds_config.get('schema', {}).get('derived_columns', [])},
            lakehouse_paths=ds_config.get('lakehouse', {}),
            quality_expectations=ds_config.get('quality', {}).get('expectations', []),
            priority=ds_config.get('priority', 'medium'),
            tags=ds_config.get('tags', []),
            status=ds_config.get('status', 'active'),
            size_estimate_gb=ds_config.get('size_estimate_gb'),
            cdc_enabled=ds_config.get('quality', {}).get('cdc', {}).get('enabled', False),
            cdc_key_column=ds_config.get('quality', {}).get('cdc', {}).get('key_column'),
            cdc_hash_columns=ds_config.get('quality', {}).get('cdc', {}).get('hash_columns')
        )

        catalog.register_dataset(metadata)

    logger.info(f"Catálogo cargado desde {yaml_path}")
    return catalog