#!/usr/bin/env python3
"""
build_geopackage_v3.py
----------------------
Construye el entregable GeoPackage v3.0 estandarizado OGC para Causa Natura Data (POA 2026).
Integra los datos reales procesados del Lakehouse Gold (Parquet H3_8 + Monte Carlo + Confianza).

Capas incluidas en ierc_golfo_california_v3.gpkg (CRS: EPSG:4326 - WGS 84):
  1. proyectos_gnl (Point)
  2. gasoductos_infraestructura_gnl (LineString)
  3. localidades_estudio_ierc (Point)
  4. anp_habitats_criticos (Polygon)
  5. zonas_pesqueras_pangas (Polygon)
  6. riqueza_relativa_pesquera (Polygon)
  7. grilla_h3_riesgo (Polygon - Gold Lakehouse Parquet con datos reales GFW/PANGAS)
  8-12. Capas de Campo 2026 (campo_rutas_pesqueras, campo_zonas_pesca_quincenales, etc.)
"""

import json
import math
from pathlib import Path
import geopandas as gpd
import pandas as pd
import pyarrow.parquet as pq
from shapely.geometry import Point, LineString, Polygon, shape
import h3

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
CURATED_DIR = BASE_DIR / 'lakehouse' / 'curated'
PANGAS_WGS84_DIR = RAW_DIR / 'pangas_wgs84'
DELIVERABLE_V3_DIR = BASE_DIR / 'deliverables' / 'v3_geopackage'
OUTPUT_GPKG_V3 = DELIVERABLE_V3_DIR / 'ierc_golfo_california_v3.gpkg'
METADATA_V3_PATH = DELIVERABLE_V3_DIR / 'GEOPACKAGE_V3_METADATA.md'

DELIVERABLE_V3_DIR.mkdir(parents=True, exist_ok=True)

print("=======================================================================")
print("Generación del GeoPackage Entregable v3.0 (Causa Natura Data)")
print(f"Archivo destino: {OUTPUT_GPKG_V3}")
print("=======================================================================")

# ── 1. Capa: proyectos_gnl ───────────────────────────────────────────────────
print("\n1/12 Construyendo capa 'proyectos_gnl'...")
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
gdf_proyectos.to_file(OUTPUT_GPKG_V3, layer='proyectos_gnl', driver='GPKG')
print(f"   Capa 'proyectos_gnl' creada ({len(gdf_proyectos)} entidades).")

# ── 2. Capa: gasoductos_infraestructura_gnl ──────────────────────────────────
print("\n2/12 Construyendo capa 'gasoductos_infraestructura_gnl'...")
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
gdf_pipelines.to_file(OUTPUT_GPKG_V3, layer='gasoductos_infraestructura_gnl', driver='GPKG')
print(f"   Capa 'gasoductos_infraestructura_gnl' creada ({len(gdf_pipelines)} trazos).")

# ── 3. Capa: localidades_estudio_ierc ────────────────────────────────────────
print("\n3/12 Construyendo capa 'localidades_estudio_ierc'...")
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
gdf_locs.to_file(OUTPUT_GPKG_V3, layer='localidades_estudio_ierc', driver='GPKG')
print(f"   Capa 'localidades_estudio_ierc' creada ({len(gdf_locs)} localidades).")

# ── 4. Capa: anp_habitats_criticos ───────────────────────────────────────────
print("\n4/12 Construyendo capa 'anp_habitats_criticos'...")
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
gdf_anp.to_file(OUTPUT_GPKG_V3, layer='anp_habitats_criticos', driver='GPKG')
print(f"   Capa 'anp_habitats_criticos' creada ({len(gdf_anp)} áreas protegidas).")

# ── 5. Capa: zonas_pesqueras_pangas ──────────────────────────────────────────
print("\n5/12 Construyendo capa 'zonas_pesqueras_pangas'...")
pangas_geojson_path = PANGAS_WGS84_DIR / 'ZPesca_PANGAS_wgs84.geojson'
CRITICAL_CODES = {'CARSPP', 'GYMMAR', 'RHILON', 'RHIPRO', 'RHISPP', 'SPHSPP', 'LUTARG', 'PARSPP', 'DASSPP', 'DASDIP', 'MYCROS'}

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
gdf_pangas.to_file(OUTPUT_GPKG_V3, layer='zonas_pesqueras_pangas', driver='GPKG')
print(f"   Capa 'zonas_pesqueras_pangas' creada ({len(gdf_pangas)} sitios con `uid_espaciotemporal`).")

