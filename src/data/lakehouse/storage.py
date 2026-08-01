"""
Lakehouse Storage - IERC-GNL
=============================
Abstracción de almacenamiento compatible S3 para lakehouse local.
Soporta: Local filesystem, MinIO, S3, Azure Blob, GCS.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, BinaryIO, Union
from dataclasses import dataclass
from datetime import datetime
import logging
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pandas as pd
import geopandas as gpd

logger = logging.getLogger(__name__)


@dataclass
class StorageConfig:
    """Configuración de almacenamiento."""
    root_path: str
    layers: Dict[str, str]  # bronze, silver, gold -> subdirectorios
    compression: str = "zstd"
    compression_level: int = 3
    partition_filename_template: str = "part-{i}.parquet"


class LocalFileStorage:
    """
    Almacenamiento local compatible con API S3-like.
    Usa pyarrow para lectura/escritura eficiente de Parquet.
    """
    
    def __init__(self, config: StorageConfig):
        self.config = config
        self.root = Path(config.root_path)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Crea estructura de directorios del lakehouse."""
        for layer_name, layer_path in self.config.layers.items():
            full_path = self.root / layer_path
            full_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directorio asegurado: {full_path}")
    
    def _resolve_path(self, layer: str, relative_path: str) -> Path:
        """Resuelve ruta relativa a absoluta."""
        if layer not in self.config.layers:
            raise ValueError(f"Capa desconocida: {layer}. Disponibles: {list(self.config.layers.keys())}")
        return self.root / self.config.layers[layer] / relative_path
    
    def write_parquet(self,
                      df: pd.DataFrame,
                      layer: str,
                      relative_path: str,
                      partition_cols: Optional[List[str]] = None,
                      compression: Optional[str] = None,
                      **kwargs) -> Path:
        """
        Escribe DataFrame a Parquet particionado.
        
        Args:
            df: DataFrame a escribir
            layer: bronze, silver, gold
            relative_path: Ruta relativa dentro de la capa (ej: "nasa/chlor_a/year=2024/month=01/")
            partition_cols: Columnas para particionar (ej: ["h3_cell_8", "year"])
            compression: Compresión (zstd, snappy, gzip)
        
        Returns:
            Path al directorio escrito
        """
        output_path = self._resolve_path(layer, relative_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Convertir a PyArrow Table para mejor control
        table = pa.Table.from_pandas(df, preserve_index=False)
        
        # Escribir dataset particionado
        pq.write_to_dataset(
            table,
            root_path=str(output_path),
            partition_cols=partition_cols or [],
            compression=compression or self.config.compression,
            compression_level=self.config.compression_level,
            basename_template=self.config.partition_filename_template,
            existing_data_behavior="overwrite_or_ignore",
            **kwargs
        )
        
        logger.info(f"Escrito {len(df)} filas a {layer}:{relative_path} "
                   f"(particiones: {partition_cols or 'ninguna'})")
        return output_path
    
    def write_geoparquet(self,
                         gdf: gpd.GeoDataFrame,
                         layer: str,
                         relative_path: str,
                         partition_cols: Optional[List[str]] = None,
                         **kwargs) -> Path:
        """Escribe GeoDataFrame a GeoParquet."""
        # GeoPandas usa pyarrow internamente para GeoParquet
        output_path = self._resolve_path(layer, relative_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Escribir como dataset particionado
        if partition_cols:
            # Para particionado, escribir cada partición por separado
            for partition_values, partition_df in gdf.groupby(partition_cols, observed=True):
                if not isinstance(partition_values, tuple):
                    partition_values = (partition_values,)
                
                partition_path = output_path
                for col, val in zip(partition_cols, partition_values):
                    partition_path = partition_path / f"{col}={val}"
                
                partition_path.mkdir(parents=True, exist_ok=True)
                file_path = partition_path / f"part-{hash(partition_values) % 10000}.parquet"
                partition_df.to_parquet(file_path, compression=self.config.compression, **kwargs)
        else:
            # Archivo único
            file_path = output_path / "data.parquet"
            gdf.to_parquet(file_path, compression=self.config.compression, **kwargs)
        
        logger.info(f"Escrito GeoDataFrame {len(gdf)} filas a {layer}:{relative_path}")
        return output_path
    
    def read_parquet(self,
                     layer: str,
                     relative_path: str,
                     columns: Optional[List[str]] = None,
                     filters: Optional[List[tuple]] = None,
                     **kwargs) -> pd.DataFrame:
        """
        Lee Parquet como DataFrame con pushdown de filtros y columnas.
        
        Args:
            layer: bronze, silver, gold
            relative_path: Ruta relativa
            columns: Columnas a leer (column pruning)
            filters: Filtros para predicate pushdown
                Ej: [("year", "=", 2024), ("h3_cell_8", "in", ["8a2a1072b5afff", "8a2a1072b5bfff"])]
        
        Returns:
            DataFrame con datos filtrados
        """
        path = self._resolve_path(layer, relative_path)
        
        if not path.exists():
            logger.warning(f"Ruta no existe: {path}")
            return pd.DataFrame()
        
        import pyarrow.compute as pc
        dataset = ds.dataset(str(path), format="parquet")
        
        # Build filter expression for predicate pushdown
        filter_expr = None
        if filters:
            for col, op, val in filters:
                field = pc.field(col)
                if op == '=':
                    expr = field == val
                elif op == '!=':
                    expr = field != val
                elif op == '>':
                    expr = field > val
                elif op == '<':
                    expr = field < val
                elif op == '>=':
                    expr = field >= val
                elif op == '<=':
                    expr = field <= val
                elif op == 'in':
                    expr = field.isin(val)
                else:
                    raise ValueError(f"Unsupported operator: {op}")
                
                if filter_expr is None:
                    filter_expr = expr
                else:
                    filter_expr = filter_expr & expr
        
        scanner = dataset.scanner(
            columns=columns,
            filter=filter_expr,
            **kwargs
        )
        
        return scanner.to_table().to_pandas()
    
    def read_geoparquet(self,
                        layer: str,
                        relative_path: str,
                        columns: Optional[List[str]] = None,
                        filters: Optional[List[tuple]] = None,
                        **kwargs) -> gpd.GeoDataFrame:
        """Lee GeoParquet como GeoDataFrame."""
        df = self.read_parquet(layer, relative_path, columns, filters, **kwargs)
        if df.empty:
            return gpd.GeoDataFrame()
        
        # Detectar columna geometría
        geom_col = None
        for col in df.columns:
            if df[col].apply(lambda x: hasattr(x, '__geo_interface__')).any():
                geom_col = col
                break
        
        if geom_col:
            return gpd.GeoDataFrame(df, geometry=geom_col, crs="EPSG:4326")
        return gpd.GeoDataFrame(df)
    
    def list_partitions(self, layer: str, relative_path: str) -> List[Dict[str, str]]:
        """Lista particiones disponibles en una ruta."""
        path = self._resolve_path(layer, relative_path)
        if not path.exists():
            return []
        
        partitions = []
        for part_dir in path.rglob("*"):
            if part_dir.is_dir() and "=" in part_dir.name:
                # Extraer pares key=value de la ruta relativa
                rel = part_dir.relative_to(path)
                parts = {}
                for component in rel.parts:
                    if "=" in component:
                        k, v = component.split("=", 1)
                        parts[k] = v
                if parts:
                    partitions.append(parts)
        
        return partitions
    
    def get_table_schema(self, layer: str, relative_path: str) -> pa.Schema:
        """Obtiene esquema de una tabla Parquet sin leer datos."""
        path = self._resolve_path(layer, relative_path)
        dataset = ds.dataset(str(path), format="parquet")
        return dataset.schema
    
    def delete_partition(self, layer: str, relative_path: str, 
                         partition_filters: Dict[str, str]) -> int:
        """Elimina particiones específicas (para re-procesamiento)."""
        path = self._resolve_path(layer, relative_path)
        if not path.exists():
            return 0
        
        deleted = 0
        for part_dir in path.rglob("*"):
            if part_dir.is_dir():
                match = True
                for k, v in partition_filters.items():
                    if f"{k}={v}" not in str(part_dir.relative_to(path)):
                        match = False
                        break
                if match:
                    shutil.rmtree(part_dir)
                    deleted += 1
        
        logger.info(f"Eliminadas {deleted} particiones de {layer}:{relative_path}")
        return deleted
    
    def get_size_bytes(self, layer: str, relative_path: str) -> int:
        """Obtiene tamaño total en bytes."""
        path = self._resolve_path(layer, relative_path)
        if not path.exists():
            return 0
        return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    
    def exists(self, layer: str, relative_path: str) -> bool:
        """Verifica si existe una ruta."""
        return self._resolve_path(layer, relative_path).exists()


def create_storage_from_config(config_path: str) -> LocalFileStorage:
    """Crea storage desde archivo de configuración YAML."""
    import yaml
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    lakehouse_config = config.get('lakehouse', {})
    storage_config = StorageConfig(
        root_path=lakehouse_config.get('root_path', '/home/gorops/ierc-gnl-project/lakehouse'),
        layers=lakehouse_config.get('layers', {
            'bronze': 'raw',
            'silver': 'processed',
            'gold': 'curated'
        }),
        compression=lakehouse_config.get('compression', 'zstd'),
        compression_level=lakehouse_config.get('compression_level', 3)
    )
    
    return LocalFileStorage(storage_config)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test rápido
    config = StorageConfig(
        root_path="/tmp/test_lakehouse",
        layers={'bronze': 'raw', 'silver': 'processed', 'gold': 'curated'}
    )
    storage = LocalFileStorage(config)
    
    # Test write/read
    import pandas as pd
    df = pd.DataFrame({
        'h3_cell_8': ['8a2a1072b5afff', '8a2a1072b5bfff', '8a2a1072b5cfff'],
        'year': [2024, 2024, 2024],
        'month': [1, 1, 2],
        'chlor_a_mean': [0.5, 0.7, 0.3],
        'chlor_a_std': [0.1, 0.2, 0.05]
    })
    
    storage.write_parquet(df, 'silver', 'nasa/chlor_a/', partition_cols=['h3_cell_8', 'year', 'month'])
    
    # Leer con filtro
    result = storage.read_parquet('silver', 'nasa/chlor_a/', 
                                  filters=[('year', '=', 2024), ('month', '=', 1)])
    print(f"Leídas {len(result)} filas con filtro year=2024, month=1")
    print(result)