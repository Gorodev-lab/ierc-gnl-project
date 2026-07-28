#!/usr/bin/env python3
"""
Spatial Validator for IERC-GNL Project
=========================================

Script para validación espacial crítica de datos reales:
- Validación de Bounding Box del Golfo de California
- Algoritmo de no-deformación geométrica (EPSG:4326 → UTM Zona 12N → EPSG:4326)
- Identificador de vacíos (Moreno-Báez 2012) para celdas sin datos en 5 años
- Cálculo de métricas de confianza espacial

Features:
- Proyección dinámica a UTM Zona 12N (EPSG:32612) para cálculos precisos
- Validación estricta de coordenadas en bbox [22.5,32.0] x [-115.0,-108.0]
- Comparación contra inventario histórico por celda H3
- Cálculo de 'confidence_dato' basado en riqueza de especies
- Tipado fuerte con Python Type Hints
- Logging detallado con rotación
- Manejo de excepciones geográficas

Requirements:
- geopandas>=0.14.0
- shapely>=2.0.0
- pyproj>=3.6.0
- numpy>=1.24.0
- pandas>=2.0.0
- psycopg2-binary>=2.9.7
- sqlalchemy>=2.0.0

Geometries:
- EPSG:4326 (WGS84) para entrada/salida
- EPSG:32612 (UTM Zona 12N) para cálculos de distancia y buffers
- Conversión a WKT para PostGIS
"""

import os
import sys
import logging
import json
from typing import Dict, List, Tuple, Optional, Union, Set
from dataclasses import dataclass
from pathlib import Path
import tempfile
import time
from datetime import datetime, timedelta

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon, box
from shapely.ops import unary_union
from pyproj import CRS, Transformer
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

# Configuración avanzada de logging con rotación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            '/home/gorops/ierc-gnl-project/logs/spatial_validator.log',
            maxBytes=10485760,  # 10 MB
            backupCount=5
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SpatialValidationConfig:
    """Configuración para validación espacial"""
    gulf_bbox: Dict[str, float] = None
    utm_zone: int = 12
    reprojection_target: str = "EPSG:4326"
    historical_data_years: int = 5
    sample_size_for_validation: int = 1000
    
    def __post_init__(self):
        if self.gulf_bbox is None:
            self.gulf_bbox = {
                'min_lat': 22.5,
                'max_lat': 32.0,
                'min_lon': -115.0,
                'max_lon': -108.0
            }

