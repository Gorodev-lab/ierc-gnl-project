#!/usr/bin/env python3
"""
prepare_dashboard_data.py
-------------------------
Prepara y sincroniza los datasets espaciales y cuantitativos para el visor interactivo Next.js:
- Exporta 11 proyectos GNL consolidados a public/data/proyectos_gnl.geojson
- Exporta contornos batimétricos GEBCO/ETOPO1 a public/data/batimetria_golfo.geojson
- Sincroniza reporte_cobertura_datos.json a public/data/reporte_cobertura.json
- Exporta grilla H3 con IERC a public/data/grilla_h3_riesgo.geojson
"""

import json
import shutil
from pathlib import Path
import geopandas as gpd

BASE = Path('/home/gorops/ierc-gnl-project')
OUTPUT_DIR = BASE / 'causanaturadata/output'
DELIVERABLE_GPKG = BASE / 'deliverables/v1_geopackage/ierc_golfo_california.gpkg'
PUBLIC_DIR = BASE / 'dashboard/public/data'

PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
print(f"[+] Exportando datos a {PUBLIC_DIR}...")

# 1. Proyectos GNL consolidados (11)
gnl_geojson = OUTPUT_DIR / 'proyectos_gnl_consolidados.geojson'
if gnl_geojson.exists():
    shutil.copy(gnl_geojson, PUBLIC_DIR / 'proyectos_gnl.geojson')
    print("   ✔ Copiado: proyectos_gnl.geojson")

# 2. Reporte de Cobertura JSON
reporte_json = OUTPUT_DIR / 'reporte_cobertura_datos.json'
if reporte_json.exists():
    shutil.copy(reporte_json, PUBLIC_DIR / 'reporte_cobertura.json')
    print("   ✔ Copiado: reporte_cobertura.json")

# 3. Batimetría GEBCO (simplificada para visor web)
gebco_gpkg = OUTPUT_DIR / 'GEBCO_Batimetria_Golfo.gpkg'
if gebco_gpkg.exists():
    gdf_gebco = gpd.read_file(gebco_gpkg, layer="batimetria_gebco_2024").to_crs("EPSG:4326")
    gdf_gebco.to_file(PUBLIC_DIR / 'batimetria_golfo.geojson', driver="GeoJSON")
    print("   ✔ Exportado: batimetria_golfo.geojson")

# 4. Malla H3 con IERC
if DELIVERABLE_GPKG.exists():
    gdf_h3 = gpd.read_file(DELIVERABLE_GPKG, layer="grilla_h3_riesgo").to_crs("EPSG:4326")
    gdf_h3.to_file(PUBLIC_DIR / 'grilla_h3_riesgo.geojson', driver="GeoJSON")
    print("   ✔ Exportado: grilla_h3_riesgo.geojson")

print("[✔] Todos los insumos del Dashboard web han sido preparados.")
