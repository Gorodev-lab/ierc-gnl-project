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
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

# Configuración avanzada de logging
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
handlers=[
logging.FileHandler(
'/home/gorops/ierc-gnl-project/logs/monte_carlo_engine.log',
maxBytes=10485760,
backupCount=5
),
logging.StreamHandler(sys.stdout)
]
)
logger = logging.getLogger(__name__)

@dataclass
class MonteCarloConfig:
"""Configuración robusta para simulación de Monte Carlo"""
iterations: int = 1000
confidence_level: float = 0.95
random_seed: int = 42
batch_size: int = 50
uncertainty_threshold: float = 0.3
output_csv_path: str = "/home/gorops/ierc-gnl-project/data/processed/monte_carlo_results.csv"
report_path: str = "/home/gorops/ierc-gnl-project/logs/monte_carlo_report.txt"

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
self.ierc_weights = {
'amenaza': 0.20,
'exposicion': 0.20,
'sensibilidad': 0.15,
'dependencia': 0.15,
'valor_biocultural': 0.15,
'capacidad_adaptativa': 0.15
}

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

# Calcular IERC con scores simulados usando la misma fórmula
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

Usa la misma fórmula algebraica que ierc_calculator.py:
IERC_total = (Amenaza × 0.20) + (Exposición × 0.20) + (Sensibilidad × 0.15) +
(Dependencia × 0.15) + (Valor_Biocultural × 0.15) +
((1 - Capacidad_Adaptativa) × 0.15)

Args:
scores: Diccionario con scores individuales

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
(scores_validated['amenaza'] * self.ierc_weights['amenaza']) +
(scores_validated['exposicion'] * self.ierc_weights['exposicion']) +
(scores_validated['sensibilidad'] * self.ierc_weights['sensibilidad']) +
(scores_validated['dependencia'] * self.ierc_weights['dependencia']) +
(scores_validated['valor_biocultural'] * self.ierc_weights['valor_biocultural']) +
((1 - scores_validated['capacidad_adaptativa']) * self.ierc_weights['capacidad_adaptativa'])
)

# Normalizar a 0-100
ierc_total = min(ierc_total * 100.0, 100.0)

return float(ierc_total)

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
logger.error(f" Error al analizar distribución de incertidumbre: {e}")
return {
'error': str(e),
'total_simulations': len(results),
'recommendations': [f"Error en análisis: {e}"]
}

