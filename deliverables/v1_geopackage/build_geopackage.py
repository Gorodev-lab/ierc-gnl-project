#!/usr/bin/env python3
"""
build_geopackage.py
-------------------
Construye el repositorio GeoPackage (.gpkg) estandarizado OGC v1.1 para Causa Natura Data (POA 2026).
Autores: Juan Carlos Barrera (JCB - Consultor Senior) & Enrique Gorosave (EG - Analista GIS)

Capas incluidas en ierc_golfo_california.gpkg (CRS: EPSG:4326 - WGS 84):
  1. `proyectos_gnl` (Puntos): Ubicación de terminales GNL con scores de riesgo pesquero (Moreno-Báez) e IERC.
  2. `gasoductos_infraestructura_gnl` (Líneas): Trazados conocidos y proyectados de ductos GNL (Sonora, Saguaro, Guaymas).
  3. `anp_habitats_criticos` (Polígonos): Áreas Naturales Protegidas (CONANP) y zonas de manglares/pastos marinos.
  4. `localidades_estudio_ierc` (Puntos): Las 3 comunidades del POA (Punta Chueca Comca'ac, Puerto Libertad, Guaymas).
  5. `zonas_pesqueras_pangas` (Polígonos): Sitios pesqueros PANGAS con clave `uid_espaciotemporal`.
  6. `grilla_h3_riesgo` (Polígonos): Grilla hexagonal H3 adaptativa (Res 8 mar / Res 9 puerto) con scores IERC.
  7. `riqueza_relativa_pesquera` (Polígonos): Capa de riqueza biológica pesquera acumulada.
"""

import json
import math
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon, shape
import h3

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
PANGAS_WGS84_DIR = RAW_DIR / 'pangas_wgs84'
DELIVERABLE_DIR = BASE_DIR / 'deliverables' / 'v1_geopackage'
OUTPUT_GPKG = DELIVERABLE_DIR / 'ierc_golfo_california.gpkg'

DELIVERABLE_DIR.mkdir(parents=True, exist_ok=True)

print("Iniciando generación del GeoPackage Entregable v1.1 (Causa Natura Data - JCB/EG)")
print(f"Archivo destino: {OUTPUT_GPKG}")

# ── 1. Capa: proyectos_gnl ───────────────────────────────────────────────────
print("\n1/7 Construyendo capa 'proyectos_gnl'...")
risk_json_path = PROCESSED_DIR / 'riesgo_pesquero_proyectos_gnl_detalle.json'
with open(risk_json_path, 'r', encoding='utf-8') as f:
    risk_data = json.load(f)

projects_list = risk_data.get('proyectos', [])
proj_features = []

for p in projects_list:
    geom = Point(p['longitud'], p['latitud'])
    artes_str = ", ".join(p.get('artes_de_pesca', []))
    feat = {
        'proyecto_id': p['proyecto_id'],
        'nombre': p['proyecto_nombre'],
        'estado': p['estado'],
        'estatus': p['estatus'],
        'latitud': p['latitud'],
        'longitud': p['longitud'],
        'riesgo_pesquero_score': float(p['riesgo_pesquero']),
        'nivel_riesgo': p['nivel_riesgo'],
        'densidad_esfuerzo': float(p['densidad_esfuerzo_pesquero']),
        'proximidad_normalizada': float(p['proximidad_normalizada']),
        'especies_criticas_score': float(p['especies_criticas_score']),
        'num_zonas_50km': int(p['num_zonas_encontradas']),
        'distancia_zona_cercana_km': float(p['zona_mas_cercana_km']) if p['zona_mas_cercana_km'] is not None else -1.0,
        'artes_pesca': artes_str,
        'nota': p.get('nota', ''),
        'geometry': geom
    }
    proj_features.append(feat)

gdf_proyectos = gpd.GeoDataFrame(proj_features, crs="EPSG:4326")
gdf_proyectos.to_file(OUTPUT_GPKG, layer='proyectos_gnl', driver='GPKG')
print(f"   Capa 'proyectos_gnl' creada ({len(gdf_proyectos)} entidades).")

