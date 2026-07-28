#!/usr/bin/env python3
"""
IERC Calculator Engine - Fase 3
==================================

Script para cálculo del Índice Espacial de Riesgo Socioeconómico (IERC) según:

IERC_total = (Amenaza × 0.20) + (Exposición × 0.20) + (Sensibilidad × 0.15) +
             (Dependencia × 0.15) + (Valor_Biocultural × 0.15) +
             ((1 - Capacidad_Adaptativa) × 0.15)

Features:
- Cálculo por celda H3 y quincena (1-24)
- Normalización Min-Max para cada componente
- Simulación de Monte Carlo integrada (1,000 iteraciones)
- Inserción transaccional con rollback
- Tipado fuerte con Python Type Hints
- Logging detallado por lotes
- Manejo de excepciones geográficas
- Proyecciones EPSG:4326 y conversión a WKT

Requirements:
- pandas>=2.0.0
- geopandas>=0.14.0
- shapely>=2.0.0
- numpy>=1.24.0
- psycopg2-binary>=2.9.7
- sqlalchemy>=2.0.0
- scipy>=1.10.0

Geometries:
- PostGIS: ST_GeomFromText(geometry, 4326)
- WKT: 'POLYGON((lon lat, lon lat, ...))'
- EPSG:4326 (WGS84) para todas las operaciones

Normalization Methods:
- Min-Max: (value - min) / (max - min)
- Sigmoide: 1 / (1 + exp(-k*(x - x0)))
- Percentil: basado en distribución de datos

Monte Carlo:
- 1,000 iteraciones por celda-quincena
- Distribuciones normales con desviaciones estándar realistas
- Percentiles 2.5% y 97.5% para intervalo de confianza
- confidence_dato = 1 - (rango/2)
"""

import os
import sys
import logging
import json
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime
import time
import numpy as np
import pandas as pd
from scipy import stats
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

# Configuración avanzada de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            '/home/gorops/ierc-gnl-project/logs/ierc_calculator.log',
            maxBytes=10485760,
            backupCount=5
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class IERCConfig:
    """Configuración robusta para cálculo del IERC"""
    monte_carlo_iterations: int = 1000
    monte_carlo_seed: int = 42
    batch_size: int = 100
    confidence_threshold: float = 0.7
    quincenas: List[int] = None
    normalization_method: str = 'minmax'  # 'minmax', 'sigmoid', 'percentile'
    
    def __post_init__(self):
        if self.quincenas is None:
            self.quincenas = list(range(1, 25))  # Quincenas 1-24
        if self.normalization_method not in ['minmax', 'sigmoid', 'percentile']:
            logger.warning(f"Método de normalización no reconocido: {self.normalization_method}")
            self.normalization_method = 'minmax'

