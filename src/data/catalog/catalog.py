"""
Data Catalog - IERC-GNL Lakehouse
==================================
Catálogo centralizado basado en DuckDB para metadata, linaje y calidad de datos.
"""

import duckdb
import yaml
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, field
from datetime import datetime
from contextlib import contextmanager
import hashlib


logger = logging.getLogger(__name__)


@dataclass
class DatasetMetadata:
    """Metadatos de un dataset en el catálogo."""
    name: str
    description: str
    source_type: str  # api, file, zenodo, doi
    source_path: str
    format: str
    crs: str
    temporal_frequency: str
    temporal_range: List[str]
    spatial_bbox: List[float]  # [min_lat, min_lon, max_lat, max_lon]
    h3_resolution: int
    schema: Dict[str, Any]
    lakehouse_paths: Dict[str, str]
    quality_expectations: List[str]
    priority: str
    tags: List[str]
    status: str = "active"
    size_estimate_gb: Optional[float] = None
    cdc_enabled: bool = False
    cdc_key_column: Optional[str] = None
    cdc_hash_columns: Optional[List[str]] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


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
    Catálogo de datos basado en DuckDB.
    
    Proporciona:
    - Registro de datasets y sus metadatos
    - Tracking de ejecuciones de ingesta (lineage)
    - Validación de calidad
    - Consulta de metadatos para pipelines downstream
    """
    
    def __init__(self, catalog_path: str):
        self.catalog_path = Path(catalog_path)
        self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.catalog_path))
        self._init_schema()
        logger.info(f"DataCatalog inicializado en {self.catalog_path}")
    
    def _init_schema(self):
        """Inicializa el esquema del catálogo."""
        # Tabla de datasets
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS datasets (
                name VARCHAR PRIMARY KEY,
                description VARCHAR,
                source_type VARCHAR,
                source_path VARCHAR,
                format VARCHAR,
                crs VARCHAR,
                temporal_frequency VARCHAR,
                temporal_range VARCHAR,  -- JSON array
                spatial_bbox VARCHAR,    -- JSON array [min_lat, min_lon, max_lat, max_lon]
                h3_resolution INTEGER,
                schema VARCHAR,          -- JSON
                lakehouse_paths VARCHAR, -- JSON
                quality_expectations VARCHAR,  -- JSON array
                priority VARCHAR,
                tags VARCHAR,            -- JSON array
                status VARCHAR DEFAULT 'active',
                size_estimate_gb DOUBLE,
                cdc_enabled BOOLEAN DEFAULT FALSE,
                cdc_key_column VARCHAR,
                cdc_hash_columns VARCHAR,  -- JSON array
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        
        # Tabla de ejecuciones de ingesta (lineage)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS ingestion_runs (
                run_id VARCHAR PRIMARY KEY,
                dataset_name VARCHAR,
                started_at TIMESTAMP,
                finished_at TIMESTAMP,
                status VARCHAR,
                records_processed BIGINT,
                records_inserted BIGINT,
                records_updated BIGINT,
                records_failed BIGINT,
                input_path VARCHAR,
                output_path VARCHAR,
                error_message VARCHAR,
                quality_results VARCHAR,  -- JSON
                FOREIGN KEY (dataset_name) REFERENCES datasets(name)
            )
        """)
        
        # Tabla de validaciones de calidad
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS quality_validations (
                validation_id VARCHAR PRIMARY KEY,
                run_id VARCHAR,
                dataset_name VARCHAR,
                expectation_name VARCHAR,
                success BOOLEAN,
                observed_value VARCHAR,
                details VARCHAR,
                validated_at TIMESTAMP,
                FOREIGN KEY (run_id) REFERENCES ingestion_runs(run_id)
            )
        """)
        
        # Tabla de H3 cells válidas por resolución (pre-calculadas)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS valid_h3_cells (
                h3_cell VARCHAR,
                resolution INTEGER,
                bbox_min_lat DOUBLE,
                bbox_min_lon DOUBLE,
                bbox_max_lat DOUBLE,
                bbox_max_lon DOUBLE,
                PRIMARY KEY (h3_cell, resolution)
            )
        """)
        
        # Índices para performance
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_ingestion_runs_dataset ON ingestion_runs(dataset_name)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_ingestion_runs_started ON ingestion_runs(started_at)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_quality_runs ON quality_validations(run_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_valid_h3_resolution ON valid_h3_cells(resolution)")
        
        logger.debug("Esquema del catálogo inicializado")
    
    @contextmanager
    def transaction(self):
        """Context manager para transacciones."""
        in_transaction = False
        try:
            # DuckDB auto-commits by default, only use explicit transaction if needed
            yield self.conn
            in_transaction = True
            self.conn.commit()
        except Exception as e:
            if in_transaction:
                try:
                    self.conn.rollback()
                except:
                    pass  # Ignore rollback errors
            logger.error(f"Transacción fallida: {e}")
            raise
    
    # ============================================================
    # Dataset Management
    # ============================================================
    
    def register_dataset(self, metadata: DatasetMetadata) -> bool:
        """Registra o actualiza un dataset en el catálogo."""
        with self.transaction():
            existing = self.conn.execute(
                "SELECT name FROM datasets WHERE name = ?", [metadata.name]
            ).fetchone()
            
            if existing:
                # Actualizar
                self.conn.execute("""
                    UPDATE datasets SET
                        description = ?, source_type = ?, source_path = ?, format = ?,
                        crs = ?, temporal_frequency = ?, temporal_range = ?, spatial_bbox = ?,
                        h3_resolution = ?, schema = ?, lakehouse_paths = ?,
                        quality_expectations = ?, priority = ?, tags = ?, status = ?,
                        size_estimate_gb = ?, cdc_enabled = ?, cdc_key_column = ?,
                        cdc_hash_columns = ?, updated_at = ?
                    WHERE name = ?
                """, [
                    metadata.description, metadata.source_type, metadata.source_path,
                    metadata.format, metadata.crs, metadata.temporal_frequency,
                    json.dumps(metadata.temporal_range), json.dumps(metadata.spatial_bbox),
                    metadata.h3_resolution, json.dumps(metadata.schema),
                    json.dumps(metadata.lakehouse_paths), json.dumps(metadata.quality_expectations),
                    metadata.priority, json.dumps(metadata.tags), metadata.status,
                    metadata.size_estimate_gb, metadata.cdc_enabled, metadata.cdc_key_column,
                    json.dumps(metadata.cdc_hash_columns) if metadata.cdc_hash_columns else None,
                    datetime.utcnow(), metadata.name
                ])
                logger.info(f"Dataset actualizado: {metadata.name}")
            else:
                # Insertar
                self.conn.execute("""
                    INSERT INTO datasets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    metadata.name, metadata.description, metadata.source_type,
                    metadata.source_path, metadata.format, metadata.crs,
                    metadata.temporal_frequency, json.dumps(metadata.temporal_range),
                    json.dumps(metadata.spatial_bbox), metadata.h3_resolution,
                    json.dumps(metadata.schema), json.dumps(metadata.lakehouse_paths),
                    json.dumps(metadata.quality_expectations), metadata.priority,
                    json.dumps(metadata.tags), metadata.status, metadata.size_estimate_gb,
                    metadata.cdc_enabled, metadata.cdc_key_column,
                    json.dumps(metadata.cdc_hash_columns) if metadata.cdc_hash_columns else None,
                    metadata.created_at, metadata.updated_at
                ])
                logger.info(f"Dataset registrado: {metadata.name}")
        return True
    
    def get_dataset(self, name: str) -> Optional[DatasetMetadata]:
        """Obtiene metadatos de un dataset."""
        row = self.conn.execute(
            "SELECT * FROM datasets WHERE name = ?", [name]
        ).fetchone()
        
        if not row:
            return None
        
        cols = [desc[0] for desc in self.conn.description]
        data = dict(zip(cols, row))
        
        # Parsear campos JSON
        for field in ['temporal_range', 'spatial_bbox', 'schema', 'lakehouse_paths', 
                      'quality_expectations', 'tags', 'cdc_hash_columns']:
            if data[field]:
                data[field] = json.loads(data[field])
        
        return DatasetMetadata(**data)
    
    def list_datasets(self, 
                      status: Optional[str] = None,
                      priority: Optional[str] = None,
                      tags: Optional[List[str]] = None) -> List[DatasetMetadata]:
        """Lista datasets con filtros opcionales."""
        query = "SELECT * FROM datasets WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        if tags:
            # Filtrar por tags (contiene alguno de los tags)
            tag_conditions = " OR ".join(["tags LIKE ?" for _ in tags])
            query += f" AND ({tag_conditions})"
            params.extend([f"%{tag}%" for tag in tags])
        
        query += " ORDER BY priority DESC, name"
        
        rows = self.conn.execute(query, params).fetchall()
        cols = [desc[0] for desc in self.conn.description]
        
        datasets = []
        for row in rows:
            data = dict(zip(cols, row))
            for field in ['temporal_range', 'spatial_bbox', 'schema', 'lakehouse_paths', 
                          'quality_expectations', 'tags', 'cdc_hash_columns']:
                if data[field]:
                    data[field] = json.loads(data[field])
            datasets.append(DatasetMetadata(**data))
        
        return datasets
    
    # ============================================================
    # Ingestion Run Tracking (Lineage)
    # ============================================================
    
    def start_ingestion_run(self, 
                            dataset_name: str,
                            input_path: Optional[str] = None,
                            run_id: Optional[str] = None) -> str:
        """Inicia tracking de una ejecución de ingesta."""
        if run_id is None:
            run_id = f"{dataset_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(str(datetime.utcnow()).encode()).hexdigest()[:8]}"
        
        run = IngestionRun(
            run_id=run_id,
            dataset_name=dataset_name,
            started_at=datetime.utcnow().isoformat(),
            input_path=input_path,
            status="running"
        )
        
        with self.transaction():
            self.conn.execute("""
                INSERT INTO ingestion_runs 
                (run_id, dataset_name, started_at, status, input_path)
                VALUES (?, ?, ?, ?, ?)
            """, [run.run_id, run.dataset_name, run.started_at, run.status, run.input_path])
        
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
        with self.transaction():
            self.conn.execute("""
                UPDATE ingestion_runs SET
                    finished_at = ?, status = ?, records_processed = ?,
                    records_inserted = ?, records_updated = ?, records_failed = ?,
                    output_path = ?, error_message = ?, quality_results = ?
                WHERE run_id = ?
            """, [
                datetime.utcnow().isoformat(), status, records_processed,
                records_inserted, records_updated, records_failed,
                output_path, error_message,
                json.dumps(quality_results) if quality_results else None,
                run_id
            ])
        
        logger.info(f"Ingestion run finalizado: {run_id} - {status}")
    
    def get_ingestion_history(self, 
                              dataset_name: Optional[str] = None,
                              limit: int = 50) -> List[IngestionRun]:
        """Obtiene historial de ejecuciones."""
        query = "SELECT * FROM ingestion_runs WHERE 1=1"
        params = []
        
        if dataset_name:
            query += " AND dataset_name = ?"
            params.append(dataset_name)
        
        query += " ORDER BY started_at DESC LIMIT ?"
        params.append(limit)
        
        rows = self.conn.execute(query, params).fetchall()
        cols = [desc[0] for desc in self.conn.description]
        
        runs = []
        for row in rows:
            data = dict(zip(cols, row))
            if data['quality_results']:
                data['quality_results'] = json.loads(data['quality_results'])
            runs.append(IngestionRun(**data))
        
        return runs
    
    # ============================================================
    # Quality Validation Tracking
    # ============================================================
    
    def record_quality_validation(self,
                                  run_id: str,
                                  dataset_name: str,
                                  expectation_name: str,
                                  success: bool,
                                  observed_value: Any,
                                  details: Optional[str] = None):
        """Registra resultado de validación de calidad."""
        validation_id = f"{run_id}_{expectation_name}_{datetime.utcnow().strftime('%H%M%S')}"
        
        with self.transaction():
            self.conn.execute("""
                INSERT INTO quality_validations
                (validation_id, run_id, dataset_name, expectation_name, success, observed_value, details, validated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                validation_id, run_id, dataset_name, expectation_name,
                success, str(observed_value), details, datetime.utcnow().isoformat()
            ])
    
    def get_quality_summary(self, dataset_name: str, 
                            last_n_runs: int = 10) -> Dict[str, Any]:
        """Resumen de calidad para un dataset."""
        query = """
            SELECT qv.expectation_name, 
                   COUNT(*) as total_runs,
                   SUM(CASE WHEN qv.success THEN 1 ELSE 0 END) as passed,
                   AVG(CASE WHEN qv.success THEN 1.0 ELSE 0.0 END) as pass_rate
            FROM quality_validations qv
            JOIN ingestion_runs ir ON qv.run_id = ir.run_id
            WHERE qv.dataset_name = ?
            GROUP BY qv.expectation_name
            ORDER BY pass_rate ASC
        """
        rows = self.conn.execute(query, [dataset_name]).fetchall()
        
        return {
            "dataset": dataset_name,
            "expectations": [
                {"name": r[0], "total_runs": r[1], "passed": r[2], "pass_rate": r[3]}
                for r in rows
            ]
        }
    
    # ============================================================
    # H3 Valid Cells
    # ============================================================
    
    def load_valid_h3_cells(self, h3_cells_by_resolution: Dict[int, List[str]], 
                            bbox: List[float]):
        """Carga celdas H3 válidas para el Golfo (pre-calculadas)."""
        with self.transaction():
            self.conn.execute("DELETE FROM valid_h3_cells")
            min_lat, min_lon, max_lat, max_lon = bbox
            
            for resolution, cells in h3_cells_by_resolution.items():
                for cell in cells:
                    self.conn.execute("""
                        INSERT INTO valid_h3_cells VALUES (?, ?, ?, ?, ?, ?)
                    """, [cell, resolution, min_lat, min_lon, max_lat, max_lon])
            
            total = sum(len(c) for c in h3_cells_by_resolution.values())
            logger.info(f"Cargadas {total} celdas H3 válidas en catálogo")
    
    def get_valid_h3_cells(self, resolution: int) -> List[str]:
        """Obtiene celdas H3 válidas para una resolución."""
        rows = self.conn.execute(
            "SELECT h3_cell FROM valid_h3_cells WHERE resolution = ?", [resolution]
        ).fetchall()
        return [r[0] for r in rows]
    
    # ============================================================
    # Utility
    # ============================================================
    
    def close(self):
        """Cierra conexión."""
        self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def load_catalog_from_yaml(catalog_path: str, yaml_path: str) -> DataCatalog:
    """Carga catálogo desde archivo YAML."""
    catalog = DataCatalog(catalog_path)
    
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Cargar datasets
    for name, ds_config in config.get('datasets', {}).items():
        if ds_config.get('status') == 'pending_access':
            continue
            
        # Extraer source_path
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
        
        # Esquema simplificado para el catálogo
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
    
    # Cargar H3 cells válidas si están en config
    catalog_config = config.get('catalog_config', {})
    if 'valid_h3_cells_gulf' in catalog_config:
        # Generar celdas H3 para el bbox si no están pre-calculadas
        pass  # Se calcularán on-demand
    
    logger.info(f"Catálogo cargado desde {yaml_path}")
    return catalog


if __name__ == "__main__":
    # Test rápido
    logging.basicConfig(level=logging.INFO)
    
    catalog = load_catalog_from_yaml(
        "/home/gorops/ierc-gnl-project/lakehouse/metadata/catalog.duckdb",
        "/home/gorops/ierc-gnl-project/config/data_catalog.yaml"
    )
    
    datasets = catalog.list_datasets()
    print(f"\nDatasets registrados: {len(datasets)}")
    for ds in datasets:
        print(f"  - {ds.name} [{ds.priority}] ({ds.format})")
    
    catalog.close()