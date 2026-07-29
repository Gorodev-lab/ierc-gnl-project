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
import csv
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import date

# ============================================================
# Proyectos GNL del Alto Golfo de California (Datos Verificados)
# ============================================================
GNL_PROJECTS = [
    {
        'proyecto_id': 'MPL_Saguaro_Puerto_Libertad',
        'proyecto_nombre': 'Saguaro Energía GNL (Mexico Pacific Limited)',
        'latitud': 29.9107,
        'longitud': -112.6835,
        'estado': 'Sonora',
        'estatus': 'propuesto',
        'radio_busqueda_km': 50.0,
    },
    {
        'proyecto_id': 'Sempra_Ensenada',
        'proyecto_nombre': 'Sempra Energy - Ensenada LNG',
        'latitud': 31.8667,
        'longitud': -116.6333,
        'estado': 'Baja California',
        'estatus': 'operacional',
        'radio_busqueda_km': 75.0,
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
        'radio_busqueda_km': 100.0,
    },
]

CRITICAL_SPECIES_CODES = {
    'carspp', 'lutarg', 'parspp', 'musspp', 'rhilon',
    'rhipro', 'rhispp', 'dasspp', 'dasdip', 'gymmar',
    'mycros', 'sphspp',
}

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_polygon_centroid(coordinates) -> Tuple[Optional[float], Optional[float]]:
    try:
        ring = coordinates[0][0]
        if not ring:
            return None, None
        lons = [c[0] for c in ring]
        lats = [c[1] for c in ring]
        return sum(lats) / len(lats), sum(lons) / len(lons)
    except (IndexError, TypeError):
        return None, None

def load_geojson_centroids(filepath: str) -> List[Dict]:
    centroids = []
    with open(filepath, 'r', encoding='utf-8') as f:
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

def calculate_fishing_risk(project: Dict, all_layers: Dict[str, List[Dict]]) -> Dict:
    plat = project['latitud']
    plon = project['longitud']
    radio_km = project['radio_busqueda_km']

    zonas_cercanas = []
    for layer_name, layer_data in all_layers.items():
        if layer_name == 'Riqueza_Relativa':
            continue

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

    usar_riqueza = len(zonas_cercanas) < 50 and 'Riqueza_Relativa' in all_layers
    if usar_riqueza:
        for item in all_layers['Riqueza_Relativa']:
            dist = haversine_distance(plat, plon, item['lat'], item['lon'])
            if dist <= radio_km * 1.5:
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

    n_zonas = len(zonas_cercanas)
    densidad = min(n_zonas / 500.0, 1.0)

    distancia_minima = min(z['distancia_km'] for z in zonas_cercanas)
    proximidad = math.exp(-distancia_minima / (radio_km * 0.1))
    proximidad = min(proximidad, 1.0)

    spp_codes_encontrados = set()
    for z in zonas_cercanas:
        if z['capa'] in ['ZPesca_PANGAS']:
            spp = z['props'].get('spp_code', '')
            if spp:
                spp_codes_encontrados.add(spp.lower())

    criticas_riqueza = 0
    for z in zonas_cercanas:
        if z['capa'] == 'Riqueza_Relativa':
            count = sum(1 for col in CRITICAL_SPECIES_CODES if z['props'].get(col, 0) and z['props'].get(col, 0) > 0)
            criticas_riqueza = max(criticas_riqueza, count)

    n_criticas_pangas = len(spp_codes_encontrados & CRITICAL_SPECIES_CODES)
    n_criticas_total = max(n_criticas_pangas, criticas_riqueza)
    especies_criticas_score = min(n_criticas_total / 5.0, 1.0)

    riesgo_raw = (0.50 * densidad) + (0.30 * proximidad) + (0.20 * especies_criticas_score)
    riesgo_pesquero = round(riesgo_raw * 100, 2)

    if riesgo_pesquero >= 70:
        nivel = 'Alto'
    elif riesgo_pesquero >= 40:
        nivel = 'Moderado'
    elif riesgo_pesquero > 0:
        nivel = 'Bajo'
    else:
        nivel = 'Sin datos'

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
    base_dir = Path('/home/gorops/ierc-gnl-project')
    pangas_dir = base_dir / 'data/raw/pangas_wgs84'
    output_dir = base_dir / 'data/processed'
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("CÁLCULO DE RIESGO PESQUERO — IERC-GNL")
    print("Basado en Moreno-Báez et al. (2011, 2012)")
    print("=" * 60)

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
            print(f"  {layer_name}: {len(centroids)} zonas cargadas")

    results = []
    for project in GNL_PROJECTS:
        result = calculate_fishing_risk(project, all_layers)
        results.append(result)

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

    print("\n¡Resultados de riesgo pesquero calculados y guardados!")

if __name__ == '__main__':
    main()
