#!/usr/bin/env python3
"""
Prepara los datos para el dashboard IERC-GNL.
- Copia el JSON de resultados procesados a public/data/
- Genera una muestra ligera del GeoJSON WGS84 de PANGAS (~500 zonas únicas)
"""

import json
from pathlib import Path

BASE = Path('/home/gorops/ierc-gnl-project')
PROCESSED_DIR = BASE / 'data/processed'
PUBLIC_DIR = BASE / 'dashboard/public/data'

PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

# ── 1. Copiar resultados de riesgo ──────────────────────────────────────────
src = PROCESSED_DIR / 'riesgo_pesquero_proyectos_gnl_detalle.json'
dst = PUBLIC_DIR / 'riesgo_proyectos.json'
if src.exists():
    with open(src, 'r', encoding='utf-8') as f:
        risk_data = json.load(f)
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(risk_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Copiado: {dst.name}")

# ── 2. Datos de especies críticas ────────────────────────────────────────────
species_data = {
    "metadata": {
        "fecha": "2026-07-29",
        "fuente": "Fish_Zones_PANGAS (Moreno-Báez et al. 2011/2012)",
        "total_zonas_analizadas": 4241
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
        "MPL_Saguaro_Puerto_Libertad": {
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
with open(species_path, 'w', encoding='utf-8') as f:
    json.dump(species_data, f, ensure_ascii=False, indent=2)

print("✓ Datos de especies críticas preparados para el dashboard.")
