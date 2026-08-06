"""
Unit Tests — Responsible AI & Human Side
=========================================
Pruebas para explainability, bias detection, smooth failing y team workflow.
"""

import pytest
import pandas as pd
import numpy as np
from src.engine.responsible_ai import (
    explain_ierc_score,
    IERCExplanation,
    SliceDimension,
    BiasReport,
    detect_bias_by_slice,
    run_full_bias_audit,
    get_component_with_fallback,
    FallbackResult,
    IERC_TEAM_ROLES,
    validate_team_coverage
)


class TestExplainability:
    """Pruebas para generación de explicaciones humanas."""

    def test_explain_ierc_score_basic(self):
        """Explicación básica con todos los componentes."""
        components = {
            'amenaza': 0.7, 'exposicion': 0.4, 'sensibilidad': 0.6,
            'dependencia': 0.5, 'valor_biocultural': 0.8, 'capacidad_adaptativa': 0.3
        }
        from src.utils.ierc import IERC_WEIGHTS, compute_ierc
        ierc = compute_ierc(**components, weights=IERC_WEIGHTS)
        
        exp = explain_ierc_score("test_cell", components, ierc * 100, 0.85, "Moderado")
        
        assert exp.h3_cell_id == "test_cell"
        assert exp.ierc_total == ierc * 100
        assert exp.confidence_dato == 0.85
        assert exp.uncertainty_level == "Moderado"
        assert exp.top_driver in components
        assert len(exp.narrative) > 0

    def test_explanation_to_markdown(self):
        """Renderizado a markdown para reportes."""
        components = {'amenaza': 0.8, 'exposicion': 0.3, 'sensibilidad': 0.4,
                      'dependencia': 0.2, 'valor_biocultural': 0.5, 'capacidad_adaptativa': 0.6}
        from src.utils.ierc import IERC_WEIGHTS, compute_ierc
        ierc = compute_ierc(**components, weights=IERC_WEIGHTS)
        
        exp = explain_ierc_score("cell_1", components, ierc * 100, 0.9, "Bajo")
        md = exp.to_markdown()
        
        assert "IERC Explanation" in md
        assert "cell_1" in md
        assert "Component Breakdown" in md
        assert "Primary Driver" in md
        assert "Narrative" in md


class TestBiasDetection:
    """Pruebas para detección de sesgo por slices."""

    @pytest.fixture
    def biased_results_df(self):
        """DataFrame sintético con sesgo conocido."""
        np.random.seed(42)
        n = 400
        df = pd.DataFrame({
            'h3_cell_id': [f'cell_{i}' for i in range(n)],
            'IERC_total': np.random.beta(2, 5, n) * 100,
            'confidence_dato': np.random.beta(5, 2, n),
            'comunidad': np.random.choice(["Comca'ac", 'Puerto Libertad', 'Guaymas', 'Bahía Kino'], n),
            'arte_pesca': np.random.choice(['Panga', 'Buceo', 'Chinchorro', 'Redes'], n),
            'zona': np.random.choice(['Norte', 'Centro', 'Sur'], n)
        })
        # Introducir sesgo sistemático: Comca'ac 30% más alto
        mask = df['comunidad'] == "Comca'ac"
        df.loc[mask, 'IERC_total'] = df.loc[mask, 'IERC_total'] * 1.3
        return df

    def test_detect_bias_by_comunidad(self, biased_results_df):
        """Detecta sesgo en comunidad Comca'ac."""
        global_mean = biased_results_df['IERC_total'].mean()
        global_conf = biased_results_df['confidence_dato'].mean()
        
        reports = detect_bias_by_slice(
            biased_results_df, SliceDimension.COMUNIDAD,
            global_mean, global_conf, disparity_threshold=0.15
        )
        
        # Debe encontrar al menos Comca'ac como WARN o CRITICAL
        comcaac_reports = [r for r in reports if r.slice_value == "Comca'ac"]
        assert len(comcaac_reports) == 1
        assert comcaac_reports[0].flag in ["WARN", "CRITICAL"]
        assert comcaac_reports[0].disparity_ratio > 0.15

    def test_detect_bias_no_false_positive(self, biased_results_df):
        """No debe reportar sesgo donde no existe (arte_pesca balanceado)."""
        global_mean = biased_results_df['IERC_total'].mean()
        global_conf = biased_results_df['confidence_dato'].mean()
        
        reports = detect_bias_by_slice(
            biased_results_df, SliceDimension.ARTE_PESCA,
            global_mean, global_conf, disparity_threshold=0.15
        )
        
        # Ningún arte debe tener disparidad > threshold
        flagged = [r for r in reports if r.flag != "OK"]
        assert len(flagged) == 0

    def test_run_full_bias_audit(self, biased_results_df):
        """Auditoría completa retorna solo slices problemáticos."""
        audit = run_full_bias_audit(biased_results_df)
        
        # Debe tener al menos comunidad
        assert SliceDimension.COMUNIDAD in audit
        assert len(audit[SliceDimension.COMUNIDAD]) >= 1
        
        # Todos los reportes deben ser WARN o CRITICAL
        for dim, reports in audit.items():
            for r in reports:
                assert r.flag in ["WARN", "CRITICAL"]


