#!/usr/bin/env python3
"""
Fishing Risk Calculator — IERC-GNL Project
============================================

Calcula el riesgo pesquero por proyecto de GNL usando:
- ZPesca_PANGAS (capa principal, 4,241 zonas con habitat/especie/método)
- ZPesca_Buceo, Chinchorro, Redes, Trampa (artes complementarios)
- Riqueza_Relativa (11,065 celdas, cobertura extendida para Guaymas)

Todos los GeoJSON están en EPSG:4326 (WGS84) ya reproyectados desde NAD27 Lambert.

Formula de Riesgo Pesquero (Moreno-Báez et al. 2011, 2012):
riesgo = (0.5 * densidad_esfuerzo) + (0.3 * proximidad_normalizada) + (0.2 * especies_criticas)

Autores: Proyecto IERC-GNL
"""

import json
import math
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import date
import csv


# ============================================================
# Proyectos GNL del Alto Golfo de California
# ============================================================
GNL_PROJECTS = [
{
'proyecto_id': 'NFE_Puerto_Libertad',
'proyecto_nombre': 'New Fortress Energy - Puerto Libertad',
'latitud': 29.9107,
'longitud': -112.6835,
'estado': 'Sonora',
'estatus': 'propuesto',
'radio_busqueda_km': 50.0,  # Radio amplio para capturar zonas pesqueras cercanas
},
{
'proyecto_id': 'Sempra_Ensenada',
'proyecto_nombre': 'Sempra Energy - Ensenada LNG',
'latitud': 31.8667,
'longitud': -116.6333,
'estado': 'Baja California',
'estatus': 'operacional',
'radio_busqueda_km': 75.0,  # Fuera del bbox PANGAS, radio mayor
},
{
'proyecto_id': 'Sempra_Costa_Azul',
'proyecto_nombre': 'Sempra LNG - Costa Azul (Expansión)',
'latitud': 31.7150,
'longitud': -116.5700,
'estado': 'Baja California',
'estatus': 'propuesto_expansion',
'radio_busqueda_km': 75.0,
},
{
'proyecto_id': 'Bazan_San_Felipe',
'proyecto_nombre': 'Terminal GNL San Felipe',
'latitud': 31.0833,
'longitud': -114.8500,
'estado': 'Baja California',
'estatus': 'propuesto',
'radio_busqueda_km': 50.0,
},
{
'proyecto_id': 'Guaymas_Terminal',
'proyecto_nombre': 'Terminal GNL Guaymas',
'latitud': 27.9179,
'longitud': -110.9039,
'estado': 'Sonora',
'estatus': 'propuesto',
'radio_busqueda_km': 100.0,  # Usar Riqueza_Relativa como fuente extendida
},
]

# Especies consideradas críticas (IUCN o alta importancia comercial en el Golfo)
CRITICAL_SPECIES_CODES = {
'carspp',   # Camarones (alta importancia comercial)
'lutarg',   # Lutjánidos (pargos)
'parspp',   # Pargos
'musspp',   # Mejillones
'rhilon',   # Rayas (amenazadas)
'rhipro',   # Rayas guitarrón
'rhispp',   # Rayas spp.
'dasspp',   # Rayas mariposa
'dasdip',   # Raya mariposa (especie específica)
'gymmar',   # Mero gigante (en peligro)
'mycros',   # Mero spp.
'sphspp',   # Tiburones spp.
}


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
"""
Calcula la distancia en km entre dos puntos usando la fórmula Haversine.
Más precisa que la aproximación lineal para distancias mayores a 10 km.
"""
R = 6371.0  # Radio de la Tierra en km
phi1, phi2 = math.radians(lat1), math.radians(lat2)
dphi = math.radians(lat2 - lat1)
dlambda = math.radians(lon2 - lon1)
a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_polygon_centroid(coordinates) -> Tuple[float, float]:
"""Calcula el centroide aproximado de un polígono (promedio de vértices del anillo exterior)."""
try:
ring = coordinates[0][0]  # Primer anillo del primer polígono
if not ring:
return None, None
lons = [c[0] for c in ring]
lats = [c[1] for c in ring]
return sum(lats) / len(lats), sum(lons) / len(lons)
except (IndexError, TypeError):
return None, None


