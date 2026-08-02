#!/usr/bin/env python3
"""
procesar_mias_completo.py
Script unificado de procesamiento para el proyecto IERC-GNL:
1. Genera geometrías vectoriales (WGS84) con matriz de precisión para 4 terminales GNL.
2. Exporta terminales_gnl_v3.geojson y terminales_gnl_v3.gpkg en gnl_research y dashboard/public/data/.
3. Extrae e indexa planos, mapas y croquis de las MIAs (PDFs) en dashboard/public/assets/mias/.
4. Genera manifest.json para la galería de imágenes del dashboard.
"""

import os
import json
import math
import shutil
import fitz  # PyMuPDF
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point, LineString
from pyproj import Transformer

RESEARCH_DIR = '/home/gorops/gnl_research'
DASHBOARD_DATA_DIR = '/home/gorops/ierc-gnl-project/dashboard/public/data'
DASHBOARD_ASSETS_DIR = '/home/gorops/ierc-gnl-project/dashboard/public/assets/mias'

os.makedirs(DASHBOARD_DATA_DIR, exist_ok=True)
os.makedirs(DASHBOARD_ASSETS_DIR, exist_ok=True)

# ============================================================
# 1. FUNCIONES GEOGRÁFICAS
# ============================================================

def circle_polygon(lon, lat, radius_m, n=32):
    """Crea un polígono circular aproximado en WGS84."""
    lat_rad = math.radians(lat)
    deg_lat = radius_m / 111000
    deg_lon = radius_m / (111000 * math.cos(lat_rad))
    coords = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        coords.append((lon + deg_lon * math.cos(angle), lat + deg_lat * math.sin(angle)))
    coords.append(coords[0])
    return Polygon(coords)

def offset_point(lon, lat, distance_km, bearing_deg):
    """Calcula un nuevo punto lat/lon desfasado por distancia y rumbo."""
    lat1, lon1 = math.radians(lat), math.radians(lon)
    d = distance_km / 6371.0
    brng = math.radians(bearing_deg)
    lat2 = math.asin(math.sin(lat1) * math.cos(d) + math.cos(lat1) * math.sin(d) * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d) * math.cos(lat1), math.cos(d) - math.sin(lat1) * math.sin(lat2))
    return (math.degrees(lon2), math.degrees(lat2))

def utm_to_wgs(x, y, zone=12):
    """Convierte coordenadas UTM a WGS84 decimal."""
    epsg = 32600 + zone
    tr = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True)
    return tr.transform(x, y)

# ============================================================
# 2. CONSTRUCCIÓN DE GEOMETRÍAS VECTORIALES (V3)
# ============================================================
print("=" * 60)
print("GENERANDO GEOMETRÍAS VECTORIALES (v3)")
print("=" * 60)

# --- 2.1 SAGUARO ENERGÍA GNL ---
saguaro_centroid = (-112.688038, 29.905838)
saguaro_areas = {
    'T1': (172.417, (0.004, 0.004), 'temporal_almacenamiento', 15),
    'T2': (46.824, (-0.004, -0.004), 'temporal_almacenamiento', 15),
    'Reserva': (0.946, (0.001, 0.001), 'conservacion', None),
    'Campamentos': (20.532, (0.002, 0.002), 'permanente_campamentos', None),
    'Caminos': (1.809, (-0.001, -0.001), 'permanente_caminos', None)
}

