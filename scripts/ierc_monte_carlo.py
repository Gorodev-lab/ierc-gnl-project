#!/usr/bin/env python3
"""
IERC Monte Carlo Simulator - Phase 6b
=====================================
Simula incertidumbre espacial mediante kriging / interpolación condicional
para generar variabilidad realista en celdas sin datos observados.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.interpolate import Rbf
from scipy.spatial.distance import cdist
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path("/home/gorops/ierc-gnl-project/src")))

from data.lakehouse.storage import create_storage_from_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
LAKEHOUSE_ROOT = Path("/home/gorops/ierc-gnl-project/lakehouse")
SILVER = LAKEHOUSE_ROOT / "processed"
GOLD = LAKEHOUSE_ROOT / "curated"


@dataclass
class MCConfig:
    """Configuración Monte Carlo."""
    n_simulations: int = 100
    n_neighbors: int = 12
    variogram_model: str = 'spherical'  # spherical, exponential, gaussian
    range_km: float = 50.0
    sill: float = 1.0
    nugget: float = 0.1
    seed: int = 42


class SpatialInterpolator:
    """Interpolación espacial con cuantificación de incertidumbre."""
    
    def __init__(self, config: MCConfig = None):
        self.config = config or MCConfig()
        np.random.seed(self.config.seed)
    
    def get_h3_centroids(self, h3_cells: List[str]) -> np.ndarray:
        """Convierte celdas H3 a coordenadas centroides (lat, lon)."""
        import h3
        coords = []
        for cell in h3_cells:
            lat, lon = h3.cell_to_latlng(cell)
            coords.append([lon, lat])  # x, y
        return np.array(coords)
    
    def rbf_interpolate(self, known_coords: np.ndarray, known_values: np.ndarray, 
                        target_coords: np.ndarray, function: str = 'multiquadric') -> np.ndarray:
        """Interpolación RBF (Radial Basis Function)."""
        try:
            rbf = Rbf(known_coords[:, 0], known_coords[:, 1], known_values, 
                     function=function, smooth=0.1)
            return rbf(target_coords[:, 0], target_coords[:, 1])
        except Exception as e:
            logger.warning(f"RBF failed: {e}, using nearest neighbor")
            return self.nearest_neighbor(known_coords, known_values, target_coords)
    
    def nearest_neighbor(self, known_coords: np.ndarray, known_values: np.ndarray,
                        target_coords: np.ndarray) -> np.ndarray:
        """Fallback: vecino más cercano."""
        dists = cdist(target_coords, known_coords)
        nearest_idx = np.argmin(dists, axis=1)
        return known_values[nearest_idx]
    
    def simulate_conditional(self, 
                            features: pd.DataFrame,
                            feature_cols: List[str],
                            n_simulations: int = 100) -> Dict[str, np.ndarray]:
        """
        Simulación condicional: genera n realizaciones para cada feature.
        
        Para celdas con datos observados: usa el valor observado + ruido pequeño
        Para celdas sin datos: interpola + ruido condicional
        """
        import h3
        
        h3_cells = features['h3_cell_8'].tolist()
        coords = self.get_h3_centroids(h3_cells)
        
        results = {col: np.zeros((len(features), n_simulations)) for col in feature_cols}
        
        for col in feature_cols:
            logger.info(f"  Simulando {col} ({n_simulations} realizaciones)...")
            
            # Identificar celdas con datos observados
            observed_mask = features[col].notna()
            n_observed = observed_mask.sum()
            n_total = len(features)
            
            if n_observed == 0:
                logger.warning(f"  {col}: sin datos observados, usando prior")
                # Generar desde prior global
                prior_mean = features[col].median() if features[col].notna().any() else 0
                prior_std = features[col].std() if features[col].notna().any() else 1
                for col_result in results[col].T:
                    col_result[:] = np.random.normal(prior_mean, prior_std, n_total)
                continue
            
            observed_coords = coords[observed_mask]
            observed_values = features.loc[observed_mask, col].values
            target_coords = coords
            
            for sim in range(n_simulations):
                # Interpolar
                interpolated = self.rbf_interpolate(observed_coords, observed_values, target_coords)
                
                # Añadir ruido condicional (incertidumbre de interpolación)
                # La incertidumbre aumenta con distancia a puntos observados
                dists = cdist(target_coords, coords[observed_mask])
                min_dists = np.min(dists, axis=1)
                
                # Convertir distancia a km (aprox)
                dist_km = min_dists * 111  # 1 grado ≈ 111 km
                
                # Varianza condicional aumenta con distancia
                conditional_std = 0.1 + 0.05 * np.clip(dist_km / 50, 0, 2)  # max 2x a 100km
                
                # Ruido condicional
                noise = np.random.normal(0, conditional_std)
                simulated = interpolated + noise
                
                # Para celdas observadas, mantener valor observado + ruido pequeño
                simulated[observed_mask] = observed_values + np.random.normal(0, 0.01, n_observed)
                
                results[col][:, sim] = simulated
        
        return results


def run_monte_carlo_ierc():
    """Ejecuta Monte Carlo completo para IERC."""
    logger.info("=" * 60)
    logger.info("IERC MONTE CARLO SIMULATION")
    logger.info("=" * 60)
    
    # Cargar features
    logger.info("Cargando features...")
    features = pd.read_parquet("/home/gorops/ierc-gnl-project/lakehouse/curated/ierc_features_h3_8.parquet")
    logger.info(f"Features: {features.shape}")
    
    # Features numéricas (excluir h3_cell_8)
    feature_cols = [c for c in features.columns if c != 'h3_cell_8' and features[c].dtype in ['float64', 'float32', 'int64', 'int32']]
    logger.info(f"Features a simular: {feature_cols}")
    
    # Configurar MC
    config = MCConfig(
        n_simulations=50,  # Empezar con 50
        n_neighbors=12,
        range_km=50.0,
        seed=42
    )
    
    interpolator = SpatialInterpolator(config)
    
    # Ejecutar simulaciones
    logger.info("Ejecutando simulaciones condicionales...")
    sim_results = interpolator.simulate_conditional(features, feature_cols, n_simulations=50)
    
    # Calcular IERC para cada simulación
    logger.info("Calculando IERC por simulación...")
    
    # Pesos (suman 1.0)
    weights = {
        'chlor_a_mean': 0.13,
        'chlor_a_max': 0.05,
        'sst_mean': 0.08,
        'sst_max': 0.05,
        'sst_std': 0.03,
        'depth_mean': 0.08,
        'depth_slope': 0.04,
        'depth_range': 0.02,
        'tnc_bajos_area_frac': 0.10,
        'tnc_coral_area_frac': 0.08,
        'asea_count': 0.12,
        'asea_terminal_gnl': 0.10,
        'asea_gasoducto': 0.08,
        'pangas_total_frac': 0.05,
    }
    
    n_sims = 50
    n_cells = len(features)
    ierc_sims = np.zeros((len(features), 50))
    
    # Normalizar cada simulación y calcular IERC
    for sim in range(50):
        sim_features = pd.DataFrame(index=range(len(features)))
        for col in features.columns:
            if col != 'h3_cell_8':
                sim_features[col] = sim_results[col][:, sim]
        
        # Normalizar (percentil 1-99)
        norm_features = {}
        for col in sim_features.columns:
            data = sim_features[col]
            p1, p99 = np.percentile(data, [1, 99])
            data_clipped = data.clip(p1, p99)
            if p99 > p1:
                norm_features[col] = ((data_clipped - p1) / (p99 - p1)) * 100
            else:
                norm_features[col] = 50
            norm_features[col] = np.clip(norm_features[col], 0, 100)
        
        # Calcular IERC
        weights = {
            'chlor_a_mean': 0.13, 'chlor_a_max': 0.05, 'sst_mean': 0.08,
            'sst_max': 0.05, 'sst_std': 0.03, 'depth_mean': 0.08,
            'depth_slope': 0.04, 'depth_range': 0.02,
            'tnc_bajos_area_frac': 0.10, 'tnc_coral_area_frac': 0.08,
            'asea_count': 0.12, 'asea_terminal_gnl': 0.10, 'asea_gasoducto': 0.08,
            'pangas_total_frac': 0.05,
        }
        
        risk = np.zeros(len(features))
        for feat, w in weights.items():
            if feat in norm_features:
                risk += norm_features[feat] * w
        
        ierc_sims[:, sim] = np.clip(risk, 0, 100)
    
    # Estadísticas Monte Carlo
    ierc_mean = ierc_sims.mean(axis=1)
    ierc_std = ierc_sims.std(axis=1)
    ierc_p05 = np.percentile(ierc_sims, 5, axis=1)
    ierc_p95 = np.percentile(ierc_sims, 95, axis=1)
    
    # DataFrame resultado
    results = pd.DataFrame({
        'h3_cell_8': features['h3_cell_8'],
        'ierc_mean': ierc_mean,
        'ierc_std': ierc_std,
        'ierc_p05': ierc_p05,
        'ierc_p95': ierc_p95,
        'ierc_median': np.median(ierc_sims, axis=1),
    })
    
    # Guardar
    GOLD = Path("/home/gorops/ierc-gnl-project/lakehouse/curated")
    output_path = GOLD / "ierc_monte_carlo_h3_8.parquet"
    results.to_parquet(output_path, compression='zstd', index=False)
    logger.info(f"Guardado: {output_path}")
    
    # Resumen
    logger.info(f"Monte Carlo completado:")
    logger.info(f"  IERC mean: {ierc_mean.mean():.1f} ± {ierc_mean.std():.1f}")
    logger.info(f"  IERC std (aleatorio): {ierc_std.mean():.2f}")
    logger.info(f"  IC 90% ancho medio: {(ierc_p95 - ierc_p05).mean():.2f}")
    
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run_monte_carlo_ierc()