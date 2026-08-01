#!/usr/bin/env python3
"""
Generate Synthetic NASA OceanColor NetCDF for Testing
======================================================
Crea archivos NetCDF de prueba con la misma estructura que MODIS-Aqua L3SMI:
- chlor_a: mg/m³, 4km resolution, daily
- sst: °C, 4km resolution, daily
- Bounding box: Golfo de California (22.5-32°N, -115 a -108°W)
"""

import numpy as np
import xarray as xr
from pathlib import Path
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración
OUTPUT_DIR = Path("/home/gorops/ierc-gnl-project/data/raw/nasa")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Golfo de California bbox
MIN_LAT, MAX_LAT = 22.5, 32.0
MIN_LON, MAX_LON = -115.0, -108.0

# Resolución 4km ≈ 0.0417 grados en latitud
RESOLUTION_DEG = 0.0417

# Generar coordenadas
lats = np.arange(MAX_LAT, MIN_LAT - RESOLUTION_DEG, -RESOLUTION_DEG)
lons = np.arange(MIN_LON, MAX_LON + RESOLUTION_DEG, RESOLUTION_DEG)

# Recortar a bbox exacto
lats = lats[(lats >= MIN_LAT) & (lats <= MAX_LAT)]
lons = lons[(lons >= MIN_LON) & (lons <= MAX_LON)]

logger.info(f"Grid: {len(lats)} lat x {len(lons)} lon = {len(lats)*len(lons)} pixels")

# Fechas: 2020-01 a 2024-12 (mensual)
dates = []
current = datetime(2020, 1, 1)
while current <= datetime(2024, 12, 1):
    dates.append(current)
    # Avanzar al primer día del mes siguiente
    if current.month == 12:
        current = current.replace(year=current.year + 1, month=1)
    else:
        current = current.replace(month=current.month + 1)

logger.info(f"Generando {len(dates)} archivos mensuales")


def generate_chlor_a_data(lat_grid, lon_grid, date):
    """Genera datos realistas de clorofila-a (mg/m³)."""
    # Patrón base: más alto cerca de costa, estacional
    # lat/lon grids son 2D
    
    # Gradiente costero (más clorofila cerca de costa)
    # Distancia aproximada a costa (simplificado)
    dist_to_coast = np.minimum(
        np.abs(lat_grid - MIN_LAT),
        np.abs(lat_grid - MAX_LAT)
    ) + np.minimum(
        np.abs(lon_grid - MIN_LON),
        np.abs(lon_grid - MAX_LON)
    )
    
    # Estacionalidad: más productividad en primavera/verano
    month = date.month
    seasonal_factor = 1.0 + 0.5 * np.sin(2 * np.pi * (month - 3) / 12)
    
    # Base + ruido
    base = 0.1 + 0.3 * np.exp(-dist_to_coast * 2)  # mg/m³
    data = base * seasonal_factor + np.random.normal(0, 0.05, lat_grid.shape)
    
    # Valores negativos a 0
    data = np.maximum(data, 0.01)
    
    # Valores muy altos (blooms) - occasional
    bloom_mask = np.random.random(lat_grid.shape) < 0.02
    data[bloom_mask] *= np.random.uniform(2, 8, bloom_mask.sum())
    
    return data.astype(np.float32)


def generate_sst_data(lat_grid, lon_grid, date):
    """Genera datos realistas de SST (°C)."""
    month = date.month
    
    # Gradiente latitudinal: más cálido al sur
    base_temp = 28 - (lat_grid - MIN_LAT) / (MAX_LAT - MIN_LAT) * 6  # 22-28°C
    
    # Estacionalidad
    seasonal = 3 * np.sin(2 * np.pi * (month - 1) / 12)  # ±3°C
    
    # Gradiente longitudinal (ligeramente más cálido al oeste)
    lon_effect = (lon_grid - MIN_LON) / (MAX_LON - MIN_LON) * 1.5
    
    data = base_temp + seasonal + lon_effect + np.random.normal(0, 0.3, lat_grid.shape)
    
    return data.astype(np.float32)


