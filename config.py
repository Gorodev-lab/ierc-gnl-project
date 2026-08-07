"""
Project Configuration — IERC-GNL
================================
Centralized paths and configuration. All hardcoded paths should use this module.
"""

from pathlib import Path
from typing import Optional


# Project root: this file is at /home/gorops/ierc-gnl-project/config.py
PROJECT_ROOT = Path(__file__).resolve().parent


def get_data_dir(subdir: str = "") -> Path:
    """
    Get a directory under PROJECT_ROOT/data/.
    
    Args:
        subdir: Optional subdirectory (e.g., "raw/gfw", "processed")
    
    Returns:
        Path object for the directory (created if needed)
    """
    path = PROJECT_ROOT / "data" / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_log_dir() -> Path:
    """Get the logs directory."""
    path = PROJECT_ROOT / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_deliverables_dir(version: str = "v1_geopackage") -> Path:
    """Get a deliverables directory."""
    path = PROJECT_ROOT / "deliverables" / version
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_config_dir() -> Path:
    """Get the config directory."""
    return PROJECT_ROOT / "config"


def get_causanatura_dir(subdir: str = "") -> Path:
    """Get a directory under causanaturadata/."""
    path = PROJECT_ROOT / "causanaturadata" / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_raw_dir(source: str) -> Path:
    """Get raw data directory for a specific source."""
    return get_data_dir(f"raw/{source}")


def get_processed_dir() -> Path:
    """Get processed data directory."""
    return get_data_dir("processed")


def get_lakehouse_dir(layer: str = "silver") -> Path:
    """Get lakehouse directory for a specific layer."""
    layer_map = {"bronze": "raw", "silver": "processed", "gold": "curated"}
    sub = layer_map.get(layer, layer)
    path = PROJECT_ROOT / "lakehouse" / sub
    path.mkdir(parents=True, exist_ok=True)
    return path


# Legacy hardcoded paths - DEPRECATED, use functions above
LEGACY_PROJECT_ROOT = Path("/home/gorops/ierc-gnl-project")
LEGACY_DATA_DIR = LEGACY_PROJECT_ROOT / "data"
LEGACY_RAW_DIR = LEGACY_DATA_DIR / "raw"
LEGACY_PROCESSED_DIR = LEGACY_DATA_DIR / "processed"
LEGACY_LOGS_DIR = LEGACY_PROJECT_ROOT / "logs"
LEGACY_DELIVERABLES_DIR = LEGACY_PROJECT_ROOT / "deliverables" / "v1_geopackage"
LEGACY_CAUSANATURA_DIR = LEGACY_PROJECT_ROOT / "causanaturadata" / "output"

# Environment-based overrides
import os

def get_env_path(env_var: str, default: Optional[Path] = None) -> Optional[Path]:
    """Get path from environment variable, with optional default."""
    value = os.environ.get(env_var)
    if value:
        return Path(value)
    return default


# Convenience functions for common paths
def gfw_raw_dir() -> Path:
    return get_raw_dir("gfw")

def pangas_raw_dir() -> Path:
    return get_raw_dir("pangas_wgs84")

def nasa_raw_dir() -> Path:
    return get_raw_dir("nasa_oceancolor")

def bathymetry_raw_dir() -> Path:
    return get_raw_dir("bathymetry")

def asea_raw_dir() -> Path:
    return get_causanatura_dir("output")

def h3_output_dir() -> Path:
    return get_lakehouse_dir("silver")

def cenegas_raw_dir() -> Path:
    return get_raw_dir("cenegas")

def sener_raw_dir() -> Path:
    return get_raw_dir("sener")

def gasoductos_raw_dir() -> Path:
    return get_raw_dir("gasoductos")

def profepa_raw_dir() -> Path:
    return get_raw_dir("profepa")

def semarnat_raw_dir() -> Path:
    return get_raw_dir("semarnat")

def ecc_raw_dir() -> Path:
    return get_raw_dir("ecc_climabase")