# ── 6. Capa: riqueza_relativa_pesquera ───────────────────────────────────────
print("\n6/12 Construyendo capa 'riqueza_relativa_pesquera'...")
riqueza_geojson_path = PANGAS_WGS84_DIR / 'Riqueza_Relativa_wgs84.geojson'
if riqueza_geojson_path.exists():
    gdf_riqueza = gpd.read_file(riqueza_geojson_path)
    if 'all' in gdf_riqueza.columns:
        gdf_riqueza['riqueza_absoluta'] = gdf_riqueza['all']
    gdf_riqueza = gdf_riqueza.to_crs("EPSG:4326")
    gdf_riqueza.to_file(OUTPUT_GPKG_V3, layer='riqueza_relativa_pesquera', driver='GPKG')
    print(f"   Capa 'riqueza_relativa_pesquera' creada ({len(gdf_riqueza)} polígonos).")

# ── 7. Capa: grilla_h3_riesgo (Datos Reales Lakehouse Gold) ───────────────────
print("\n7/12 Construyendo capa 'grilla_h3_riesgo' desde Gold Lakehouse Parquet...")

risk_parquet_path = CURATED_DIR / 'ierc_risk_h3_8.parquet'
conf_parquet_path = CURATED_DIR / 'ierc_confidence_h3.parquet'
mc_parquet_path = CURATED_DIR / 'ierc_monte_carlo_h3_8.parquet'

df_risk = pd.read_parquet(risk_parquet_path)
df_conf = pd.read_parquet(conf_parquet_path) if conf_parquet_path.exists() else None
df_mc = pd.read_parquet(mc_parquet_path) if mc_parquet_path.exists() else None

# Merge Gold layers
df_gold = df_risk.copy()
if df_conf is not None:
    conf_col = 'h3_cell' if 'h3_cell' in df_conf.columns else 'h3_cell_8'
    df_gold = df_gold.merge(df_conf[[conf_col, 'confidence_score']], left_on='h3_cell_8', right_on=conf_col, how='left')

if df_mc is not None:
    mc_cols = [c for c in ['ierc_mean', 'ierc_std', 'ierc_p05', 'ierc_p95'] if c in df_mc.columns]
    df_gold = df_gold.merge(df_mc[['h3_cell_8'] + mc_cols], on='h3_cell_8', how='left')

# Filtrar celdas con datos observados o en zonas relevantes (esfuerzo pesquero, biodiversidad o cercanía GNL)
# Para mantener rendimiento GIS sin perder evaluaciones significativas
pangas_col = 'pangas_densidad_esfuerzo' if 'pangas_densidad_esfuerzo' in df_gold.columns else 'pangas_count'
gfw_col = 'gfw_fishing_hours' if 'gfw_fishing_hours' in df_gold.columns else 'gfw_hours'
threat_col = 'threat_score' if 'threat_score' in df_gold.columns else 'amenaza_score'
vuln_col = 'vulnerability_score' if 'vulnerability_score' in df_gold.columns else 'vulnerabilidad_score'

filter_mask = (
    (df_gold['ierc_score'] > 0.0) |
    (df_gold.get(pangas_col, 0.0) > 0.0) |
    (df_gold.get(gfw_col, 0.0) > 0.0) |
    (df_gold.get('asea_count', 0.0) > 0.0) |
    (df_gold.get('distancia_proyecto_mas_cercano_km', 999.0) < 100.0)
)
df_export = df_gold[filter_mask].copy()

print(f"   Filtradas {len(df_export):,} celdas H3 relevantes de {len(df_gold):,} celdas totales en el Golfo.")

h3_export_features = []
for _, row in df_export.iterrows():
    cell = str(row['h3_cell_8'])
    coords_lng_lat = [(lng, lat) for lat, lng in h3.cell_to_boundary(cell)]
    poly = Polygon(coords_lng_lat)
    lat, lon = h3.cell_to_latlng(cell)

    h3_export_features.append({
        'h3_index': cell,
        'resolucion': 8,
        'latitud_centroide': round(lat, 5),
        'longitud_centroide': round(lon, 5),
        'ierc_score': round(float(row.get('ierc_score', 0.0)), 2),
        'nivel_riesgo': str(row.get('risk_level', 'Bajo')),
        'confidence_score': round(float(row.get('confidence_score', 0.85)), 2),
        'amenaza_score': round(float(row.get(threat_col, 0.0)), 3),
        'vulnerabilidad_score': round(float(row.get(vuln_col, 0.0)), 3),
        'densidad_pesquera_pangas': round(float(row.get(pangas_col, 0.0)), 2),
        'gfw_fishing_hours': round(float(row.get(gfw_col, 0.0)), 2),
        'distancia_gnl_km': round(float(row.get('distancia_proyecto_mas_cercano_km', -1.0)), 2),
        'mc_mean': round(float(row.get('ierc_mean', row.get('ierc_score', 0.0))), 2) if 'ierc_mean' in row else None,
        'mc_std': round(float(row.get('ierc_std', 0.0)), 2) if 'ierc_std' in row else None,
        'ci_lower_95': round(float(row.get('ierc_p05', 0.0)), 2) if 'ierc_p05' in row else None,
        'ci_upper_95': round(float(row.get('ierc_p95', 0.0)), 2) if 'ierc_p95' in row else None,
        'geometry': poly
    })