def load_geojson_centroids(filepath: str) -> List[Dict]:
"""
Carga un GeoJSON y extrae centroides de cada feature con sus propiedades.
Retorna lista de dicts con lat, lon y properties.
"""
centroids = []
with open(filepath, 'r') as f:
data = json.load(f)

for feat in data.get('features', []):
try:
geom = feat.get('geometry', {})
props = feat.get('properties', {})

if geom.get('type') == 'MultiPolygon':
lat, lon = get_polygon_centroid(geom['coordinates'])
elif geom.get('type') == 'Polygon':
lat, lon = get_polygon_centroid([geom['coordinates']])
else:
continue

if lat is not None and -90 <= lat <= 90 and -180 <= lon <= 180:
centroids.append({'lat': lat, 'lon': lon, 'props': props})
except Exception:
continue

return centroids


def count_critical_species_in_riqueza(riqueza_centroids: List[Dict]) -> Dict[Tuple, int]:
"""
Para la capa Riqueza_Relativa, cuenta cuántas especies críticas hay por centroide.
Retorna dict {(lat, lon): count_criticas}
"""
result = {}
for item in riqueza_centroids:
props = item['props']
count = sum(1 for col in CRITICAL_SPECIES_CODES if props.get(col, 0) and props.get(col, 0) > 0)
result[(item['lat'], item['lon'])] = count
return result


def calculate_fishing_risk(project: Dict, all_layers: Dict[str, List[Dict]]) -> Dict:
"""
Calcula el riesgo pesquero para un proyecto GNL dado usando múltiples capas.

Args:
project: Diccionario con datos del proyecto GNL
all_layers: Diccionario con capas cargadas {nombre_capa: [centroides]}

Returns:
Diccionario con métricas de riesgo pesquero
"""
plat = project['latitud']
plon = project['longitud']
radio_km = project['radio_busqueda_km']

# Recopilar todas las zonas dentro del radio de búsqueda
zonas_cercanas = []

# Capas principales de pesca activa
for layer_name, layer_data in all_layers.items():
if layer_name == 'Riqueza_Relativa':
continue  # Se usa diferente abajo

for item in layer_data:
dist = haversine_distance(plat, plon, item['lat'], item['lon'])
if dist <= radio_km:
zonas_cercanas.append({
'capa': layer_name,
'distancia_km': dist,
'props': item['props'],
'lat': item['lat'],
'lon': item['lon'],
})

# Usar Riqueza_Relativa como fuente adicional si hay pocas zonas (ej. Guaymas)
usar_riqueza = len(zonas_cercanas) < 50 and 'Riqueza_Relativa' in all_layers
if usar_riqueza:
for item in all_layers['Riqueza_Relativa']:
dist = haversine_distance(plat, plon, item['lat'], item['lon'])
if dist <= radio_km * 1.5:  # Radio extendido para Riqueza_Relativa
zonas_cercanas.append({
'capa': 'Riqueza_Relativa',
'distancia_km': dist,
'props': item['props'],
'lat': item['lat'],
'lon': item['lon'],
})

if not zonas_cercanas:
return {
**{k: project[k] for k in ['proyecto_id', 'proyecto_nombre', 'latitud', 'longitud', 'estado', 'estatus']},
'radio_busqueda_km': radio_km,
'num_zonas_encontradas': 0,
'zona_mas_cercana_km': None,
'densidad_esfuerzo_pesquero': 0.0,
'proximidad_normalizada': 0.0,
'especies_criticas_score': 0.0,
'riesgo_pesquero': 0.0,
'nivel_riesgo': 'Sin datos',
'artes_de_pesca': [],
'fuentes_usadas': [],
'nota': 'Sin zonas pesqueras en radio de búsqueda'
}

