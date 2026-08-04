"""
Unit Tests — DataCatalog & LocalFileStorage
============================================
"""

import pytest
import pandas as pd
from src.data.catalog.catalog import DataCatalog, DatasetMetadata
from src.data.lakehouse.storage import LocalFileStorage, StorageConfig


def test_datacatalog_register_and_get(temp_dir):
    """Prueba el registro y recuperación de metadatos de dataset en el catálogo JSON."""
    catalog = DataCatalog(catalog_dir=temp_dir / "catalog")
    metadata = DatasetMetadata(
        name="test_dataset",
        description="Dataset de prueba para la suite unitaria",
        format="parquet",
        h3_resolution=8,
        priority="high"
    )

    registered = catalog.register_dataset(metadata)
    assert registered is True

    retrieved = catalog.get_dataset("test_dataset")
    assert retrieved is not None
    assert retrieved.name == "test_dataset"
    assert retrieved.priority == "high"
    assert retrieved.h3_resolution == 8


def test_datacatalog_ingestion_run_tracking(temp_dir):
    """Prueba el tracking de ejecuciones de ingesta (runs.jsonl)."""
    catalog = DataCatalog(catalog_dir=temp_dir / "catalog")
    run_id = catalog.start_ingestion_run(dataset_name="test_dataset", input_path="data/raw/test.csv")
    assert run_id.startswith("test_dataset_")

    catalog.finish_ingestion_run(
        run_id=run_id,
        status="success",
        records_processed=100,
        records_inserted=100
    )

    history = catalog.get_ingestion_history("test_dataset")
    assert len(history) == 1
    assert history[0].run_id == run_id
    assert history[0].status == "success"
    assert history[0].records_processed == 100


def test_local_file_storage_parquet_roundtrip(temp_dir, sample_fishing_df):
    """Prueba la escritura y lectura Parquet particionado en LocalFileStorage."""
    config = StorageConfig(
        root_path=str(temp_dir / "lakehouse"),
        layers={"bronze": "raw", "silver": "processed", "gold": "curated"},
        compression="zstd"
    )
    storage = LocalFileStorage(config)

    # Write
    out_path = storage.write_parquet(
        df=sample_fishing_df,
        layer="silver",
        relative_path="gfw/test_effort",
        partition_cols=["year"]
    )
    assert out_path.exists()

    # Read back
    read_df = storage.read_parquet(layer="silver", relative_path="gfw/test_effort")
    assert not read_df.empty
    assert len(read_df) == len(sample_fishing_df)
    assert set(read_df.columns) == set(sample_fishing_df.columns)


def test_local_file_storage_predicate_pushdown(temp_dir, sample_fishing_df):
    """Prueba el filtrado predicate pushdown al leer Parquet."""
    config = StorageConfig(
        root_path=str(temp_dir / "lakehouse"),
        layers={"silver": "processed"}
    )
    storage = LocalFileStorage(config)

    storage.write_parquet(
        df=sample_fishing_df,
        layer="silver",
        relative_path="gfw/test_filter",
        partition_cols=["year"]
    )

    filtered_df = storage.read_parquet(
        layer="silver",
        relative_path="gfw/test_filter",
        filters=[("year", "=", 2022)]
    )
    assert len(filtered_df) == 2
    assert (filtered_df["year"] == 2022).all()
