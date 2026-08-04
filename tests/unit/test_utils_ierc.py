"""
Unit Tests — IERC Shared Formula (src/utils/ierc.py)
=====================================================
"""

import pytest
from src.utils.ierc import compute_ierc, compute_ierc_components, IERC_WEIGHTS


def test_compute_ierc_bounds():
    """Verifica que el índice IERC se mantenga estrictamente entre 0.0 y 1.0."""
    # Min risk case (capacidad adaptativa = 1.0, resto 0.0)
    min_risk = compute_ierc(0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    assert min_risk == pytest.approx(0.0)

    # Max risk case (capacidad adaptativa = 0.0, resto 1.0)
    max_risk = compute_ierc(1.0, 1.0, 1.0, 1.0, 1.0, 0.0)
    assert max_risk == pytest.approx(1.0)


def test_compute_ierc_weights_sum():
    """Verifica que la suma de los pesos oficiales sea exactamente 1.0."""
    total_weight = sum(IERC_WEIGHTS.values())
    assert total_weight == pytest.approx(1.0)


def test_compute_ierc_components(sample_ierc_components):
    """Prueba la función wrapper compute_ierc_components."""
    score = compute_ierc_components(sample_ierc_components)
    assert 0.0 <= score <= 1.0

    # Test error cuando falta un componente
    incomplete = sample_ierc_components.copy()
    del incomplete["amenaza"]
    with pytest.raises(ValueError, match="Missing required components"):
        compute_ierc_components(incomplete)


def test_adaptive_capacity_inverse_relation():
    """Verifica que mayor capacidad adaptativa reduzca el riesgo IERC."""
    base_kwargs = {
        "amenaza": 0.5,
        "exposicion": 0.5,
        "sensibilidad": 0.5,
        "dependencia": 0.5,
        "valor_biocultural": 0.5,
    }
    low_adapt = compute_ierc(**base_kwargs, capacidad_adaptativa=0.2)
    high_adapt = compute_ierc(**base_kwargs, capacidad_adaptativa=0.8)
    assert high_adapt < low_adapt
