#!/usr/bin/env python3
"""
H3 Indexer for IERC-GNL Project
==================================

Script para generar malla hexagonal H3 y poblar la tabla h3_cells en Supabase/PostgreSQL.

Features:
- Generación de celdas H3 nivel 8 para el Golfo de California
- Generación de celdas H3 nivel 10 para zonas portuarias
- Función point_to_h3 para asignación de índices H3
- Conexión segura a PostgreSQL/Supabase
- Manejo robusto de excepciones geográficas
- Tipado fuerte con Python Type Hints

Requirements:
- geopandas>=0.14.0
- shapely>=2.0.0
- h3>=3.7.6
- psycopg2-binary>=2.9.7
- sqlalchemy>=2.0.0
- pyproj>=3.6.0
"""

import os
import sys
import logging
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
import json

import h3
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, MultiPolygon, Point, box
from shapely.ops import unary_union
import psycopg2
from psycopg2 import sql, extras
from psycopg2.extensions import connection as _connection
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from pyproj import CRS, Transformer

# Configuración de logging
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
handlers=[
logging.FileHandler('/home/gorops/ierc-gnl-project/logs/h3_indexer.log'),
logging.StreamHandler()
]
)
logger = logging.getLogger(__name__)

@dataclass
class H3CellConfig:
"""Configuración para generación de celdas H3"""
resolution: int
zone: str
is_port_area: bool = False
is_navigation_channel: bool = False
buffer_km: float = 0.0

@dataclass
class DBConfig:
"""Configuración de conexión a la base de datos"""
host: str
port: int
database: str
user: str
password: str
sslmode: str = "require"

def get_connection_string(self) -> str:
"""Genera cadena de conexión para SQLAlchemy"""
return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

def validate_coordinates(lat: float, lon: float) -> bool:
"""Valida que las coordenadas estén dentro del rango válido para H3"""
return -90 <= lat <= 90 and -180 <= lon <= 180

def point_to_h3(lat: float, lon: float, resolution: int) -> Optional[int]:
"""
Convierte coordenadas geográficas a índice H3.

Args:
lat: Latitud en grados decimales (WGS84)
lon: Longitud en grados decimales (WGS84)
resolution: Nivel de resolución H3 (0-15)

Returns:
Índice H3 como entero o None si las coordenadas son inválidas
"""
if not validate_coordinates(lat, lon):
logger.error(f"Coordenadas inválidas: lat={lat}, lon={lon}")
return None

try:
h3_index = h3.geo_to_h3(lat, lon, resolution)
return h3_index
except Exception as e:
logger.error(f"Error al convertir a H3: {e}")
return None

def polygon_to_h3_cells(geometry: Union[Polygon, MultiPolygon], 
resolution: int, 
buffer_km: float = 0.0) -> List[int]:
"""
Convierte un polígono o multipolígono a una lista de índices H3.

Args:
geometry: Geometría de Shapely (Polygon o MultiPolygon)
resolution: Nivel de resolución H3
buffer_km: Buffer en kilómetros para expandir el área

Returns:
Lista de índices H3 que cubren el área
"""
if buffer_km > 0:
# Convertir buffer de km a grados (aproximado)
# 1 grado ≈ 111 km en el ecuador
buffer_deg = buffer_km / 111.0
geometry = geometry.buffer(buffer_deg)

# Obtener el bounding box de la geometría
min_lon, min_lat, max_lon, max_lat = geometry.bounds

# Generar celdas H3 que intersectan con el bounding box
h3_indices = set()

# Iterar sobre una cuadrícula aproximada para cubrir el área
lon_step = 0.01  # ~1.1 km
lat_step = 0.01  # ~1.1 km

lon = min_lon
while lon <= max_lon:
lat = min_lat
while lat <= max_lat:
# Verificar si el centro de la celda está dentro de la geometría
if geometry.contains(Point(lon, lat)):
h3_index = point_to_h3(lat, lon, resolution)
if h3_index:
h3_indices.add(h3_index)
lat += lat_step
lon += lon_step

# Asegurar que todas las celdas que intersectan con el polígono estén incluidas
for cell in h3.grid_disk(h3.geo_to_h3(min_lat, min_lon, resolution), 2):
cell_geom = h3.h3_to_geo_boundary(cell, True)
cell_poly = Polygon(cell_geom)
if geometry.intersects(cell_poly):
h3_indices.add(cell)

return sorted(list(h3_indices))

def create_h3_cell_geometry(h3_index: int) -> Polygon:
"""
Crea un objeto Polygon de Shapely a partir de un índice H3.

Args:
h3_index: Índice H3

Returns:
Objeto Polygon de Shapely
"""
try:
boundary = h3.h3_to_geo_boundary(h3_index, True)
return Polygon(boundary)
except Exception as e:
logger.error(f"Error al crear geometría para H3 {h3_index}: {e}")
raise ValueError(f"No se pudo crear geometría para H3 {h3_index}")

