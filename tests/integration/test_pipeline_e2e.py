"""
Integration Test — End-to-End IERC Pipeline
==============================================
Procesa datos sintéticos a través de H3, Catálogo, Storage y Simulación Monte Carlo.
"""

import pytest
import pandas as pd
from src.utils.h3 import add_h3_column_vectorized
from src.utils.ierc import compute_ierc
from src.data.catalog.catalog import DataCatalog, DatasetMetadata
from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
from src.engine.monte_carlo_engine import MonteCarloEngine, MonteCarloConfig


def test_pipeline_e2e_flow(temp_dir, sample_fishing_df):
    """
    Ejecución del pipeline sintético end-to-end:
    1. Registro de dataset en DataCatalog
    2. Adición de celdas H3
    3. Escritura en Lakehouse (Parquet particionado)
    4. Lectura desde Lakehouse y cálculo IERC + Monte Carlo
    """
    # 1. Init DataCatalog & Storage
    catalog = DataCatalog(catalog_dir=temp_dir / "catalog")
    storage_config = StorageConfig(
        root_path=str(temp_dir / "lakehouse"),
        layers={"bronze": "raw", "silver": "processed", "gold": "curated"}
    )
    storage = LocalFileStorage(storage_config)

    metadata = DatasetMetadata(
        name="gfw_fishing_effort",
        description="Esfuerzo pesquero de prueba E2E",
        format="parquet",
        h3_resolution=8
    )
    catalog.register_dataset(metadata)

    # 2. Add H3 cells
    df_h3 = add_h3_column_vectorized(sample_fishing_df, lat_col="lat", lon_col="lon", h3_col="h3_cell", resolution=8)
    assert "h3_cell" in df_h3.columns

    # 3. Write to Silver layer
    run_id = catalog.start_ingestion_run(dataset_name="gfw_fishing_effort")
    out_path = storage.write_parquet(
        df=df_h3,
        layer="silver",
        relative_path="gfw/effort_h3",
        partition_cols=["year"]
    )
    catalog.finish_ingestion_run(run_id=run_id, status="success", records_processed=len(df_h3))

    # 4. Read back and compute IERC
    read_df = storage.read_parquet(layer="silver", relative_path="gfw/effort_h3")
    assert len(read_df) == len(sample_fishing_df)

    # Simulate component scores for each unique H3 cell
    unique_cells = read_df["h3_cell"].unique()
    mc_engine = MonteCarloEngine(db_engine=None, config=MonteCarloConfig(iterations=100))

    mc_results = []
    for cell in unique_cells:
        scores = {
            "amenaza": 0.4,
            "exposicion": 0.5,
            "sensibilidad": 0.3,
            "dependencia": 0.2,
            "valor_biocultural": 0.7,
            "capacidad_adaptativa": 0.6
        }
        res = mc_engine.simulate_uncertainty(scores)
        res["h3_cell"] = cell
        mc_results.append(res)

    assert len(mc_results) == len(unique_cells)
    assert all("mean_IERC" in r for r in mc_results)
