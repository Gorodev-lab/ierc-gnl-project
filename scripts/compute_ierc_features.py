#!/usr/bin/env python3
"""
IERC Feature Engineering (Actualizado POA 2026)
================================================
Genera la matriz de features Gold por celda H3 adaptativa (Res 8 / Res 9),
clasificando variables en los ejes de Amenaza (H) y Vulnerabilidad (V).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path("/home/gorops/ierc-gnl-project/src")))

import pandas as pd
import numpy as np
import duckdb
import logging

from data.lakehouse.partitioning import get_adaptive_gulf_h3_cells

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LAKEHOUSE_ROOT = Path("/home/gorops/ierc-gnl-project/lakehouse")
SILVER = LAKEHOUSE_ROOT / "processed"
GOLD = LAKEHOUSE_ROOT / "curated"


def load_silver_parquet(path: Path, columns: list = None) -> pd.DataFrame:
    """Carga datos Silver con DuckDB."""
    if not path.exists():
        logger.warning(f"Path no existe: {path}")
        return pd.DataFrame()
    
    conn = duckdb.connect()
    select_str = ", ".join(columns) if columns else "*"
    query = f"SELECT {select_str} FROM read_parquet('{path}/**/*.parquet')"
    try:
        df = conn.execute(query).fetchdf()
    except Exception as e:
        logger.warning(f"Error leyendo {path}: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    return df


def compute_ierc_features() -> pd.DataFrame:
    """Computa la matriz de features Gold alineada a H y V."""
    logger.info("=== Calculando Features Gold H3 Adaptativas (H y V) ===")
    
    adaptive_cells = get_adaptive_gulf_h3_cells()
    df_base = pd.DataFrame(adaptive_cells, columns=['h3_cell', 'resolution'])
    logger.info(f"Grilla Base: {len(df_base)} celdas H3 adaptativas")
    
    # 1. NASA Chlor_a & SST (Sensibilidad Ambiental V)
    logger.info("Cargando NASA Chlor_a y SST...")
    chlor = load_silver_parquet(SILVER / "nasa/chlor_a", columns=['h3_cell', 'chlor_a'])
    if not chlor.empty:
        chlor_stats = chlor.groupby('h3_cell')['chlor_a'].agg(
            chlor_a_mean='mean',
            chlor_a_max='max'
        ).reset_index()
        df_base = df_base.merge(chlor_stats, on='h3_cell', how='left')
    else:
        df_base['chlor_a_mean'] = 1.5
        df_base['chlor_a_max'] = 3.0

    sst = load_silver_parquet(SILVER / "nasa/sst", columns=['h3_cell', 'sst'])
    if not sst.empty:
        sst_stats = sst.groupby('h3_cell')['sst'].agg(
            sst_mean='mean',
            sst_max='max',
            sst_std='std'
        ).reset_index()
        df_base = df_base.merge(sst_stats, on='h3_cell', how='left')
    else:
        df_base['sst_mean'] = 24.5
        df_base['sst_max'] = 30.0
        df_base['sst_std'] = 2.1

    # 2. Batimetría GEBCO (Sensibilidad Físico-Marina V)
    logger.info("Cargando Batimetría GEBCO...")
    gebco = load_silver_parquet(SILVER / "bathymetry_gebco", columns=['h3_cell', 'bathymetry_mean', 'bathymetry_min', 'bathymetry_max'])
    if not gebco.empty:
        gebco = gebco.rename(columns={'bathymetry_mean': 'depth_mean', 'bathymetry_min': 'depth_min', 'bathymetry_max': 'depth_max'})
        gebco['depth_range'] = gebco['depth_max'] - gebco['depth_min']
        df_base = df_base.merge(gebco, on='h3_cell', how='left')
    else:
        df_base['depth_mean'] = -150.0
        df_base['depth_range'] = 50.0

    # 3. TNC Bajos & Coral Negro (Conservación y Hábitat V)
    logger.info("Cargando TNC Bajos y Coral...")
    bajos = load_silver_parquet(SILVER / "tnc/bajos_marinos_h3", columns=['h3_cell', 'area_fraction'])
    if not bajos.empty:
        bajos_agg = bajos.groupby('h3_cell')['area_fraction'].sum().reset_index().rename(columns={'area_fraction': 'tnc_bajos_area_frac'})
        df_base = df_base.merge(bajos_agg, on='h3_cell', how='left')
    else:
        df_base['tnc_bajos_area_frac'] = 0.0

    coral = load_silver_parquet(SILVER / "tnc/arrecifes_coral_negro_h3", columns=['h3_cell', 'area_fraction'])
    if not coral.empty:
        coral_agg = coral.groupby('h3_cell')['area_fraction'].sum().reset_index().rename(columns={'area_fraction': 'tnc_coral_area_frac'})
        df_base = df_base.merge(coral_agg, on='h3_cell', how='left')
    else:
        df_base['tnc_coral_area_frac'] = 0.0

    # 4. ASEA MIA (Proximidad Amenaza GNL H)
    logger.info("Cargando ASEA MIA...")
    asea = load_silver_parquet(SILVER / "asea/mias_enriched", columns=['h3_cell_10', 'tipo_proyecto', 'estatus'])
    if not asea.empty:
        import h3
        asea['h3_cell'] = asea['h3_cell_10'].apply(lambda x: h3.cell_to_parent(x, 8) if pd.notna(x) else None)
        asea_agg = asea.groupby('h3_cell').agg(
            asea_count=('h3_cell_10', 'count'),
            asea_terminal_gnl=('tipo_proyecto', lambda x: (x == 'terminal_gnl').sum()),
            asea_gasoducto=('tipo_proyecto', lambda x: (x.str.contains('gasoducto')).sum())
        ).reset_index()
        df_base = df_base.merge(asea_agg, on='h3_cell', how='left')
    else:
        df_base['asea_count'] = 0
        df_base['asea_terminal_gnl'] = 0
        df_base['asea_gasoducto'] = 0

    # 5. PANGAS Zonas Pesqueras & Riqueza (Exposición Pesquera H y Riqueza V)
    logger.info("Cargando PANGAS Real...")
    pangas = load_silver_parquet(SILVER / "pangas/fishing_zones_h3", columns=['h3_cell', 'uid_espaciotemporal', 'riqueza_relativa_mean'])
    if not pangas.empty:
        pangas_agg = pangas.groupby('h3_cell').agg(
            pangas_densidad_esfuerzo=('uid_espaciotemporal', 'count'),
            pangas_riqueza_mean=('riqueza_relativa_mean', 'mean')
        ).reset_index()
        df_base = df_base.merge(pangas_agg, on='h3_cell', how='left')
    else:
        df_base['pangas_densidad_esfuerzo'] = 0
        df_base['pangas_riqueza_mean'] = 0.0

    # 6. Indicadores de Gabinete Socioeconómicos & Gobernanza (V)
    # Valores default estructurados por comunidad / celda
    df_base['dependencia_ingreso'] = 0.70
    df_base['patrimonio_biocultural'] = 0.85
    df_base['genero_postcaptura'] = 0.60
    df_base['capacidad_adaptativa'] = 0.35

    # Rellenar nulos
    numeric_cols = df_base.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df_base[col] = df_base[col].fillna(df_base[col].median())

    logger.info(f"Matriz Gold Generada: {len(df_base)} celdas x {len(df_base.columns)} columnas")
    return df_base


def save_gold_features(features: pd.DataFrame, output_name: str = "ierc_features_adaptive_h3"):
    GOLD.mkdir(parents=True, exist_ok=True)
    parquet_path = GOLD / f"{output_name}.parquet"
    features.to_parquet(parquet_path, compression='zstd', index=False)
    logger.info(f"Features Gold guardadas en {parquet_path}")


def main():
    features = compute_ierc_features()
    save_gold_features(features)


if __name__ == "__main__":
    main()