def generate_golfo_california_h3_cells(resolution: int = 8) -> gpd.GeoDataFrame:
"""
Genera la malla hexagonal H3 para el Golfo de California.

Args:
resolution: Nivel de resolución H3 (8 para ~0.73 km²)

Returns:
GeoDataFrame con las celdas H3 generadas
"""
logger.info(f"Generando malla H3 nivel {resolution} para Golfo de California...")

# Coordenadas del Golfo de California (aproximadas)
min_lat, min_lon = 22.5, -115.0  # Sureste
max_lat, max_lon = 32.0, -108.0  # Noroeste

# Generar celdas H3 que cubren el área
h3_indices = set()

# Crear una cuadrícula de puntos para generar celdas
lat = min_lat
while lat <= max_lat:
lon = min_lon
while lon <= max_lon:
h3_index = point_to_h3(lat, lon, resolution)
if h3_index:
h3_indices.add(h3_index)
lon += 0.1  # ~11 km
lat += 0.1

logger.info(f"Generadas {len(h3_indices)} celdas H3 nivel {resolution}")

# Crear GeoDataFrame
records = []
for h3_index in h3_indices:
try:
geom = create_h3_cell_geometry(h3_index)
records.append({
'h3_index': h3_index,
'h3_index_port': None,
'geometry': geom,
'resolution': resolution,
'zone': 'Mar Abierto',
'is_port_area': False,
'is_navigation_channel': False
})
except Exception as e:
logger.warning(f"Error al procesar celda H3 {h3_index}: {e}")
continue

gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")
logger.info(f"GeoDataFrame creado con {len(gdf)} celdas válidas")

return gdf

def generate_port_areas_h3_cells(config: H3CellConfig) -> gpd.GeoDataFrame:
"""
Genera celdas H3 para zonas portuarias específicas.

Args:
config: Configuración H3CellConfig con zona y resolución

Returns:
GeoDataFrame con las celdas H3 para el puerto
"""
logger.info(f"Generando celdas H3 para {config.zone} (resolución {config.resolution})...")

# Coordenadas aproximadas de las zonas portuarias
port_coords = {
'Puerto Libertad': {
'center': (29.9000, -112.6833),
'buffer_km': 10.0
},
'Guaymas': {
'center': (27.9500, -110.9000),
'buffer_km': 15.0
}
}

if config.zone not in port_coords:
raise ValueError(f"Zona portuaria no reconocida: {config.zone}")

center_lat, center_lon = port_coords[config.zone]['center']
buffer_km = port_coords[config.zone]['buffer_km']

# Crear un círculo alrededor del puerto
circle = Point(center_lon, center_lat).buffer(buffer_km / 111.0)

# Generar celdas H3 para el área
h3_indices = polygon_to_h3_cells(circle, config.resolution, buffer_km)

logger.info(f"Generadas {len(h3_indices)} celdas H3 para {config.zone}")

# Crear GeoDataFrame
records = []
for h3_index in h3_indices:
try:
geom = create_h3_cell_geometry(h3_index)
records.append({
'h3_index': h3_index,
'h3_index_port': h3_index,  # Mismo índice para puerto
'geometry': geom,
'resolution': config.resolution,
'zone': config.zone,
'is_port_area': config.is_port_area,
'is_navigation_channel': config.is_navigation_channel
})
except Exception as e:
logger.warning(f"Error al procesar celda H3 {h3_index} en {config.zone}: {e}")
continue

gdf = gpd.GeoDataFrame(records, crs="EPSG:4326")
logger.info(f"GeoDataFrame creado con {len(gdf)} celdas válidas para {config.zone}")

return gdf

def connect_to_database(db_config: DBConfig) -> Engine:
"""
Establece conexión a la base de datos PostgreSQL/Supabase.

Args:
db_config: Configuración de conexión

Returns:
Engine de SQLAlchemy
"""
try:
connection_string = db_config.get_connection_string()
logger.info(f"Conectando a {db_config.host}:{db_config.port}/{db_config.database}")

engine = create_engine(
connection_string,
pool_size=5,
max_overflow=10,
pool_pre_ping=True,
pool_recycle=3600,
echo=False  # Cambiar a True para debugging
)

# Verificar conexión
with engine.connect() as conn:
logger.info("Conexión a la base de datos establecida exitosamente")

return engine
except SQLAlchemyError as e:
logger.error(f"Error al conectar a la base de datos: {e}")
raise
except Exception as e:
logger.error(f"Error inesperado al conectar a la base de datos: {e}")
raise

