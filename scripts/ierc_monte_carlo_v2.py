#!/usr/bin/env python3
"""
IERC Monte Carlo Efficient - Phase 6b
=====================================
Versión eficiente usando H3 k-ring neighbors + vectorización batch.
Evita matrices de distancias masivas usando H3 spatial indexing.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import h3
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path("/home/gorops/ierc-gnl-project/src")))

from data.lakehouse.storage import create_storage_from_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
LAKEHOUSE_ROOT = Path("/home/gorops/ierc-gnl-project/lakehouse")
GOLD = LAKEHOUSE_ROOT / "curated"


@dataclass
class MCConfig:
    n_simulations: int = 30
    k_ring: int = 2
    noise_base: float = 0.1
    noise_dist_factor: float = 0.05
    max_dist_km: float = 100.0
    seed: int = 42


def get_h3_centroids(h3_cells: List[str]) -> np.ndarray:
    """Convierte celdas H3 a coordenadas centroides."""
    coords = np.array([h3.cell_to_latlng(cell) for cell in h3_cells])
    return coords[:, [1, 0]]  # [lon, lat]


def get_valid_h3_cells() -> set:
    """Celdas H3_8 válidas en el Golfo."""
    bbox = h3.geo_to_cells({
        "type": "Polygon",
        "coordinates": [[[-115.0, 22.5], [-108.0, 22.5], [-108.0, 32.0], [-115.0, 32.0], [-115.0, 22.5]]]
    }, 8)
    return set(bbox)


def load_features() -> pd.DataFrame:
    """Carga features desde Gold."""
    return pd.read_parquet("/home/gorops/ierc-gnl-project/lakehouse/curated/ierc_features_h3_8.parquet")


def run_efficient_monte_carlo():
    """Monte Carlo eficiente usando H3 spatial indexing."""
    logger.info("=" * 60)
    logger.info("IERC MONTE CARLO - EFICIENTE (H3 k-ring)")
    logger.info("=" * 60)

    # Cargar features
    logger.info("Cargando features...")
    features = pd.read_parquet("/home/gorops/ierc-gnl-project/lakehouse/curated/ierc_features_h3_8.parquet")
    logger.info(f"Features: {features.shape}")

    # Preparar mapeos H3
    cell_to_idx = {cell: i for i, cell in enumerate(features['h3_cell_8'])}
    features = features.set_index('h3_cell_8')

    # Columnas a simular
    feature_cols = [c for c in features.columns if features[c].dtype in ['float64', 'float32']]
    logger.info(f"Features a simular: {len(feature_cols)}")

    # Configuración
    n_sims = 30
    n_cells = len(features)
    k_ring = 2

    # Pre-calcular vecinos k-ring para todas las celdas
    logger.info(f"Pre-calculando vecinos grid_ring k={k_ring}...")
    all_neighbors = {}
    for cell in features.index:
        neighbors = h3.grid_ring(cell, k_ring)
        valid = [n for n in neighbors if n in cell_to_idx]
        all_neighbors[cell] = valid

    # Pesos IERC
    weights = {
        'chlor_a_mean': 0.13, 'chlor_a_max': 0.05, 'sst_mean': 0.08,
        'sst_max': 0.05, 'sst_std': 0.03, 'depth_mean': 0.08,
        'depth_slope': 0.04, 'depth_range': 0.02,
        'tnc_bajos_area_frac': 0.10, 'tnc_coral_area_frac': 0.08,
        'asea_count': 0.12, 'asea_terminal_gnl': 0.10, 'asea_gasoducto': 0.08,
        'pangas_total_frac': 0.05,
    }

    n_sims = 30
    n_cells = len(features)
    ierc_sims = np.zeros((n_cells, 30))

    # Simulaciones
    logger.info(f"Ejecutando {n_sims} simulaciones Monte Carlo...")

    for sim in range(30):
        if sim % 5 == 0:
            logger.info(f"  Simulación {sim+1}/30...")

        # Generar muestra normalizada para cada feature
        sim_features = {}

        for col in features.columns:
            if col not in features.columns:
                continue

            data = features[col]
            observed_mask = data.notna()

            # Normalizar (percentil 1-99)
            observed = data[observed_mask]
            if len(observed) == 0:
                sim_features[col] = np.full(len(features), 50.0)
                continue

            p1, p99 = np.percentile(observed, [1, 99])
            clipped = observed.clip(p1, p99)

            if p99 > p1:
                normalized = ((clipped - p1) / (p99 - p1)) * 100
            else:
                normalized = pd.Series(50, index=observed.index)

            # Interpolar valores faltantes usando vecinos H3
            normalized_full = normalized.reindex(features.index)

            # Para cada celda faltante, promediar vecinos observados
            missing_mask = normalized_full.isna()
            if missing_mask.any():
                for idx in features.index[missing_mask]:
                    neighbors = [n for n in all_neighbors.get(idx, []) if n in features.index]
                    neighbor_vals = features.loc[neighbors, col] if neighbors else pd.Series()
                    neighbor_norm = neighbor_vals[neighbor_vals.notna()]

                    if len(neighbor_norm) > 0:
                        normalized_full[idx] = neighbor_norm.mean()
                    else:
                        normalized_full[idx] = np.nan

            # Rellenar restantes con prior
            still_missing = normalized_full.isna()
            if still_missing.any():
                prior_mean = 50
                prior_std = 15
                normalized_full[still_missing] = np.random.normal(prior_mean, prior_std, still_missing.sum())

            # Clip y ruido
            normalized_full = normalized_full.clip(0, 100)
            noise = np.random.normal(0, 0.1, len(normalized_full))
            sim_features[col] = (normalized_full + np.random.normal(0, 0.1, len(normalized_full))).clip(0, 100)

        # Calcular IERC
        sim_df = pd.DataFrame(sim_features, index=features.index)
        risk = np.zeros(len(features))

        weights = {
            'chlor_a_mean': 0.13, 'chlor_a_max': 0.05, 'sst_mean': 0.08,
            'sst_max': 0.05, 'sst_std': 0.03, 'depth_mean': 0.08,
            'depth_slope': 0.04, 'depth_range': 0.02,
            'tnc_bajos_area_frac': 0.10, 'tnc_coral_area_frac': 0.08,
            'asea_count': 0.12, 'asea_terminal_gnl': 0.10, 'asea_gasoducto': 0.08,
            'pangas_total_frac': 0.05,
        }

        for feat, w in weights.items():
            if feat in sim_df.columns:
                risk += sim_df[feat] * w

        ierc_sims[:, sim] = np.clip(risk, 0, 100)

    # Resultados Monte Carlo
    ierc_mean = ierc_sims.mean(axis=1)
    ierc_std = ierc_sims.std(axis=1)
    ierc_p05 = np.percentile(ierc_sims, 5, axis=1)
    ierc_p95 = np.percentile(ierc_sims, 95, axis=1)
    ierc_median = np.median(ierc_sims, axis=1)

    # DataFrame resultado
    results = pd.DataFrame({
        'h3_cell_8': features.index,
        'ierc_mean': ierc_mean,
        'ierc_std': ierc_std,
        'ierc_p05': ierc_p05,
        'ierc_p95': ierc_p95,
        'ierc_median': ierc_median,
    }).reset_index(drop=True)

    # Guardar
    GOLD = Path("/home/gorops/ierc-gnl-project/lakehouse/curated")
    output_path = GOLD / "ierc_monte_carlo_h3_8.parquet"
    results.to_parquet(output_path, compression='zstd', index=False)
    logger.info(f"Guardado: {output_path}")

    logger.info(f"Monte Carlo completado:")
    logger.info(f"  IERC mean: {ierc_mean.mean():.1f} ± {ierc_mean.std():.1f}")
    logger.info(f"  IERC std (aleatorio): {ierc_std.mean():.2f}")
    logger.info(f"  IC 90% ancho medio: {(ierc_p95 - ierc_p05).mean():.2f}")

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run_efficient_monte_carlo()