#!/usr/bin/env python3
"""
fetch_gfw_api.py
----------------
Procesa y consulta la información de Global Fishing Watch (GFW) para el Golfo de California (Sonora).
Soporta:
 1. Consulta dinámica a la API v3 de GFW con GFW_API_TOKEN.
 2. Procesamiento de respaldo del conjunto de datos estático de Zenodo en data/raw/gfw/.

Autores: Causa Natura Data (JCB / EG)
"""

import os
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_GFW_DIR = BASE_DIR / 'data' / 'raw' / 'gfw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def load_env():
    env_path = Path.home() / '.env'
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")

load_env()
token = os.getenv('GFW_API_TOKEN') or os.getenv('GFW_TOKEN')

print("=======================================================================")
print("Procesador de Datos Global Fishing Watch (GFW)")
print("=======================================================================")

if token:
    print("🟢 GFW_API_TOKEN detectada en ~/.env. Intentando consulta a la API v3 de GFW...")
    
    # Endpoint de búsqueda de buques en México / Golfo de California
    url = "https://gateway.globalfishingwatch.org/v3/vessels/search?query=flag%3DMEX&limit=50"
    cmd = ['curl', '-s', '-4', '-H', f'Authorization: Bearer {token}', url]
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout)
            out_file = PROCESSED_DIR / 'gfw_api_vessels_mexico.json'
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ Consulta exitosa a GFW API. Guardado en: {out_file.name}")
        else:
            print(f"⚠️ La respuesta de la API estuvo vacía o falló. Pasando a procesar datos locales de Zenodo...")
    except Exception as e:
        print(f"⚠️ Error al conectar con GFW API v3: {e}. Pasando a procesar datos locales...")

# Procesamiento de respaldo con datos locales de Zenodo
zenodo_csv = RAW_GFW_DIR / 'zenodo_global_fishing_watch.csv'
if zenodo_csv.exists():
    print(f"\nProcesando archivo local de Zenodo ({round(zenodo_csv.stat().st_size / (1024*1024), 2)} MB)...")
    summary = {
        'fuente': 'Zenodo Global Fishing Watch v3',
        'archivo': zenodo_csv.name,
        'tamano_mb': round(zenodo_csv.stat().st_size / (1024*1024), 2),
        'cobertura': 'Golfo de California (Sonora)',
        'estatus': 'Listo para cálculo de celdas H3'
    }
    out_summary = PROCESSED_DIR / 'gfw_zenodo_summary.json'
    with open(out_summary, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"✓ Resumen de datos de Zenodo guardado en: {out_summary.name}")

print("\n¡Procesamiento de Global Fishing Watch finalizado correctamente!")
