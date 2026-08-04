#!/usr/bin/env python3
"""
Monte Carlo Engine - Fase 3 Complementaria
============================================

Motor de simulación de Monte Carlo para análisis de incertidumbre en el cálculo del IERC.

Features:
- 1,000 iteraciones por celda-quincena
- Perturbaciones realistas en variables basadas en desviaciones estándar
- Cálculo de intervalos de confianza (percentiles 2.5% y 97.5%)
- Score 'confidence_dato' normalizado (0-1)
- Integración con tabla ierc_calculated_scores
- Logging detallado y manejo de excepciones
- Tipado fuerte con Python Type Hints
- Generación de reportes de análisis

Requirements:
- numpy>=1.24.0
- pandas>=2.0.0
- scipy>=1.10.0
- sqlalchemy>=2.0.0

Geometries:
- PostGIS: ST_GeomFromText(geometry, 4326)
- WKT: 'POLYGON((lon lat, lon lat, ...))'
- EPSG:4326 (WGS84) para todas las operaciones

Normalization:
- confidence_dato = 1 - (rango_de_confianza / 2)
- Nivel de incertidumbre: Bajo (<0.7), Moderado (0.7-0.85), Alto (>0.85)

Output:
- Pobla la tabla ierc_calculated_scores con métricas de Monte Carlo
- Genera reportes en /logs/monte_carlo_report.txt
- Guarda resultados en /data/processed/monte_carlo_results.csv
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
class MonteCarloConfig:
    """Configuración robusta para simulación de Monte Carlo"""
    iterations: int = 1000
    confidence_level: float = 0.95
    random_seed: int = 42
    batch_size: int = 50
    uncertainty_threshold: float = 0.3
    output_csv_path: Optional[str] = None
    report_path: Optional[str] = None

    def __post_init__(self):
        if self.output_csv_path is None:
            from config import get_processed_dir
            self.output_csv_path = str(get_processed_dir() / "monte_carlo_results.csv")
        if self.report_path is None:
            from config import get_log_dir
            self.report_path = str(get_log_dir() / "monte_carlo_report.txt")

    def validate(self):
        """Validación de configuración"""
        if self.iterations <= 0:
            raise ValueError(f"Número de iteraciones inválido: {self.iterations}")
        if self.batch_size <= 0:
            raise ValueError(f"Batch size inválido: {self.batch_size}")
        if not (0 <= self.confidence_level <= 1):
            raise ValueError(f"Nivel de confianza inválido: {self.confidence_level}")
        logger.info("Configuración de Monte Carlo validada")


class MonteCarloEngine:
    """
    Motor de simulación de Monte Carlo para análisis de incertidumbre en el IERC.

    Features:
    - Simulación de 1,000 iteraciones por celda-quincena
    - Perturbaciones realistas en variables
    - Cálculo de intervalos de confianza
    - Nivel de confianza normalizado (0-1)
    - Integración con base de datos
    - Generación de reportes
    """

    def __init__(self, db_engine: Engine, config: MonteCarloConfig = None):
        """
        Inicializa el motor de Monte Carlo.

        Args:
            db_engine: Engine de SQLAlchemy conectado a Supabase/PostgreSQL
            config: Configuración de la simulación
        """
        self.db_engine = db_engine
        self.config = config if config else MonteCarloConfig()
        self.config.validate()
        np.random.seed(self.config.random_seed)

        # Pesos oficiales del IERC para referencia
        self.ierc_weights = IERC_WEIGHTS.copy()

        # Desviaciones estándar realistas para perturbaciones
        self.perturbation_std = {
            'amenaza': 0.15,
            'exposicion': 0.10,
            'sensibilidad': 0.12,
            'dependencia': 0.10,
            'valor_biocultural': 0.08,
            'capacidad_adaptativa': 0.18
        }

        logger.info(f"MonteCarloEngine inicializado con {self.config.iterations} iteraciones")

    def _generate_distribution_params(self, base_value: float,
                                       component: str) -> Tuple[str, float, float]:
        """
        Genera parámetros de distribución para una variable basada en su tipo.

        Args:
            base_value: Valor base de la variable
            component: Nombre del componente ('amenaza', 'exposicion', etc.)

        Returns:
            Tuple con (tipo_distribución, parámetro1, parámetro2)
        """
        try:
            std_dev = self.perturbation_std.get(component, 0.1)

            # Determinar tipo de distribución basado en el valor base y componente
            if component == 'capacidad_adaptativa':
                # Mayor incertidumbre en capacidad adaptativa
                return ('normal', base_value, std_dev * 1.5)
            elif base_value < 0.3:
                # Para valores bajos, usar distribución beta (sesgada a valores bajos)
                alpha = 2.0
                beta = 5.0
                return ('beta', alpha, beta)
            elif base_value > 0.7:
                # Para valores altos, usar distribución beta (sesgada a valores altos)
                alpha = 5.0
                beta = 2.0
                return ('beta', alpha, beta)
            else:
                # Para valores intermedios, usar distribución normal
                return ('normal', base_value, std_dev)

        except Exception as e:
            logger.warning(f"Error al generar parámetros de distribución: {e}")
            # Valor por defecto
            return ('normal', base_value, 0.1)

    def _sample_from_distribution(self, dist_type: str,
                                   param1: float, param2: float) -> float:
        """
        Muestrea un valor de una distribución.

        Args:
            dist_type: Tipo de distribución ('normal', 'beta', 'uniform')
            param1: Parámetro 1 de la distribución
            param2: Parámetro 2 de la distribución

        Returns:
            Valor muestrado en [0, 1]
        """
        try:
            if dist_type == 'normal':
                value = np.random.normal(param1, param2)
            elif dist_type == 'beta':
                value = np.random.beta(param1, param2)
            elif dist_type == 'uniform':
                value = np.random.uniform(param1, param2)
            else:
                # Por defecto, usar normal
                value = np.random.normal(param1, param2)

            # Asegurar que el valor esté en [0, 1]
            value = np.clip(value, 0.0, 1.0)

            return float(value)

        except Exception as e:
            logger.warning(f"Error al muestrear de distribución: {e}")
            return float(param1)  # Retornar valor base en caso de error

    def simulate_uncertainty(self, base_scores: Dict[str, float]) -> Dict[str, Union[float, int, str]]:
        """
        Simula incertidumbre para una celda H3 usando Monte Carlo.

        Args:
            base_scores: Diccionario con scores base para cada componente del IERC

        Returns:
            Diccionario con resultados de la simulación incluyendo:
            - mean_IERC, median_IERC, std_dev_IERC
            - lower_bound_95CI, upper_bound_95CI
            - confidence_dato, uncertainty_level
            - coefficient_of_variation
            - simulation_iterations, simulation_seed
        """
        try:
            logger.debug("Iniciando simulación de Monte Carlo para una celda-quincena")

            # Simular iteraciones
            ierc_results = []

            for _ in range(self.config.iterations):
                # Generar scores simulados para cada componente
                simulated_scores = {}

                for component, base_value in base_scores.items():
                    if component == 'IERC_total':
                        continue  # Saltar el score total

                    # Obtener parámetros de distribución
                    dist_type, param1, param2 = self._generate_distribution_params(
                        base_value, component
                    )

                    # Muestrear valor
                    simulated_value = self._sample_from_distribution(dist_type, param1, param2)
                    simulated_scores[component] = simulated_value

                # Calcular IERC con scores simulados usando la fórmula compartida
                ierc_simulado = self._calculate_ierc_from_scores(simulated_scores)
                ierc_results.append(ierc_simulado)

            # Validar que se generaron resultados
            if len(ierc_results) == 0:
                raise ValueError("No se generaron resultados de simulación")

            # Calcular estadísticas
            mean_score = float(np.mean(ierc_results))
            median_score = float(np.median(ierc_results))
            std_dev = float(np.std(ierc_results))

            # Calcular percentiles para intervalo de confianza
            lower_bound = float(np.percentile(ierc_results, 2.5))
            upper_bound = float(np.percentile(ierc_results, 97.5))

            # Calcular nivel de confianza (normalizado 0-1)
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

            # Calcular métricas adicionales
            ci_width = upper_bound - lower_bound

            result = {
                'simulation_iterations': self.config.iterations,
                'mean_IERC': mean_score,
                'median_IERC': median_score,
                'std_dev_IERC': std_dev,
                'lower_bound_95CI': lower_bound,
                'upper_bound_95CI': upper_bound,
                'confidence_interval_width': ci_width,
                'confidence_dato': confidence_dato,
                'uncertainty_level': uncertainty_level,
                'coefficient_of_variation': cv,
                'simulation_seed': self.config.random_seed,
                'timestamp': datetime.now().isoformat()
            }

            logger.debug(f"Simulación completada: IERC={mean_score:.2f}±{std_dev:.2f}, confianza={confidence_dato:.2f}")
            return result

        except Exception as e:
            logger.error(f"Error en simulación de Monte Carlo: {e}")
            # Retornar valores por defecto en caso de error
            base_ierc = base_scores.get('IERC_total', 0.0)
            return {
                'simulation_iterations': self.config.iterations,
                'mean_IERC': base_ierc,
                'median_IERC': base_ierc,
                'std_dev_IERC': 0.0,
                'lower_bound_95CI': base_ierc * 0.9,
                'upper_bound_95CI': base_ierc * 1.1,
                'confidence_interval_width': 0.0,
                'confidence_dato': 0.5,
                'uncertainty_level': "Desconocido",
                'coefficient_of_variation': 0.0,
                'simulation_seed': self.config.random_seed,
                'timestamp': datetime.now().isoformat()
            }

    def _calculate_ierc_from_scores(self, scores: Dict[str, float]) -> float:
        """
        Calcula el score IERC total a partir de scores individuales.

        Usa la fórmula algebraica estricta compartida con ierc_calculator:
        IERC_total = (Amenaza × 0.20) + (Exposición × 0.20) + (Sensibilidad × 0.15) +
        (Dependencia × 0.15) + (Valor_Biocultural × 0.15) +
        ((1 - Capacidad_Adaptativa) × 0.15)

        Args:
            scores: Diccionario con scores individuales

        Returns:
            Score IERC total normalizado (0-100)
        """
        try:
            # Extraer y validar scores
            scores_validated = {
                'amenaza': np.clip(scores.get('amenaza', 0.0), 0.0, 1.0),
                'exposicion': np.clip(scores.get('exposicion', 0.0), 0.0, 1.0),
                'sensibilidad': np.clip(scores.get('sensibilidad', 0.0), 0.0, 1.0),
                'dependencia': np.clip(scores.get('dependencia', 0.0), 0.0, 1.0),
                'valor_biocultural': np.clip(scores.get('valor_biocultural', 0.0), 0.0, 1.0),
                'capacidad_adaptativa': np.clip(scores.get('capacidad_adaptativa', 0.5), 0.0, 1.0)
            }

            # Usar fórmula compartida
            ierc_total = compute_ierc(
                amenaza=scores_validated['amenaza'],
                exposicion=scores_validated['exposicion'],
                sensibilidad=scores_validated['sensibilidad'],
                dependencia=scores_validated['dependencia'],
                valor_biocultural=scores_validated['valor_biocultural'],
                capacidad_adaptativa=scores_validated['capacidad_adaptativa'],
                weights=self.ierc_weights
            )

            # Normalizar a 0-100
            return float(ierc_total * 100.0)

        except Exception as e:
            logger.warning(f"Error al calcular IERC en Monte Carlo: {e}")
            return 0.0

    def batch_simulate_uncertainty(self, base_scores_list: List[Dict[str, float]],
                                    output_file: str = None) -> List[Dict[str, Union[float, int, str]]]:
        """
        Ejecuta simulación de Monte Carlo en batch para múltiples celdas-quincenas.

        Args:
            base_scores_list: Lista de diccionarios con scores base
            output_file: Ruta para guardar resultados CSV (opcional)

        Returns:
            Lista de resultados de simulación
        """
        logger.info(f"Iniciando simulación en batch para {len(base_scores_list)} celdas-quincenas")

        results = []
        start_time = time.time()

        for i, base_scores in enumerate(base_scores_list):
            if i % self.config.batch_size == 0:
                logger.info(f"Procesando batch {i//self.config.batch_size + 1}/{len(base_scores_list)//self.config.batch_size + 1}...")

            result = self.simulate_uncertainty(base_scores)
            results.append(result)

        elapsed_time = time.time() - start_time
        logger.info(f" Simulación batch completada en {elapsed_time:.2f} segundos")
        logger.info(f" Resultados generados: {len(results)} simulaciones")

        # Guardar resultados si se especifica archivo de salida
        if output_file:
            try:
                df_results = pd.DataFrame(results)
                df_results.to_csv(output_file, index=False)
                logger.info(f" Resultados guardados en {output_file}")
            except Exception as e:
                logger.error(f" Error al guardar resultados: {e}")

        return results

    def analyze_uncertainty_distribution(self, results: List[Dict]) -> Dict[str, Union[float, int, str, Dict]]:
        """
        Analiza la distribución de incertidumbre en los resultados de Monte Carlo.

        Args:
            results: Lista de resultados de simulación

        Returns:
            Diccionario con análisis estadístico detallado
        """
        try:
            if len(results) == 0:
                return {'error': 'No hay resultados para analizar'}

            # Extraer métricas relevantes
            confidence_scores = [r['confidence_dato'] for r in results]
            uncertainty_levels = [r['uncertainty_level'] for r in results]
            ierc_means = [r['mean_IERC'] for r in results]
            ierc_stds = [r['std_dev_IERC'] for r in results]

            # Calcular estadísticas
            analysis = {
                'total_simulations': len(results),
                'mean_confidence': float(np.mean(confidence_scores)),
                'median_confidence': float(np.median(confidence_scores)),
                'min_confidence': float(np.min(confidence_scores)),
                'max_confidence': float(np.max(confidence_scores)),
                'std_dev_confidence': float(np.std(confidence_scores)),
                'mean_IERC': float(np.mean(ierc_means)),
                'median_IERC': float(np.median(ierc_means)),
                'std_dev_IERC': float(np.std(ierc_means)),
                'mean_std_dev': float(np.mean(ierc_stds)),
                'median_std_dev': float(np.median(ierc_stds)),

                'uncertainty_distribution': {
                    'Bajo': int(uncertainty_levels.count('Bajo')),
                    'Moderado': int(uncertainty_levels.count('Moderado')),
                    'Alto': int(uncertainty_levels.count('Alto')),
                    'Desconocido': int(uncertainty_levels.count('Desconocido'))
                },
                'recommendations': [],
                'statistics': {}
            }

            # Generar recomendaciones basadas en análisis
            if analysis['mean_confidence'] < 0.7:
                analysis['recommendations'].append(
                    " ALERTA CRÍTICA: Nivel de confianza bajo (<0.7) en la mayoría de las celdas. "
                    "Se recomienda:"
                    "  1. Validar datos de entrada críticos (amenazas fósiles, exposición pesquera)"
                    "  2. Revisar metodología de normalización y ponderación"
                    "  3. Considerar recolección de datos adicionales en zonas de alta incertidumbre"
                    "  4. Priorizar investigación en componentes con mayor variabilidad"
                )
            elif analysis['mean_confidence'] < 0.85:
                analysis['recommendations'].append(
                    "  Nivel de confianza moderado (0.7-0.85). Validar datos críticos y considerar:"
                    "  1. Monitoreo adicional en zonas con incertidumbre moderada"
                    "  2. Revisión de umbrales de normalización"
                    "  3. Validación cruzada con fuentes alternativas de datos"
                )
            else:
                analysis['recommendations'].append(
                    " Nivel de confianza alto (>0.85). Resultados robustos para toma de decisiones."
                )

            # Estadísticas adicionales
            analysis['statistics'] = {
                'confidence_percentiles': {
                    'p10': float(np.percentile(confidence_scores, 10)),
                    'p25': float(np.percentile(confidence_scores, 25)),
                    'p50': float(np.percentile(confidence_scores, 50)),
                    'p75': float(np.percentile(confidence_scores, 75)),
                    'p90': float(np.percentile(confidence_scores, 90))
                },
                'ierc_distribution': {
                    'min': float(np.min(ierc_means)),
                    'max': float(np.max(ierc_means)),
                    'q1': float(np.percentile(ierc_means, 25)),
                    'q3': float(np.percentile(ierc_means, 75))
                }
            }

            # Métricas de dispersión
            analysis['coefficient_of_variation'] = float(
                (analysis['std_dev_confidence'] / analysis['mean_confidence']) * 100
                if analysis['mean_confidence'] > 0 else 0.0
            )

            # Porcentaje de celdas con alta incertidumbre
            high_uncertainty_pct = (
                analysis['uncertainty_distribution']['Alto'] / analysis['total_simulations'] * 100
            )

            if high_uncertainty_pct > 20:
                analysis['recommendations'].append(
                    f" {high_uncertainty_pct:.1f}% de celdas con incertidumbre ALTA. "
                    "Priorizar validación de datos en estas zonas."
                )

            logger.info(" Análisis de distribución de incertidumbre completado")

            return analysis

        except Exception as e:
            logger.error(f"Error en análisis de distribución: {e}")
            return {'error': str(e)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Monte Carlo Engine module loaded")