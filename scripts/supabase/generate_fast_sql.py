#!/usr/bin/env python3
"""
Fast Multi-Row SQL Migration Script for Supabase
Generates multi-row INSERT INTO table VALUES (...), (...) statements for fast execution.
"""

import os
import json
import geopandas as gpd
import pandas as pd
import shapely.geometry

GPKG_PATH = "deliverables/v1_geopackage/ierc_golfo_california.gpkg"
PARQUET_PATH = "lakehouse/curated/ierc_features_h3_8.parquet"
OUTPUT_DIR = "scripts/supabase/fast_sql"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_str(val):
    if pd.isna(val) or val is None:
        return "NULL"
    s = str(val).replace("'", "''")
    return f"'{s}'"

def sanitize_num(val):
    if pd.isna(val) or val is None:
        return "NULL"
    return str(val)

def geom_to_st(geom):
    if geom is None or geom.is_empty:
        return "NULL"
    geojson = json.dumps(shapely.geometry.mapping(geom))
    return f"ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'), 4326)"

def generate_multi_insert(table_name, cols, value_tuples, conflict_col=None, batch_size=200):
    col_str = ", ".join(cols)
    conflict_clause = f" ON CONFLICT ({conflict_col}) DO NOTHING;" if conflict_col else ";"
    files = []
    
    for i in range(0, len(value_tuples), batch_size):
        chunk = value_tuples[i:i + batch_size]
        vals_str = ",\n".join([f"({', '.join(t)})" for t in chunk])
        sql = f"INSERT INTO public.{table_name} ({col_str}) VALUES\n{vals_str}{conflict_clause}"
        
        filename = os.path.join(OUTPUT_DIR, f"{table_name}_batch_{i//batch_size:03d}.sql")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(sql)
        files.append(filename)
    print(f"Table {table_name}: {len(value_tuples)} rows across {len(files)} files.")
    return files

def process_grilla_h3():
    gdf = gpd.read_file(GPKG_PATH, layer="grilla_h3_riesgo")
    cols = ["h3_index", "resolucion", "latitud_centroide", "longitud_centroide", "ierc_score", "nivel_riesgo",
            "amenaza_score", "exposicion_score", "sensibilidad_score", "dependencia_score", "biocultural_score",
            "capacidad_adaptativa_score", "distancia_proyecto_mas_cercano_km", "geometry"]
    tuples = []
    for _, r in gdf.iterrows():
        t = (sanitize_str(r.get('h3_index')), sanitize_num(r.get('resolucion')),
             sanitize_num(r.get('latitud_centroide')), sanitize_num(r.get('longitud_centroide')),
             sanitize_num(r.get('ierc_score')), sanitize_str(r.get('nivel_riesgo')),
             sanitize_num(r.get('amenaza_score')), sanitize_num(r.get('exposicion_score')),
             sanitize_num(r.get('sensibilidad_score')), sanitize_num(r.get('dependencia_score')),
             sanitize_num(r.get('biocultural_score')), sanitize_num(r.get('capacidad_adaptativa_score')),
             sanitize_num(r.get('distancia_proyecto_mas_cercano_km')), geom_to_st(r.geometry))
        tuples.append(t)
    generate_multi_insert("grilla_h3_riesgo", cols, tuples, conflict_col="h3_index", batch_size=1000)

def process_features_summary():
    df = pd.read_parquet(PARQUET_PATH)
    gdf_grid = gpd.read_file(GPKG_PATH, layer="grilla_h3_riesgo")
    h3_grid_set = set(gdf_grid["h3_index"])
    depth_median = df['depth_mean'].median()
    chlor_median = df['chlor_a_mean'].median()
    
    observed = df[df['h3_cell_8'].isin(h3_grid_set)].copy()
    cols = ["h3_index", "chlor_a_mean", "sst_mean", "depth_mean", "bajos_count", "coral_count", "has_observed_data"]
    tuples = []
    for _, r in observed.iterrows():
        has_obs = "TRUE" if ((r.get('depth_mean') != depth_median) or (r.get('chlor_a_mean') != chlor_median) or (r.get('tnc_bajos_count') > 0)) else "FALSE"
        t = (sanitize_str(r.get('h3_cell_8')), sanitize_num(r.get('chlor_a_mean')),
             sanitize_num(r.get('sst_mean')), sanitize_num(r.get('depth_mean')),
             sanitize_num(r.get('tnc_bajos_count')), sanitize_num(r.get('tnc_coral_count')), has_obs)
        tuples.append(t)
    generate_multi_insert("ierc_features_summary", cols, tuples, conflict_col="h3_index", batch_size=1000)

def process_riqueza():
    gdf = gpd.read_file(GPKG_PATH, layer="riqueza_relativa_pesquera")
    cols = ["riqueza_absoluta", "shape_length", "shape_area", "geometry"]
    tuples = []
    for _, r in gdf.iterrows():
        t = (sanitize_num(r.get('riqueza_absoluta')), sanitize_num(r.get('Shape_Length')),
             sanitize_num(r.get('Shape_Area')), geom_to_st(r.geometry))
        tuples.append(t)
    generate_multi_insert("riqueza_relativa_pesquera", cols, tuples, conflict_col=None, batch_size=1000)

if __name__ == "__main__":
    process_grilla_h3()
    process_features_summary()
    process_riqueza()
    print("Fast multi-row SQL generation complete!")
