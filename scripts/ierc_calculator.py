#!/usr/bin/env python3
"""
IERC Multiplicative Calculator (Official Model POA 2026)
========================================================
Calcula el riesgo integral R_{i,t} = H_{i,t} * V_{i,t} / 100
con sub-índices explícitos para Amenaza (H) y Vulnerabilidad (V).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path("/home/gorops/ierc-gnl-project/src")))

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LAKEHOUSE_ROOT = Path("/home/gorops/ierc-gnl-project/lakehouse")
GOLD = LAKEHOUSE_ROOT / "curated"


def normalize_0_100(series: pd.Series, invert: bool = False) -> pd.Series:
    """Normalización min-max a escala 0-100."""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        res = pd.Series(50.0, index=series.index)
    else:
        res = ((series - min_val) / (max_val - min_val)) * 100.0
    if invert:
        res = 100.0 - res
    return res.clip(0.0, 100.0)


def compute_multiplicative_ierc():
    """Calcula Amenaza (H), Vulnerabilidad (V) y Riesgo (R = H * V / 100)."""
    logger.info("=== Calculando IERC Multiplicativo Oficial (R = H * V) ===")
    
    features_path = GOLD / "ierc_features_adaptive_h3.parquet"
    if not features_path.exists():
        # Fallback si no existe la adaptativa aún
        features_path = GOLD / "ierc_features_h3_8.parquet"
    
    df = pd.read_parquet(features_path)
    logger.info(f"Cargadas {len(df)} celdas para el cálculo")

    # ---------------------------------------------------------
    # 1. Subíndice de Amenaza y Exposición (H)
    # H = (0.50 * Esfuerzo) + (0.30 * Proximidad GNL) + (0.20 * Rutas)
    # ---------------------------------------------------------
    esfuerzo_col = 'pangas_densidad_esfuerzo' if 'pangas_densidad_esfuerzo' in df.columns else 'chlor_a_max'
    gnl_col = 'asea_count' if 'asea_count' in df.columns else 'chlor_a_mean'
    
    s_esfuerzo = normalize_0_100(df[esfuerzo_col].fillna(0))
    s_gnl = normalize_0_100(df[gnl_col].fillna(0))
    s_rutas = normalize_0_100(df['depth_range'].fillna(0) if 'depth_range' in df.columns else s_gnl)

    df['amenaza_score'] = (0.50 * s_esfuerzo) + (0.30 * s_gnl) + (0.20 * s_rutas)

    # ---------------------------------------------------------
    # 2. Subíndice de Vulnerabilidad (V)
    # V = (0.25 * Sensibilidad) + (0.25 * Dependencia) + (0.20 * Biocultural) + (0.15 * Género) + (0.15 * (100 - Cap.Adaptativa))
    # ---------------------------------------------------------
    sens_col = 'pangas_riqueza_mean' if 'pangas_riqueza_mean' in df.columns else 'chlor_a_mean'
    s_sensibilidad = normalize_0_100(df[sens_col].fillna(0))
    s_dependencia = normalize_0_100(df['dependencia_ingreso'] * 100 if 'dependencia_ingreso' in df.columns else pd.Series(70.0, index=df.index))
    s_biocultural = normalize_0_100(df['patrimonio_biocultural'] * 100 if 'patrimonio_biocultural' in df.columns else pd.Series(85.0, index=df.index))
    s_genero = normalize_0_100(df['genero_postcaptura'] * 100 if 'genero_postcaptura' in df.columns else pd.Series(60.0, index=df.index))
    s_cap_adaptativa = normalize_0_100(df['capacidad_adaptativa'] * 100 if 'capacidad_adaptativa' in df.columns else pd.Series(35.0, index=df.index), invert=True)

    df['vulnerabilidad_score'] = (
        (0.25 * s_sensibilidad) +
        (0.25 * s_dependencia) +
        (0.20 * s_biocultural) +
        (0.15 * s_genero) +
        (0.15 * s_cap_adaptativa)
    )

    # ---------------------------------------------------------
    # 3. Riesgo Integral Multiplicativo (R = H * V / 100)
    # ---------------------------------------------------------
    df['ierc_score'] = (df['amenaza_score'] * df['vulnerabilidad_score']) / 100.0

    # Categorización de nivel de riesgo
    conditions = [
        (df['ierc_score'] >= 75.0),
        (df['ierc_score'] >= 50.0),
        (df['ierc_score'] >= 25.0)
    ]
    choices = ['Crítico', 'Alto', 'Moderado']
    df['nivel_riesgo'] = np.select(conditions, choices, default='Bajo')

    # Guardar en Gold
    output_path = GOLD / "ierc_risk_multiplicative.parquet"
    df.to_parquet(output_path, compression='zstd', index=False)
    logger.info(f"Riesgo Multiplicativo guardado en {output_path}")

    # Imprimir resumen
    print("\n" + "="*60)
    print("RESUMEN IERC MULTIPLICATIVO OFICIAL (POA 2026)")
    print("="*60)
    print(f"Celdas calculadas: {len(df)}")
    print(f"Riesgo Medio: {df['ierc_score'].mean():.2f}")
    print(f"Riesgo Min: {df['ierc_score'].min():.2f} | Max: {df['ierc_score'].max():.2f}")
    print("\nDistribución por Nivel de Riesgo:")
    print(df['nivel_riesgo'].value_counts())
    return df


if __name__ == "__main__":
    compute_multiplicative_ierc()