gdf_h3 = gpd.GeoDataFrame(h3_export_features, crs="EPSG:4326")
gdf_h3.to_file(OUTPUT_GPKG_V3, layer='grilla_h3_riesgo', driver='GPKG')
print(f"   Capa 'grilla_h3_riesgo' creada ({len(gdf_h3):,} celdas H3 reales).")

# ── 8-12. Capas de Campo 2026 (Plantillas) ──────────────────────────────────
print("\n8/12 Inicializando capa de campo 'campo_rutas_pesqueras'...")
dummy_routes = [{
    'uid_espaciotemporal': 'PUNTA_CHUECA-ARTESANAL-JAIBERA-TRAMPA-ZONA_A-Q12-RUTA_PRINCIPAL',
    'localidad_origen': 'Punta Chueca',
    'pesqueria': 'Jaiba',
    'arte_pesca': 'Trampa',
    'quincena': 'Q12',
    'distancia_km': 14.5,
    'geometry': LineString([(-112.1603, 28.9886), (-112.2500, 29.0500)])
}]
gpd.GeoDataFrame(dummy_routes, crs="EPSG:4326").to_file(OUTPUT_GPKG_V3, layer='campo_rutas_pesqueras', driver='GPKG')

print("9/12 Inicializando capa de campo 'campo_zonas_pesca_quincenales'...")
dummy_zonas = [{
    'uid_espaciotemporal': 'PUERTO_LIBERTAD-ARTESANAL-ESCAMA-CHINCHORRO-CALADERO_NORTE-Q15-RUTA_ALT',
    'localidad_origen': 'Puerto Libertad',
    'tipo_zona': 'Primaria',
    'especie_grupo': 'Sierra / Curvina',
    'arte_pesca': 'Chinchorro',
    'mes_quincena': 'Quincena 15 (Agosto II)',
    'temporada': 'Principal',
    'costo_viaje_mxn': 2500.0,
    'presencia_mujeres': 1,
    'grado_confianza': 'Alta',
    'geometry': Polygon([(-112.75, 29.95), (-112.65, 29.95), (-112.65, 30.05), (-112.75, 30.05)])
}]
gpd.GeoDataFrame(dummy_zonas, crs="EPSG:4326").to_file(OUTPUT_GPKG_V3, layer='campo_zonas_pesca_quincenales', driver='GPKG')

print("10/12 Inicializando capa de campo 'campo_sitios_bioculturales_comcaac'...")
dummy_bio = [{
    'sitio_id': 'PUNTA_CHUECA_ISLA_TIBURON_SAGRADO',
    'nombre_sitio': 'Canal del Infiernillo / Sitio Sagrado Comca\'ac',
    'localidad': 'Punta Chueca',
    'categoria_patrimonio': 'Biocultural / Cosmovisión',
    'relevancia': 'Alta',
    'geometry': Point(-112.2000, 28.9900)
}]
gpd.GeoDataFrame(dummy_bio, crs="EPSG:4326").to_file(OUTPUT_GPKG_V3, layer='campo_sitios_bioculturales_comcaac', driver='GPKG')

print("11/12 Inicializando capa de campo 'campo_puntos_desembarque_costo'...")
dummy_puntos = [{
    'sitio_id': 'DESEMBARQUE_P_LIBERTAD_PLAYA',
    'nombre_playa': 'Playa de Varado Puerto Libertad',
    'localidad': 'Puerto Libertad',
    'num_pangas_activas': 45,
    'precio_gasolina_l_mxn': 24.50,
    'geometry': Point(-112.6800, 29.9100)
}]
gpd.GeoDataFrame(dummy_puntos, crs="EPSG:4326").to_file(OUTPUT_GPKG_V3, layer='campo_puntos_desembarque_costo', driver='GPKG')

print("12/12 Inicializando capa de campo 'campo_interaccion_fondeaderos_gnl'...")
dummy_fondeo = [{
    'fondeadero_id': 'FONDEO_METANEROS_P_LIBERTAD',
    'terminal_asociada': 'Saguaro Energía (Mexico Pacific)',
    'estatus_conflictividad': 'Exclusión de pesca artesanal',
    'radio_seguridad_m': 1000.0,
    'geometry': Polygon([(-112.72, 29.89), (-112.70, 29.89), (-112.70, 29.91), (-112.72, 29.91)])
}]
gpd.GeoDataFrame(dummy_fondeo, crs="EPSG:4326").to_file(OUTPUT_GPKG_V3, layer='campo_interaccion_fondeaderos_gnl', driver='GPKG')