# ----------------------------------------------------------------
# Componente 1: Densidad de esfuerzo pesquero (0-1)
# Número de zonas pesqueras dentro del radio, normalizado
# Umbral: 500+ zonas = máximo riesgo
# ----------------------------------------------------------------
n_zonas = len(zonas_cercanas)
densidad = min(n_zonas / 500.0, 1.0)

# ----------------------------------------------------------------
# Componente 2: Proximidad normalizada (0-1)
# Zona más cercana: 0 km = riesgo máximo, radio_km = riesgo 0
# ----------------------------------------------------------------
distancia_minima = min(z['distancia_km'] for z in zonas_cercanas)
# Fórmula de decaimiento exponencial: mayor riesgo si más cerca
proximidad = math.exp(-distancia_minima / (radio_km * 0.1))
proximidad = min(proximidad, 1.0)

# ----------------------------------------------------------------
# Componente 3: Especies críticas (0-1)
# ----------------------------------------------------------------
# Para ZPesca_PANGAS: usar spp_code
spp_codes_encontrados = set()
for z in zonas_cercanas:
if z['capa'] in ['ZPesca_PANGAS']:
spp = z['props'].get('spp_code', '')
if spp:
spp_codes_encontrados.add(spp.lower())

# Para Riqueza_Relativa: contar columnas de especies críticas > 0
criticas_riqueza = 0
for z in zonas_cercanas:
if z['capa'] == 'Riqueza_Relativa':
count = sum(1 for col in CRITICAL_SPECIES_CODES if z['props'].get(col, 0) and z['props'].get(col, 0) > 0)
criticas_riqueza = max(criticas_riqueza, count)

n_criticas_pangas = len(spp_codes_encontrados & CRITICAL_SPECIES_CODES)
n_criticas_total = max(n_criticas_pangas, criticas_riqueza)
especies_criticas_score = min(n_criticas_total / 5.0, 1.0)  # 5+ especies = máximo riesgo

# ----------------------------------------------------------------
# Riesgo pesquero final (0-100)
# Ponderación Moreno-Báez et al.: 50% densidad, 30% proximidad, 20% especies
# ----------------------------------------------------------------
riesgo_raw = (0.50 * densidad) + (0.30 * proximidad) + (0.20 * especies_criticas_score)
riesgo_pesquero = round(riesgo_raw * 100, 2)

# Nivel de riesgo
if riesgo_pesquero >= 70:
nivel = 'Alto'
elif riesgo_pesquero >= 40:
nivel = 'Moderado'
elif riesgo_pesquero > 0:
nivel = 'Bajo'
else:
nivel = 'Sin datos'

# Artes de pesca encontradas
artes = list(set(z['capa'].replace('ZPesca_', '').replace('_wgs84', '') for z in zonas_cercanas))
fuentes = list(set(z['capa'] for z in zonas_cercanas))

return {
'proyecto_id': project['proyecto_id'],
'proyecto_nombre': project['proyecto_nombre'],
'latitud': plat,
'longitud': plon,
'estado': project['estado'],
'estatus': project['estatus'],
'radio_busqueda_km': radio_km,
'num_zonas_encontradas': n_zonas,
'zona_mas_cercana_km': round(distancia_minima, 2),
'densidad_esfuerzo_pesquero': round(densidad, 4),
'proximidad_normalizada': round(proximidad, 4),
'especies_criticas_score': round(especies_criticas_score, 4),
'riesgo_pesquero': riesgo_pesquero,
'nivel_riesgo': nivel,
'artes_de_pesca': sorted(artes),
'fuentes_usadas': sorted(fuentes),
'nota': f'{"Riqueza_Relativa incluida (extensión de cobertura)" if usar_riqueza else "Solo capas ZPesca"}'
}


def main():
"""Ejecuta el cálculo de riesgo pesquero para todos los proyectos GNL."""
base_dir = Path('/home/gorops/ierc-gnl-project')
pangas_dir = base_dir / 'data/raw/pangas_wgs84'
output_dir = base_dir / 'data/processed'
output_dir.mkdir(exist_ok=True)

