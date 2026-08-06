#!/usr/bin/env python3
"""
High-Speed PostgREST Migrator for Supabase
Pushes JSON batches directly via PostgREST endpoint.
"""

import os
import json
import geopandas as gpd
import pandas as pd
import shapely.geometry
import requests

SUPABASE_URL = "https://jhgdwhobefoyodrsmpnc.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpoZ2R3aG9iZWZveW9kcnNtcG5jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU5NjI5NTgsImV4cCI6MjEwMTUzODk1OH0.Ii8gWRA1xDEFzZqZGkWsaTlulug0Tp1z4JAPGIrIMEY"

GPKG_PATH = "deliverables/v1_geopackage/ierc_golfo_california.gpkg"
PARQUET_PATH = "lakehouse/curated/ierc_features_h3_8.parquet"

HEADERS = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def geom_to_ewkt(geom):
    if geom is None or geom.is_empty:
        return None
    return f"SRID=4326;{geom.wkt}"

def push_table(table_name: str, records: list, batch_size: int = 500):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    total = len(records)
    print(f"Pushing {total} records to {table_name}...")
    
    for i in range(0, total, batch_size):
        chunk = records[i:i + batch_size]
        res = requests.post(url, headers=HEADERS, json=chunk)
        if res.status_code not in (200, 201, 204):
            print(f"Error in batch {i//batch_size} ({res.status_code}): {res.text}")
        else:
            print(f"Batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size} done.")
    print(f"Table {table_name} migration complete!")

def migrate_grilla():
    gdf = gpd.read_file(GPKG_PATH, layer="grilla_h3_riesgo")
    records = []
    for _, r in gdf.iterrows():
        records.append({
            "h3_index": str(r.get("h3_index")),
            "resolucion": int(r.get("resolucion")),
            "latitud_centroide": float(r.get("latitud_centroide")) if pd.notna(r.get("latitud_centroide")) else None,
            "longitud_centroide": float(r.get("longitud_centroide")) if pd.notna(r.get("longitud_centroide")) else None,
            "ierc_score": float(r.get("ierc_score")) if pd.notna(r.get("ierc_score")) else None,
            "nivel_riesgo": str(r.get("nivel_riesgo")) if pd.notna(r.get("nivel_riesgo")) else None,
            "amenaza_score": float(r.get("amenaza_score")) if pd.notna(r.get("amenaza_score")) else None,
            "exposicion_score": float(r.get("exposicion_score")) if pd.notna(r.get("exposicion_score")) else None,
            "sensibilidad_score": float(r.get("sensibilidad_score")) if pd.notna(r.get("sensibilidad_score")) else None,
            "dependencia_score": float(r.get("dependencia_score")) if pd.notna(r.get("dependencia_score")) else None,
            "biocultural_score": float(r.get("biocultural_score")) if pd.notna(r.get("biocultural_score")) else None,
            "capacidad_adaptativa_score": float(r.get("capacidad_adaptativa_score")) if pd.notna(r.get("capacidad_adaptativa_score")) else None,
            "distancia_proyecto_mas_cercano_km": float(r.get("distancia_proyecto_mas_cercano_km")) if pd.notna(r.get("distancia_proyecto_mas_cercano_km")) else None,
            "geometry": geom_to_ewkt(r.geometry)
        })
    push_table("grilla_h3_riesgo", records, batch_size=500)

def migrate_features_summary():
    df = pd.read_parquet(PARQUET_PATH)
    gdf_grid = gpd.read_file(GPKG_PATH, layer="grilla_h3_riesgo")
    h3_grid_set = set(gdf_grid["h3_index"])
    depth_median = float(df['depth_mean'].median())
    chlor_median = float(df['chlor_a_mean'].median())
    
    observed = df[df['h3_cell_8'].isin(h3_grid_set)].copy()
    records = []
    for _, r in observed.iterrows():
        d_val = float(r.get("depth_mean")) if pd.notna(r.get("depth_mean")) else None
        c_val = float(r.get("chlor_a_mean")) if pd.notna(r.get("chlor_a_mean")) else None
        b_cnt = int(r.get("tnc_bajos_count")) if pd.notna(r.get("tnc_bajos_count")) else 0
        cr_cnt = int(r.get("tnc_coral_count")) if pd.notna(r.get("tnc_coral_count")) else 0
        has_obs = bool((d_val != depth_median) or (c_val != chlor_median) or (b_cnt > 0))
        
        records.append({
            "h3_index": str(r.get("h3_cell_8")),
            "chlor_a_mean": c_val,
            "sst_mean": float(r.get("sst_mean")) if pd.notna(r.get("sst_mean")) else None,
            "depth_mean": d_val,
            "bajos_count": b_cnt,
            "coral_count": cr_cnt,
            "has_observed_data": has_obs
        })
    push_table("ierc_features_summary", records, batch_size=500)

def migrate_riqueza():
    gdf = gpd.read_file(GPKG_PATH, layer="riqueza_relativa_pesquera")
    records = []
    for _, r in gdf.iterrows():
        records.append({
            "riqueza_absoluta": float(r.get("riqueza_absoluta")) if pd.notna(r.get("riqueza_absoluta")) else None,
            "shape_length": float(r.get("Shape_Length")) if pd.notna(r.get("Shape_Length")) else None,
            "shape_area": float(r.get("Shape_Area")) if pd.notna(r.get("Shape_Area")) else None,
            "geometry": geom_to_ewkt(r.geometry)
        })
    push_table("riqueza_relativa_pesquera", records, batch_size=500)

if __name__ == "__main__":
    migrate_grilla()
    migrate_features_summary()
    migrate_riqueza()
    print("PostgREST migration successfully finished!")
