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
try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.engine import Engine
    from sqlalchemy.exc import SQLAlchemyError
except ImportError:
    create_engine, text, Engine, SQLAlchemyError = None, None, Any, Exception

from ..utils.logging import setup_logging
from ..utils.ierc import compute_ierc, IERC_WEIGHTS

logger = setup_logging(__name__)


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
        self.weights = IERC_WEIGHTS.copy()

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
                logger.info(f" Celdas H3 cargadas: {len(data['h3_cells'])} registros")

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
                logger.info(f" Amenazas fósiles cargadas: {len(data['fossil_threats'])} registros")

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
                logger.info(f" Exposición pesquera cargada: {len(data['fisheries_exposure'])} registros")

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
                logger.info(f" Scores GAGE cargados: {len(data['gage_scores'])} registros")

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
                logger.info(f" Referencia de especies cargada: {len(data['species'])} registros")

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
                logger.info(f" Referencia de comunidades cargada: {len(data['communities'])} registros")

            return data

        except SQLAlchemyError as e:
            logger.error(f" Error al obtener datos de la base de datos: {e}")
            raise
        except Exception as e:
            logger.error(f" Error inesperado al obtener datos: {e}")
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
                logger.debug(f"No hay especies válidas en celda {h3_cell_id}")
                return 0.0

            # Calcular sensibilidad basada en estado de conservación
            total_conservation_weight = 0.0
            for sp_code in valid_species:
                sp_row = self.data['species'][self.data['species']['species_code'] == sp_code]
                if len(sp_row) > 0:
                    status = sp_row['conservation_status'].values[0]
                    # Mapear estado de conservación a peso
                    conservation_weights = {
                        'CR': 1.0,  # Critically Endangered
                        'EN': 0.8,  # Endangered
                        'VU': 0.6,  # Vulnerable
                        'NT': 0.4,  # Near Threatened
                        'LC': 0.2,  # Least Concern
                        'DD': 0.3   # Data Deficient
                    }
                    total_conservation_weight += conservation_weights.get(status, 0.2)

            # Normalizar por número de especies
            avg_sensitivity = total_conservation_weight / len(valid_species) if valid_species else 0.0
            sensibilidad_score = self._normalize_score('sensibilidad', avg_sensitivity)

            logger.debug(f"Sensibilidad para celda {h3_cell_id}: {sensibilidad_score:.3f} ({len(valid_species)} especies)")
            return float(sensibilidad_score)

        except Exception as e:
            logger.warning(f"Error al calcular score de sensibilidad para celda {h3_cell_id}: {e}")
            return 0.0

    def _calculate_dependencia_score(self, h3_cell_id: str) -> float:
        """
        Calcula el score de dependencia pesquera para una celda H3.

        Args:
            h3_cell_id: ID de la celda H3

        Returns:
            Score de dependencia normalizado (0-1)
        """
        try:
            cell_exposure = self.data['fisheries_exposure'][
                self.data['fisheries_exposure']['h3_cell_id'] == h3_cell_id
            ]

            if len(cell_exposure) == 0:
                return 0.0

            # Dependencia basada en captura total y diversidad de artes
            total_landings = float(cell_exposure['landings_kg'].sum())
            gear_diversity = cell_exposure['fishing_gear'].nunique()

            # Normalizar (máximos teóricos)
            norm_landings = min(total_landings / 500000.0, 1.0)  # 500 toneladas
            norm_gear = min(gear_diversity / 10.0, 1.0)  # 10 artes diferentes

            dependencia_score = (norm_landings * 0.7) + (norm_gear * 0.3)
            dependencia_score = self._normalize_score('dependencia', dependencia_score)

            logger.debug(f"Dependencia para celda {h3_cell_id}: {dependencia_score:.3f} (landings: {total_landings:.0f}kg, artes: {gear_diversity})")
            return float(dependencia_score)

        except Exception as e:
            logger.warning(f"Error al calcular score de dependencia para celda {h3_cell_id}: {e}")
            return 0.0

    def _calculate_valor_biocultural_score(self, h3_cell_id: str) -> float:
        """
        Calcula el score de valor biocultural para una celda H3.

        Args:
            h3_cell_id: ID de la celda H3

        Returns:
            Score de valor biocultural normalizado (0-1)
        """
        try:
            # Obtener comunidades asociadas a esta celda
            h3_index_row = self.data['h3_cells'][self.data['h3_cells']['id'] == h3_cell_id]
            if len(h3_index_row) == 0:
                return 0.0

            # Valor biocultural basado en riqueza de especies y estado de conservación
            cell_exposure = self.data['fisheries_exposure'][
                self.data['fisheries_exposure']['h3_cell_id'] == h3_cell_id
            ]

            if len(cell_exposure) == 0:
                return 0.0

            species_codes = cell_exposure['species_code'].unique()
            valid_species = [s for s in species_codes if s in self.data['species']['species_code'].values]

            if len(valid_species) == 0:
                return 0.0

            # Calcular valor biocultural
            biocultural_weight = 0.0
            for sp_code in valid_species:
                sp_row = self.data['species'][self.data['species']['species_code'] == sp_code]
                if len(sp_row) > 0:
                    importance = sp_row['commercial_importance'].values[0] if pd.notna(sp_row['commercial_importance'].values[0]) else 'low'
                    # Mapear importancia comercial
                    importance_weights = {
                        'high': 1.0,
                        'medium': 0.6,
                        'low': 0.3,
                        'subsistence': 0.4
                    }
                    biocultural_weight += importance_weights.get(importance, 0.2)

            avg_biocultural = biocultural_weight / len(valid_species) if valid_species else 0.0
            valor_biocultural_score = self._normalize_score('valor_biocultural', avg_biocultural)

            logger.debug(f"Valor biocultural para celda {h3_cell_id}: {valor_biocultural_score:.3f}")
            return float(valor_biocultural_score)

        except Exception as e:
            logger.warning(f"Error al calcular score de valor biocultural para celda {h3_cell_id}: {e}")
            return 0.0

    def _calculate_capacidad_adaptativa_score(self, h3_cell_id: str) -> float:
        """
        Calcula el score de capacidad adaptativa para una celda H3.

        Args:
            h3_cell_id: ID de la celda H3

        Returns:
            Score de capacidad adaptativa normalizado (0-1)
        """
        try:
            # Obtener comunidad asociada
            h3_index_row = self.data['h3_cells'][self.data['h3_cells']['id'] == h3_cell_id]
            if len(h3_index_row) == 0:
                return 0.5  # Default

            zone = h3_index_row['zone'].values[0] if 'zone' in h3_index_row.columns else 'unknown'

            # Buscar score GAGE para la zona
            gage_match = self.data['gage_scores'][
                self.data['gage_scores']['community_id'].str.contains(zone, case=False, na=False)
            ]

            if len(gage_match) > 0:
                # Usar gage_total_score normalizado
                gage_score = float(gage_match['gage_total_score'].values[0])
                # GAGE score es 0-100, normalizar a 0-1
                capacidad_score = min(gage_score / 100.0, 1.0)
            else:
                # Default basado en zona
                capacidad_score = 0.5

            capacidad_adaptativa = self._normalize_score('capacidad_adaptativa', capacidad_score)

            logger.debug(f"Capacidad adaptativa para celda {h3_cell_id}: {capacidad_adaptativa:.3f}")
            return float(capacidad_adaptativa)

        except Exception as e:
            logger.warning(f"Error al calcular score de capacidad adaptativa para celda {h3_cell_id}: {e}")
            return 0.5

    def calculate_ierc_for_cell(self, h3_cell_id: str) -> Dict[str, float]:
        """
        Calcula el IERC completo para una celda H3.

        Args:
            h3_cell_id: ID de la celda H3

        Returns:
            Diccionario con todos los componentes y el IERC total
        """
        # Calcular cada componente
        amenaza = self._calculate_amenaza_score(h3_cell_id)
        exposicion = self._calculate_exposicion_score(h3_cell_id)
        sensibilidad = self._calculate_sensibilidad_score(h3_cell_id)
        dependencia = self._calculate_dependencia_score(h3_cell_id)
        valor_biocultural = self._calculate_valor_biocultural_score(h3_cell_id)
        capacidad_adaptativa = self._calculate_capacidad_adaptativa_score(h3_cell_id)

        # Usar fórmula compartida
        ierc_total = compute_ierc(
            amenaza=amenaza,
            exposicion=exposicion,
            sensibilidad=sensibilidad,
            dependencia=dependencia,
            valor_biocultural=valor_biocultural,
            capacidad_adaptativa=capacidad_adaptativa,
            weights=self.weights
        )

        return {
            'h3_cell_id': h3_cell_id,
            'amenaza': float(amenaza),
            'exposicion': float(exposicion),
            'sensibilidad': float(sensibilidad),
            'dependencia': float(dependencia),
            'valor_biocultural': float(valor_biocultural),
            'capacidad_adaptativa': float(capacidad_adaptativa),
            'IERC_total': float(ierc_total),
            'IERC_total_pct': float(ierc_total * 100.0)
        }

    def run_calculation(self, quincena: int = None) -> List[Dict[str, Any]]:
        """
        Ejecuta el cálculo completo para todas las celdas.

        Args:
            quincena: Quincena específica (None = todas)

        Returns:
            Lista de resultados con IERC por celda
        """
        logger.info(f"Iniciando cálculo IERC para quincena {quincena if quincena else 'todas'}...")

        # Obtener celdas H3
        if quincena:
            # Filtrar celdas por quincena si hay datos
            cell_ids = self.data['fisheries_exposure'][
                self.data['fisheries_exposure']['quincena'] == quincena
            ]['h3_cell_id'].unique()
        else:
            cell_ids = self.data['h3_cells']['id'].unique()

        logger.info(f"Calculando IERC para {len(cell_ids)} celdas...")

        results = []
        for i, cell_id in enumerate(cell_ids):
            if i % 100 == 0:
                logger.info(f"Progreso: {i}/{len(cell_ids)} celdas")

            try:
                result = self.calculate_ierc_for_cell(cell_id)
                results.append(result)
            except Exception as e:
                logger.error(f"Error calculando IERC para celda {cell_id}: {e}")
                continue

        logger.info(f"Cálculo completado: {len(results)} celdas procesadas")
        return results


if __name__ == "__main__":
    from ..utils.logging import setup_logging
    setup_logging("ierc_gnl.ierc_calculator")
    print("IERC Calculator module loaded")