saguaro_rows = []
for name, (area_ha, offset, tipo_area, cap) in saguaro_areas.items():
    r_m = math.sqrt(area_ha * 10000 / math.pi)
    lon = saguaro_centroid[0] + offset[0]
    lat = saguaro_centroid[1] + offset[1]
    poly = circle_polygon(lon, lat, r_m)
    saguaro_rows.append({
        'id': f'saguaro_{name.lower()}',
        'proyecto': 'Saguaro Energía GNL',
        'componente': f'Saguaro {name}',
        'promovente': 'Mexico Pacific Limited',
        'empresa_madre': 'Mexico Pacific Limited',
        'estado': 'Sonora',
        'municipio': 'Pitiquito',
        'localidad': 'Puerto Libertad',
        'tipo_area': tipo_area,
        'capacidad_mtpa': cap,
        'fase': 'Fase 1 (Trenes 1-3)',
        'superficie_ha': area_ha,
        'status': 'Proposed / Pre-FID',
        'status_code': 'proposed',
        'precision_level': 'approximate_centroid',
        'precision_label': '[APROXIMADO]',
        'clave_asea': '02BC2006G0008 / M-09-MGA0107-08-23',
        'fuente_coordenadas': 'Centroide GEM Wiki / MIA-R Tablas II.5-II.9 (UTM reservadas)',
        'geometry': poly
    })

# --- 2.2 AMIGO LNG ---
amigo_coord = (-110.868082, 27.922867)
amigo_poly = circle_polygon(amigo_coord[0], amigo_coord[1], 440) # ~60 ha

amigo_rows = [
    {
        'id': 'amigo_lng_t1',
        'proyecto': 'Amigo LNG',
        'componente': 'Amigo LNG - Tren 1',
        'promovente': 'AMIGO LNG, S.A. de C.V.',
        'empresa_madre': 'LNG Alliance / Epcilon LNG LLC',
        'estado': 'Sonora',
        'municipio': 'Guaymas',
        'localidad': 'Guaymas',
        'tipo_area': 'terminal_licuefaccion',
        'capacidad_mtpa': 4.2,
        'fase': 'Tren 1',
        'superficie_ha': 30.0,
        'status': 'Proposed / Pre-FID',
        'status_code': 'proposed',
        'precision_level': 'exact_gem_wiki',
        'precision_label': '[EXACTO]',
        'clave_asea': '26SO2025G0143',
        'fuente_coordenadas': 'GEM Wiki Coordenadas Exactas (27.922867, -110.868082)',
        'geometry': amigo_poly
    },
    {
        'id': 'amigo_lng_t2',
        'proyecto': 'Amigo LNG',
        'componente': 'Amigo LNG - Tren 2',
        'promovente': 'AMIGO LNG, S.A. de C.V.',
        'empresa_madre': 'LNG Alliance / Epcilon LNG LLC',
        'estado': 'Sonora',
        'municipio': 'Guaymas',
        'localidad': 'Guaymas',
        'tipo_area': 'terminal_licuefaccion',
        'capacidad_mtpa': 3.6,
        'fase': 'Tren 2',
        'superficie_ha': 30.0,
        'status': 'Proposed / Pre-FID',
        'status_code': 'proposed',
        'precision_level': 'exact_gem_wiki',
        'precision_label': '[EXACTO]',
        'clave_asea': '26SO2025G0143',
        'fuente_coordenadas': 'GEM Wiki Coordenadas Exactas (27.922867, -110.868082)',
        'geometry': amigo_poly
    }
]

# --- 2.3 VISTA PACÍFICO LNG (CANCELADO) ---
topolobampo = (-109.0881, 25.6033)
flng_pos = offset_point(topolobampo[0], topolobampo[1], 2.228, 225)
r_marina = math.sqrt(22.13 * 10000 / math.pi)
r_terrestre = math.sqrt(0.97 * 10000 / math.pi)