print("=" * 60)
print("CÁLCULO DE RIESGO PESQUERO — IERC-GNL")
print("Basado en Moreno-Báez et al. (2011, 2012)")
print("=" * 60)
print()

# Cargar todas las capas GeoJSON reproyectadas
layer_files = {
'ZPesca_PANGAS': 'ZPesca_PANGAS_wgs84.geojson',
'ZPesca_Buceo': 'ZPesca_Buceo_wgs84.geojson',
'ZPesca_Chinchorro': 'ZPesca_Chinchorro_wgs84.geojson',
'ZPesca_Redes': 'ZPesca_Redes_wgs84.geojson',
'ZPesca_Redes_Manta_Camaron': 'ZPesca_Redes_Manta_Camaron_wgs84.geojson',
'ZPesca_Trampa': 'ZPesca_Trampa_wgs84.geojson',
'Riqueza_Relativa': 'Riqueza_Relativa_wgs84.geojson',
}

all_layers = {}
for layer_name, filename in layer_files.items():
filepath = pangas_dir / filename
if filepath.exists():
centroids = load_geojson_centroids(str(filepath))
all_layers[layer_name] = centroids
print(f" {layer_name}: {len(centroids)} zonas cargadas")
else:
print(f" {layer_name}: archivo no encontrado ({filepath})")

print()
print("Calculando riesgo pesquero por proyecto GNL...")
print()

results = []
for project in GNL_PROJECTS:
print(f" {project['proyecto_id']} ({project['latitud']}°N, {project['longitud']}°E)...")
result = calculate_fishing_risk(project, all_layers)
results.append(result)
print(f"   Zonas encontradas: {result['num_zonas_encontradas']}")
print(f"   Zona más cercana: {result['zona_mas_cercana_km']} km")
print(f"   Riesgo pesquero: {result['riesgo_pesquero']:.1f}/100 ({result['nivel_riesgo']})")
print(f"   Nota: {result['nota']}")
print()

# Guardar CSV
csv_path = output_dir / 'riesgo_pesquero_proyectos_gnl.csv'
fieldnames = [
'proyecto_id', 'proyecto_nombre', 'latitud', 'longitud', 'estado', 'estatus',
'radio_busqueda_km', 'num_zonas_encontradas', 'zona_mas_cercana_km',
'densidad_esfuerzo_pesquero', 'proximidad_normalizada', 'especies_criticas_score',
'riesgo_pesquero', 'nivel_riesgo', 'nota'
]
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
writer.writeheader()
writer.writerows(results)
print(f" CSV guardado: {csv_path}")

# Guardar JSON detallado
json_path = output_dir / 'riesgo_pesquero_proyectos_gnl_detalle.json'
with open(json_path, 'w', encoding='utf-8') as f:
json.dump({
'fecha_calculo': str(date.today()),
'metodologia': 'Moreno-Báez et al. (2011, 2012) - Fish_Zones_PANGAS GDB reproyectado a EPSG:4326',
'formula': 'riesgo = (0.50 * densidad_esfuerzo) + (0.30 * proximidad_norm) + (0.20 * especies_criticas)',
'capas_usadas': list(all_layers.keys()),
'total_proyectos': len(results),
'proyectos': results
}, f, ensure_ascii=False, indent=2)
print(f" JSON detallado guardado: {json_path}")

# Resumen
print()
print("=" * 60)
print("RESUMEN DE RESULTADOS")
print("=" * 60)
print(f"{'Proyecto':<35} {'Riesgo':>7} {'Nivel':<12} {'Zonas':>6} {'Dist. min':>10}")
print("-" * 60)
for r in sorted(results, key=lambda x: x['riesgo_pesquero'], reverse=True):
zona_str = f"{r['zona_mas_cercana_km']} km" if r['zona_mas_cercana_km'] else 'N/A'
print(f"{r['proyecto_id']:<35} {r['riesgo_pesquero']:>6.1f} {r['nivel_riesgo']:<12} {r['num_zonas_encontradas']:>6} {zona_str:>10}")

return results


if __name__ == '__main__':
main()
