#!/usr/bin/env python3
"""
Generate Synthetic TNC Vector Data (Shapefiles)
================================================
Crea shapefiles sintéticos para:
- Bajos marinos (polígonos) - montes submarinos, bancos
- Arrecifes coral negro (polígonos) - Antipatharia

Compatible con el ingester TNC existente.
"""

import geopandas as gpd
from shapely.geometry import Polygon, Point
import numpy as np
from pathlib import Path
import zipfile
import tempfile

# Config
OUTPUT_DIR = Path("/home/gorops/ierc-gnl-project/data/raw/tnc")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Golfo de California bbox
MIN_LAT, MAX_LAT = 22.5, 32.0
MIN_LON, MAX_LON = -115.0, -108.0

def create_bajos_marinos():
    """Crea polígonos de bajos marinos (seamounts, bancos) en el Golfo."""
    
    np.random.seed(42)
    features = []
    
    # Nombres reales de bajos marinos del Golfo
    nombres = [
        "Bajo Espíritu Santo", "Bajo San Lorenzo", "Bajo San Esteban",
        "Bajo San Pedro Mártir", "Bajo San Ildefonso", "Bajo San Rafael",
        "Banco de Cabo Pulmo", "Banco de La Paz", "Banco de Loreto",
        "Banco de Santa Rosalía", "Banco de Guaymas", "Banco de Puerto Libertad",
        "Monte Submarino Alarcón", "Monte Submarino Tamayo", "Monte Submarino Gorda",
        "Monte Submarino Farallón", "Monte Submarino San Marcos", "Monte Submarino Tortugas",
    ]
    
    for i, nombre in enumerate(nombres):
        # Posición aleatoria en el Golfo
        lon = np.random.uniform(MIN_LON + 0.5, MAX_LON - 0.5)
        lat = np.random.uniform(MIN_LAT + 0.5, MAX_LAT - 0.5)
        
        # Radio aleatorio (0.01-0.1 grados ≈ 1-11 km)
        radius = np.random.uniform(0.01, 0.1)
        
        # Crear polígono circular (aproximado)
        n_points = 32
        angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
        coords = [(lon + radius * np.cos(a), lat + radius * np.sin(a)) for a in angles]
        coords.append(coords[0])  # cerrar polígono
        
        poly = Polygon(coords)
        
        # Profundidad típica de bajos (50-500m)
        prof_min = np.random.uniform(20, 200)
        prof_max = prof_min + np.random.uniform(50, 300)
        
        # Área aproximada
        area_km2 = poly.area * 111 * 111 * np.cos(np.radians(lat))  # rough conversion
        
        features.append({
            'objectid': i + 1,
            'nombre': nombre,
            'tipo': 'bajo_marino' if 'Bajo' in nombre else 'monte_submarino' if 'Monte' in nombre else 'banco',
            'area_km2': round(area_km2, 2),
            'profundidad_min_m': round(prof_min, 1),
            'profundidad_max_m': round(prof_max, 1),
            'geometry': poly
        })
    
    gdf = gpd.GeoDataFrame(features, crs="EPSG:4326")
    return gdf


def create_arrecifes_coral_negro():
    """Crea polígonos de arrecifes de coral negro (Antipatharia)."""
    
    np.random.seed(123)
    features = []
    
    # Nombres reales de arrecifes coral negro
    nombres = [
        "Arrecife Coral Negro Cabo Pulmo", "Arrecife Coral Negro San José",
        "Arrecife Coral Negro La Paz", "Arrecife Coral Negro Loreto",
        "Arrecife Coral Negro Santa Rosalía", "Arrecife Coral Negro Guaymas",
        "Arrecife Coral Negro Puerto Libertad", "Arrecife Coral Negro Bahía Kino",
        "Arrecife Coral Negro Isla Tiburón", "Arrecife Coral Negro Isla Ángel de la Guarda",
    ]
    
    for i, nombre in enumerate(nombres):
        # Posición en aguas más profundas (coral negro vive 50-1000m)
        lon = np.random.uniform(MIN_LON + 0.3, MAX_LON - 0.3)
        lat = np.random.uniform(MIN_LAT + 0.3, MAX_LAT - 0.3)
        
        # Arrecifes más pequeños y alargados
        width = np.random.uniform(0.005, 0.02)
        height = np.random.uniform(0.01, 0.03)
        angle = np.random.uniform(0, 2*np.pi)
        
        # Crear elipse rotada
        n_points = 24
        angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
        coords = []
        for a in angles:
            x = width * np.cos(a)
            y = height * np.sin(a)
            # Rotar
            xr = x * np.cos(angle) - y * np.sin(angle)
            yr = x * np.sin(angle) + y * np.cos(angle)
            coords.append((lon + xr, lat + yr))
        coords.append(coords[0])
        
        poly = Polygon(coords)
        
        # Coral negro: 50-800m profundidad
        prof_min = np.random.uniform(50, 300)
        prof_max = prof_min + np.random.uniform(50, 200)
        
        area_km2 = poly.area * 111 * 111 * np.cos(np.radians(lat))
        
        features.append({
            'objectid': i + 1,
            'nombre': nombre,
            'area_km2': round(area_km2, 2),
            'profundidad_min_m': round(prof_min, 1),
            'profundidad_max_m': round(prof_max, 1),
            'geometry': poly
        })
    
    gdf = gpd.GeoDataFrame(features, crs="EPSG:4326")
    return gdf


def save_shapefile_zip(gdf, filename):
    """Guarda GeoDataFrame como shapefile dentro de ZIP."""
    
    zip_path = OUTPUT_DIR / filename
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Guardar shapefile
        shp_path = tmpdir / filename.replace('.zip', '.shp')
        gdf.to_file(shp_path, driver='ESRI Shapefile')
        
        # Crear ZIP
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for shp_file in tmpdir.glob(f"{filename.replace('.zip', '')}.*"):
                zf.write(shp_file, shp_file.name)
    
    print(f"✅ Creado: {zip_path} ({len(gdf)} features)")
    return zip_path


def main():
    print("=== Generando datos vectoriales sintéticos TNC ===")
    
    # 1. Bajos marinos
    print("\n1. Generando bajos marinos...")
    gdf_bajos = create_bajos_marinos()
    save_shapefile_zip(gdf_bajos, "tnc_bajos_marinos_golfo_california.zip")
    print(f"   Features: {len(gdf_bajos)}")
    print(f"   Tipos: {gdf_bajos['tipo'].value_counts().to_dict()}")
    
    # 2. Arrecifes coral negro
    print("\n2. Generando arrecifes coral negro...")
    gdf_coral = create_arrecifes_coral_negro()
    save_shapefile_zip(gdf_coral, "tnc_arrecifes_coral_negro_golfo_california.zip")
    print(f"   Features: {len(gdf_coral)}")
    
    print(f"\n✅ Completado en {OUTPUT_DIR}")


if __name__ == "__main__":
    main()