vista_rows = [
    {
        'id': 'vista_pacifico_flng',
        'proyecto': 'Vista Pacífico LNG',
        'componente': 'Vista Pacífico - Unidad FLNG',
        'promovente': 'Vista Pacífico LNG, S.A.P.I. de C.V.',
        'empresa_madre': 'Sempra Infrastructure',
        'estado': 'Sinaloa',
        'municipio': 'Ahome',
        'localidad': 'Topolobampo',
        'tipo_area': 'unidad_flng',
        'capacidad_mtpa': 5.05,
        'fase': 'FLNG Offshore',
        'superficie_ha': 22.13,
        'status': 'CANCELADO (Feb 2026)',
        'status_code': 'cancelled',
        'precision_level': 'calculated_from_text',
        'precision_label': '[CALCULADO]',
        'clave_asea': '25SI2024G0038',
        'fuente_coordenadas': 'Estudio de Riesgo ASEA: 2.228 km offshore SW Topolobampo',
        'geometry': circle_polygon(flng_pos[0], flng_pos[1], r_marina)
    },
    {
        'id': 'vista_pacifico_terrestre',
        'proyecto': 'Vista Pacífico LNG',
        'componente': 'Vista Pacífico - Instalaciones Terrestres',
        'promovente': 'Vista Pacífico LNG, S.A.P.I. de C.V.',
        'empresa_madre': 'Sempra Infrastructure',
        'estado': 'Sinaloa',
        'municipio': 'Ahome',
        'localidad': 'Topolobampo',
        'tipo_area': 'area_terrestre',
        'capacidad_mtpa': 5.05,
        'fase': 'ASIPONA Topolobampo',
        'superficie_ha': 0.97,
        'status': 'CANCELADO (Feb 2026)',
        'status_code': 'cancelled',
        'precision_level': 'calculated_from_text',
        'precision_label': '[CALCULADO]',
        'clave_asea': '25SI2024G0038',
        'fuente_coordenadas': 'Estudio de Riesgo ASEA: 0.97 ha en ASIPONA Topolobampo',
        'geometry': circle_polygon(topolobampo[0] + 0.002, topolobampo[1] + 0.002, r_terrestre)
    }
]

# --- 2.4 GNL COSALÁ ---
cosala_mazatlan = (-106.42, 23.25)
cosala_zapopan = (-103.42, 20.70)

cosala_rows = [
    {
        'id': 'gnl_cosala_mazatlan',
        'proyecto': 'GNL Cosalá',
        'componente': 'GNL Cosalá - Planta Mazatlán',
        'promovente': 'GNL Cosalá, S.A. de C.V.',
        'empresa_madre': 'GNL Cosalá, S.A. de C.V.',
        'estado': 'Sinaloa',
        'municipio': 'Mazatlán',
        'localidad': 'El Habal / Casas Viejas',
        'tipo_area': 'estacion_compresion_expendio',
        'capacidad_mtpa': 0.5,
        'fase': 'MIA-P (En Evaluación)',
        'superficie_ha': 1.5,
        'status': 'En Evaluación ASEA',
        'status_code': 'under_review',
        'precision_level': 'geocoded_approximate',
        'precision_label': '[APROXIMADO]',
        'clave_asea': '25SI2023G0009 / 25SI2025G0030',
        'fuente_coordenadas': 'Geocodificación dirección: Casas Viejas, El Habal, Mazatlán',
        'geometry': circle_polygon(cosala_mazatlan[0], cosala_mazatlan[1], 180)
    },
    {
        'id': 'gnl_cosala_zapopan',
        'proyecto': 'GNL Cosalá',
        'componente': 'GNL Cosalá - Estación Zapopan',
        'promovente': 'GNL Cosalá, S.A. de C.V.',
        'empresa_madre': 'GNL Cosalá, S.A. de C.V.',
        'estado': 'Jalisco',
        'municipio': 'Zapopan',
        'localidad': 'Santa Lucía',
        'tipo_area': 'estacion_descompresion',
        'capacidad_mtpa': 0.2,
        'fase': 'MIA-P (En Evaluación)',
        'superficie_ha': 0.3,
        'status': 'En Evaluación ASEA',
        'status_code': 'under_review',
        'precision_level': 'geocoded_approximate',
        'precision_label': '[APROXIMADO]',
        'clave_asea': '14JA2025G0073',
        'fuente_coordenadas': 'Geocodificación dirección: Av. de las Agujas 450, Zapopan',
        'geometry': circle_polygon(cosala_zapopan[0], cosala_zapopan[1], 100)
    }
]

# Consolidar
all_rows = saguaro_rows + amigo_rows + vista_rows + cosala_rows
gdf_all = gpd.GeoDataFrame(all_rows, crs="EPSG:4326")