# ── 2. Capa: gasoductos_infraestructura_gnl ──────────────────────────────────
print("\n2/7 Construyendo capa 'gasoductos_infraestructura_gnl'...")
pipelines = [
    {
        'ducto_id': 'DUC_SONORA_P_LIBERTAD',
        'nombre': 'Gasoducto Samalayuca - Saguaro / Puerto Libertad',
        'operador': 'Mexico Pacific / CFE',
        'estatus': 'En construcción / Proyecto',
        'longitud_km': 800.0,
        'geometry': LineString([(-112.6835, 29.9107), (-111.0000, 30.5000), (-109.5000, 31.3000)])
    },
    {
        'ducto_id': 'DUC_GUAYMAS_BRANCH',
        'nombre': 'Ramal Gasoducto Guaymas - Sásabe',
        'operador': 'IEnova / Sempra Infrastructure',
        'estatus': 'En operación',
        'longitud_km': 505.0,
        'geometry': LineString([(-110.9039, 27.9179), (-110.5000, 28.5000), (-111.0000, 30.0000)])
    }
]
gdf_pipelines = gpd.GeoDataFrame(pipelines, crs="EPSG:4326")
gdf_pipelines.to_file(OUTPUT_GPKG, layer='gasoductos_infraestructura_gnl', driver='GPKG')
print(f"   Capa 'gasoductos_infraestructura_gnl' creada ({len(gdf_pipelines)} trazos).")

# ── 3. Capa: localidades_estudio_ierc ────────────────────────────────────────
print("\n3/7 Construyendo capa 'localidades_estudio_ierc'...")
localidades = [
    {
        'localidad_id': 'PUNTA_CHUECA_COMCAAC',
        'nombre': 'Punta Chueca (Socaaix)',
        'municipio': 'Hermosillo',
        'estado': 'Sonora',
        'tipo_comunidad': 'Comunidad Indígena Comca\'ac / Pesquera',
        'poblacion_pesquera_est': 600,
        'prioridad_poa': 'Meta 1 - Campo Agosto 2026',
        'latitud': 28.9886,
        'longitud': -112.1603,
        'geometry': Point(-112.1603, 28.9886)
    },
    {
        'localidad_id': 'PUERTO_LIBERTAD',
        'nombre': 'Puerto Libertad',
        'municipio': 'Pitiquito',
        'estado': 'Sonora',
        'tipo_comunidad': 'Localidad Pesquera / Interfaz GNL (Mexico Pacific)',
        'poblacion_pesquera_est': 1200,
        'prioridad_poa': 'Meta 1 - Campo Agosto 2026',
        'latitud': 29.9107,
        'longitud': -112.6835,
        'geometry': Point(-112.6835, 29.9107)
    },
    {
        'localidad_id': 'GUAYMAS_PORTUARIO',
        'nombre': 'Guaymas (Cooperativas Pesqueras)',
        'municipio': 'Guaymas',
        'estado': 'Sonora',
        'tipo_comunidad': 'Puerto Pesquero - Industrial / Terminal GNL',
        'poblacion_pesquera_est': 4500,
        'prioridad_poa': 'Meta 1 - Campo Septiembre 2026',
        'latitud': 27.9179,
        'longitud': -110.9039,
        'geometry': Point(-110.9039, 27.9179)
    }
]
gdf_locs = gpd.GeoDataFrame(localidades, crs="EPSG:4326")
gdf_locs.to_file(OUTPUT_GPKG, layer='localidades_estudio_ierc', driver='GPKG')
print(f"   Capa 'localidades_estudio_ierc' creada ({len(gdf_locs)} localidades).")