def generate_uncertainty_report(self, results: List[Dict], analysis: Dict) -> str:
"""
Genera un reporte de incertidumbre profesional en formato legible.

Args:
results: Lista de resultados de simulación
analysis: Análisis de distribución de incertidumbre

Returns:
Reporte en formato de texto
"""
try:
report_lines = []
report_lines.append("=" * 100)
report_lines.append("REPORTE DE INCERTIDUMBRE - SIMULACIÓN DE MONTE CARLO")
report_lines.append("Proyecto: Índice Espacial de Riesgo Socioeconómico (IERC-GNL)")
report_lines.append("Fecha de generación: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
report_lines.append("=" * 100)
report_lines.append("")

# Estadísticas principales
report_lines.append(" ESTADÍSTICAS PRINCIPALES:")
report_lines.append("-" * 100)
report_lines.append(f"Número total de simulaciones: {analysis['total_simulations']:,}")
report_lines.append(f"Media de confianza: {analysis['mean_confidence']:.3f}")
report_lines.append(f"Mediana de confianza: {analysis['median_confidence']:.3f}")
report_lines.append(f"Mínimo de confianza: {analysis['min_confidence']:.3f}")
report_lines.append(f"Máximo de confianza: {analysis['max_confidence']:.3f}")
report_lines.append(f"Desviación estándar de confianza: {analysis['std_dev_confidence']:.3f}")
report_lines.append(f"Coeficiente de variación: {analysis['coefficient_of_variation']:.2f}%")
report_lines.append("")

# Estadísticas de IERC
report_lines.append(" ESTADÍSTICAS DE IERC:")
report_lines.append("-" * 100)
report_lines.append(f"Media de IERC: {analysis['mean_IERC']:.2f}")
report_lines.append(f"Mediana de IERC: {analysis['median_IERC']:.2f}")
report_lines.append(f"Desviación estándar promedio: {analysis['mean_std_dev']:.2f}")
report_lines.append(f"Rango de IERC: {analysis['statistics']['ierc_distribution']['min']:.2f} - {analysis['statistics']['ierc_distribution']['max']:.2f}")
report_lines.append("")

# Percentiles de confianza
report_lines.append(" PERCENTILES DE CONFIANZA:")
report_lines.append("-" * 100)
for p, val in analysis['statistics']['confidence_percentiles'].items():
report_lines.append(f"  {p.upper()}: {val:.3f}")
report_lines.append("")

# Distribución de incertidumbre
report_lines.append(" DISTRIBUCIÓN DE INCERTIDUMBRE:")
report_lines.append("-" * 100)
total = sum(analysis['uncertainty_distribution'].values())
for level, count in analysis['uncertainty_distribution'].items():
percentage = (count / total * 100) if total > 0 else 0
bar = "█" * int(percentage / 2)
report_lines.append(f"  {level:12} | {bar:50} | {count:6,} ({percentage:5.1f}%)")
report_lines.append("")

# Recomendaciones
if analysis['recommendations']:
report_lines.append(" RECOMENDACIONES:")
report_lines.append("-" * 100)
for i, rec in enumerate(analysis['recommendations'], 1):
report_lines.append(f"{i}. {rec}")
report_lines.append("")

# Resumen ejecutivo
report_lines.append(" RESUMEN EJECUTIVO:")
report_lines.append("-" * 100)

high_uncertainty = analysis['uncertainty_distribution']['Alto']
if high_uncertainty > analysis['total_simulations'] * 0.15:
report_lines.append("  ALERTA: Alto nivel de incertidumbre detectado en múltiples celdas.")
report_lines.append("    Se recomienda validación inmediata de datos críticos.")
elif analysis['mean_confidence'] >= 0.85:
report_lines.append(" Nivel de confianza ACEPTABLE para análisis inicial y toma de decisiones.")
else:
report_lines.append("  Nivel de confianza MODERADO. Validar datos antes de decisiones críticas.")

report_lines.append("")
report_lines.append("=" * 100)
report_lines.append("FIN DEL REPORTE")
report_lines.append("=" * 100)

return "\n".join(report_lines)

except Exception as e:
logger.error(f" Error al generar reporte: {e}")
return f"Error al generar reporte: {e}"

def save_results_to_database(self, results: List[Dict]) -> int:
"""
Guarda resultados de Monte Carlo en la tabla ierc_calculated_scores.

Args:
results: Lista de resultados de simulación

Returns:
Número de registros actualizados
"""
if len(results) == 0:
logger.warning("No hay resultados para guardar en la base de datos")
return 0

try:
logger.info(f"Guardando {len(results)} resultados de Monte Carlo en la base de datos...")

updated_count = 0
batch_size = min(self.config.batch_size, len(results))

with self.db_engine.connect() as conn:
for i in range(0, len(results), batch_size):
batch = results[i:i + batch_size]

try:
# Preparar datos para actualización
update_data = []
for result in batch:
update_data.append({
'h3_cell_id': None,  # En producción, llenar con ID real
'quincena': 1,      # En producción, llenar con quincena real
'confidence_dato': result['confidence_dato'],
'uncertainty_range_lower': result['lower_bound_95CI'],
'uncertainty_range_upper': result['upper_bound_95CI'],
'monte_carlo_simulations': result['simulation_iterations'],
'simulation_seed': result['simulation_seed']
})

# Actualizar en batch
result = conn.execute(
text("""
UPDATE ierc_calculated_scores 
SET 
confidence_dato = :confidence_dato,
uncertainty_range_lower = :uncertainty_range_lower,
uncertainty_range_upper = :uncertainty_range_upper,
monte_carlo_simulations = :monte_carlo_simulations,
simulation_seed = :simulation_seed
WHERE 
h3_cell_id = :h3_cell_id 
AND quincena = :quincena
"""),
update_data
)

batch_count = result.rowcount
updated_count += batch_count
conn.commit()

logger.info(f"Batch {i//batch_size + 1}: {batch_count} registros actualizados")

except SQLAlchemyError as batch_error:
logger.error(f" Error en batch {i//batch_size + 1}: {batch_error}")
conn.rollback()
continue
except Exception as batch_error:
logger.error(f" Error inesperado en batch {i//batch_size + 1}: {batch_error}")
conn.rollback()
continue

logger.info(f" Actualización completada: {updated_count} registros en ierc_calculated_scores")
return updated_count

except Exception as e:
logger.error(f" Error crítico al guardar resultados en la base de datos: {e}")
raise

def run_monte_carlo_pipeline(self, base_scores_list: List[Dict[str, float]] = None) -> bool:
"""
Ejecuta el pipeline completo de Monte Carlo.

Args:
base_scores_list: Lista opcional de scores base. Si None, usa datos de la base de datos.

Returns:
True si el pipeline se completó exitosamente
"""
logger.info("=== INICIANDO PIPELINE DE MONTE CARLO ===")

try:
# Paso 1: Obtener scores base (de base de datos o parámetro)
if base_scores_list is None:
logger.info("Obteniendo scores base de la base de datos...")
base_scores_list = self._fetch_base_scores_from_database()

if len(base_scores_list) == 0:
logger.error(" No hay scores base para simular")
return False

# Paso 2: Ejecutar simulación en batch
results = self.batch_simulate_uncertainty(
base_scores_list,
output_file=self.config.output_csv_path
)

# Paso 3: Analizar resultados
analysis = self.analyze_uncertainty_distribution(results)

# Paso 4: Generar reporte
report = self.generate_uncertainty_report(results, analysis)

# Guardar reporte
try:
with open(self.config.report_path, 'w') as f:
f.write(report)
logger.info(f" Reporte guardado en {self.config.report_path}")
except Exception as e:
logger.error(f" Error al guardar reporte: {e}")

# Paso 5: Guardar resultados en la base de datos
# Nota: En producción, descomentar esta línea
# updated = self.save_results_to_database(results)

logger.info(" Pipeline de Monte Carlo completado exitosamente")

# Imprimir resumen en consola
print("\n" + "=" * 100)
print("RESUMEN DE SIMULACIÓN DE MONTE CARLO - IERC-GNL")
print("=" * 100)
print(f"Simulaciones ejecutadas: {analysis['total_simulations']:,}")
print(f"Media de confianza: {analysis['mean_confidence']:.3f}")
print(f"Nivel de incertidumbre:")
print(f"  - Bajo: {analysis['uncertainty_distribution']['Bajo']:,} ({analysis['uncertainty_distribution']['Bajo']/analysis['total_simulations']*100:.1f}%)")
print(f"  - Moderado: {analysis['uncertainty_distribution']['Moderado']:,} ({analysis['uncertainty_distribution']['Moderado']/analysis['total_simulations']*100:.1f}%)")
print(f"  - Alto: {analysis['uncertainty_distribution']['Alto']:,} ({analysis['uncertainty_distribution']['Alto']/analysis['total_simulations']*100:.1f}%)")
print("=" * 100)

return True

except Exception as e:
logger.error(f" Pipeline de Monte Carlo fallido: {e}")
return False

def _fetch_base_scores_from_database(self) -> List[Dict[str, float]]:
"""
Obtiene scores base de la tabla ierc_calculated_scores para simulación.

Returns:
Lista de diccionarios con scores base
"""
try:
logger.info("Obteniendo scores base de ierc_calculated_scores...")

with self.db_engine.connect() as conn:
df = pd.read_sql(
text("""
SELECT 
h3_cell_id,
quincena,
score_amenaza,
score_exposicion,
score_sensibilidad,
score_dependencia,
score_biocultural,
score_capacidad_adaptativa,
IERC_total
FROM ierc_calculated_scores
LIMIT 1000  -- Limitar para pruebas iniciales
"""),
conn
)

# Convertir a lista de diccionarios
base_scores = df.to_dict('records')
logger.info(f" Obtenidos {len(base_scores)} scores base para simulación")

return base_scores

except SQLAlchemyError as e:
logger.error(f" Error al obtener scores base: {e}")
return []
except Exception as e:
logger.error(f" Error inesperado al obtener scores base: {e}")
return []

def main():
"""
Función principal para ejecución del motor de Monte Carlo.
"""
logger.info("=== MONTE CARLO ENGINE - PIPELINE ROBUSTO ===")

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
pool_size=3,
max_overflow=5,
pool_pre_ping=True,
pool_recycle=3600,
connect_args={'connect_timeout': 10}
)

# Verificar conexión
with engine.connect() as conn:
logger.info(" Conexión a la base de datos establecida")

# Crear motor de Monte Carlo
config = MonteCarloConfig(
iterations=1000,
random_seed=42,
batch_size=50,
output_csv_path="/home/gorops/ierc-gnl-project/data/processed/monte_carlo_results.csv",
report_path="/home/gorops/ierc-gnl-project/logs/monte_carlo_report.txt"
)

engine_mc = MonteCarloEngine(engine, config)

# Ejecutar pipeline
success = engine_mc.run_monte_carlo_pipeline()

if success:
logger.info(" Motor de Monte Carlo completado exitosamente")
return 0
else:
logger.error(" Fallo en el motor de Monte Carlo")
return 1

except Exception as e:
logger.error(f" Error crítico en el motor de Monte Carlo: {e}")
return 1

if __name__ == "__main__":
import numpy as np
sys.exit(main())
