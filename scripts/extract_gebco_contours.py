#!/usr/bin/env python3
"""
extract_gebco_contours.py
=========================
Procesa el raster de batimetría GEBCO 2024 / ETOPO1 recortado al Golfo de California
(Lat 23-32 N, Lon -114 a -105 W) y genera contornos vectoriales estandarizados (EPSG:4326),
corrigiendo la alineación del eje Y de latitud (flanqueado mar adentro).
"""

import os
import sys
import numpy as np
import rasterio
import geopandas as gpd
from shapely.geometry import LineString
from matplotlib import pyplot as plt

BOUNDS = {
    'lat_min': 23.0,
    'lat_max': 32.0,
    'lon_min': -114.0,
    'lon_max': -105.0
}

DEPTH_CLASSES = [
    (-5000, -2000, "-5000 a -2000m", "Profunda"),
    (-2000, -1000, "-2000 a -1000m", "Batiatlántica"),
    (-1000, -500, "-1000 a -500m", "Talud superior"),
    (-500, -200, "-500 a -200m", "Borde de plataforma"),
    (-200, -100, "-200 a -100m", "Plataforma externa"),
    (-100, -50, "-100 a -50m", "Plataforma media"),
    (-50, -20, "-50 a -20m", "Plataforma interna"),
    (-20, -10, "-20 a -10m", "Zona nerítica"),
    (-10, -1, "-10 a -1m", "Zona somera/costera")
]

# Niveles marinos subacuáticos estrictos
CONTOUR_LEVELS = [-3000, -2000, -1000, -500, -200, -100, -50, -20, -10]

def get_raster_path():
    gebco_path = "causanaturadata/batimetria/GEBCO_2024_Golfo_California.tif"
    etopo_path = "causanaturadata/batimetria/ETOPO1_Gulf_California.tif"
    if os.path.exists(gebco_path) and os.path.getsize(gebco_path) > 1000:
        return gebco_path, "GEBCO 2024 (15 arc-sec)"
    elif os.path.exists(etopo_path):
        return etopo_path, "ETOPO1 (1 arc-min)"
    else:
        raise FileNotFoundError("No se encontró ningún archivo de batimetría raster.")

def main():
    raster_file, fuente = get_raster_path()
    print(f"[+] Procesando batimetría desde: {raster_file} ({fuente})")

    with rasterio.open(raster_file) as src:
        raw_data = src.read(1).astype(float)
        bounds = src.bounds

    # Invertir verticalmente la matriz para sincronizar la fila 0 con bounds.bottom (lat_min)
    data = np.flipud(raw_data)
    
    # Enmascarar superficie terrestre (mantenimiento exclusivo de elevaciones mar adentro < -1m)
    data[data >= -1.0] = np.nan

    ny, nx = data.shape
    x = np.linspace(bounds.left, bounds.right, nx)
    y = np.linspace(bounds.bottom, bounds.top, ny)
    X, Y = np.meshgrid(x, y)

    print(f"[+] Grid ajustado: {nx}x{ny}, Rango marino: [{np.nanmin(data):.1f}m, {np.nanmax(data):.1f}m]")

    # Generar contornos con matplotlib en el espacio de coordenadas geográficas correcto
    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, data, levels=CONTOUR_LEVELS)

    records = []
    for level, segs in zip(cs.levels, cs.allsegs):
        if level >= 0:
            continue
        for poly in segs:
            if len(poly) >= 3:
                # Determinar clase de profundidad
                cat = "Desconocida"
                for min_d, max_d, label, desc in DEPTH_CLASSES:
                    if min_d <= level <= max_d:
                        cat = label
                        break
                
                records.append({
                    'geometry': LineString(poly),
                    'profundidad_m': float(level),
                    'clase_profundidad': cat,
                    'fuente': fuente
                })

    plt.close(fig)

    gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")
    print(f"[+] Total de contornos marinos bien alineados (< 0m): {len(gdf)}")
    print(f"[+] Centroide medio marino: Lon={gdf.geometry.centroid.x.mean():.4f}, Lat={gdf.geometry.centroid.y.mean():.4f}")

    output_dir = "causanaturadata/output"
    os.makedirs(output_dir, exist_ok=True)
    gpkg_out = os.path.join(output_dir, "GEBCO_Batimetria_Golfo.gpkg")

    gdf.to_file(gpkg_out, layer="batimetria_gebco_2024", driver="GPKG")
    print(f"[✔] Capa de contornos guardada en: {gpkg_out} (layer='batimetria_gebco_2024')")

if __name__ == "__main__":
    main()