# Guardar GeoJSON y GeoPackage en ambas ubicaciones
geojson_research = os.path.join(RESEARCH_DIR, 'terminales_gnl_v3.geojson')
gpkg_research = os.path.join(RESEARCH_DIR, 'terminales_gnl_v3.gpkg')
geojson_dash = os.path.join(DASHBOARD_DATA_DIR, 'terminales_gnl_v3.geojson')
gpkg_dash = os.path.join(DASHBOARD_DATA_DIR, 'terminales_gnl_v3.gpkg')

gdf_all.to_file(geojson_research, driver='GeoJSON')
gdf_all.to_file(gpkg_research, driver='GPKG')
gdf_all.to_file(geojson_dash, driver='GeoJSON')
gdf_all.to_file(gpkg_dash, driver='GPKG')

print(f"✅ Generados {len(gdf_all)} features vectoriales:")
print(f"   GeoJSON: {geojson_dash}")
print(f"   GeoPackage: {gpkg_dash}")

# ============================================================
# 3. EXTRAER Y OPTIMIZAR IMÁGENES/PLANOS DE LAS MIAS
# ============================================================
print("\n" + "=" * 60)
print("EXTRAYENDO PLANOS E IMÁGENES DE LAS MIAS")
print("=" * 60)

manifest = []

def copy_or_save_image(src_path, dest_dir, filename):
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)
    shutil.copy2(src_path, dest_path)
    return f"/assets/mias/{os.path.basename(dest_dir)}/{filename}"

# Copiar imágenes renderizadas existentes en gnl_research
copy_map = [
    # Saguaro
    ('Saguaro_page_019.png', 'saguaro', 'saguaro_p19_macro.png', 'Mapa de Macrolocalización y Áreas Temporales', 'macrolocalizacion', 'Saguaro_M-09_MGA0107.pdf', 19),
    ('Saguaro_page_020.png', 'saguaro', 'saguaro_p20_t1_t2.png', 'Tabla II.5 y II.6 Coordenadas T1 y T2', 'tabla_coordenadas', 'Saguaro_M-09_MGA0107.pdf', 20),
    ('crop_p20_T1.png', 'saguaro', 'saguaro_crop_t1.png', 'Croquis de Polígono T1 (17 Vértices)', 'distribucion_planta', 'Saguaro_M-09_MGA0107.pdf', 20),
    ('crop_p20_T2.png', 'saguaro', 'saguaro_crop_t2.png', 'Croquis de Polígono T2 (29 Vértices)', 'distribucion_planta', 'Saguaro_M-09_MGA0107.pdf', 20),
    ('crop_p21_reserva.png', 'saguaro', 'saguaro_crop_reserva.png', 'Área de Reserva para Conservación', 'ambiental', 'Saguaro_M-09_MGA0107.pdf', 21),
    ('crop_p21_campamentos.png', 'saguaro', 'saguaro_crop_campamentos.png', 'Campamentos Habitacionales', 'distribucion_planta', 'Saguaro_M-09_MGA0107.pdf', 21),

    # Amigo LNG
    ('Amigo_page_002.png', 'amigo', 'amigo_p02_caratula.png', 'Resumen Ejecutivo y Ubicación Guaymas', 'macrolocalizacion', 'Amigo_ER_26SO2025G0143.pdf', 2),
    ('Amigo_page_075.png', 'amigo', 'amigo_p75_layout.png', 'Esquema General de Terminal Licuefacción', 'distribucion_planta', 'Amigo_ER_26SO2025G0143.pdf', 75),
    ('Amigo_page_080.png', 'amigo', 'amigo_p80_sitio.png', 'Plano de Macrolocalización Guaymas', 'macrolocalizacion', 'Amigo_ER_26SO2025G0143.pdf', 80),

    # Vista Pacífico
    ('Vista_Pacifico_page_090.png', 'vista_pacifico', 'vista_p90_instrumentacion.png', 'Diagrama de Instalaciones FLNG', 'distribucion_planta', 'Vista_Pacifico_ER_25SI2024G0038.pdf', 90),
    ('Vista_Pacifico_page_092.png', 'vista_pacifico', 'vista_p92_tabla.png', 'Tabla V.1 Especificación FLNG y Jetty', 'tabla_coordenadas', 'Vista_Pacifico_ER_25SI2024G0038.pdf', 92),
    ('crop_vista_p23_table.png', 'vista_pacifico', 'vista_crop_p23.png', 'Coordenadas Marinas FLNG 2.228 km', 'microlocalizacion', 'Vista_Pacifico_ER_25SI2024G0038.pdf', 23),
    ('crop_vista_p25_table.png', 'vista_pacifico', 'vista_crop_p25.png', 'Polígono Terrestre ASIPONA Topolobampo', 'microlocalizacion', 'Vista_Pacifico_ER_25SI2024G0038.pdf', 25),

    # Cosalá
    ('Gaceta_28-2025.pdf', 'cosala', 'cosala_gaceta28.png', 'Publicación Gaceta ASEA 28-2025 (Mazatlán y Zapopan)', 'macrolocalizacion', 'Gaceta_28-2025.pdf', 1)
]

