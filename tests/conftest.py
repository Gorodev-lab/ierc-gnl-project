"""
Pytest Fixtures — IERC-GNL Test Suite
======================================
Fixtures compartidos para pruebas unitarias e integración.
"""

import tempfile
from pathlib import Path
import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon


@pytest.fixture
def sample_coords():
    """Coordenadas de prueba en el Golfo de California (Puerto Libertad / Guaymas)."""
    return [
        {"lat": 29.9107, "lon": -112.6835, "site": "Puerto Libertad"},
        {"lat": 27.9179, "lon": -110.9039, "site": "Guaymas"},
        {"lat": 31.8667, "lon": -116.6333, "site": "Ensenada"},
    ]


@pytest.fixture
def sample_fishing_df():
    """DataFrame sintético de esfuerzo pesquero para pruebas de H3 e ingesta."""
    return pd.DataFrame({
        "lat": [29.9107, 29.9150, 27.9179, 31.0833],
        "lon": [-112.6835, -112.6800, -110.9039, -114.8500],
        "fishing_hours": [12.5, 8.0, 24.1, 5.5],
        "mmsi": ["123456789", "987654321", "123456789", "555555555"],
        "gear_type": ["trawlers", "longliners", "trawlers", "fixed_gear"],
        "flag": ["MEX", "MEX", "USA", "MEX"],
        "year": [2022, 2022, 2023, 2023],
        "month": [5, 5, 10, 10]
    })


@pytest.fixture
def sample_gdf():
    """GeoDataFrame sintético de polígonos de zonas de pesca PANGAS."""
    poly1 = Polygon([(-112.7, 29.9), (-112.6, 29.9), (-112.6, 30.0), (-112.7, 30.0)])
    poly2 = Polygon([(-111.0, 27.9), (-110.8, 27.9), (-110.8, 28.0), (-111.0, 28.0)])
    return gpd.GeoDataFrame({
        "zone_id": ["Z001", "Z002"],
        "arte_pesca": ["PANGAS", "BUCEO"],
        "spp_code": ["carspp", "lutarg"],
        "geometry": [poly1, poly2]
    }, crs="EPSG:4326")


@pytest.fixture
def sample_ierc_components():
    """Componentes normalizados del IERC (0 a 1)."""
    return {
        "amenaza": 0.65,
        "exposicion": 0.50,
        "sensibilidad": 0.40,
        "dependencia": 0.30,
        "valor_biocultural": 0.80,
        "capacidad_adaptativa": 0.60
    }


@pytest.fixture
def temp_dir():
    """Directorio temporal para catálogo y pruebas de almacenamiento."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
