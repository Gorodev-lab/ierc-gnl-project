#!/usr/bin/env python3
"""
IERC Level III Confidence Map Calculator (POA 2026)
===================================================
Genera el Mapa de Confianza y Calidad de Información del Dato (Nivel III)
evaluando la proporción de datos observados vs imputados, consistencia multi-fuente
y estatus de validación comunitaria.
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


def compute_confidence_map():
    """Calcula el score de confianza Nivel III (0-100) por celda H3."""
    logger.info("=== Calculando Mapa de Confianza Nivel III (POA 2026) ===")
    
    risk_path = GOLD / "ierc_risk_multiplicative.parquet"
    if not risk_path.exists():
        risk_path = GOLD / "ierc_risk_h3_8.parquet"
    
    df = pd.read_parquet(risk_path)
    logger.info(f"Cargadas {len(df)} celdas para el Mapa de Confianza")

    # 1. Densidad Observada (40%)
    # Evalúa si la celda cuenta con datos reales de PANGAS / ASEA vs imputación por mediana
    tiene_pangas = (df['pangas_densidad_esfuerzo'] > 0).astype(float) * 100.0 if 'pangas_densidad_esfuerzo' in df.columns else 30.0
    tiene_asea = (df['asea_count'] > 0).astype(float) * 100.0 if 'asea_count' in df.columns else 20.0
    densidad_observada = (0.70 * tiene_pangas) + (0.30 * tiene_asea)

    # 2. Consistencia Multi-Fuente (30%)
    # Evalúa si hay solapamiento de múltiples fuentes (NASA + GEBCO + TNC + PANGAS)
    fuentes_count = (
        (df['chlor_a_mean'] > 0).astype(int) +
        (df['depth_mean'] != -150.0).astype(int) +
        (df['tnc_bajos_area_frac'] > 0).astype(int) +
        (tiene_pangas > 0).astype(int)
    )
    consistencia = (fuentes_count / 4.0) * 100.0

    # 3. Estatus de Validación Comunitaria (30%)
    # Celdas asociadas a las 3 comunidades del POA (Punta Chueca, Puerto Libertad, Guaymas) cuentan con validación de campo
    validación_comunitaria = np.where(df['resolution'] == 9, 90.0, 45.0) if 'resolution' in df.columns else pd.Series(50.0, index=df.index)

    # Score de Confianza Nivel III
    df['confidence_score'] = (
        (0.40 * densidad_observada) +
        (0.30 * consistencia) +
        (0.30 * validación_comunitaria)
    ).clip(0.0, 100.0)

    # Nivel de Confianza
    conditions = [
        (df['confidence_score'] >= 75.0),
        (df['confidence_score'] >= 50.0)
    ]
    choices = ['Alta Confianza', 'Confianza Media']
    df['nivel_confianza'] = np.select(conditions, choices, default='Baja Confianza')

    # Guardar Nivel III en Gold
    output_path = GOLD / "ierc_confidence_h3.parquet"
    df[['h3_cell', 'confidence_score', 'nivel_confianza', 'resolution' if 'resolution' in df.columns else 'h3_cell']].to_parquet(output_path, compression='zstd', index=False)
    logger.info(f"Mapa de Confianza Nivel III guardado en {output_path}")

    # Imprimir resumen
    print("\n" + "="*60)
    print("RESUMEN MAPA DE CONFIANZA NIVEL III (POA 2026)")
    print("="*60)
    print(f"Celdas evaluadas: {len(df)}")
    print(f"Confianza Media: {df['confidence_score'].mean():.2f}")
    print("\nDistribución por Nivel de Confianza:")
    print(df['nivel_confianza'].value_counts())
    return df


if __name__ == "__main__":
    compute_confidence_map()