def create_netcdf_file(variable, date, output_path):
    """Crea archivo NetCDF CF-compliant."""
    
    # Crear malla 2D
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    if variable == 'chlor_a':
        data = generate_chlor_a_data(lat_grid, lon_grid, date)
        units = 'mg m^-3'
        long_name = 'Chlorophyll-a concentration'
        standard_name = 'mass_concentration_of_chlorophyll_a_in_sea_water'
        fill_value = -32767.0
    else:  # sst
        data = generate_sst_data(lat_grid, lon_grid, date)
        units = 'degree_Celsius'
        long_name = 'Sea Surface Temperature'
        standard_name = 'sea_surface_temperature'
        fill_value = -32767.0
    
    # Crear dataset xarray
    ds = xr.Dataset(
        {
            variable: (['lat', 'lon'], data, {
                'units': units,
                'long_name': long_name,
                'standard_name': standard_name,
                'valid_min': 0.0 if variable == 'chlor_a' else -2.0,
                'valid_max': 100.0 if variable == 'chlor_a' else 40.0,
            })
        },
        coords={
            'lat': (['lat'], lats, {
                'units': 'degrees_north',
                'long_name': 'Latitude',
                'standard_name': 'latitude',
            }),
            'lon': (['lon'], lons, {
                'units': 'degrees_east',
                'long_name': 'Longitude',
                'standard_name': 'longitude',
            }),
            'time': ([], np.datetime64(date), {
                'long_name': 'Time',
                'standard_name': 'time',
            })
        }
    )
    
    # Atributos globales CF
    ds.attrs = {
        'title': f'MODISA L3SMI {variable.upper()} Monthly Composite',
        'institution': 'NASA/GSFC/OBPG (Synthetic Test Data)',
        'source': 'MODIS-Aqua',
        'processing_level': 'L3SMI',
        'date_created': datetime.utcnow().isoformat() + 'Z',
        'geospatial_lat_min': float(MIN_LAT),
        'geospatial_lat_max': float(MAX_LAT),
        'geospatial_lon_min': float(MIN_LON),
        'geospatial_lon_max': float(MAX_LON),
        'time_coverage_start': date.strftime('%Y-%m-%dT00:00:00Z'),
        'time_coverage_end': date.strftime('%Y-%m-%dT23:59:59Z'),
        'Conventions': 'CF-1.6, ACDD-1.3',
        'standard_name_vocabulary': 'CF Standard Name Table v70',
    }
    
    # Codificación para NetCDF4
    encoding = {
        variable: {
            'zlib': True,
            'complevel': 4,
            '_FillValue': fill_value,
            'dtype': 'float32',
        },
        'lat': {'dtype': 'float32'},
        'lon': {'dtype': 'float32'},
    }
    
    ds.to_netcdf(output_path, format='NETCDF4', encoding=encoding)
    logger.info(f"  Creado: {output_path.name} ({variable}, {date.strftime('%Y-%m')}, {data.shape})")


def main():
    logger.info("=== Generando datos NetCDF sintéticos NASA OceanColor ===")
    
    for date in dates:
        year = date.year
        month = date.month
        
        # Chlorofila-a
        chlor_file = OUTPUT_DIR / f"nasa_chlor_a_{year}_{month:02d}.nc"
        create_netcdf_file('chlor_a', date, chlor_file)
        
        # SST
        sst_file = OUTPUT_DIR / f"nasa_sst_{year}_{month:02d}.nc"
        create_netcdf_file('sst', date, sst_file)
    
    logger.info(f"\n✅ Completado: {len(dates)*2} archivos en {OUTPUT_DIR}")
    logger.info("Patrones: nasa_chlor_a_YYYY_MM.nc, nasa_sst_YYYY_MM.nc")


if __name__ == "__main__":
    main()