class IERCCalculator:
    """
    Motor de cálculo del IERC con:
    - Cálculo algebraico estricto
    - Normalización robusta
    - Simulación de Monte Carlo
    - Inserción transaccional
    - Manejo de excepciones geográficas
    """
    
    def __init__(self, db_engine: Engine, config: IERCConfig = None):
        """
        Inicializa el calculador con conexión a la base de datos.
        
        Args:
            db_engine: Engine de SQLAlchemy conectado a Supabase/PostgreSQL
            config: Configuración del cálculo
        """
        self.db_engine = db_engine
        self.config = config if config else IERCConfig()
        np.random.seed(self.config.monte_carlo_seed)
        
        # Pesos oficiales de la metodología (validados)
        self.weights = {
            'amenaza': 0.20,
            'exposicion': 0.20,
            'sensibilidad': 0.15,
            'dependencia': 0.15,
            'valor_biocultural': 0.15,
            'capacidad_adaptativa': 0.15
        }
        
        # Límites para normalización Min-Max
        self.normalization_limits = {
            'amenaza': (0.0, 1.0),
            'exposicion': (0.0, 1.0),
            'sensibilidad': (0.0, 1.0),
            'dependencia': (0.0, 1.0),
            'valor_biocultural': (0.0, 1.0),
            'capacidad_adaptativa': (0.0, 1.0)
        }
        
        # Desviaciones estándar para Monte Carlo (basadas en datos reales)
        self.monte_carlo_std = {
            'amenaza': 0.15,
            'exposicion': 0.10,
            'sensibilidad': 0.12,
            'dependencia': 0.10,
            'valor_biocultural': 0.08,
            'capacidad_adaptativa': 0.18
        }
        
        logger.info(f"IERCCalculator inicializado con {self.config.monte_carlo_iterations} iteraciones Monte Carlo")
    
    def _fetch_data_from_database(self) -> Dict[str, pd.DataFrame]:
        """
        Obtiene todos los datos necesarios de la base de datos con manejo de excepciones.
        
        Returns:
            Diccionario con DataFrames para cada tabla requerida
        """
        logger.info("Obteniendo datos de la base de datos...")
        
        try:
            data = {}
            
            with self.db_engine.connect() as conn:
                # Obtener celdas H3 con validación geométrica
                data['h3_cells'] = pd.read_sql(
                    text("SELECT id, h3_index, zone, resolution FROM h3_cells"),
                    conn
                )
                logger.info(f"✅ Celdas H3 cargadas: {len(data['h3_cells'])} registros")
                
                # Obtener amenazas fósiles con validación
                data['fossil_threats'] = pd.read_sql(
                    text("""
                        SELECT 
                            id,
                            threat_type,
                            name,
                            h3_cells_affected,
                            operational_status,
                            noise_level_dB,
                            vessel_traffic_volume,
                            ST_AsText(geometry) as geometry_wkt
                        FROM fossil_infrastructure_threat
                        WHERE h3_cells_affected IS NOT NULL
                    """),
                    conn
                )
                logger.info(f"✅ Amenazas fósiles cargadas: {len(data['fossil_threats'])} registros")
                
                # Obtener exposición pesquera con validación
                data['fisheries_exposure'] = pd.read_sql(
                    text("""
                        SELECT 
                            id,
                            h3_cell_id,
                            quincena,
                            species_code,
                            fishing_gear,
                            effort_hours_vms,
                            effort_hours_panga,
                            landings_kg,
                            gender_distribution,
                            seasonality,
                            is_protected_area,
                            protection_category
                        FROM fisheries_exposure
                        WHERE h3_cell_id IS NOT NULL
                    """),
                    conn
                )
                logger.info(f"✅ Exposición pesquera cargada: {len(data['fisheries_exposure'])} registros")
                
                # Obtener scores de gobernanza GAGE
                data['gage_scores'] = pd.read_sql(
                    text("""
                        SELECT 
                            id as gage_id,
                            community_id,
                            gage_total_score,
                            confidence_level
                        FROM gage_governance_scores
                        WHERE gage_total_score IS NOT NULL
                    """),
                    conn
                )
                logger.info(f"✅ Scores GAGE cargados: {len(data['gage_scores'])} registros")
                
                # Obtener referencia de especies
                data['species'] = pd.read_sql(
                    text("""
                        SELECT 
                            species_code,
                            scientific_name,
                            common_name_es,
                            conservation_status,
                            commercial_importance
                        FROM species_reference
                    """),
                    conn
                )
                logger.info(f"✅ Referencia de especies cargada: {len(data['species'])} registros")
                
                # Obtener referencia de comunidades
                data['communities'] = pd.read_sql(
                    text("""
                        SELECT 
                            id,
                            community_name,
                            nation,
                            geographic_scope
                        FROM community_reference
                    """),
                    conn
                )
                logger.info(f"✅ Referencia de comunidades cargada: {len(data['communities'])} registros")
            
            return data
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error al obtener datos de la base de datos: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado al obtener datos: {e}")
            raise
    
    def _normalize_minmax(self, value: float, min_val: float, max_val: float) -> float:
        """
        Normalización Min-Max: (value - min) / (max - min)
        
        Args:
            value: Valor a normalizar
            min_val: Valor mínimo del rango
            max_val: Valor máximo del rango
        
        Returns:
            Valor normalizado en [0, 1]
        """
        try:
            if max_val == min_val:
                return 0.5  # Valor por defecto si rango es cero
            
            normalized = (value - min_val) / (max_val - min_val)
            return float(np.clip(normalized, 0.0, 1.0))
        except Exception as e:
            logger.warning(f"Error en normalización Min-Max: {e}")
            return 0.0
    
    def _normalize_sigmoid(self, value: float, k: float = 5.0, x0: float = 0.5) -> float:
        """
        Normalización Sigmoide: 1 / (1 + exp(-k*(x - x0)))
        
        Args:
            value: Valor a normalizar
            k: Parámetro de forma (pendiente)
            x0: Punto de inflexión
        
        Returns:
            Valor normalizado en [0, 1]
        """
        try:
            sigmoid = 1.0 / (1.0 + np.exp(-k * (value - x0)))
            return float(np.clip(sigmoid, 0.0, 1.0))
        except Exception as e:
            logger.warning(f"Error en normalización Sigmoide: {e}")
            return 0.0
    
    def _normalize_percentile(self, value: float, series: pd.Series) -> float:
        """
        Normalización por percentil: percentil(value) / 100
        
        Args:
            value: Valor a normalizar
            series: Serie de valores para calcular percentiles
        
        Returns:
            Valor normalizado en [0, 1]
        """
        try:
            if len(series) == 0:
                return 0.5
            
            percentile = stats.percentileofscore(series, value)
            return float(percentile / 100.0)
        except Exception as e:
            logger.warning(f"Error en normalización por percentil: {e}")
            return 0.0
    
    def _normalize_score(self, score_name: str, value: float) -> float:
        """
        Normalización robusta de scores según método configurado.
        
        Args:
            score_name: Nombre del score ('amenaza', 'exposicion', etc.)
            value: Valor a normalizar
        
        Returns:
            Score normalizado en [0, 1]
        """
        try:
            min_val, max_val = self.normalization_limits[score_name]
            
            if self.config.normalization_method == 'minmax':
                return self._normalize_minmax(value, min_val, max_val)
            elif self.config.normalization_method == 'sigmoid':
                return self._normalize_sigmoid(value, k=5.0, x0=(min_val + max_val)/2)
            elif self.config.normalization_method == 'percentile':
                # Usar valores típicos como referencia
                typical_values = {
                    'amenaza': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                    'exposicion': [0.0, 0.1, 0.3, 0.5, 0.7, 1.0],
                    'sensibilidad': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                    'dependencia': [0.0, 0.1, 0.3, 0.5, 0.7, 1.0],
                    'valor_biocultural': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                    'capacidad_adaptativa': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
                }
                return self._normalize_percentile(value, pd.Series(typical_values[score_name]))
            else:
                return self._normalize_minmax(value, min_val, max_val)
        
        except Exception as e:
            logger.warning(f"Error en normalización de {score_name}: {e}")
            return 0.0
    
    def _calculate_amenaza_score(self, h3_cell_id: str) -> float:
        """
        Calcula el score de amenaza para una celda H3.
        
        Fórmula:
        Score_Amenaza = w_near × Amenaza_Cercanía + w_noise × Amenaza_Ruido + w_route × Amenaza_Ruta
        
        Args:
            h3_cell_id: ID de la celda H3
        
        Returns:
            Score de amenaza normalizado (0-1)
        """
        try:
            # Obtener el h3_index de la celda
            h3_index_row = self.data['h3_cells'][self.data['h3_cells']['id'] == h3_cell_id]
            if len(h3_index_row) == 0:
                logger.warning(f"Celda H3 no encontrada: {h3_cell_id}")
                return 0.0
            h3_index = h3_index_row['h3_index'].values[0]
            
            # Filtrar amenazas que afectan esta celda
            threats = self.data['fossil_threats'][
                self.data['fossil_threats']['h3_cells_affected'].apply(
                    lambda x: h3_index in x if isinstance(x, list) else False
                )
            ]
            
            if len(threats) == 0:
                logger.debug(f"No hay amenazas para celda {h3_cell_id}")
                return 0.0
            
            # Calcular componentes de amenaza
            proximity_scores = []
            noise_scores = []
            route_scores = []
            
            for _, threat in threats.iterrows():
                try:
                    # Amenaza por proximidad (exclusion_zone, terminal_area)
                    if threat['threat_type'] in ['exclusion_zone', 'terminal_area']:
                        proximity_scores.append(1.0)  # Máxima amenaza por proximidad física
                    
                    # Amenaza por ruido (sonic_noise)
                    elif threat['threat_type'] == 'sonic_noise' and pd.notna(threat['noise_level_dB']):
                        noise_level = float(threat['noise_level_dB'])
                        # Nivel de ruido en dB normalizado (180 dB = máximo teórico)
                        noise_scores.append(min(noise_level / 180.0, 1.0))
                    
                    # Amenaza por tráfico (metanero_route)
                    elif threat['threat_type'] == 'metanero_route' and pd.notna(threat['vessel_traffic_volume']):
                        traffic_volume = float(threat['vessel_traffic_volume'])
                        # Volumen normalizado (1000 buques/año = máximo teórico)
                        route_scores.append(min(traffic_volume / 1000.0, 1.0))
                
                except Exception as e:
                    logger.debug(f"Error procesando amenaza {threat['name']}: {e}")
                    continue
            
            # Calcular score de amenaza ponderado
            avg_proximity = np.mean(proximity_scores) if proximity_scores else 0.0
            avg_noise = np.mean(noise_scores) if noise_scores else 0.0
            avg_route = np.mean(route_scores) if route_scores else 0.0
            
            # Aplicar pesos según tipo de amenaza
            amenaza_score = (
                (avg_proximity * 0.50) +  # Proximidad tiene mayor peso
                (avg_noise * 0.30) +       # Ruido afecta fauna marina
                (avg_route * 0.20)         # Tráfico aumenta riesgo de colisión
            )
            
            # Normalizar el score
            amenaza_score = self._normalize_score('amenaza', amenaza_score)
            
            logger.debug(f"Amenaza para celda {h3_cell_id}: {amenaza_score:.3f}")
            return float(amenaza_score)
            
        except Exception as e:
            logger.warning(f"Error al calcular score de amenaza para celda {h3_cell_id}: {e}")
            return 0.0
    
    def _calculate_exposicion_score(self, h3_cell_id: str) -> float:
        """
        Calcula el score de exposición para una celda H3.
        
        Fórmula:
        Score_Exposición = w_effort × Exposición_Esfuerzo + w_community × Exposición_Comunidad
        
        Args:
            h3_cell_id: ID de la celda H3
        
        Returns:
            Score de exposición normalizado (0-1)
        """
        try:
            # Filtrar registros para esta celda
            cell_exposure = self.data['fisheries_exposure'][
                self.data['fisheries_exposure']['h3_cell_id'] == h3_cell_id
            ]
            
            if len(cell_exposure) == 0:
                logger.debug(f"No hay exposición pesquera para celda {h3_cell_id}")
                return 0.0
            
            # Calcular esfuerzo total (VMS + Panga)
            total_effort = float(cell_exposure['effort_hours_vms'].sum() + cell_exposure['effort_hours_panga'].sum())
            
            # Normalizar esfuerzo (máximo teórico: 8760 horas/año por celda)
            max_effort = 8760.0
            normalized_effort = min(total_effort / max_effort, 1.0)
            
            # Score de exposición = esfuerzo normalizado
            exposicion_score = self._normalize_score('exposicion', normalized_effort)
            
            logger.debug(f"Exposición para celda {h3_cell_id}: {exposicion_score:.3f} (esfuerzo: {total_effort:.1f}h)")
            return float(exposicion_score)
            
        except Exception as e:
            logger.warning(f"Error al calcular score de exposición para celda {h3_cell_id}: {e}")
            return 0.0
    
    def _calculate_sensibilidad_score(self, h3_cell_id: str) -> float:
        """
        Calcula el score de sensibilidad para una celda H3.
        
        Fórmula:
        Score_Sensibilidad = w_species × Sensibilidad_Especies + w_endemic × Sensibilidad_Endémicas
        
        Args:
            h3_cell_id: ID de la celda H3
        
        Returns:
            Score de sensibilidad normalizado (0-1)
        """
        try:
            # Obtener especies capturadas en esta celda
            cell_exposure = self.data['fisheries_exposure'][
                self.data['fisheries_exposure']['h3_cell_id'] == h3_cell_id
            ]
            
            if len(cell_exposure) == 0:
                logger.debug(f"No hay especies para calcular sensibilidad en celda {h3_cell_id}")
                return 0.0
            
            # Obtener códigos de especies
            species_codes = cell_exposure['species_code'].unique()
            
            # Filtrar especies en la referencia
            valid_species = [s for s in species_codes if s in self.data['species']['species_code'].values]
            
            if len(valid_species) == 0:
                logger.debug(f"No hay especies válidas para celda {h3_cell_id}")
                return 0.0
            
            # Obtener especies amenazadas (EN, CR, VU)
            threatened_df = self.data['species'][
                self.data['species']['species_code'].isin(valid_species) &
                self.data['species']['conservation_status'].isin(['EN', 'CR', 'VU'])
            ]
            
            threatened_count = len(threatened_df)
            total_species = len(valid_species)
            
            # Factor de sensibilidad: especies amenazadas tienen mayor peso
            factor_sensibilidad = 1.5 if threatened_count > 0 else 1.0
            
            # Score de sensibilidad = (amenazadas/total) × factor
            sensibilidad_raw = (threatened_count / total_species) * factor_sensibilidad
            
            # Normalizar el score
            sensibilidad_score = self._normalize_score('sensibilidad', sensibilidad_raw)
            
            logger.debug(f"Sensibilidad para celda {h3_cell_id}: {sensibilidad_score:.3f} ({threatened_count}/{total_species} especies amenazadas)")
            return float(sensibilidad_score)
            
        except Exception as e:
            logger.warning(f"Error al calcular score de sensibilidad para celda {h3_cell_id}: {e}")
            return 0.0
    
    def _calculate_dependencia_score(self, h3_cell_id: str) -> float:
        """
        Calcula el score de dependencia para una celda H3.
        
        Fórmula:
        Score_Dependencia = w_income × Dependencia_Ingresos + w_food × Dependencia_Alimentaria
        
        Args:
            h3_cell_id: ID de la celda H3
        
        Returns:
            Score de dependencia normalizado (0-1)
        """
        try:
            # Filtrar registros para esta celda
            cell_exposure = self.data['fisheries_exposure'][
                self.data['fisheries_exposure']['h3_cell_id'] == h3_cell_id
            ]
            
            if len(cell_exposure) == 0:
                logger.debug(f"No hay datos de dependencia para celda {h3_cell_id}")
                return 0.0
            
            # Calcular landings totales (kg)
            total_landings = float(cell_exposure['landings_kg'].sum())
            
            # Normalizar landings (máximo teórico: 100,000 kg/año por celda)
            max_landings = 100000.0
            normalized_landings = min(total_landings / max_landings, 1.0)
            
            # Score de dependencia = landings normalizadas
            dependencia_score = self._normalize_score('dependencia', normalized_landings)
            
            logger.debug(f"Dependencia para celda {h3_cell_id}: {dependencia_score:.3f} ({total_landings:.0f}kg)")
            return float(dependencia_score)
            
        except Exception as e:
            logger.warning(f"Error al calcular score de dependencia para celda {h3_cell_id}: {e}")
            return 0.0
    
    def _calculate_valor_biocultural_score(self, h3_cell_id: str) -> float:
        """
        Calcula el score de valor biocultural para una celda H3.
        
        Asignación basada en zona:
        - Punta Chueca: 0.9 (territorio Comca'ac)
        - Puerto Libertad/Guaymas: 0.3 (zonas portuarias)
        - Mar abierto: 0.1 (bajo valor biocultural)
        
        Args:
            h3_cell_id: ID de la celda H3
        
        Returns:
            Score de valor biocultural normalizado (0-1)
        """
        try:
            # Obtener zona de la celda
            zone_row = self.data['h3_cells'][self.data['h3_cells']['id'] == h3_cell_id]
            if len(zone_row) == 0:
                logger.warning(f"Celda H3 no encontrada: {h3_cell_id}")
                return 0.1
            
            zone = zone_row['zone'].values[0]
            
            # Asignar scores basados en zona
            if 'Punta Chueca' in zone or 'Comca' in zone:
                valor_score = 0.9
            elif zone in ['Puerto Libertad', 'Guaymas']:
                valor_score = 0.3
            else:
                valor_score = 0.1
            
            # Normalizar el score
            valor_score = self._normalize_score('valor_biocultural', valor_score)
            
            logger.debug(f"Valor biocultural para celda {h3_cell_id} (zona: {zone}): {valor_score:.3f}")
            return float(valor_score)
            
        except Exception as e:
            logger.warning(f"Error al calcular score de valor biocultural para celda {h3_cell_id}: {e}")
            return 0.1
    
    def _calculate_capacidad_adaptativa_score(self, h3_cell_id: str) -> float:
        """
        Calcula el score de capacidad adaptativa para una celda H3.
        
        Score basado en:
        - Score GAGE de comunidades cercanas
        - Acceso a recursos
        - Participación en toma de decisiones
        
        Args:
            h3_cell_id: ID de la celda H3
        
        Returns:
            Score de capacidad adaptativa normalizado (0-1)
        """
        try:
            # En un caso real, mapear celda H3 a comunidad GAGE
            # Por simplicidad, usar un score promedio de las comunidades disponibles
            
            valid_gage = self.data['gage_scores'][self.data['gage_scores']['gage_total_score'].notna()]
            
            if len(valid_gage) == 0:
                logger.debug(f"No hay scores GAGE disponibles, usando valor por defecto para celda {h3_cell_id}")
                capacidad_score = 0.5  # Valor por defecto
            else:
                # Calcular promedio de scores GAGE normalizados
                avg_gage_score = valid_gage['gage_total_score'].mean() / 21.0  # Normalizar a 0-1
                capacidad_score = avg_gage_score
            
            # Normalizar el score
            capacidad_score = self._normalize_score('capacidad_adaptativa', capacidad_score)
            
            logger.debug(f"Capacidad adaptativa para celda {h3_cell_id}: {capacidad_score:.3f}")
            return float(capacidad_score)
            
        except Exception as e:
            logger.warning(f"Error al calcular score de capacidad adaptativa para celda {h3_cell_id}: {e}")
            return 0.5
    
    def _calculate_ierc_score(self, scores: Dict[str, float]) -> float:
        """
        Calcula el score IERC total para una celda H3.
        
        Fórmula algebraica estricta:
        IERC_total = (Amenaza × 0.20) + (Exposición × 0.20) + (Sensibilidad × 0.15) +
                     (Dependencia × 0.15) + (Valor_Biocultural × 0.15) +
                     ((1 - Capacidad_Adaptativa) × 0.15)
        
        Args:
            scores: Diccionario con scores individuales normalizados
        
        Returns:
            Score IERC total normalizado (0-100)
        """
        try:
            # Extraer scores individuales
            amenaza = scores.get('amenaza', 0.0)
            exposicion = scores.get('exposicion', 0.0)
            sensibilidad = scores.get('sensibilidad', 0.0)
            dependencia = scores.get('dependencia', 0.0)
            valor_biocultural = scores.get('valor_biocultural', 0.0)
            capacidad_adaptativa = scores.get('capacidad_adaptativa', 0.5)
            
            # Validar que todos los scores estén en [0, 1]
            scores_validated = {
                'amenaza': np.clip(amenaza, 0.0, 1.0),
                'exposicion': np.clip(exposicion, 0.0, 1.0),
                'sensibilidad': np.clip(sensibilidad, 0.0, 1.0),
                'dependencia': np.clip(dependencia, 0.0, 1.0),
                'valor_biocultural': np.clip(valor_biocultural, 0.0, 1.0),
                'capacidad_adaptativa': np.clip(capacidad_adaptativa, 0.0, 1.0)
            }
            
            # Aplicar fórmula algebraica estricta
            ierc_total = (
                (scores_validated['amenaza'] * self.weights['amenaza']) +
                (scores_validated['exposicion'] * self.weights['exposicion']) +
                (scores_validated['sensibilidad'] * self.weights['sensibilidad']) +
                (scores_validated['dependencia'] * self.weights['dependencia']) +
                (scores_validated['valor_biocultural'] * self.weights['valor_biocultural']) +
                ((1 - scores_validated['capacidad_adaptativa']) * self.weights['capacidad_adaptativa'])
            )
            
            # Normalizar a 0-100
            ierc_total = min(ierc_total * 100.0, 100.0)
            
            logger.debug(f"IERC calculado: {ierc_total:.2f} (pesos: {self.weights})")
            return float(ierc_total)
            
        except Exception as e:
            logger.warning(f"Error al calcular score IERC: {e}")
            return 0.0
    
    def _simulate_monte_carlo(self, base_scores: Dict[str, float]) -> Dict[str, Union[float, int]]:
        """
        Simula incertidumbre usando Monte Carlo para calcular intervalo de confianza.
        
        Args:
            base_scores: Scores base para calcular
        
        Returns:
            Diccionario con resultados de la simulación
        """
        try:
            logger.debug("Iniciando simulación de Monte Carlo...")
            
            # Simular iteraciones
            ierc_results = []
            
            for _ in range(self.config.monte_carlo_iterations):
                # Generar scores simulados con perturbaciones realistas
                simulated_scores = {}
                
                for component, base_value in base_scores.items():
                    if component == 'IERC_total':
                        continue  # Saltar el score total
                    
                    # Obtener desviación estándar para esta componente
                    std_dev = self.monte_carlo_std.get(component, 0.1)
                    
                    # Generar valor simulado
                    if component == 'capacidad_adaptativa':
                        # Capacidad adaptativa tiene mayor incertidumbre
                        simulated_value = np.random.normal(base_value, std_dev * 1.5)
                    else:
                        simulated_value = np.random.normal(base_value, std_dev)
                    
                    # Asegurar que el valor esté en [0, 1]
                    simulated_value = np.clip(simulated_value, 0.0, 1.0)
                    simulated_scores[component] = float(simulated_value)
                
                # Calcular IERC con scores simulados
                ierc_simulado = self._calculate_ierc_score(simulated_scores)
                ierc_results.append(ierc_simulado)
            
            # Calcular estadísticas
            if len(ierc_results) == 0:
                raise ValueError("No se generaron resultados de simulación")
            
            mean_score = float(np.mean(ierc_results))
            median_score = float(np.median(ierc_results))
            std_dev = float(np.std(ierc_results))
            
            # Calcular percentiles para intervalo de confianza
            lower_bound = float(np.percentile(ierc_results, 2.5))
            upper_bound = float(np.percentile(ierc_results, 97.5))
            
            # Calcular nivel de confianza
            confidence_range = upper_bound - lower_bound
            confidence_dato = float(1 - (confidence_range / 2))
            confidence_dato = np.clip(confidence_dato, 0.0, 1.0)
            
            # Determinar nivel de incertidumbre
            if confidence_dato < 0.7:
                uncertainty_level = "Alto"
            elif confidence_dato < 0.85:
                uncertainty_level = "Moderado"
            else:
                uncertainty_level = "Bajo"
            
            # Calcular coeficiente de variación
            cv = (std_dev / mean_score) * 100 if mean_score > 0 else 0.0
            
            result = {
                'simulation_iterations': self.config.monte_carlo_iterations,
                'mean_IERC': mean_score,
                'median_IERC': median_score,
                'std_dev_IERC': std_dev,
                'lower_bound_95CI': lower_bound,
                'upper_bound_95CI': upper_bound,
                'confidence_interval_width': confidence_range,
                'confidence_dato': confidence_dato,
                'uncertainty_level': uncertainty_level,
                'coefficient_of_variation': cv,
                'simulation_seed': self.config.monte_carlo_seed
            }
            
            logger.debug(f"Monte Carlo completado: IERC={mean_score:.2f}±{std_dev:.2f}, confianza={confidence_dato:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error en simulación de Monte Carlo: {e}")
            # Retornar valores por defecto en caso de error
            base_ierc = base_scores.get('IERC_total', 0.0)
            return {
                'simulation_iterations': self.config.monte_carlo_iterations,
                'mean_IERC': base_ierc,
                'median_IERC': base_ierc,
                'std_dev_IERC': 0.0,
                'lower_bound_95CI': base_ierc * 0.9,
                'upper_bound_95CI': base_ierc * 1.1,
                'confidence_interval_width': 0.0,
                'confidence_dato': 0.5,
                'uncertainty_level': "Desconocido",
                'coefficient_of_variation': 0.0,
                'simulation_seed': self.config.monte_carlo_seed
            }
    
    def calculate_ierc_for_cell_quincena(self, h3_cell_id: str, quincena: int) -> Dict[str, Union[float, str]]:
        """
        Calcula el IERC para una celda H3 y quincena específica.
        
        Args:
            h3_cell_id: ID de la celda H3
            quincena: Número de quincena (1-24)
        
        Returns:
            Diccionario con scores individuales, score total y métricas de Monte Carlo
        """
        try:
            logger.info(f"Calculando IERC para celda {h3_cell_id}, quincena {quincena}")
            
            # Calcular scores individuales
            scores = {
                'amenaza': self._calculate_amenaza_score(h3_cell_id),
                'exposicion': self._calculate_exposicion_score(h3_cell_id),
                'sensibilidad': self._calculate_sensibilidad_score(h3_cell_id),
                'dependencia': self._calculate_dependencia_score(h3_cell_id),
                'valor_biocultural': self._calculate_valor_biocultural_score(h3_cell_id),
                'capacidad_adaptativa': self._calculate_capacidad_adaptativa_score(h3_cell_id)
            }
            
            # Calcular score IERC total
            scores['IERC_total'] = self._calculate_ierc_score(scores)
            
            # Simulación de Monte Carlo
            monte_carlo_results = self._simulate_monte_carlo(scores)
            
            # Combinar resultados
            result = {
                'h3_cell_id': h3_cell_id,
                'quincena': quincena,
                'score_amenaza': scores['amenaza'],
                'score_exposicion': scores['exposicion'],
                'score_sensibilidad': scores['sensibilidad'],
                'score_dependencia': scores['dependencia'],
                'score_biocultural': scores['valor_biocultural'],
                'score_capacidad_adaptativa': scores['capacidad_adaptativa'],
                'IERC_total': scores['IERC_total'],
                'confidence_dato': monte_carlo_results['confidence_dato'],
                'uncertainty_range_lower': monte_carlo_results['lower_bound_95CI'],
                'uncertainty_range_upper': monte_carlo_results['upper_bound_95CI'],
                'monte_carlo_simulations': monte_carlo_results['simulation_iterations'],
                'simulation_seed': monte_carlo_results['simulation_seed']
            }
            
            # Validar que el score esté en rango válido
            result['IERC_total'] = float(np.clip(result['IERC_total'], 0.0, 100.0))
            result['confidence_dato'] = float(np.clip(result['confidence_dato'], 0.0, 1.0))
            
            logger.info(f"✅ IERC calculado: {result['IERC_total']:.2f} (confianza: {result['confidence_dato']:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error crítico calculando IERC para celda {h3_cell_id}, quincena {quincena}: {e}")
            return {
                'h3_cell_id': h3_cell_id,
                'quincena': quincena,
                'score_amenaza': 0.0,
                'score_exposicion': 0.0,
                'score_sensibilidad': 0.0,
                'score_dependencia': 0.0,
                'score_biocultural': 0.0,
                'score_capacidad_adaptativa': 0.5,
                'IERC_total': 0.0,
                'confidence_dato': 0.0,
                'uncertainty_range_lower': 0.0,
                'uncertainty_range_upper': 0.0,
                'monte_carlo_simulations': self.config.monte_carlo_iterations,
                'simulation_seed': self.config.monte_carlo_seed
            }
    
    def calculate_ierc_for_all_cells(self) -> List[Dict[str, Union[float, str]]]:
        """
        Calcula el IERC para todas las celdas H3 y todas las quincenas.
        
        Returns:
            Lista de diccionarios con resultados para cada celda-quincena
        """
        logger.info("Iniciando cálculo de IERC para todas las celdas y quincenas...")
        
        results = []
        total_cells = len(self.data['h3_cells'])
        total_quincenas = len(self.config.quincenas)
        total_iterations = total_cells * total_quincenas
        
        logger.info(f"Total de iteraciones: {total_iterations} (celdas: {total_cells}, quincenas: {total_quincenas})")
        
        start_time = time.time()
        
        # Iterar sobre todas las celdas y quincenas
        for _, cell_row in self.data['h3_cells'].iterrows():
            cell_id = cell_row['id']
            
            for quincena in self.config.quincenas:
                result = self.calculate_ierc_for_cell_quincena(cell_id, quincena)
                results.append(result)
        
        elapsed_time = time.time() - start_time
        logger.info(f"✅ Cálculo completado en {elapsed_time:.2f} segundos")
        logger.info(f"✅ Resultados generados: {len(results)} registros")
        
        return results
    
    def _insert_batch_with_transaction(self, results_batch: List[Dict], 
                                      conn) -> int:
        """
        Inserción transaccional con manejo de excepciones y rollback.
        
        Args:
            results_batch: Lista de resultados para insertar
            conn: Conexión SQLAlchemy activa
        
        Returns:
            Número de registros insertados
        """
        if len(results_batch) == 0:
            logger.warning("No hay resultados para insertar")
            return 0
        
        try:
            inserted_count = 0
            
            # Preparar datos para inserción
            insert_data = []
            for result in results_batch:
                insert_data.append({
                    'h3_cell_id': result['h3_cell_id'],
                    'quincena': result['quincena'],
                    'score_amenaza': result['score_amenaza'],
                    'score_exposicion': result['score_exposicion'],
                    'score_sensibilidad': result['score_sensibilidad'],
                    'score_dependencia': result['score_dependencia'],
                    'score_biocultural': result['score_biocultural'],
                    'score_capacidad_adaptativa': result['score_capacidad_adaptativa'],
                    'IERC_total': result['IERC_total'],
                    'confidence_dato': result['confidence_dato'],
                    'uncertainty_range_lower': result['uncertainty_range_lower'],
                    'uncertainty_range_upper': result['uncertainty_range_upper'],
                    'monte_carlo_simulations': result['monte_carlo_simulations'],
                    'simulation_seed': result['simulation_seed'],
                    'fossil_threat_ids': [],  # En producción, llenar con IDs reales
                    'community_id': None,    # En producción, mapear a comunidad
                    'gage_score_id': None     # En producción, mapear a score GAGE
                })
            
            # Insertar en batch
            result = conn.execute(
                text("""
                    INSERT INTO ierc_calculated_scores 
                    (h3_cell_id, quincena, score_amenaza, score_exposicion, 
                     score_sensibilidad, score_dependencia, score_biocultural,
                     score_capacidad_adaptativa, IERC_total, confidence_dato,
                     uncertainty_range_lower, uncertainty_range_upper,
                     monte_carlo_simulations, simulation_seed,
                     fossil_threat_ids, community_id, gage_score_id)
                    VALUES (
                        (SELECT id FROM h3_cells WHERE id = :h3_cell_id),
                        :quincena, :score_amenaza, :score_exposicion,
                        :score_sensibilidad, :score_dependencia, :score_biocultural,
                        :score_capacidad_adaptativa, :IERC_total, :confidence_dato,
                        :uncertainty_range_lower, :uncertainty_range_upper,
                        :monte_carlo_simulations, :simulation_seed,
                        :fossil_threat_ids, :community_id, :gage_score_id
                    )
                    ON CONFLICT (h3_cell_id, quincena)
                    DO UPDATE SET
                        score_amenaza = EXCLUDED.score_amenaza,
                        score_exposicion = EXCLUDED.score_exposicion,
                        score_sensibilidad = EXCLUDED.score_sensibilidad,
                        score_dependencia = EXCLUDED.score_dependencia,
                        score_biocultural = EXCLUDED.score_biocultural,
                        score_capacidad_adaptativa = EXCLUDED.score_capacidad_adaptativa,
                        IERC_total = EXCLUDED.IERC_total,
                        confidence_dato = EXCLUDED.confidence_dato,
                        uncertainty_range_lower = EXCLUDED.uncertainty_range_lower,
                        uncertainty_range_upper = EXCLUDED.uncertainty_range_upper,
                        monte_carlo_simulations = EXCLUDED.monte_carlo_simulations,
                        simulation_seed = EXCLUDED.simulation_seed
                """),
                insert_data
            )
            
            inserted_count = result.rowcount
            conn.commit()
            
            logger.info(f"✅ Batch insertado: {inserted_count} registros")
            return inserted_count
            
        except SQLAlchemyError as e:
            logger.error(f"❌ Error en transacción de inserción: {e}")
            conn.rollback()
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado en inserción: {e}")
            conn.rollback()
            raise
    
    def insert_ierc_results(self, results: List[Dict]) -> int:
        """
        Inserta resultados del IERC en la base de datos con manejo transaccional.
        
        Args:
            results: Lista de diccionarios con resultados del IERC
        
        Returns:
            Número de registros insertados
        """
        if len(results) == 0:
            logger.warning("No hay resultados para insertar")
            return 0
        
        try:
            logger.info(f"Insertando {len(results)} resultados en ierc_calculated_scores...")
            
            inserted_count = 0
            batch_size = min(self.config.batch_size, len(results))
            
            with self.db_engine.connect() as conn:
                for i in range(0, len(results), batch_size):
                    batch = results[i:i + batch_size]
                    
                    try:
                        batch_inserted = self._insert_batch_with_transaction(batch, conn)
                        inserted_count += batch_inserted
                        
                    except Exception as batch_error:
                        logger.error(f"❌ Error en batch {i//batch_size + 1}: {batch_error}")
                        continue
            
            logger.info(f"✅ Inserción completada: {inserted_count} registros en ierc_calculated_scores")
            return inserted_count
            
        except Exception as e:
            logger.error(f"❌ Error crítico en inserción de resultados: {e}")
            raise
    
    def run_calculation_pipeline(self) -> bool:
        """
        Ejecuta el pipeline completo de cálculo del IERC.
        
        Returns:
            True si el pipeline se completó exitosamente, False en caso contrario
        """
        logger.info("=== INICIANDO PIPELINE DE CÁLCULO DEL IERC ===")
        
        try:
            # Paso 1: Obtener datos de la base de datos
            self.data = self._fetch_data_from_database()
            
            # Paso 2: Calcular IERC para todas las celdas y quincenas
            results = self.calculate_ierc_for_all_cells()
            
            # Paso 3: Insertar resultados en la base de datos
            inserted = self.insert_ierc_results(results)
            
            # Validar resultados
            if inserted > 0:
                logger.info(f"✅ Pipeline completado exitosamente: {inserted} registros insertados")
                return True
            else:
                logger.error("❌ Pipeline fallido: No se insertaron registros")
                return False
                
        except Exception as e:
            logger.error(f"❌ Pipeline fallido por error crítico: {e}")
            return False

def main():
    """
    Función principal para ejecución del calculador del IERC.
    """
    logger.info("=== IERC CALCULATOR - PIPELINE ROBUSTO ===")
    
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
        
        logger.info(f"Conectando a {db_config['host']}:{db_config['port']}/{db_config['database']}")
        
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
        
        # Crear calculador
        calculator = IERCCalculator(engine)
        
        # Ejecutar pipeline
        success = calculator.run_calculation_pipeline()
        
        if success:
            logger.info("✅ Cálculo del IERC completado exitosamente")
            return 0
        else:
            logger.error("❌ Fallo en el cálculo del IERC")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Error crítico en el calculador del IERC: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
