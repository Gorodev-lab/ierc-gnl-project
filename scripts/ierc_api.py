#!/usr/bin/env python3
"""
IERC API Server - Phase 7
=========================
FastAPI service serving IERC risk data from DuckDB/Parquet.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path("/home/gorops/ierc-gnl-project/src")))

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import duckdb
import pandas as pd
import numpy as np
import h3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
LAKEHOUSE_ROOT = Path("/home/gorops/ierc-gnl-project/lakehouse")
GOLD = LAKEHOUSE_ROOT / "curated"
SILVER = LAKEHOUSE_ROOT / "processed"
CATALOG_DB = LAKEHOUSE_ROOT / "metadata" / "catalog.duckdb"

app = FastAPI(
    title="IERC-GNL Risk API",
    description="Índice de Riesgo Socioeconómico - Golfo de California",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global connection
conn = duckdb.connect(str(CATALOG_DB), read_only=True)


class CellRiskResponse(BaseModel):
    h3_cell_8: str
    ierc_score: float
    risk_level: str
    ierc_percentile: float
    lat: float
    lng: float


class MonteCarloResponse(BaseModel):
    h3_cell_8: str
    ierc_mean: float
    ierc_std: float
    ierc_p05: float
    ierc_p95: float
    ierc_median: float
    lat: float
    lng: float


class FeatureResponse(BaseModel):
    h3_cell_8: str
    features: Dict[str, float]
    lat: float
    lng: float


class BBoxQuery(BaseModel):
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float


@app.get("/")
def root():
    return {
        "service": "IERC-GNL Risk API",
        "version": "2.0.0",
        "description": "Índice de Riesgo Socioeconómico para proyectos GNL en Golfo de California (POA 2026)",
        "endpoints": {
            "/risk/multiplicative": "IERC oficial R = H * V con sub-índices H y V",
            "/risk/confidence": "Mapa de Confianza y Calidad del Dato Nivel III",
            "/risk/deterministic": "IERC determinista por celda H3_8",
            "/risk/monte-carlo": "IERC Monte Carlo con IC 90%",
            "/features": "Features originales por celda",
            "/catalog/datasets": "Datasets registrados en catálogo",
            "/catalog/runs": "Historial de ingestas",
            "/health": "Health check"
        }
    }


@app.get("/health")
def health():
    return {"status": "healthy", "lakehouse": str(LAKEHOUSE_ROOT)}


@app.get("/risk/multiplicative")
def get_multiplicative_risk(
    h3_cell: Optional[str] = Query(None, description="Celda H3 específica"),
    risk_level: Optional[str] = Query(None, description="Bajo, Moderado, Alto, Crítico"),
    limit: int = Query(1000, le=10000)
):
    """Obtiene el IERC oficial multiplicativo R = H * V con sub-scores de Amenaza (H) y Vulnerabilidad (V)."""
    parquet_path = GOLD / "ierc_risk_multiplicative.parquet"
    if not parquet_path.exists():
        parquet_path = GOLD / "ierc_risk_h3_8.parquet"

    query = "SELECT * FROM read_parquet(?)"
    params = [str(parquet_path)]

    where_clauses = []
    if h3_cell:
        where_clauses.append("(h3_cell = ? OR h3_cell_8 = ?)")
        params.extend([h3_cell, h3_cell])

    if risk_level:
        where_clauses.append("nivel_riesgo = ?")
        params.append(risk_level)

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    query += " ORDER BY ierc_score DESC LIMIT ?"
    params.append(limit)

    df = conn.execute(query, params).fetchdf()
    if len(df) > 0:
        col = 'h3_cell' if 'h3_cell' in df.columns else 'h3_cell_8'
        df['lat'] = df[col].apply(lambda c: h3.cell_to_latlng(c)[0] if pd.notna(c) else None)
        df['lng'] = df[col].apply(lambda c: h3.cell_to_latlng(c)[1] if pd.notna(c) else None)

    return df.to_dict(orient="records")


@app.get("/risk/confidence")
def get_confidence_map(
    h3_cell: Optional[str] = Query(None),
    limit: int = Query(1000, le=10000)
):
    """Obtiene el Mapa de Confianza Nivel III (0-100) por celda H3."""
    parquet_path = GOLD / "ierc_confidence_h3.parquet"
    if not parquet_path.exists():
        raise HTTPException(status_code=404, detail="Mapa de Confianza Nivel III no generado aún.")

    query = "SELECT * FROM read_parquet(?)"
    params = [str(parquet_path)]

    if h3_cell:
        query += " WHERE h3_cell = ?"
        params.append(h3_cell)

    query += " ORDER BY confidence_score DESC LIMIT ?"
    params.append(limit)

    df = conn.execute(query, params).fetchdf()
    if len(df) > 0 and 'h3_cell' in df.columns:
        df['lat'] = df['h3_cell'].apply(lambda c: h3.cell_to_latlng(c)[0] if pd.notna(c) else None)
        df['lng'] = df['h3_cell'].apply(lambda c: h3.cell_to_latlng(c)[1] if pd.notna(c) else None)

    return df.to_dict(orient="records")


@app.get("/risk/deterministic")
def get_deterministic_risk(
    h3_cell_8: Optional[str] = Query(None, description="Celda H3_8 específica"),
    min_lat: Optional[float] = Query(None),
    max_lat: Optional[float] = Query(None),
    min_lng: Optional[float] = Query(None),
    max_lng: Optional[float] = Query(None),
    risk_level: Optional[str] = Query(None, description="Filtrar por nivel: Bajo, Moderado, Alto, Crítico"),
    limit: int = Query(1000, le=10000)
):
    """Obtiene IERC determinista para celdas H3_8."""
    
    query = """
        SELECT h3_cell_8, ierc_score, risk_level, ierc_percentile
        FROM read_parquet(?)
    """
    params = [str(GOLD / "ierc_risk_h3_8.parquet")]
    
    where_clauses = []
    if h3_cell_8:
        where_clauses.append("h3_cell_8 = ?")
        params.append(h3_cell_8)
    
    if risk_level:
        where_clauses.append("risk_level = ?")
        params.append(risk_level)
    
    # Spatial filter via H3 cell lookup
    if min_lat is not None and max_lat is not None and min_lng is not None and max_lng is not None:
        # Get H3 cells in bbox
        cells_in_bbox = h3.geo_to_cells({
            "type": "Polygon",
            "coordinates": [[[min_lng, min_lat], [max_lng, min_lat], 
                           [max_lng, max_lat], [min_lng, max_lat], [min_lng, min_lat]]]
        }, 8)
        if cells_in_bbox:
            placeholders = ",".join(["?"] * len(cells_in_bbox))
            where_clauses.append(f"h3_cell_8 IN ({placeholders})")
            params.extend(cells_in_bbox)
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += " ORDER BY ierc_score DESC LIMIT ?"
    params.append(limit)
    
    df = conn.execute(query, params).fetchdf()
    
    # Add lat/lng
    if len(df) > 0:
        df['lat'] = df['h3_cell_8'].apply(lambda c: h3.cell_to_latlng(c)[0])
        df['lng'] = df['h3_cell_8'].apply(lambda c: h3.cell_to_latlng(c)[1])
    
    return df.to_dict(orient="records")


@app.get("/risk/monte-carlo")
def get_monte_carlo_risk(
    h3_cell_8: Optional[str] = Query(None),
    min_lat: Optional[float] = Query(None),
    max_lat: Optional[float] = Query(None),
    min_lng: Optional[float] = Query(None),
    max_lng: Optional[float] = Query(None),
    limit: int = Query(1000, le=10000)
):
    """Obtiene IERC Monte Carlo con intervalos de confianza."""
    
    query = """
        SELECT h3_cell_8, ierc_mean, ierc_std, ierc_p05, ierc_p95, ierc_median
        FROM read_parquet(?)
    """
    params = [str(GOLD / "ierc_monte_carlo_h3_8.parquet")]
    
    where_clauses = []
    if h3_cell_8:
        where_clauses.append("h3_cell_8 = ?")
        params.append(h3_cell_8)
    
    if min_lat is not None and max_lat is not None and min_lng is not None and max_lng is not None:
        cells_in_bbox = h3.geo_to_cells({
            "type": "Polygon",
            "coordinates": [[[min_lng, min_lat], [max_lng, min_lat],
                           [max_lng, max_lat], [min_lng, max_lat], [min_lng, min_lat]]]
        }, 8)
        if cells_in_bbox:
            placeholders = ",".join(["?"] * len(cells_in_bbox))
            where_clauses.append(f"h3_cell_8 IN ({placeholders})")
            params.extend(cells_in_bbox)
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += " ORDER BY ierc_mean DESC LIMIT ?"
    params.append(limit)
    
    df = conn.execute(query, params).fetchdf()
    
    if len(df) > 0:
        df['lat'] = df['h3_cell_8'].apply(lambda c: h3.cell_to_latlng(c)[0])
        df['lng'] = df['h3_cell_8'].apply(lambda c: h3.cell_to_latlng(c)[1])
    
    return df.to_dict(orient="records")


@app.get("/features")
def get_features(
    h3_cell_8: Optional[str] = Query(None),
    limit: int = Query(100, le=1000)
):
    """Obtiene features originales para una celda."""
    
    query = """
        SELECT * FROM read_parquet(?)
    """
    params = [str(GOLD / "ierc_features_h3_8.parquet")]
    
    if h3_cell_8:
        query += " WHERE h3_cell_8 = ?"
        params.append(h3_cell_8)
    
    query += " LIMIT ?"
    params.append(limit)
    
    df = conn.execute(query, params).fetchdf()
    
    if len(df) > 0:
        df['lat'] = df['h3_cell_8'].apply(lambda c: h3.cell_to_latlng(c)[0])
        df['lng'] = df['h3_cell_8'].apply(lambda c: h3.cell_to_latlng(c)[1])
    
    return df.to_dict(orient="records")


@app.get("/catalog/datasets")
def get_datasets():
    """Lista datasets registrados en catálogo."""
    df = conn.execute("SELECT * FROM datasets ORDER BY priority, name").fetchdf()
    # Handle NaN values
    df = df.fillna("")
    return df.to_dict(orient="records")


@app.get("/catalog/runs")
def get_runs(
    dataset_name: Optional[str] = Query(None),
    limit: int = Query(50)
):
    """Historial de ejecuciones de ingesta."""
    query = "SELECT * FROM ingestion_runs"
    params = []
    
    if dataset_name:
        query += " WHERE dataset_name = ?"
        params.append(dataset_name)
    
    query += " ORDER BY started_at DESC LIMIT ?"
    params.append(limit)
    
    df = conn.execute(query, params).fetchdf()
    return df.to_dict(orient="records")


@app.get("/catalog/quality")
def get_quality():
    """Validaciones de calidad."""
    df = conn.execute("SELECT * FROM quality_validations ORDER BY run_id DESC").fetchdf()
    return df.to_dict(orient="records")


@app.post("/risk/bbox")
def risk_by_bbox(bbox: BBoxQuery, limit: int = Query(5000, le=50000)):
    """Obtiene riesgo para todas las celdas en un bounding box."""
    
    cells_in_bbox = h3.geo_to_cells({
        "type": "Polygon",
        "coordinates": [[[bbox.min_lng, bbox.min_lat], [bbox.max_lng, bbox.min_lat],
                       [bbox.max_lng, bbox.max_lat], [bbox.min_lng, bbox.max_lat], [bbox.min_lng, bbox.min_lat]]]
    }, 8)
    
    if not cells_in_bbox:
        return []
    
    placeholders = ",".join(["?"] * len(cells_in_bbox))
    query = f"""
        SELECT h3_cell_8, ierc_score, risk_level, ierc_percentile
        FROM read_parquet(?)
        WHERE h3_cell_8 IN ({placeholders})
        ORDER BY ierc_score DESC
        LIMIT ?
    """
    params = [str(GOLD / "ierc_risk_h3_8.parquet")] + list(cells_in_bbox) + [limit]
    
    df = conn.execute(query, params).fetchdf()
    
    if len(df) > 0:
        df['lat'] = df['h3_cell_8'].apply(lambda c: h3.cell_to_latlng(c)[0])
        df['lng'] = df['h3_cell_8'].apply(lambda c: h3.cell_to_latlng(c)[1])
    
    return df.to_dict(orient="records")


@app.get("/stats/summary")
def get_summary_stats():
    """Estadísticas globales del IERC."""
    
    det = conn.execute("""
        SELECT 
            COUNT(*) as total_cells,
            AVG(ierc_score) as mean_score,
            STDDEV(ierc_score) as std_score,
            MIN(ierc_score) as min_score,
            MAX(ierc_score) as max_score,
            risk_level,
            COUNT(*) as count
        FROM read_parquet(?)
        GROUP BY risk_level
    """, [str(GOLD / "ierc_risk_h3_8.parquet")]).fetchdf()
    
    mc = conn.execute("""
        SELECT 
            AVG(ierc_mean) as mc_mean,
            STDDEV(ierc_mean) as mc_std,
            AVG(ierc_std) as mc_aleatory_std,
            AVG(ierc_p95 - ierc_p05) as mc_ic_width
        FROM read_parquet(?)
    """, [str(GOLD / "ierc_monte_carlo_h3_8.parquet")]).fetchdf()
    
    return {
        "deterministic": det.to_dict(orient="records"),
        "monte_carlo": mc.to_dict(orient="records")[0] if len(mc) > 0 else {}
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)