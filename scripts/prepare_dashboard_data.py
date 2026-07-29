#!/usr/bin/env python3
"""
Prepara los datos para el dashboard IERC-GNL.
- Copia el JSON de resultados procesados a public/data/
- Genera una muestra ligera del GeoJSON WGS84 de PANGAS (~500 zonas únicas)
El archivo PANGAS_wgs84 tiene filas de entrevistas con spp_code y sitio_code.
Agrupamos por sitio y contamos especies críticas.
"""

import json
import math
from pathlib import Path
from collections import defaultdict

BASE = Path('/home/gorops/ierc-gnl-project')
PANGAS_DIR = BASE / 'data/raw/pangas_wgs84'
PROCESSED_DIR = BASE / 'data/processed'
PUBLIC_DIR = BASE / 'dashboard/public/data'

PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

# ── 1. Copiar resultados de riesgo ──────────────────────────────────────────
src = PROCESSED_DIR / 'riesgo_pesquero_proyectos_gnl_detalle.json'
dst = PUBLIC_DIR / 'riesgo_proyectos.json'
with open(src) as f:
risk_data = json.load(f)
with open(dst, 'w') as f:
json.dump(risk_data, f, ensure_ascii=False, indent=2)
print(f" Copiado: {dst}")

# ── 2. Especies críticas ─────────────────────────────────────────────────────
CRITICAL_CODES = {
'CARSPP', 'GYMMAR', 'RHILON', 'RHIPRO', 'RHISPP', 'SPHSPP',
'LUTARG', 'PARSPP', 'DASSPP', 'DASDIP', 'MYCROS',
# También códigos en minúscula por si acaso
'carspp', 'gymmar', 'rhilon', 'rhipro', 'rhispp', 'sphspp',
'lutarg', 'parspp', 'dasspp', 'dasdip', 'mycros',
}

# ── 3. Cargar y agrupar ZPesca_PANGAS_wgs84 por sitio ──────────────────────
print("⏳ Procesando ZPesca_PANGAS_wgs84.geojson (registros de entrevista)…")
pangas_file = PANGAS_DIR / 'ZPesca_PANGAS_wgs84.geojson'

with open(pangas_file) as f:
gj = json.load(f)

all_features = gj.get('features', [])
print(f"   Total registros: {len(all_features)}")

# Agrupar por sitio_code: guardar geometría + conjunto de especies
sites: dict = {}  # sitio_code -> {geometry, species_set, record_count}

for feat in all_features:
props = feat.get('properties', {}) or {}
geom  = feat.get('geometry', {})
sitio = props.get('sitio_code') or props.get('sitio_nomb') or 'unknown'
spp   = (props.get('spp_code') or '').upper()

if sitio not in sites:
sites[sitio] = {
'geometry': geom,
'species': set(),
'count': 0,
'habitat': props.get('HABITAT', ''),
}
if spp:
sites[sitio]['species'].add(spp)
sites[sitio]['count'] += 1

print(f"   Sitios únicos: {len(sites)}")

# Convertir a features GeoJSON
sample_features = []
MAX_FEATURES = 500

# Ordenar sitios por número de especies críticas desc
def crit_count(site_data):
return len([s for s in site_data['species'] if s in CRITICAL_CODES])

sorted_sites = sorted(sites.items(), key=lambda x: (crit_count(x[1]), x[1]['count']), reverse=True)

for sitio_code, site_data in sorted_sites[:MAX_FEATURES]:
crit = crit_count(site_data)
sample_features.append({
'type': 'Feature',
'properties': {
'sitio': sitio_code,
'total_records': site_data['count'],
'critical_species': crit,
'all_species': len(site_data['species']),
'habitat': site_data['habitat'],
},
'geometry': site_data['geometry']
})

sample_geojson = {
'type': 'FeatureCollection',
'name': 'fish_zones_sample',
'features': sample_features
}

out_path = PUBLIC_DIR / 'fish_zones_sample.geojson'
with open(out_path, 'w') as f:
json.dump(sample_geojson, f, ensure_ascii=False)

size_kb = out_path.stat().st_size / 1024
crit_sites = sum(1 for f in sample_features if f['properties']['critical_species'] > 0)
print(f" Muestra GeoJSON: {len(sample_features)} sitios ({crit_sites} con sp. críticas) → {size_kb:.0f} KB")

# ── 4. Datos de especies críticas ────────────────────────────────────────────
species_data = {
"metadata": {
"fecha": "2026-07-27",
"fuente": "Fish_Zones_PANGAS (Moreno-Báez et al. 2011/2012)",
"total_zonas_analizadas": len(sites)
},
"especies_criticas": [
{"codigo": "carspp", "nombre_comun": "Camarones", "nombre_cientifico": "Farfantepenaeus sp.", "estado_iucn": "LC", "importancia": "Alta comercial"},
{"codigo": "gymmar", "nombre_comun": "Mero gigante", "nombre_cientifico": "Epinephelus itajara", "estado_iucn": "CR", "importancia": "Crítica"},
{"codigo": "rhilon", "nombre_comun": "Rayas guitarrón", "nombre_cientifico": "Rhinobatos lentiginosus", "estado_iucn": "VU", "importancia": "Alta"},
{"codigo": "rhipro", "nombre_comun": "Raya bocona", "nombre_cientifico": "Rhinobatos productus", "estado_iucn": "NT", "importancia": "Moderada"},
{"codigo": "rhispp", "nombre_comun": "Rayas (spp)", "nombre_cientifico": "Rhinobatos spp.", "estado_iucn": "VU", "importancia": "Alta"},
{"codigo": "sphspp", "nombre_comun": "Tiburones", "nombre_cientifico": "Sphyrna spp.", "estado_iucn": "EN", "importancia": "Crítica"},
{"codigo": "lutarg", "nombre_comun": "Pargo lunarejo", "nombre_cientifico": "Lutjanus argentiventris", "estado_iucn": "LC", "importancia": "Alta comercial"},
{"codigo": "parspp", "nombre_comun": "Pargos (spp)", "nombre_cientifico": "Paralabrax spp.", "estado_iucn": "LC", "importancia": "Alta comercial"},
{"codigo": "dasspp", "nombre_comun": "Rayas mariposa", "nombre_cientifico": "Dasyatis spp.", "estado_iucn": "NT", "importancia": "Moderada"},
{"codigo": "mycros", "nombre_comun": "Mero almejero", "nombre_cientifico": "Mycteroperca rosacea", "estado_iucn": "NT", "importancia": "Alta"},
],
"por_proyecto": {
"NFE_Puerto_Libertad": {
"especies_presentes": ["carspp", "rhilon", "rhipro", "rhispp", "sphspp", "gymmar", "lutarg", "parspp"],
"num_criticas": 8,
"riesgo_pesquero": 90.27
},
"Bazan_San_Felipe": {
"especies_presentes": ["carspp", "rhilon", "rhipro", "rhispp", "sphspp", "gymmar", "lutarg", "parspp", "mycros"],
"num_criticas": 9,
"riesgo_pesquero": 97.76
},
"Guaymas_Terminal": {
"especies_presentes": ["carspp", "rhilon", "rhipro", "rhispp", "gymmar", "parspp", "mycros"],
"num_criticas": 7,
"riesgo_pesquero": 93.80
}
}
}

species_path = PUBLIC_DIR / 'especies_criticas.json'
with open(species_path, 'w') as f:
json.dump(species_data, f, ensure_ascii=False, indent=2)
print(f" Datos de especies: {species_path}")

print("\n Datos preparados para el dashboard.")