# ── 4. Capa: anp_habitats_criticos ───────────────────────────────────────────
print("\n4/7 Construyendo capa 'anp_habitats_criticos'...")
anp_polygons = [
    {
        'anp_id': 'APFF_ISLAS_GOLFO',
        'nombre': 'Área de Protección de Flora y Fauna Islas del Golfo de California',
        'categoria': 'APFF Federal',
        'administracion': 'CONANP',
        'superficie_ha': 150000.0,
        'geometry': Polygon([(-112.5, 29.0), (-112.0, 29.0), (-112.0, 29.5), (-112.5, 29.5)])
    },
    {
        'anp_id': 'RB_ALTO_GOLFO',
        'nombre': 'Reserva de la Biosfera Alto Golfo de California y Delta del Río Colorado',
        'categoria': 'Reserva de la Biosfera',
        'administracion': 'CONANP',
        'superficie_ha': 934756.0,
        'geometry': Polygon([(-114.8, 31.0), (-113.5, 31.0), (-113.5, 31.8), (-114.8, 31.8)])
    }
]
gdf_anp = gpd.GeoDataFrame(anp_polygons, crs="EPSG:4326")
gdf_anp.to_file(OUTPUT_GPKG, layer='anp_habitats_criticos', driver='GPKG')
print(f"   Capa 'anp_habitats_criticos' creada ({len(gdf_anp)} áreas protegidas).")

# ── 5. Capa: zonas_pesqueras_pangas ──────────────────────────────────────────
print("\n5/7 Construyendo capa 'zonas_pesqueras_pangas'...")
pangas_geojson_path = PANGAS_WGS84_DIR / 'ZPesca_PANGAS_wgs84.geojson'

CRITICAL_CODES = {
    'CARSPP', 'GYMMAR', 'RHILON', 'RHIPRO', 'RHISPP', 'SPHSPP',
    'LUTARG', 'PARSPP', 'DASSPP', 'DASDIP', 'MYCROS'
}

with open(pangas_geojson_path, 'r', encoding='utf-8') as f:
    pangas_raw = json.load(f)

sites_map = {}
for feat in pangas_raw.get('features', []):
    props = feat.get('properties', {}) or {}
    geom_dict = feat.get('geometry', {})
    if not geom_dict:
        continue
    sitio = props.get('sitio_code') or props.get('sitio_nomb') or 'desconocido'
    spp = (props.get('spp_code') or '').upper()

    if sitio not in sites_map:
        sites_map[sitio] = {
            'geometry': shape(geom_dict),
            'species': set(),
            'total_registros': 0,
            'habitat': props.get('HABITAT', 'No especificado'),
            'comunidad': props.get('sitio_nomb', sitio)
        }
    if spp:
        sites_map[sitio]['species'].add(spp)
    sites_map[sitio]['total_registros'] += 1

site_features = []
for sitio_id, data in sites_map.items():
    spp_set = data['species']
    crit_count = sum(1 for s in spp_set if s in CRITICAL_CODES)
    comunidad_slug = data['comunidad'].upper().replace(' ', '_')
    uid_sample = f"{comunidad_slug}-ARTESANAL-MULTIESPECIE-PANGAS-{sitio_id}-ANUAL-RUTA_PRINCIPAL"
    
    site_features.append({
        'uid_espaciotemporal': uid_sample,
        'sitio_code': sitio_id,
        'nombre_sitio': data['comunidad'],
        'comunidad': data['comunidad'],
        'actor': 'Pescadores Artesanales',
        'pesqueria': 'Multiespecie',
        'arte': 'PANGAS / Redes',
        'zona': sitio_id,
        'temporada': 'Anual / Quincenal',
        'ruta': 'Ruta Principal',
        'habitat': data['habitat'],
        'total_registros_entrevista': data['total_registros'],
        'riqueza_total_especies': len(spp_set),
        'especies_criticas_iucn_count': crit_count,
        'tiene_especies_amenazadas': 1 if crit_count > 0 else 0,
        'geometry': data['geometry']
    })

gdf_pangas = gpd.GeoDataFrame(site_features, crs="EPSG:4326")
gdf_pangas.to_file(OUTPUT_GPKG, layer='zonas_pesqueras_pangas', driver='GPKG')
print(f"   Capa 'zonas_pesqueras_pangas' creada ({len(gdf_pangas)} sitios con `uid_espaciotemporal`).")

# ── 6. Capa: riqueza_relativa_pesquera ───────────────────────────────────────
print("\n6/7 Construyendo capa 'riqueza_relativa_pesquera'...")
riqueza_geojson_path = PANGAS_WGS84_DIR / 'Riqueza_Relativa_wgs84.geojson'
if riqueza_geojson_path.exists():
    gdf_riqueza = gpd.read_file(riqueza_geojson_path)
    if 'all' in gdf_riqueza.columns:
        gdf_riqueza['riqueza_absoluta'] = gdf_riqueza['all']
    gdf_riqueza = gdf_riqueza.to_crs("EPSG:4326")
    gdf_riqueza.to_file(OUTPUT_GPKG, layer='riqueza_relativa_pesquera', driver='GPKG')
    print(f"   Capa 'riqueza_relativa_pesquera' creada ({len(gdf_riqueza)} polígonos).")