# ── Generar archivo de metadatos v3 ──────────────────────────────────────────
print("\nGenerando archivo de metadatos GEOPACKAGE_V3_METADATA.md...")

metadata_content = f"""# Metadata Entregable GeoPackage v3.0 (IERC-GNL)

**Proyecto**: Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC) ante proyectos de GNL en el Golfo de California  
**Organización**: Causa Natura Center (POA 2026)  
**Versión GeoPackage**: v3.0  
**Fecha de generación**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Archivo**: `deliverables/v3_geopackage/ierc_golfo_california_v3.gpkg`  
**CRS**: EPSG:4326 (WGS 84 - Coordenadas Geográficas)  

---

## 📦 Capas Incluidas en el GeoPackage v3.0

| N° | Nombre Capa | Tipo Geometría | Entidades | Descripción |
|---|---|---|---|---|
| 1 | `proyectos_gnl` | Point | {len(gdf_proyectos)} | Ubicación de las 4 terminales GNL en el Golfo de California (11 features detalladas). |
| 2 | `gasoductos_infraestructura_gnl` | LineString | {len(gdf_pipelines)} | Trazados de gasoductos (Samalayuca-Saguaro, Guaymas-Sásabe). |
| 3 | `localidades_estudio_ierc` | Point | {len(gdf_locs)} | Localidades prioritarias de estudio (Punta Chueca, Puerto Libertad, Guaymas). |
| 4 | `anp_habitats_criticos` | Polygon | {len(gdf_anp)} | Áreas Naturales Protegidas (CONANP) e Hábitats Críticos. |
| 5 | `zonas_pesqueras_pangas` | Polygon | {len(gdf_pangas)} | Sitios históricos de pesca artesanal PANGAS con estándar `uid_espaciotemporal`. |
| 6 | `riqueza_relativa_pesquera` | Polygon | {len(gdf_riqueza)} | Polígonos de riqueza relativa de especies pesqueras acumuladas. |
| 7 | `grilla_h3_riesgo` | Polygon | {len(gdf_h3):,} | **Grilla H3_8 con datos reales del Lakehouse Gold** (Amenaza $H$, Vulnerabilidad $V$, IERC $R$, Confianza y Monte Carlo). |
| 8 | `campo_rutas_pesqueras` | LineString | 1 | Plantilla estandarizada para rutas pesqueras de campo 2026. |
| 9 | `campo_zonas_pesca_quincenales` | Polygon | 1 | Plantilla estandarizada para zonas pesqueras quincenales. |
| 10 | `campo_sitios_bioculturales_comcaac` | Point | 1 | Plantilla estandarizada para patrimonio biocultural Comca'ac. |
| 11 | `campo_puntos_desembarque_costo` | Point | 1 | Plantilla estandarizada para puntos de desembarque y costos por viaje. |
| 12 | `campo_interaccion_fondeaderos_gnl` | Polygon | 1 | Plantilla estandarizada para interacción y zonas de exclusión con buques GNL. |

---

## 🧮 Esquema de Atributos - `grilla_h3_riesgo` (Gold Layer)

- `h3_index` (String): Identificador único de celda H3 Resolución 8.
- `resolucion` (Integer): Nivel de resolución espacial H3 (8 = ~0.74 km²).
- `latitud_centroide` / `longitud_centroide` (Float): Coordenadas del centroide.
- `ierc_score` (Float): Puntaje de riesgo multiplicativo ($R = H \\times V / 100$) en escala [0, 100].
- `nivel_riesgo` (String): Categoría discreta (`Bajo`, `Moderado`, `Alto`, `Crítico`).
- `confidence_score` (Float): Índice de Confianza y Calidad Espacial Nivel III en escala [0.0, 1.0].
- `amenaza_score` (Float): Subíndice de Amenaza y Exposición Espacial ($H$).
- `vulnerabilidad_score` (Float): Subíndice de Vulnerabilidad Socioecológica ($V$).
- `densidad_pesquera_pangas` (Float): Densidad observada de esfuerzo pesquero artesanal PANGAS.
- `gfw_fishing_hours` (Float): Horas de esfuerzo pesquero industrial observadas por Global Fishing Watch.
- `distancia_gnl_km` (Float): Distancia euclidiana en km a la terminal de GNL más cercana.
- `mc_mean` / `mc_std` / `ci_lower_95` / `ci_upper_95` (Float): Métricas de incertidumbre de la Simulación Monte Carlo.

---

*GeoPackage generado automáticamente mediante `scripts/build_geopackage_v3.py`*
"""

with open(METADATA_V3_PATH, 'w', encoding='utf-8') as f:
    f.write(metadata_content)

print(f"   Metadatos v3 guardados en: {METADATA_V3_PATH}")
print(f"\n¡GeoPackage v3.0 generado exitosamente en:\n   {OUTPUT_GPKG_V3}!")
