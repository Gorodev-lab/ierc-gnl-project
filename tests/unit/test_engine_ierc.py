"""
Unit Tests — IERC Calculator Engine & Monte Carlo Engine
==========================================================
"""

import pytest
from src.engine.ierc_calculator import IERCConfig, IERCCalculator
from src.engine.monte_carlo_engine import MonteCarloConfig, MonteCarloEngine


def test_ierc_config_defaults():
    """Verifica valores por defecto de la configuración IERC."""
    config = IERCConfig()
    assert config.monte_carlo_iterations == 1000
    assert config.confidence_threshold == 0.7
    assert len(config.quincenas) == 24
    assert config.normalization_method == "minmax"


def test_monte_carlo_config_validation(temp_dir):
    """Prueba la validación y rutas por defecto en MonteCarloConfig."""
    config = MonteCarloConfig(
        output_csv_path=str(temp_dir / "monte_carlo.csv"),
        report_path=str(temp_dir / "monte_carlo_report.txt")
    )
    config.validate()
    assert config.iterations == 1000
    assert config.output_csv_path.endswith("monte_carlo.csv")


def test_monte_carlo_engine_simulation(sample_ierc_components):
    """Prueba la simulación de incertidumbre en Monte Carlo sin base de datos."""
    engine = MonteCarloEngine(db_engine=None)
    result = engine.simulate_uncertainty(sample_ierc_components)

    assert "mean_IERC" in result
    assert "std_dev_IERC" in result
    assert "confidence_dato" in result
    assert "uncertainty_level" in result

    assert 0.0 <= result["mean_IERC"] <= 100.0
    assert 0.0 <= result["confidence_dato"] <= 1.0
    assert result["uncertainty_level"] in ["Bajo", "Moderado", "Alto", "Desconocido"]