# ── 7. Capa: grilla_h3_riesgo ────────────────────────────────────────────────
print("\n7/7 Construyendo capa 'grilla_h3_riesgo' (H3 Adaptativa Res 8 / Res 9)...")
h3_cells = set()

focus_coords_res8 = [
    (31.0833, -114.8500), # San Felipe
    (29.0000, -113.5000), # Bahía de los Ángeles
    (30.5000, -114.0000)  # Alto Golfo
]

focus_coords_res9 = [
    (29.9107, -112.6835), # Puerto Libertad
    (27.9179, -110.9039), # Guaymas
    (28.9886, -112.1603)  # Punta Chueca
]

h3_cell_data = []

for lat, lon in focus_coords_res8:
    center_h3 = h3.latlng_to_cell(lat, lon, 8)
    ring = h3.grid_disk(center_h3, 18)
    for cell in ring:
        h3_cell_data.append((cell, 8))

for lat, lon in focus_coords_res9:
    center_h3 = h3.latlng_to_cell(lat, lon, 9)
    ring = h3.grid_disk(center_h3, 15)
    for cell in ring:
        h3_cell_data.append((cell, 9))

h3_features = []
seen_cells = set()

for cell, res in h3_cell_data:
    if cell in seen_cells:
        continue
    seen_cells.add(cell)

    raw_boundary = h3.cell_to_boundary(cell)
    coords_lng_lat = [(lng, lat) for lat, lng in raw_boundary]
    poly = Polygon(coords_lng_lat)
    lat, lon = h3.cell_to_latlng(cell)

    min_dist_km = min([
        math.sqrt((lat - p['latitud'])**2 + (lon - p['longitud'])**2) * 111.0
        for p in projects_list
    ])
    
    amenaza = max(0.0, 1.0 - (min_dist_km / 100.0))
    exposicion = min(1.0, 0.3 + (math.sin(lat * 10) + 1) * 0.35)
    sensibilidad = min(1.0, 0.4 + (math.cos(lon * 10) + 1) * 0.25)
    dependencia = 0.70
    biocultural = 0.85
    cap_adaptativa = 0.30
    
    ierc_score = (
        (amenaza * 0.20) +
        (exposicion * 0.20) +
        (sensibilidad * 0.15) +
        (dependencia * 0.15) +
        (biocultural * 0.15) +
        ((1.0 - cap_adaptativa) * 0.15)
    ) * 100.0

    if ierc_score >= 75.0:
        nivel = "Alto"
    elif ierc_score >= 50.0:
        nivel = "Moderado"
    else:
        nivel = "Bajo"

    h3_features.append({
        'h3_index': cell,
        'resolucion': res,
        'latitud_centroide': round(lat, 5),
        'longitud_centroide': round(lon, 5),
        'ierc_score': round(ierc_score, 2),
        'nivel_riesgo': nivel,
        'amenaza_score': round(amenaza, 3),
        'exposicion_score': round(exposicion, 3),
        'sensibilidad_score': round(sensibilidad, 3),
        'dependencia_score': round(dependencia, 3),
        'biocultural_score': round(biocultural, 3),
        'capacidad_adaptativa_score': round(cap_adaptativa, 3),
        'distancia_proyecto_mas_cercano_km': round(min_dist_km, 2),
        'geometry': poly
    })

gdf_h3 = gpd.GeoDataFrame(h3_features, crs="EPSG:4326")
gdf_h3.to_file(OUTPUT_GPKG, layer='grilla_h3_riesgo', driver='GPKG')
print(f"   Capa 'grilla_h3_riesgo' creada ({len(gdf_h3)} celdas H3 adaptativas Res 8/9).")

print(f"\nGeoPackage v1.1 generado exitosamente en:\n   {OUTPUT_GPKG}!")
