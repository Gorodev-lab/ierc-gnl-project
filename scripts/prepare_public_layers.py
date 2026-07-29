#!/usr/bin/env python3
"""
prepare_public_layers.py
------------------------
Genera las capas GeoJSON completas (100% de entidades de QGIS) con metadatos enriquecidos del Atlas PANGAS
y colores exactos de simbología de QGIS.

Autores: Causa Natura Data (JCB / EG)
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PANGAS_DIR = BASE_DIR / 'data' / 'raw' / 'pangas_wgs84'
PUBLIC_DATA_DIR = BASE_DIR / 'dashboard' / 'public' / 'data'

PUBLIC_DATA_DIR.mkdir(parents=True, exist_ok=True)

CRITICAL_CODES = {'CARSPP', 'GYMMAR', 'RHILON', 'RHIPRO', 'RHISPP', 'SPHSPP', 'LUTARG', 'PARSPP', 'DASSPP', 'DASDIP', 'MYCROS'}

METADATA_MAP = {
    'ZPesca_PANGAS': {
        'titulo': 'Base Unificada de Zonas Pesqueras PANGAS',
        'artes': 'Multiespecie / PANGAS',
        'imagen': '/atlas_pangas_jpg/mapa_ZPesca_PANGAS.jpg',
        'descripcion': 'Capa maestra consolidada (4,241 polígonos) de campos pesqueros artesanales.',
        'color_qgis': '#8D6E63' # Brown / Ochre (QGIS Screenshot 4)
    },
    'ZPesca_Buceo': {
        'titulo': 'Polígonos de Pesca Comercial por Buceo',
        'artes': 'Buceo autónomo y semiautónomo (Hookah)',
        'imagen': '/atlas_pangas_jpg/mapa_ZPesca_Buceo.jpg',
        'descripcion': 'Sitios extractivos de moluscos, callo de hacha, erizo y pepino de mar (249 polígonos).',
        'color_qgis': '#E91E63' # Pink / Magenta (QGIS Screenshot 2)
    },
    'ZPesca_Chinchorro': {
        'titulo': 'Polígonos de Pesca con Chinchorro de Línea',
        'artes': 'Chinchorro de línea / Redes agalleras',
        'imagen': '/atlas_pangas_jpg/mapa_ZPesca_Chinchorro.jpg',
        'descripcion': 'Zonas de operación pesquera artesanal para especies de escama (2,209 polígonos).',
        'color_qgis': '#C0392B' # Deep Red (QGIS Screenshot 3)
    },
    'ZPesca_Redes': {
        'titulo': 'Polígonos de Pesca con Redes de Enmalle',
        'artes': 'Redes de enmalle / Agalleras de fondo',
        'imagen': '/atlas_pangas_jpg/mapa_ZPesca_Redes.jpg',
        'descripcion': 'Zonas de esfuerzo artesanal para peces demersales y pelágicos (1,263 polígonos).',
        'color_qgis': '#27AE60' # Green (QGIS Screenshot 5)
    },
    'ZPesca_Redes_Manta_Camaron': {
        'titulo': 'Polígonos de Pesca de Camarón y Redes de Manta',
        'artes': 'Redes de manta / Surpera / Camarón',
        'imagen': '/atlas_pangas_jpg/mapa_ZPesca_Redes_Manta_Camaron.jpg',
        'descripcion': 'Caladeros de pesca estacional de camarón (783 polígonos).',
        'color_qgis': '#D35400' # Orange
    },
    'ZPesca_Trampa': {
        'titulo': 'Polígonos de Pesca con Trampas (Jaiba y Peces)',
        'artes': 'Trampas jaiberas / Nasas',
        'imagen': '/atlas_pangas_jpg/mapa_ZPesca_Trampa.jpg',
        'descripcion': 'Sitios de pesca artesanal costera mediante trampas (360 polígonos).',
        'color_qgis': '#8E44AD' # Purple
    },
    'Riqueza_Relativa': {
        'titulo': 'Malla de Riqueza Biológica Pesquera Relativa',
        'artes': 'Todas las artes registradas',
        'imagen': '/atlas_pangas_jpg/mapa_Riqueza_Relativa.jpg',
        'descripcion': 'Malla de acumulación de riqueza de especies pesqueras (11,065 celdas).',
        'color_qgis': '#2C3E50' # Dark Blue Grid (QGIS Screenshot 1)
    }
}

print("Procesando capas COMPLETAS del Atlas PANGAS para igualar QGIS...")

for layer_name, meta in METADATA_MAP.items():
    file_name = f"{layer_name}_wgs84.geojson"
    input_path = RAW_PANGAS_DIR / file_name
    output_path = PUBLIC_DATA_DIR / f"{layer_name.lower()}_sample.geojson"

    if not input_path.exists():
        print(f"  [OMITIDO] Archivo {file_name} no encontrado.")
        continue

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    features = data.get('features', [])
    # Procesar el 100% de los polígonos (sin recortar a 350)
    processed_features = []
    for feat in features:
        props = feat.get('properties', {}) or {}
        spp = (props.get('spp_code') or '').upper()
        sitio = props.get('sitio_code') or props.get('sitio_nomb') or props.get('comunidad') or 'Sitio Pesquero'

        feat['properties'] = {
            'layer_id': layer_name,
            'layer_titulo': meta['titulo'],
            'layer_artes': meta['artes'],
            'layer_imagen': meta['imagen'],
            'layer_descripcion': meta['descripcion'],
            'color_qgis': meta['color_qgis'],
            'sitio': sitio,
            'comunidad': props.get('comunidad') or props.get('sitio_nomb') or 'Golfo de California',
            'spp_code': spp,
            'critical_species': 1 if spp in CRITICAL_CODES else 0,
            'habitat': props.get('HABITAT', 'No especificado'),
            'total_records': props.get('Ent_num', 1)
        }
        processed_features.append(feat)

    out_data = {
        'type': 'FeatureCollection',
        'layer_name': layer_name,
        'metadata': meta,
        'features': processed_features
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False)

    print(f"  [OK] Capa {layer_name}: {len(processed_features)} de {len(features)} polígonos exportados a {output_path.name}.")

print("\n¡Procesamiento de capas completas finalizado!")