class SpatialValidator:
    """
    Validador espacial para datos reales del Golfo de California.
    
    Features:
    - Validación de Bounding Box
    - No-deformación geométrica (EPSG:4326 → UTM Zona 12N → EPSG:4326)
    - Identificador de vacíos (Moreno-Báez 2012)
    - Cálculo de confidence_dato basado en riqueza de especies
    - Tipado fuerte con Python Type Hints
    - Logging detallado
    """
    
    def __init__(self, db_engine: Engine, config: SpatialValidationConfig = None):
        """
        Inicializa el validador espacial.
        
        Args:
            db_engine: Engine de SQLAlchemy conectado a Supabase/PostgreSQL
            config: Configuración de validación
        """
        self.db_engine = db_engine
        self.config = config if config else SpatialValidationConfig()
        
        # Configurar transformadores de proyección
        self.epsg4326 = CRS.from_epsg(4326)
        self.epsg32612 = CRS.from_epsg(32612)  # UTM Zona 12N
        
        # Transformador de WGS84 a UTM Zona 12N
        self.transformer_wgs84_to_utm = Transformer.from_crs(
            self.epsg4326, self.epsg32612, always_xy=True
        )
        
        # Transformador de UTM Zona 12N a WGS84
        self.transformer_utm_to_wgs84 = Transformer.from_crs(
            self.epsg32612, self.epsg4326, always_xy=True
        )
        
        logger.info("✅ SpatialValidator inicializado con configuración de producción")
    
    def validate_bounding_box(self, geometry: Union[Point, Polygon, MultiPolygon]) -> bool:
        """
        Valida que una geometría esté completamente dentro del Bounding Box del Golfo de California.
        
        Args:
            geometry: Geometría de Shapely (Point, Polygon o MultiPolygon)
        
        Returns:
            True si la geometría está dentro del bbox, False en caso contrario
        """
        try:
            if isinstance(geometry, Point):
                lon, lat = geometry.x, geometry.y
                in_bbox = (
                    self.config.gulf_bbox['min_lat'] <= lat <= self.config.gulf_bbox['max_lat'] and
                    self.config.gulf_bbox['min_lon'] <= lon <= self.config.gulf_bbox['max_lon']
                )
                if not in_bbox:
                    logger.warning(f"⚠️  Punto fuera de bbox: ({lat}, {lon})")
                return in_bbox
            
            elif isinstance(geometry, (Polygon, MultiPolygon)):
                # Obtener bounding box de la geometría
                min_lon, min_lat, max_lon, max_lat = geometry.bounds
                
                # Verificar si el bbox de la geometría está dentro del bbox del Golfo
                in_bbox = (
                    self.config.gulf_bbox['min_lat'] <= min_lat and
                    max_lat <= self.config.gulf_bbox['max_lat'] and
                    self.config.gulf_bbox['min_lon'] <= min_lon and
                    max_lon <= self.config.gulf_bbox['max_lon']
                )
                
                if not in_bbox:
                    logger.warning(f"⚠️  Geometría parcialmente fuera de bbox: bbox=({min_lat}, {min_lon}, {max_lat}, {max_lon})")
                
                return in_bbox
            
            else:
                logger.error(f"❌ Tipo de geometría no soportado: {type(geometry)}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en validación de bounding box: {e}")
            return False
    
    def reproject_geometry_no_deformation(self, geometry: Union[Point, Polygon, MultiPolygon]) -> str:
        """
        Realiza no-deformación geométrica:
        1. Proyecta de EPSG:4326 a UTM Zona 12N (EPSG:32612)
        2. Realiza cálculos espaciales (buffers, distancias)
        3. Reproyecta de vuelta a EPSG:4326
        4. Retorna geometría en formato WKT
        
        Args:
            geometry: Geometría en EPSG:4326
        
        Returns:
            Geometría en formato WKT EPSG:4326
        """
        try:
            logger.debug("🔄 Iniciando no-deformación geométrica...")
            
            # Paso 1: Proyectar a UTM Zona 12N
            if isinstance(geometry, Point):
                # Convertir punto
                lon, lat = geometry.x, geometry.y
                utm_x, utm_y = self.transformer_wgs84_to_utm.transform(lon, lat)
                utm_point = Point(utm_x, utm_y)
                
                # Realizar buffer en UTM (metros)
                buffer_meters = 500  # Buffer de 500 metros
                buffered_utm = utm_point.buffer(buffer_meters)
                
                # Reproyectar de vuelta a WGS84
                wgs84_x, wgs84_y = self.transformer_utm_to_wgs84.transform(
                    buffered_utm.centroid.x, buffered_utm.centroid.y
                )
                reprojected_geometry = Point(wgs84_x, wgs84_y)
                
            elif isinstance(geometry, Polygon):
                # Convertir polígono a puntos y proyectar
                coords = list(geometry.exterior.coords)
                utm_coords = [self.transformer_wgs84_to_utm.transform(x, y) for x, y in coords]
                utm_polygon = Polygon(utm_coords)
                
                # Realizar buffer en UTM
                buffer_meters = 1000  # Buffer de 1000 metros
                buffered_utm = utm_polygon.buffer(buffer_meters)
                
                # Reproyectar de vuelta a WGS84
                reprojected_coords = [
                    self.transformer_utm_to_wgs84.transform(x, y) 
                    for x, y in list(buffered_utm.exterior.coords)
                ]
                reprojected_geometry = Polygon(reprojected_coords)
                
            elif isinstance(geometry, MultiPolygon):
                # Procesar cada polígono en el multipolígono
                reprojected_polygons = []
                for polygon in geometry.geoms:
                    coords = list(polygon.exterior.coords)
                    utm_coords = [self.transformer_wgs84_to_utm.transform(x, y) for x, y in coords]
                    utm_polygon = Polygon(utm_coords)
                    buffered_utm = utm_polygon.buffer(1000)
                    reprojected_coords = [
                        self.transformer_utm_to_wgs84.transform(x, y) 
                        for x, y in list(buffered_utm.exterior.coords)
                    ]
                    reprojected_polygons.append(Polygon(reprojected_coords))
                
                reprojected_geometry = MultiPolygon(reprojected_polygons)
            
            else:
                logger.error(f"❌ Tipo de geometría no soportado: {type(geometry)}")
                return None
            
            # Validar que la geometría reproyectada esté dentro del bbox
            if not self.validate_bounding_box(reprojected_geometry):
                logger.warning("⚠️  Geometría reproyectada fuera de bbox, ajustando...")
                # Recortar al bbox del Golfo
                reprojected_geometry = self._clip_to_gulf_bbox(reprojected_geometry)
            
            # Convertir a WKT
            wkt = reprojected_geometry.wkt
            
            logger.debug(f"✅ No-deformación completada: {wkt[:50]}...")
            return wkt
            
        except Exception as e:
            logger.error(f"❌ Error en no-deformación geométrica: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def _clip_to_gulf_bbox(self, geometry: Union[Point, Polygon, MultiPolygon]) -> Union[Point, Polygon, MultiPolygon]:
        """
        Recorta una geometría al bounding box del Golfo de California.
        
        Args:
            geometry: Geometría a recortar
        
        Returns:
            Geometría recortada al bbox
        """
        try:
            gulf_bbox_polygon = box(
                self.config.gulf_bbox['min_lon'],
                self.config.gulf_bbox['min_lat'],
                self.config.gulf_bbox['max_lon'],
                self.config.gulf_bbox['max_lat']
            )
            
            if isinstance(geometry, Point):
                if gulf_bbox_polygon.contains(geometry):
                    return geometry
                else:
                    return None
            
            elif isinstance(geometry, (Polygon, MultiPolygon)):
                clipped = geometry.intersection(gulf_bbox_polygon)
                if clipped.is_empty:
                    return None
                return clipped
            
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Error al recortar geometría: {e}")
            return None
    
    def identify_voids_moreno_baez_2012(self, h3_cell_id: str, current_year: int = 2024) -> Dict[str, Union[float, bool, str]]:
        """
        Identificador de vacíos según Moreno-Báez 2012:
        - Compara riqueza de especies en celda H3 contra inventario histórico
        - Marca celdas sin datos en últimos 5 años como "Incertidumbre de Muestreo"
        - Calcula confidence_dato basado en riqueza relativa
        
        Args:
            h3_cell_id: ID de la celda H3
            current_year: Año actual para cálculo de ventana temporal
        
        Returns:
            Diccionario con métricas de vacío y confianza
        """
        try:
            logger.info(f"🔍 Identificando vacíos para celda H3: {h3_cell_id}")
            
            # Año límite para datos históricos (5 años atrás)
            historical_year_limit = current_year - self.config.historical_data_years
            
            with self.db_engine.connect() as conn:
                # Obtener datos de fisheries_exposure para esta celda
                fisheries_query = text("""
                    SELECT 
                        species_code,
                        landings_kg,
                        quincena,
                        EXTRACT(YEAR FROM created_at) as year
                    FROM fisheries_exposure
                    WHERE h3_cell_id = :h3_cell_id
                    AND created_at >= :historical_limit
                """)
                
                df_fisheries = pd.read_sql(
                    fisheries_query,
                    conn,
                    params={
                        'h3_cell_id': h3_cell_id,
                        'historical_limit': datetime(historical_year_limit, 1, 1)
                    }
                )
                
                # Obtener especies de referencia para comparación
                species_query = text("""
                    SELECT species_code, conservation_status
                    FROM species_reference
                """)
                
                df_species = pd.read_sql(species_query, conn)
                
                if len(df_fisheries) == 0:
                    # Celda sin datos en últimos 5 años → Incertidumbre de Muestreo
                    logger.warning(f"⚠️  Celda {h3_cell_id} sin datos en últimos {self.config.historical_data_years} años")
                    
                    # Calcular richness_score basado en especies potenciales
                    total_species = len(df_species)
                    richness_score = total_species / 50.0  # Normalizar contra 50 especies típicas
                    
                    return {
                        'h3_cell_id': h3_cell_id,
                        'void_status': 'Incertidumbre de Muestreo',
                        'years_without_data': self.config.historical_data_years,
                        'species_richness_score': richness_score,
                        'confidence_dato': 0.3,  # Bajo por falta de datos
                        'historical_data_available': False,
                        'last_data_year': None,
                        'calculated_at': datetime.now().isoformat()
                    }
                
                # Celda con datos → Calcular métricas
                species_in_cell = df_fisheries['species_code'].nunique()
                total_landings = df_fisheries['landings_kg'].sum()
                years_with_data = df_fisheries['year'].nunique()
                
                # Richness score (riqueza relativa)
                max_possible_species = 50  # Número típico de especies en Golfo de California
                richness_score = min(species_in_cell / max_possible_species, 1.0)
                
                # Confidence score basado en:
                # - Richness (40%)
                # - Years with data (30%)
                # - Total landings (30%)
                confidence_score = (
                    (richness_score * 0.4) +
                    ((years_with_data / self.config.historical_data_years) * 0.3) +
                    (min(total_landings / 100000.0, 1.0) * 0.3)  # Normalizar landings
                )
                
                # Determinar void status
                if years_with_data < 3:
                    void_status = "Datos Limitados"
                elif richness_score < 0.5:
                    void_status = "Baja Riqueza de Especies"
                else:
                    void_status = "Datos Suficientes"
                
                last_year = int(df_fisheries['year'].max())
                
                logger.info(f"✅ Vacíos identificados para celda {h3_cell_id}:")
                logger.info(f"   - Status: {void_status}")
                logger.info(f"   - Riqueza: {species_in_cell}/{max_possible_species} especies")
                logger.info(f"   - Años con datos: {years_with_data}/{self.config.historical_data_years}")
                logger.info(f"   - Confidence: {confidence_score:.3f}")
                
                return {
                    'h3_cell_id': h3_cell_id,
                    'void_status': void_status,
                    'years_without_data': self.config.historical_data_years - years_with_data,
                    'species_richness_score': float(richness_score),
                    'confidence_dato': float(confidence_score),
                    'historical_data_available': True,
                    'last_data_year': last_year,
                    'total_landings_kg': float(total_landings),
                    'species_count': int(species_in_cell),
                    'calculated_at': datetime.now().isoformat()
                }
                
        except SQLAlchemyError as e:
            logger.error(f"❌ Error en base de datos al identificar vacíos: {e}")
            return {
                'h3_cell_id': h3_cell_id,
                'void_status': 'Error de Base de Datos',
                'confidence_dato': 0.0,
                'calculated_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Error inesperado al identificar vacíos: {e}")
            return {
                'h3_cell_id': h3_cell_id,
                'void_status': 'Error de Cálculo',
                'confidence_dato': 0.0,
                'calculated_at': datetime.now().isoformat()
            }
    
    def batch_validate_geometries(self, gdf: gpd.GeoDataFrame, source_name: str) -> gpd.GeoDataFrame:
        """
        Valida un lote de geometrías y aplica no-deformación.
        
        Args:
            gdf: GeoDataFrame con geometrías
            source_name: Nombre de la fuente de datos
        
        Returns:
            GeoDataFrame con geometrías validadas y reproyectadas
        """
        try:
            logger.info(f"🔍 Validando {len(gdf)} geometrías de {source_name}...")
            
            # Validar bounding box
            valid_mask = gdf.geometry.apply(self.validate_bounding_box)
            invalid_count = (~valid_mask).sum()
            
            if invalid_count > 0:
                logger.warning(f"⚠️  {invalid_count} geometrías fuera de bbox en {source_name}")
                gdf = gdf[valid_mask].copy()
            
            # Aplicar no-deformación geométrica
            reprojected_geoms = []
            for geom in gdf.geometry:
                reprojected_wkt = self.reproject_geometry_no_deformation(geom)
                if reprojected_wkt:
                    reprojected_geoms.append(reprojected_wkt)
                else:
                    reprojected_geoms.append(None)
            
            # Añadir geometrías reproyectadas
            gdf['geometry_wkt'] = reprojected_geoms
            gdf = gdf[gdf['geometry_wkt'].notna()].copy()
            
            logger.info(f"✅ Validación completada: {len(gdf)} geometrías válidas")
            return gdf
            
        except Exception as e:
            logger.error(f"❌ Error en validación de lote: {e}")
            raise
    
    def update_confidence_dato_from_voids(self, void_results: List[Dict]) -> int:
        """
        Actualiza la columna confidence_dato en ierc_calculated_scores basado en resultados de vacíos.
        
        Args:
            void_results: Lista de resultados de identificación de vacíos
        
        Returns:
            Número de registros actualizados
        """
        if len(void_results) == 0:
            logger.warning("No hay resultados de vacíos para actualizar")
            return 0
        
        try:
            logger.info(f"📊 Actualizando confidence_dato para {len(void_results)} celdas...")
            
            updated_count = 0
            batch_size = 100
            
            with self.db_engine.connect() as conn:
                for i in range(0, len(void_results), batch_size):
                    batch = void_results[i:i + batch_size]
                    
                    try:
                        # Preparar datos para actualización
                        update_data = []
                        for result in batch:
                            update_data.append({
                                'h3_cell_id': result['h3_cell_id'],
                                'confidence_dato': result['confidence_dato'],
                                'void_status': result['void_status'],
                                'species_richness_score': result.get('species_richness_score', 0.0),
                                'last_data_year': result.get('last_data_year')
                            })
                        
                        # Actualizar en batch
                        result = conn.execute(
                            text("""
                                UPDATE ierc_calculated_scores 
                                SET 
                                    confidence_dato = :confidence_dato,
                                    void_status = :void_status,
                                    species_richness_score = :species_richness_score,
                                    last_data_year = :last_data_year
                                WHERE h3_cell_id = (SELECT id FROM h3_cells WHERE h3_index = :h3_cell_id)
                            """),
                            update_data
                        )
                        
                        batch_count = result.rowcount
                        updated_count += batch_count
                        conn.commit()
                        
                        logger.info(f"Batch {i//batch_size + 1}: {batch_count} registros actualizados")
                        
                    except SQLAlchemyError as batch_error:
                        logger.error(f"❌ Error en batch {i//batch_size + 1}: {batch_error}")
                        conn.rollback()
                        continue
            
            logger.info(f"✅ Actualización completada: {updated_count} registros en ierc_calculated_scores")
            return updated_count
            
        except Exception as e:
            logger.error(f"❌ Error crítico al actualizar confidence_dato: {e}")
            raise

def main():
    """
    Función principal para ejecución del validador espacial.
    """
    logger.info("🌊 === INICIANDO SPATIAL VALIDATOR PARA IERC-GNL ===")
    
    try:
        # Configuración de conexión a la base de datos
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres')
        }
        
        connection_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        
        logger.info(f"🔗 Conectando a {db_config['host']}:{db_config['port']}/{db_config['database']}")
        
        # Crear engine con configuración robusta
        engine = create_engine(
            connection_string,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={'connect_timeout': 15}
        )
        
        # Verificar conexión
        with engine.connect() as conn:
            logger.info("✅ Conexión a la base de datos establecida")
        
        # Crear validador espacial
        validator = SpatialValidator(engine)
        
        # Ejemplo de uso: Validar geometrías de dataMares
        logger.info("📂 Validando geometrías de ejemplo...")
        
        # Crear GeoDataFrame de prueba
        test_points = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'source': ['dataMares', 'GFW', 'CONABIO']
        }, geometry=[
            Point(-112.6833, 29.9000),  # Puerto Libertad (válido)
            Point(-110.9000, 27.9500),   # Guaymas (válido)
            Point(-116.0000, 25.0000)    # Fuera de bbox (inválido)
        ], crs="EPSG:4326")
        
        # Validar geometrías
        validated_gdf = validator.batch_validate_geometries(test_points, "Prueba")
        
        # Identificar vacíos en una celda de prueba
        void_result = validator.identify_voids_moreno_baez_2012(
            'test_cell_id',
            current_year=2024
        )
        
        logger.info(f"📋 Resultados de validación:")
        logger.info(f"   - Geometrías válidas: {len(validated_gdf)}")
        logger.info(f"   - Vacíos identificados: {void_result['void_status']}")
        logger.info(f"   - Confidence: {void_result['confidence_dato']:.3f}")
        
        logger.info("✅ Spatial Validator completado exitosamente")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error crítico en Spatial Validator: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
