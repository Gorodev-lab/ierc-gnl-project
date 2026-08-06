#!/usr/bin/env python3
"""
IERC-GNL Supabase Migration Script
Migrates 7 GeoPackage layers + Gold Parquet features to Supabase PostgreSQL PostGIS.
"""

import os
import json
import geopandas as gpd
import pandas as pd
import shapely.geometry
from typing import List

GPKG_PATH = "deliverables/v1_geopackage/ierc_golfo_california.gpkg"
PARQUET_PATH = "lakehouse/curated/ierc_features_h3_8.parquet"
OUTPUT_DIR = "scripts/supabase/data_sql"

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

def build_grilla_h3_sql():
    print("Building SQL for grilla_h3_riesgo...")
    gdf = gpd.read_file(GPKG_PATH, layer="grilla_h3_riesgo")
    statements = []
    
    for _, r in gdf.iterrows():
        st_geom = geom_to_st(r.geometry)
        sql = f"""INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            {sanitize_str(r.get('h3_index'))}, {sanitize_num(r.get('resolucion'))},
            {sanitize_num(r.get('latitud_centroide'))}, {sanitize_num(r.get('longitud_centroide'))},
            {sanitize_num(r.get('ierc_score'))}, {sanitize_str(r.get('nivel_riesgo'))},
            {sanitize_num(r.get('amenaza_score'))}, {sanitize_num(r.get('exposicion_score'))},
            {sanitize_num(r.get('sensibilidad_score'))}, {sanitize_num(r.get('dependencia_score'))},
            {sanitize_num(r.get('biocultural_score'))}, {sanitize_num(r.get('capacidad_adaptativa_score'))},
            {sanitize_num(r.get('distancia_proyecto_mas_cercano_km'))}, {st_geom}
        ) ON CONFLICT (h3_index) DO NOTHING;"""
        statements.append(sql)
    return statements

def build_proyectos_gnl_sql():
    print("Building SQL for proyectos_gnl...")
    gdf = gpd.read_file(GPKG_PATH, layer="proyectos_gnl")
    statements = []
    for _, r in gdf.iterrows():
        st_geom = geom_to_st(r.geometry)
        sql = f"""INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            {sanitize_str(r.get('nombre_proyecto'))}, {sanitize_str(r.get('estado'))},
            {sanitize_str(r.get('municipio'))}, {sanitize_str(r.get('tipo_infraestructura'))},
            {sanitize_str(r.get('empresa_promovente'))}, {sanitize_str(r.get('estatus_permiso'))},
            {sanitize_str(r.get('fuente_oficial'))}, {sanitize_num(r.get('capacidad_mtpa'))},
            {sanitize_num(r.get('latitud'))}, {sanitize_num(r.get('longitud'))}, {st_geom}
        );"""
        statements.append(sql)
    return statements

def build_gasoductos_sql():
    print("Building SQL for gasoductos_infraestructura_gnl...")
    gdf = gpd.read_file(GPKG_PATH, layer="gasoductos_infraestructura_gnl")
    statements = []
    for _, r in gdf.iterrows():
        st_geom = geom_to_st(r.geometry)
        sql = f"""INSERT INTO public.gasoductos_infraestructura_gnl (
            ducto_id, nombre, operador, estatus, longitud_km, geometry
        ) VALUES (
            {sanitize_str(r.get('ducto_id'))}, {sanitize_str(r.get('nombre'))},
            {sanitize_str(r.get('operador'))}, {sanitize_str(r.get('estatus'))},
            {sanitize_num(r.get('longitud_km'))}, {st_geom}
        );"""
        statements.append(sql)
    return statements

def build_pangas_sql():
    print("Building SQL for zonas_pesqueras_pangas...")
    gdf = gpd.read_file(GPKG_PATH, layer="zonas_pesqueras_pangas")
    statements = []
    for _, r in gdf.iterrows():
        st_geom = geom_to_st(r.geometry)
        sql = f"""INSERT INTO public.zonas_pesqueras_pangas (
            uid_espaciotemporal, sitio_code, nombre_sitio, comunidad, actor, pesqueria,
            arte, zona, temporada, ruta, habitat, total_registros_entrevista,
            riqueza_total_especies, especies_criticas_iucn_count, tiene_especies_amenazadas, geometry
        ) VALUES (
            {sanitize_str(r.get('uid_espaciotemporal'))}, {sanitize_str(r.get('sitio_code'))},
            {sanitize_str(r.get('nombre_sitio'))}, {sanitize_str(r.get('comunidad'))},
            {sanitize_str(r.get('actor'))}, {sanitize_str(r.get('pesqueria'))},
            {sanitize_str(r.get('arte'))}, {sanitize_str(r.get('zona'))},
            {sanitize_str(r.get('temporada'))}, {sanitize_str(r.get('ruta'))},
            {sanitize_str(r.get('habitat'))}, {sanitize_num(r.get('total_registros_entrevista'))},
            {sanitize_num(r.get('riqueza_total_especies'))}, {sanitize_num(r.get('especies_criticas_iucn_count'))},
            {sanitize_num(r.get('tiene_especies_amenazadas'))}, {st_geom}
        ) ON CONFLICT (uid_espaciotemporal) DO NOTHING;"""
        statements.append(sql)
    return statements