def create_h3_cells_table(engine: Engine) -> None:
"""
Crea la tabla h3_cells si no existe.

Args:
engine: Engine de SQLAlchemy
"""
create_table_sql = """
CREATE TABLE IF NOT EXISTS h3_cells (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
h3_index BIGINT NOT NULL UNIQUE,
h3_index_port BIGINT,
geometry GEOMETRY(POLYGON, 4326) NOT NULL,
resolution INTEGER NOT NULL CHECK (resolution BETWEEN 8 AND 11),
zone VARCHAR(50) NOT NULL CHECK (
zone IN ('Puerto Libertad', 'Guaymas', 'Punta Chueca', 'Mar Abierto')
),
is_port_area BOOLEAN DEFAULT FALSE,
is_navigation_channel BOOLEAN DEFAULT FALSE,
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_h3_cells_geometry ON h3_cells USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_h3_cells_h3_index ON h3_cells(h3_index);
CREATE INDEX IF NOT EXISTS idx_h3_cells_zone ON h3_cells(zone);
"""

try:
with engine.connect() as conn:
conn.execute(text(create_table_sql))
conn.commit()
logger.info("Tabla h3_cells creada/verificada exitosamente")
except SQLAlchemyError as e:
logger.error(f"Error al crear tabla h3_cells: {e}")
raise

def insert_h3_cells(engine: Engine, gdf: gpd.GeoDataFrame) -> int:
"""
Inserta celdas H3 en la base de datos.

Args:
engine: Engine de SQLAlchemy
gdf: GeoDataFrame con las celdas H3

Returns:
Número de registros insertados
"""
if len(gdf) == 0:
logger.warning("No hay celdas H3 para insertar")
return 0

try:
# Convertir GeoDataFrame a lista de diccionarios
records = gdf.to_dict('records')

# Convertir geometrías a WKT
for record in records:
record['geometry'] = gpd.GeoSeries([record['geometry']]).to_wkt()[0]

# Insertar en batch
with engine.connect() as conn:
result = conn.execute(
text("""
INSERT INTO h3_cells 
(h3_index, h3_index_port, geometry, resolution, zone, 
is_port_area, is_navigation_channel)
VALUES (:h3_index, :h3_index_port, ST_GeomFromText(:geometry, 4326),
:resolution, :zone, :is_port_area, :is_navigation_channel)
ON CONFLICT (h3_index) DO NOTHING
"""),
records
)
conn.commit()

logger.info(f"Insertadas {result.rowcount} celdas H3 en la base de datos")
return result.rowcount

except SQLAlchemyError as e:
logger.error(f"Error al insertar celdas H3: {e}")
raise
except Exception as e:
logger.error(f"Error inesperado al insertar celdas H3: {e}")
raise

def generate_complete_h3_grid() -> gpd.GeoDataFrame:
"""
Genera la malla completa de celdas H3 para el proyecto IERC-GNL.

Returns:
GeoDataFrame combinado con todas las celdas
"""
logger.info("Generando malla H3 completa para IERC-GNL...")

# Configuraciones para cada zona
configs = [
H3CellConfig(resolution=8, zone='Mar Abierto'),
H3CellConfig(resolution=10, zone='Puerto Libertad', is_port_area=True),
H3CellConfig(resolution=10, zone='Guaymas', is_port_area=True),
H3CellConfig(resolution=10, zone='Punta Chueca', is_port_area=False)
]

all_gdfs = []

for config in configs:
if config.zone == 'Mar Abierto':
gdf = generate_golfo_california_h3_cells(config.resolution)
else:
gdf = generate_port_areas_h3_cells(config)

all_gdfs.append(gdf)
logger.info(f"Agregadas {len(gdf)} celdas para {config.zone}")

# Combinar todos los GeoDataFrames
combined_gdf = gpd.GeoDataFrame(pd.concat(all_gdfs, ignore_index=True), crs="EPSG:4326")

# Eliminar duplicados por h3_index
combined_gdf = combined_gdf.drop_duplicates(subset=['h3_index'])

logger.info(f"Malla H3 completa generada: {len(combined_gdf)} celdas únicas")

return combined_gdf

def main():
"""
Función principal para generar e insertar la malla H3.
"""
logger.info("=== Iniciando generador de malla H3 para IERC-GNL ===")

try:
# Configuración de la base de datos (leer de variables de entorno o usar defaults)
db_config = DBConfig(
host=os.getenv('DB_HOST', 'localhost'),
port=int(os.getenv('DB_PORT', '5432')),
database=os.getenv('DB_NAME', 'postgres'),
user=os.getenv('DB_USER', 'postgres'),
password=os.getenv('DB_PASSWORD', 'postgres')
)

# Conectar a la base de datos
engine = connect_to_database(db_config)

# Crear tabla si no existe
create_h3_cells_table(engine)

# Generar malla H3 completa
h3_gdf = generate_complete_h3_grid()

# Insertar en la base de datos
inserted_count = insert_h3_cells(engine, h3_gdf)

logger.info(f"=== Proceso completado: {inserted_count} celdas H3 insertadas ===")

return 0

except Exception as e:
logger.error(f"=== Proceso fallido: {e} ===")
return 1

if __name__ == "__main__":
import pandas as pd
sys.exit(main())