for src_name, proj_dir, target_name, title, cat, fuente_pdf, pag in copy_map:
    src_file = os.path.join(RESEARCH_DIR, src_name)
    if os.path.exists(src_file) and src_name.endswith('.png'):
        dest_folder = os.path.join(DASHBOARD_ASSETS_DIR, proj_dir)
        rel_url = copy_or_save_image(src_file, dest_folder, target_name)
        manifest.append({
            'id': f"{proj_dir}_{target_name.split('.')[0]}",
            'proyecto': proj_dir,
            'titulo': title,
            'tipo_plano': cat,
            'url': rel_url,
            'fuente_pdf': fuente_pdf,
            'pagina': pag
        })
        print(f"  [OK] Copiado asset: {rel_url}")

# Extraer imágenes adicionales embebidas en PDFs usando PyMuPDF
pdf_sources = [
    ('Saguaro_M-09_MGA0107.pdf', 'saguaro', [19, 20, 21, 22, 23]),
    ('Amigo_ER_26SO2025G0143.pdf', 'amigo', [2, 20, 75, 80]),
    ('Vista_Pacifico_ER_25SI2024G0038.pdf', 'vista_pacifico', [23, 25, 100, 101, 102])
]

for pdf_name, proj_key, pages in pdf_sources:
    pdf_path = os.path.join(RESEARCH_DIR, pdf_name)
    if not os.path.exists(pdf_path):
        continue
    doc = fitz.open(pdf_path)
    dest_folder = os.path.join(DASHBOARD_ASSETS_DIR, proj_key)
    for page_num in pages:
        if page_num - 1 >= len(doc):
            continue
        page = doc[page_num - 1]
        image_list = page.get_images(full=True)
        for img_idx, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            if len(image_bytes) < 15000:  # Filtrar iconos y gráficos pequeños
                continue
            out_filename = f"{proj_key}_p{page_num}_img{img_idx+1}.{image_ext}"
            out_filepath = os.path.join(dest_folder, out_filename)
            with open(out_filepath, "wb") as f:
                f.write(image_bytes)
            rel_url = f"/assets/mias/{proj_key}/{out_filename}"
            manifest.append({
                'id': f"{proj_key}_p{page_num}_img{img_idx+1}",
                'proyecto': proj_key,
                'titulo': f"Plano/Diagrama Extraído de MIA pág. {page_num}",
                'tipo_plano': 'distribucion_planta' if img_idx > 0 else 'macrolocalizacion',
                'url': rel_url,
                'fuente_pdf': pdf_name,
                'pagina': page_num
            })
            print(f"  [PDF Extraído] {rel_url}")

# Guardar manifest.json
manifest_path = os.path.join(DASHBOARD_ASSETS_DIR, 'manifest.json')
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"\n✅ Catálogo manifest.json generado con {len(manifest)} ítems:")
print(f"   Ruta: {manifest_path}")
print("=" * 60)
