"""
Shared IERC Formula — IERC-GNL
================================
Pure function for IERC calculation. Used by both calculator and Monte Carlo.
"""

from typing import Dict
import numpy as np


IERC_WEIGHTS = {
    'amenaza': 0.20,
    'exposicion': 0.20,
    'sensibilidad': 0.15,
    'dependencia': 0.15,
    'valor_biocultural': 0.15,
    'capacidad_adaptativa': 0.15
}


def compute_ierc(
    amenaza: float,
    exposicion: float,
    sensibilidad: float,
    dependencia: float,
    valor_biocultural: float,
    capacidad_adaptativa: float,
    weights: Dict[str, float] = None
) -> float:
    """
    Compute IERC index from component scores.
    
    IERC_total = (Amenaza × 0.20) + (Exposición × 0.20) + (Sensibilidad × 0.15) +
                 (Dependencia × 0.15) + (Valor_Biocultural × 0.15) +
                 ((1 - Capacidad_Adaptativa) × 0.15)
    
    All inputs should be normalized to [0, 1].
    
    Args:
        amenaza: Normalized threat score [0, 1]
        exposicion: Normalized exposure score [0, 1]
        sensibilidad: Normalized sensitivity score [0, 1]
        dependencia: Normalized dependency score [0, 1]
        valor_biocultural: Normalized biocultural value score [0, 1]
        capacidad_adaptativa: Normalized adaptive capacity score [0, 1]
        weights: Optional custom weights (defaults to official methodology)
    
    Returns:
        IERC total score [0, 1]
    """
    w = weights or IERC_WEIGHTS
    
    ierc = (
        amenaza * w['amenaza'] +
        exposicion * w['exposicion'] +
        sensibilidad * w['sensibilidad'] +
        dependencia * w['dependencia'] +
        valor_biocultural * w['valor_biocultural'] +
        (1.0 - capacidad_adaptativa) * w['capacidad_adaptativa']
    )
    
    return float(np.clip(ierc, 0.0, 1.0))


def compute_ierc_components(
    component_scores: Dict[str, float],
    weights: Dict[str, float] = None
) -> float:
    """
    Compute IERC from a dict of component scores.
    
    Args:
        component_scores: Dict with keys matching IERC_WEIGHTS
        weights: Optional custom weights
    
    Returns:
        IERC total score [0, 1]
    """
    w = weights or IERC_WEIGHTS
    required = set(w.keys())
    missing = required - set(component_scores.keys())
    if missing:
        raise ValueError(f"Missing required components: {missing}")
    
    return compute_ierc(
        amenaza=component_scores['amenaza'],
        exposicion=component_scores['exposicion'],
        sensibilidad=component_scores['sensibilidad'],
        dependencia=component_scores['dependencia'],
        valor_biocultural=component_scores['valor_biocultural'],
        capacidad_adaptativa=component_scores['capacidad_adaptativa'],
        weights=weights
    )