class TestSmoothFailing:
    """Pruebas para graceful degradation."""

    def test_primary_succeeds(self):
        """Función primaria retorna valor → no usa fallbacks."""
        def primary(): return 0.75
        def fallback(): return 0.5
        
        result = get_component_with_fallback(primary, [fallback], 'test_comp', 'cell_1')
        
        assert result.value == 0.75
        assert result.source == "primary"
        assert result.confidence_penalty == 0.0

    def test_primary_fails_fallback_works(self):
        """Primaria falla → usa primer fallback."""
        def primary(): raise ValueError("DB down")
        def fallback(): return 0.4
        
        result = get_component_with_fallback(primary, [fallback], 'capacidad_adaptativa', 'cell_1')
        
        assert result.value == 0.4
        assert result.source == "fallback_1"
        assert result.confidence_penalty == 0.15

    def test_all_fail_default_conservative(self):
        """Todo falla → valor por defecto conservador."""
        def primary(): raise ValueError("DB down")
        def fallback1(): raise ValueError("Cache miss")
        def fallback2(): return None
        
        result = get_component_with_fallback(primary, [fallback1, fallback2], 'amenaza', 'cell_1')
        
        assert result.value == 0.0  # default para no-capacidad
        assert result.source == "fallback_default"
        assert result.confidence_penalty == 0.5

    def test_capacidad_adaptativa_default_is_0_5(self):
        """Default para capacidad_adaptativa es 0.5 (no 0.0)."""
        def primary(): raise ValueError("DB down")
        def fallback(): raise ValueError("Cache miss")
        
        result = get_component_with_fallback(primary, [fallback], 'capacidad_adaptativa', 'cell_1')
        
        assert result.value == 0.5
        assert result.source == "fallback_default"


class TestTeamWorkflow:
    """Pruebas para validación de cobertura de roles."""

    def test_all_roles_defined(self):
        """Todos los 6 roles críticos están definidos."""
        expected = {'gis_analyst', 'data_engineer', 'ml_engineer', 
                    'domain_expert', 'community_liaison', 'frontend_engineer', 'project_lead'}
        assert set(IERC_TEAM_ROLES.keys()) == expected

    def test_validate_team_coverage_complete(self):
        """Equipo completo → sin handoffs faltantes."""
        active = list(IERC_TEAM_ROLES.keys())
        missing = validate_team_coverage(active)
        assert len(missing) == 0

    def test_validate_team_coverage_missing(self):
        """Equipo incompleto → detecta handoffs faltantes."""
        active = ['gis_analyst', 'ml_engineer', 'project_lead']  # falta data_engineer, domain_expert, etc.
        missing = validate_team_coverage(active)
        assert len(missing) > 0
        # gis_analyst → data_engineer debe faltar
        assert any('gis_analyst' in m and 'data_engineer' in m for m in missing)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])