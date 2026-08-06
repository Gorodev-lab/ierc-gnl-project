"""
Ingestion Factory Helpers - IERC-GNL
====================================
Shared factory functions to avoid boilerplate.
"""

from typing import Dict, Any, Optional, Type
from src.data.ingestion.base import IngestionConfig
from src.data.catalog.catalog import DataCatalog
from src.data.lakehouse.storage import LocalFileStorage


# Default configurations per dataset type
DATASET_DEFAULTS = {
    "pangas_fishing_zones": {
        "layer": "silver",
        "partition_cols": [],
        "h3_resolution": 8,
        "bbox": (22.5, -115.0, 32.0, -108.0),
        "compression": "zstd",
        "batch_size": 50000,
        "validate": True
    },
    "tnc_bajos_marinos": {
        "layer": "silver",
        "partition_cols": ["tnc_layer"],
        "h3_resolution": 8,
        "bbox": (22.5, -115.0, 32.0, -108.0),
        "compression": "zstd",
        "batch_size": 50000,
        "validate": True
    },
    "tnc_arrecifes_coral_negro": {
        "layer": "silver",
        "partition_cols": ["tnc_layer"],
        "h3_resolution": 8,
        "bbox": (22.5, -115.0, 32.0, -108.0),
        "compression": "zstd",
        "batch_size": 50000,
        "validate": True
    },
    "nasa_chlor_a": {
        "layer": "silver",
        "partition_cols": ["year", "month"],
        "h3_resolution": 8,
        "bbox": (22.5, -115.0, 32.0, -108.0),
        "compression": "zstd",
        "batch_size": 50000,
        "validate": False
    },
    "nasa_sst": {
        "layer": "silver",
        "partition_cols": ["year", "month"],
        "h3_resolution": 8,
        "bbox": (22.5, -115.0, 32.0, -108.0),
        "compression": "zstd",
        "batch_size": 50000,
        "validate": False
    },
    "bathymetry_gebco": {
        "layer": "silver",
        "partition_cols": ["resolution"],
        "h3_resolution": 8,
        "bbox": (22.5, -115.0, 32.0, -108.0),
        "compression": "zstd",
        "batch_size": 50000,
        "validate": True
    },
    "gfw_fishing_effort": {
        "layer": "silver",
        "partition_cols": ["h3_cell", "year", "month"],
        "h3_resolution": 8,
        "bbox": (22.5, -115.0, 32.0, -108.0),
        "compression": "zstd",
        "batch_size": 100000,
        "validate": True
    },
    "gfw_vessels": {
        "layer": "silver",
        "partition_cols": [],
        "h3_resolution": 8,
        "bbox": (22.5, -115.0, 32.0, -108.0),
        "compression": "zstd",
        "batch_size": 50000,
        "validate": True
    },
    "asea_mias": {
        "layer": "silver",
        "partition_cols": ["h3_cell_10", "year", "month"],
        "h3_resolution": 10,
        "bbox": (22.5, -115.0, 32.0, -108.0),
        "compression": "zstd",
        "batch_size": 50000,
        "validate": True,
        "cdc_key_column": "proyecto_id",
        "cdc_hash_columns": ["nombre", "estado", "tipo_proyecto", "lat", "lon", "estatus", "capacidad_mtpa", "longitud_km", "folio_asea", "pdf_url"]
    }
}


def make_ingester_config(dataset_name: str, overrides: Optional[Dict[str, Any]] = None) -> IngestionConfig:
    """Create IngestionConfig from defaults + overrides."""
    defaults = DATASET_DEFAULTS.get(dataset_name, {})
    if not defaults:
        raise ValueError(f"Unknown dataset: {dataset_name}. Available: {list(DATASET_DEFAULTS.keys())}")

    config = IngestionConfig(dataset_name=dataset_name, **defaults)
    
    if overrides:
        for k, v in overrides.items():
            setattr(config, k, v)
    
    return config


def create_ingester(ingester_class: Type, dataset_name: str,
                    catalog: DataCatalog, storage: LocalFileStorage,
                    config_overrides: Optional[Dict[str, Any]] = None,
                    **class_kwargs) -> Any:
    """Generic factory for creating ingesters."""
    config = make_ingester_config(dataset_name, config_overrides)
    return ingester_class(
        config=config,
        catalog=catalog,
        storage=storage,
        **class_kwargs
    )


if __name__ == "__main__":
    print("Available datasets:", list(DATASET_DEFAULTS.keys()))