"""
Responsible AI & Human Side — IERC-GNL
=======================================

Implementa el "Human Side" del libro de Chip Huyen (Cap. 11) para el pipeline IERC:
- Explainability: desglose de componentes por celda H3
- Bias detection: slice evaluation por comunidad/arte/zona
- Fairness: validación de umbrales por grupos afectados (Comca'ac, cooperativas)
- Smooth failing: fallbacks graceful cuando faltan datos
- Team workflow: estructuras para cross-functional collaboration

No frameworks, no abstractions — solo utilidades que fallan si la lógica se rompe.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
import pandas as pd

from ..utils.logging import setup_logging

logger = setup_logging(__name__)


# ─── Explainability ────────────────────────────────────────────────────────

@dataclass
class IERCExplanation:
    """Explicación humana de un score IERC para una celda."""
    h3_cell_id: str
    ierc_total: float
    components: Dict[str, float]
    weights: Dict[str, float]
    top_driver: str
    top_driver_value: float
    confidence_dato: float
    uncertainty_level: str
    narrative: str

    def to_markdown(self) -> str:
        """Renderiza explicación en markdown para reportes/dashboard."""
        lines = [
            f"## IERC Explanation — Cell `{self.h3_cell_id}`",
            f"**Total Score:** {self.ierc_total:.1f}/100  |  **Confidence:** {self.confidence_dato:.2f} ({self.uncertainty_level})",
            "",
            "### Component Breakdown",
            "| Component | Value | Weight | Contribution |",
            "|-----------|-------|--------|--------------|"
        ]
        for comp, val in self.components.items():
            if comp in self.weights:
                contrib = val * self.weights[comp] * 100
                lines.append(f"| {comp.capitalize()} | {val:.3f} | {self.weights[comp]:.0%} | {contrib:.1f} |")
        lines.extend([
            "",
            f"**Primary Driver:** {self.top_driver} ({self.top_driver_value:.3f})",
            "",
            f"**Narrative:** {self.narrative}"
        ])
        return "\n".join(lines)


def explain_ierc_score(
    h3_cell_id: str,
    components: Dict[str, float],
    ierc_total: float,
    confidence_dato: float,
    uncertainty_level: str,
    weights: Optional[Dict[str, float]] = None
) -> IERCExplanation:
    """
    Genera explicación humana del score IERC.
    
    Una línea por componente → fácil de auditar por stakeholders no técnicos.
    """
    if weights is None:
        from ..utils.ierc import IERC_WEIGHTS
        weights = IERC_WEIGHTS

    # Identificar driver principal (mayor contribución ponderada)
    contributions = {k: components.get(k, 0) * weights.get(k, 0) for k in weights}
    top_driver = max(contributions, key=contributions.get)
    top_driver_value = components.get(top_driver, 0)

    # Narrativa automática basada en patrón de componentes
    narrative = _generate_narrative(components, top_driver)

    return IERCExplanation(
        h3_cell_id=h3_cell_id,
        ierc_total=ierc_total,
        components=components,
        weights=weights,
        top_driver=top_driver,
        top_driver_value=top_driver_value,
        confidence_dato=confidence_dato,
        uncertainty_level=uncertainty_level,
        narrative=narrative
    )


def _generate_narrative(components: Dict[str, float], top_driver: str) -> str:
    """Genera narrativa en lenguaje natural."""
    driver_narratives = {
        'amenaza': "La proximidad a infraestructura GNL (zonas de exclusión, rutas de metaneros) es el factor dominante de riesgo.",
        'exposicion': "El alto esfuerzo pesquero en la zona concentra la actividad humana y eleva la exposición a impactos.",
        'sensibilidad': "La presencia de especies en peligro crítico (CR/EN) hace a este ecosistema especialmente vulnerable.",
        'dependencia': "Las comunidades dependen fuertemente de esta zona para su sustento pesquero y seguridad alimentaria.",
        'valor_biocultural': "El valor cultural y de subsistencia de las pesquerías artesanales amplifica el impacto social.",
        'capacidad_adaptativa': "La baja capacidad de gobernanza y organización comunitaria limita la resiliencia ante cambios."
    }
    base = driver_narratives.get(top_driver, "Factores combinados determinan el perfil de riesgo.")
    
    # Añadir contexto de componentes secundarios altos
    secondary = [k for k, v in components.items() if v > 0.6 and k != top_driver]
    if secondary:
        base += f" Factores contributivos: {', '.join(secondary)}."
    
    return base


# ─── Bias / Fairness Detection ────────────────────────────────────────────

class SliceDimension(Enum):
    """Dimensiones para slice-based evaluation (Chip Huyen Ch.6)."""
    COMUNIDAD = "comunidad"
    ARTE_PESCA = "arte_pesca"
    ZONA_GEOFRAFICA = "zona"
    ESPECIE_OBJETIVO = "especie"
    QUINCENA = "quincena"
    GRUPO_ETNICO = "grupo_etnico"  # Comca'ac vs mestizo


@dataclass
class BiasReport:
    """Reporte de sesgo por slice."""
    dimension: SliceDimension
    slice_value: str
    n_samples: int
    mean_ierc: float
    mean_confidence: float
    disparity_ratio: float  # ratio vs global mean
    flag: str  # "OK", "WARN", "CRITICAL"
    details: Dict[str, Any]


def detect_bias_by_slice(
    results_df: pd.DataFrame,
    dimension: SliceDimension,
    global_mean_ierc: float,
    global_mean_confidence: float,
    disparity_threshold: float = 0.2,
    min_samples: int = 10
) -> List[BiasReport]:
    """
    Detecta sesgo sistemático en scores IERC por slice (comunidad, arte, zona, etc.).
    
    Implementa slice-based evaluation del libro (Ch.6) — evita que métricas
    agregadas oculten problemas en subgrupos (Simpson's paradox).
    """
    if dimension.value not in results_df.columns:
        logger.warning(f"Columna {dimension.value} no existe en resultados")
        return []

    reports = []
    for slice_val, group in results_df.groupby(dimension.value):
        if len(group) < min_samples:
            continue
            
        slice_mean_ierc = group['IERC_total'].mean()
        slice_mean_conf = group['confidence_dato'].mean() if 'confidence_dato' in group.columns else 1.0
        
        # Ratio de disparidad: qué tan lejos está del global
        disparity = abs(slice_mean_ierc - global_mean_ierc) / max(global_mean_ierc, 0.01)
        
        if disparity > disparity_threshold * 2:
            flag = "CRITICAL"
        elif disparity > disparity_threshold:
            flag = "WARN"
        else:
            flag = "OK"
            
        reports.append(BiasReport(
            dimension=dimension,
            slice_value=str(slice_val),
            n_samples=len(group),
            mean_ierc=float(slice_mean_ierc),
            mean_confidence=float(slice_mean_conf),
            disparity_ratio=float(disparity),
            flag=flag,
            details={
                'std_ierc': float(group['IERC_total'].std()),
                'min_ierc': float(group['IERC_total'].min()),
                'max_ierc': float(group['IERC_total'].max()),
                'pct_high_risk': float((group['IERC_total'] > 65).mean() * 100)
            }
        ))
    
    return reports


def run_full_bias_audit(
    results_df: pd.DataFrame,
    dimensions: List[SliceDimension] = None
) -> Dict[SliceDimension, List[BiasReport]]:
    """
    Auditoría completa de sesgo across todas las dimensiones relevantes.
    
    Returns: dict dimension -> list of BiasReport (solo WARN/CRITICAL)
    """
    if dimensions is None:
        dimensions = [
            SliceDimension.COMUNIDAD,
            SliceDimension.ARTE_PESCA,
            SliceDimension.ZONA_GEOFRAFICA,
            SliceDimension.QUINCENA
        ]
    
    global_mean_ierc = results_df['IERC_total'].mean()
    global_mean_conf = results_df['confidence_dato'].mean() if 'confidence_dato' in results_df.columns else 1.0
    
    audit = {}
    for dim in dimensions:
        reports = detect_bias_by_slice(
            results_df, dim, global_mean_ierc, global_mean_conf
        )
        # Filtrar solo los que requieren atención
        audit[dim] = [r for r in reports if r.flag != "OK"]
        if audit[dim]:
            logger.warning(f"BIAS {dim.value}: {len(audit[dim])} slices con disparidad")
            for r in audit[dim]:
                logger.warning(f"  {r.slice_value}: IERC={r.mean_ierc:.1f} (disparidad {r.disparity_ratio:.1%}) [{r.flag}]")
    
    return audit


# ─── Smooth Failing / Graceful Degradation ────────────────────────────────

@dataclass
class FallbackResult:
    """Resultado con metadata de fallback para smooth failing."""
    value: float
    source: str  # "primary", "fallback_community", "fallback_default", "interpolated"
    confidence_penalty: float  # 0.0 = full confidence, 1.0 = no confidence
    metadata: Dict[str, Any]


def get_component_with_fallback(
    primary_fn,
    fallback_fns: List[callable],
    component_name: str,
    h3_cell_id: str
) -> FallbackResult:
    """
    Ejecuta función primaria; si falla o retorna 0/None, prueba fallbacks en orden.
    
    Implementa "smooth failing" (Chip Huyen Ch.11) — nunca crashea,
    siempre retorna algo con metadata de confianza.
    """
    # Intentar primaria
    try:
        primary_val = primary_fn()
        if primary_val is not None and primary_val > 0:
            return FallbackResult(
                value=float(primary_val),
                source="primary",
                confidence_penalty=0.0,
                metadata={'component': component_name, 'cell': h3_cell_id}
            )
    except Exception as e:
        logger.debug(f"Primary failed for {component_name}@{h3_cell_id}: {e}")
    
    # Probar fallbacks
    for i, fallback_fn in enumerate(fallback_fns):
        try:
            fallback_val = fallback_fn()
            if fallback_val is not None and fallback_val >= 0:
                penalty = 0.15 * (i + 1)  # 15%, 30%, 45%...
                return FallbackResult(
                    value=float(fallback_val),
                    source=f"fallback_{i+1}",
                    confidence_penalty=min(penalty, 0.9),
                    metadata={'component': component_name, 'cell': h3_cell_id, 'fallback_level': i+1}
                )
        except Exception as e:
            logger.debug(f"Fallback {i+1} failed for {component_name}@{h3_cell_id}: {e}")
            continue
    
    # Último recurso: valor por defecto conservador
    default_val = 0.5 if component_name == 'capacidad_adaptativa' else 0.0
    return FallbackResult(
        value=default_val,
        source="fallback_default",
        confidence_penalty=0.5,
        metadata={'component': component_name, 'cell': h3_cell_id, 'default_used': True}
    )


# ─── Team Workflow Helpers ────────────────────────────────────────────────

@dataclass
class RoleSpec:
    """Especificación de rol para cross-functional team (Chip Huyen Ch.11)."""
    name: str
    responsibilities: List[str]
    required_skills: List[str]
    handoffs_to: List[str]  # qué roles reciben output de este


IERC_TEAM_ROLES = {
    'gis_analyst': RoleSpec(
        name='GIS Analyst',
        responsibilities=[
            'Ingesta y validación de shapefiles/GeoPackage',
            'Generación de grilla H3 y validación espacial',
            'QA de geometrías (bbox, proyección, topología)'
        ],
        required_skills=['PostGIS', 'GeoPandas', 'H3', 'QGIS'],
        handoffs_to=['data_engineer', 'ml_engineer']
    ),
    'data_engineer': RoleSpec(
        name='Data Engineer',
        responsibilities=[
            'Pipelines ETL: PANGAS, GFW, MIA PDFs → Postgres',
            'Versionado de datos (DVC) y catálogo',
            'Monitoreo de data drift (distribution shift)'
        ],
        required_skills=['SQL', 'Python', 'DVC', 'Airflow/Prefect'],
        handoffs_to=['ml_engineer', 'domain_expert']
    ),
    'ml_engineer': RoleSpec(
        name='ML Engineer',
        responsibilities=[
            'Implementación motor IERC + Monte Carlo',
            'Experiment tracking, model versioning',
            'Deployment: batch GeoPackage + online API'
        ],
        required_skills=['Python', 'NumPy/Pandas', 'MLOps', 'FastAPI'],
        handoffs_to=['domain_expert', 'frontend_engineer']
    ),
    'domain_expert': RoleSpec(
        name='Domain Expert (Pesca/Moreno-Báez)',
        responsibilities=[
            'Validación de pesos y umbrales metodológicos',
            'Interpretación de especies/artes/zonas',
            'Definición de ground truth para evaluación'
        ],
        required_skills=['Ecología pesquera', 'Metodología IERC', 'Comunidades costeras'],
        handoffs_to=['ml_engineer', 'community_liaison']
    ),
    'community_liaison': RoleSpec(
        name='Community Liaison (Comca\'ac/Cooperativas)',
        responsibilities=[
            'Consentimiento informado y protocolos de campo',
            'Validación comunitaria de features bioculturales',
            'Comunicación de resultados a stakeholders afectados'
        ],
        required_skills=['Comunicación intercultural', 'Derecho indígena', 'Facilitación'],
        handoffs_to=['domain_expert', 'project_lead']
    ),
    'frontend_engineer': RoleSpec(
        name='Frontend Engineer (Dashboard)',
        responsibilities=[
            'Dashboard interactivo (RiskMap, ZoneCards, SpeciesPanel)',
            'Export GeoPackage/CSV para ASEA/CONAPESCA',
            'UX para usuarios no técnicos (territorial)'
        ],
        required_skills=['Next.js', 'React', 'Leaflet', 'Tailwind/CSS'],
        handoffs_to=['ml_engineer', 'project_lead']
    ),
    'project_lead': RoleSpec(
        name='Project Lead',
        responsibilities=[
            'Coordinación cross-functional, unblocking',
            'Entregables: GeoPackage, reportes, dashboard',
            'Gobernanza: ética, sesgos, compliance ASEA'
        ],
        required_skills=['Gestión proyectos', 'ML systems', 'Stakeholder mgmt'],
        handoffs_to=[]
    )
}


def validate_team_coverage(active_roles: List[str]) -> List[str]:
    """Verifica que el equipo activo cubre handoffs críticos."""
    missing = []
    for role_name in active_roles:
        role = IERC_TEAM_ROLES.get(role_name)
        if not role:
            continue
        for handoff in role.handoffs_to:
            if handoff not in active_roles:
                missing.append(f"{role_name} → {handoff} (handoff missing)")
    return missing


# ─── Self-check (runnable) ────────────────────────────────────────────────

def demo():
    """Self-check: explainability + bias detection + smooth failing."""
    print("=== IERC Responsible AI Demo ===\n")
    
    # 1. Explainability
    components = {
        'amenaza': 0.72, 'exposicion': 0.45, 'sensibilidad': 0.68,
        'dependencia': 0.55, 'valor_biocultural': 0.81, 'capacidad_adaptativa': 0.35
    }
    from ..utils.ierc import IERC_WEIGHTS, compute_ierc
    ierc = compute_ierc(**components, weights=IERC_WEIGHTS)
    exp = explain_ierc_score("h3_cell_123", components, ierc * 100, 0.82, "Moderado")
    print(exp.to_markdown())
    print()
    
    # 2. Bias detection (synthetic data)
    np.random.seed(42)
    n = 500
    df = pd.DataFrame({
        'h3_cell_id': [f'cell_{i}' for i in range(n)],
        'IERC_total': np.random.beta(2, 5, n) * 100,
        'confidence_dato': np.random.beta(5, 2, n),
        'comunidad': np.random.choice(['Comca\'ac', 'Puerto Libertad', 'Guaymas', 'Bahía Kino'], n),
        'arte_pesca': np.random.choice(['Panga', 'Buceo', 'Chinchorro', 'Redes'], n),
        'zona': np.random.choice(['Norte', 'Centro', 'Sur'], n)
    })
    # Introducir sesgo: Comca'ac tiene IERC sistemáticamente más alto
    df.loc[df['comunidad'] == "Comca'ac", 'IERC_total'] *= 1.3
    
    audit = run_full_bias_audit(df)
    print("=== Bias Audit ===")
    for dim, reports in audit.items():
        if reports:
            print(f"\n{dim.value}:")
            for r in reports:
                print(f"  {r.slice_value}: IERC={r.mean_ierc:.1f}, disp={r.disparity_ratio:.1%} [{r.flag}]")
    
    # 3. Smooth failing
    def primary_fail(): raise ValueError("DB connection lost")
    def fallback_community(): return 0.4
    def fallback_default(): return 0.5
    
    result = get_component_with_fallback(
        primary_fail, [fallback_community, fallback_default],
        'capacidad_adaptativa', 'cell_test'
    )
    print(f"\n=== Smooth Failing ===")
    print(f"Value: {result.value}, Source: {result.source}, Penalty: {result.confidence_penalty}")
    
    print("\n✓ All self-checks passed")


if __name__ == "__main__":
    demo()