def build_anp_sql():
    print("Building SQL for anp_habitats_criticos...")
    gdf = gpd.read_file(GPKG_PATH, layer="anp_habitats_criticos")
    statements = []
    for _, r in gdf.iterrows():
        st_geom = geom_to_st(r.geometry)
        sql = f"""INSERT INTO public.anp_habitats_criticos (
            anp_id, nombre, categoria, administracion, superficie_ha, geometry
        ) VALUES (
            {sanitize_str(r.get('anp_id'))}, {sanitize_str(r.get('nombre'))},
            {sanitize_str(r.get('categoria'))}, {sanitize_str(r.get('administracion'))},
            {sanitize_num(r.get('superficie_ha'))}, {st_geom}
        );"""
        statements.append(sql)
    return statements

def build_localidades_sql():
    print("Building SQL for localidades_estudio_ierc...")
    gdf = gpd.read_file(GPKG_PATH, layer="localidades_estudio_ierc")
    statements = []
    for _, r in gdf.iterrows():
        st_geom = geom_to_st(r.geometry)
        sql = f"""INSERT INTO public.localidades_estudio_ierc (
            localidad_id, nombre, municipio, estado, tipo_comunidad,
            poblacion_pesquera_est, prioridad_poa, latitud, longitud, geometry
        ) VALUES (
            {sanitize_str(r.get('localidad_id'))}, {sanitize_str(r.get('nombre'))},
            {sanitize_str(r.get('municipio'))}, {sanitize_str(r.get('estado'))},
            {sanitize_str(r.get('tipo_comunidad'))}, {sanitize_num(r.get('poblacion_pesquera_est'))},
            {sanitize_str(r.get('prioridad_poa'))}, {sanitize_num(r.get('latitud'))},
            {sanitize_num(r.get('longitud'))}, {st_geom}
        ) ON CONFLICT (localidad_id) DO NOTHING;"""
        statements.append(sql)
    return statements

def build_riqueza_sql():
    print("Building SQL for riqueza_relativa_pesquera...")
    gdf = gpd.read_file(GPKG_PATH, layer="riqueza_relativa_pesquera")
    statements = []
    for _, r in gdf.iterrows():
        st_geom = geom_to_st(r.geometry)
        sql = f"""INSERT INTO public.riqueza_relativa_pesquera (
            riqueza_absoluta, shape_length, shape_area, geometry
        ) VALUES (
            {sanitize_num(r.get('riqueza_absoluta'))}, {sanitize_num(r.get('Shape_Length'))},
            {sanitize_num(r.get('Shape_Area'))}, {st_geom}
        );"""
        statements.append(sql)
    return statements

def build_features_summary_sql():
    print("Building SQL for ierc_features_summary...")
    df = pd.read_parquet(PARQUET_PATH)
    gdf_grid = gpd.read_file(GPKG_PATH, layer="grilla_h3_riesgo")
    h3_grid_set = set(gdf_grid["h3_index"])
    
    depth_median = df['depth_mean'].median()
    chlor_median = df['chlor_a_mean'].median()
    
    observed = df[df['h3_cell_8'].isin(h3_grid_set)].copy()
    print(f"Total features rows: {len(df)}, Grid-matched summary rows: {len(observed)}")
    
    statements = []
    for _, r in observed.iterrows():
        has_obs = (r.get('depth_mean') != depth_median) or (r.get('chlor_a_mean') != chlor_median) or (r.get('tnc_bajos_count') > 0)
        sql = f"""INSERT INTO public.ierc_features_summary (
            h3_index, chlor_a_mean, sst_mean, depth_mean, bajos_count, coral_count, has_observed_data
        ) VALUES (
            {sanitize_str(r.get('h3_cell_8'))}, {sanitize_num(r.get('chlor_a_mean'))},
            {sanitize_num(r.get('sst_mean'))}, {sanitize_num(r.get('depth_mean'))},
            {sanitize_num(r.get('tnc_bajos_count'))}, {sanitize_num(r.get('tnc_coral_count'))}, {'TRUE' if has_obs else 'FALSE'}
        ) ON CONFLICT (h3_index) DO NOTHING;"""
        statements.append(sql)
    return statements

def save_batches(layer_name: str, statements: List[str], batch_size: int = 250):
    chunks = [statements[i:i + batch_size] for i in range(0, len(statements), batch_size)]
    files = []
    for idx, chunk in enumerate(chunks):
        filename = os.path.join(OUTPUT_DIR, f"{layer_name}_batch_{idx:03d}.sql")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(chunk))
        files.append(filename)
    print(f"Layer {layer_name}: {len(statements)} statements saved across {len(files)} files.")
    return files

if __name__ == "__main__":
    save_batches("proyectos_gnl", build_proyectos_gnl_sql(), batch_size=50)
    save_batches("gasoductos", build_gasoductos_sql(), batch_size=50)
    save_batches("pangas", build_pangas_sql(), batch_size=50)
    save_batches("anp", build_anp_sql(), batch_size=50)
    save_batches("localidades", build_localidades_sql(), batch_size=50)
    save_batches("grilla_h3", build_grilla_h3_sql(), batch_size=300)
    save_batches("riqueza", build_riqueza_sql(), batch_size=400)
    save_batches("features_summary", build_features_summary_sql(), batch_size=500)
    print("SQL batch generation complete!")
