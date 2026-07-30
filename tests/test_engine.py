"""
Test Suite for IERC-GNL Data Pipeline
=======================================
Suite de pruebas unitarias con pytest.
"""

import os
import sys
import pytest
import logging
import json
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_geopackage_existence():
    """Valida la existencia del GeoPackage entregable."""
    gpkg_path = Path("/home/gorops/ierc-gnl-project/deliverables/v1_geopackage/ierc_golfo_california.gpkg")
    assert gpkg_path.exists(), "El GeoPackage entregable v1.1 debe existir."

def test_data_output():
    """Valida la generación de datasets de cobertura."""
    json_path = Path("/home/gorops/ierc-gnl-project/causanaturadata/output/reporte_cobertura_datos.json")
    assert json_path.exists(), "El reporte de cobertura JSON debe existir."
