"""
Test Suite for IERC-GNL Data Pipeline
=======================================

Suite de pruebas unitarias con pytest para validar:
- h3_indexer.py: Conversión de coordenadas y manejo de excepciones
- ierc_calculator.py: Fórmula algebraica y normalización
- monte_carlo_engine.py: Simulación de Monte Carlo

Features:
- Datasets sintéticos que imitan estructura real
- Validación de excepciones controladas
- Pruebas de fórmula matemática
- Pruebas de rendimiento y estabilidad
- Tipado fuerte con Python Type Hints
- Logging detallado

Requirements:
- pytest>=7.0.0
- pandas>=2.0.0
- geopandas>=0.14.0
- numpy>=1.24.0
- shapely>=2.0.0
- h3>=3.7.6
"""

import os
import sys
import pytest
import logging
import json
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path
import tempfile
import math

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
import numpy as np

# Configurar logging para pruebas
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
handlers=[
logging.FileHandler('/home/gorops/ierc-gnl-project/logs/test_engine.log'),
logging.StreamHandler()
]
)
logger = logging.getLogger(__name__)

# Constantes para pruebas
TEST_DATA_DIR = Path('/home/gorops/ierc-gnl-project/tests/data')
TEST_LOGS_DIR = Path('/home/gorops/ierc-gnl-project/logs')
TEST_LOGS_DIR.mkdir(exist_ok=True)

class TestH3Indexer:
"""Pruebas unitarias para h3_indexer.py"""

def setup_method(self):
"""Configuración inicial para cada prueba"""
logger.info(" Configurando pruebas para h3_indexer.py")

# Importar módulo bajo prueba
sys.path.insert(0, '/home/gorops/ierc-gnl-project/src/h3_indexer')
import h3_indexer
self.indexer = h3_indexer

def test_point_to_h3_valid_coordinates(self):
"""Prueba conversión de coordenadas válidas a H3"""
logger.info(" Probando conversión de coordenadas válidas a H3")

# Coordenadas en el Golfo de California
test_cases = [
(29.9000, -112.6833, 8),  # Puerto Libertad
(27.9500, -110.9000, 8),  # Guaymas
(25.0000, -111.0000, 8),  # Mar abierto
]

for lat, lon, resolution in test_cases:
h3_index = self.indexer.point_to_h3(lat, lon, resolution)
assert h3_index is not None, f"Fallo en conversión para ({lat}, {lon})"
assert isinstance(h3_index, int), "Índice H3 debe ser entero"
assert h3_index > 0, "Índice H3 debe ser positivo"
logger.info(f" Coordenadas ({lat}, {lon}) → H3 {h3_index}")

def test_point_to_h3_invalid_coordinates(self):
"""Prueba que coordenadas inválidas lancen excepciones controladas"""
logger.info(" Probando manejo de coordenadas inválidas")

# Coordenadas inválidas
invalid_cases = [
(95.0, -112.6833, 8),   # Latitud > 90
(-95.0, -112.6833, 8),  # Latitud < -90
(29.9000, 200.0, 8),    # Longitud > 180
(29.9000, -200.0, 8),   # Longitud < -180
(None, -112.6833, 8),   # Latitud None
(29.9000, None, 8),     # Longitud None
]

for lat, lon, resolution in invalid_cases:
h3_index = self.indexer.point_to_h3(lat, lon, resolution)
assert h3_index is None, f"Debe retornar None para coordenadas inválidas: ({lat}, {lon})"
logger.info(f" Coordenadas inválidas ({lat}, {lon}) correctamente manejadas")

def test_point_to_h3_outside_golfo_california(self):
"""Prueba coordenadas fuera del Golfo de California"""
logger.info(" Probando coordenadas fuera del Golfo de California")

# Coordenadas fuera del bbox del Golfo
outside_cases = [
(20.0, -112.0, 8),   # Sur de Baja California
(35.0, -112.0, 8),   # Norte de Sonora
(25.0, -116.0, 8),   # Oeste de Baja California
(25.0, -107.0, 8),   # Este de Sonora
]

for lat, lon, resolution in outside_cases:
h3_index = self.indexer.point_to_h3(lat, lon, resolution)
# Debe retornar un índice válido (H3 acepta cualquier coordenada válida)
assert h3_index is not None, f"Fallo en conversión para coordenadas fuera del Golfo: ({lat}, {lon})"
logger.info(f" Coordenadas fuera del Golfo ({lat}, {lon}) → H3 {h3_index}")

def test_point_to_h3_different_resolutions(self):
"""Prueba conversión con diferentes resoluciones H3"""
logger.info(" Probando diferentes resoluciones H3")

lat, lon = 29.9000, -112.6833

for resolution in range(0, 16):
h3_index = self.indexer.point_to_h3(lat, lon, resolution)
if resolution <= 15:
assert h3_index is not None, f"Fallo en resolución {resolution}"
logger.info(f" Resolución {resolution} → H3 {h3_index}")
else:
# Resoluciones > 15 pueden fallar
logger.warning(f"  Resolución {resolution} puede no ser soportada")

def test_create_h3_cell_geometry(self):
"""Prueba creación de geometría de celda H3"""
logger.info(" Probando creación de geometrías de celdas H3")

# Crear geometría para una celda H3 conocida
h3_index = h3.geo_to_h3(29.9000, -112.6833, 8)

geometry = self.indexer.create_h3_cell_geometry(h3_index)
assert geometry is not None, "Geometría no debe ser None"
assert isinstance(geometry, Polygon), "Geometría debe ser un Polygon"
assert not geometry.is_empty, "Geometría no debe estar vacía"

logger.info(f" Geometría creada para H3 {h3_index}")
logger.info(f"   - Tipo: {type(geometry)}")
logger.info(f"   - Vértices: {len(geometry.exterior.coords)}")

class TestIERCCalculator:
"""Pruebas unitarias para ierc_calculator.py"""

def setup_method(self):
"""Configuración inicial para cada prueba"""
logger.info(" Configurando pruebas para ierc_calculator.py")

# Importar módulo bajo prueba
sys.path.insert(0, '/home/gorops/ierc-gnl-project/src/engine')
import ierc_calculator
self.calculator = ierc_calculator

# Configuración de prueba
self.config = ierc_calculator.IERCConfig(
monte_carlo_iterations=100,  # Reducido para pruebas rápidas
batch_size=10,
normalization_method='minmax'
)

def test_ierc_formula_algebraica(self):
"""Prueba que la fórmula algebraica produzca resultados válidos"""
logger.info(" Probando fórmula algebraica del IERC")

# Scores de prueba (todos en rango [0, 1])
test_scores = {
'amenaza': 0.85,
'exposicion': 0.60,
'sensibilidad': 0.75,
'dependencia': 0.80,
'valor_biocultural': 0.90,
'capacidad_adaptativa': 0.40
}

# Calcular IERC
ierc_total = self.calculator.IERCCalculator._calculate_ierc_score(
self.calculator.IERCCalculator, test_scores
)

# Validar que esté en rango [0, 100]
assert 0 <= ierc_total <= 100, f"IERC debe estar en [0, 100], obtenido {ierc_total}"

# Validar pesos (suma debe ser 1.0)
weights_sum = sum(self.calculator.weights.values())
assert abs(weights_sum - 1.0) < 0.001, "La suma de pesos debe ser 1.0"

logger.info(f" Fórmula algebraica válida: IERC = {ierc_total:.2f}")
logger.info(f"   - Pesos: {self.calculator.weights}")

def test_ierc_formula_scores_out_of_range(self):
"""Prueba que scores fuera de rango [0, 1] sean normalizados"""
logger.info(" Probando normalización de scores fuera de rango")

# Scores fuera de rango
test_scores = {
'amenaza': 1.5,      # > 1
'exposicion': -0.2,   # < 0
'sensibilidad': 2.0,  # > 1
'dependencia': 0.5,
'valor_biocultural': 0.8,
'capacidad_adaptativa': 1.2  # > 1
}

# Calcular IERC
ierc_total = self.calculator.IERCCalculator._calculate_ierc_score(
self.calculator.IERCCalculator, test_scores
)

# Validar que esté en rango [0, 100]
assert 0 <= ierc_total <= 100, f"IERC debe estar en [0, 100], obtenido {ierc_total}"

logger.info(f" Scores fuera de rango normalizados: IERC = {ierc_total:.2f}")

def test_normalization_methods(self):
"""Prueba los diferentes métodos de normalización"""
logger.info(" Probando métodos de normalización")

test_value = 0.75
min_val, max_val = 0.0, 1.0

# Min-Max
normalized_minmax = self.calculator.IERCCalculator._normalize_minmax(
self.calculator.IERCCalculator, test_value, min_val, max_val
)
assert 0 <= normalized_minmax <= 1, "Normalización Min-Max debe estar en [0, 1]"
logger.info(f" Normalización Min-Max: {test_value} → {normalized_minmax:.3f}")

# Sigmoide
normalized_sigmoid = self.calculator.IERCCalculator._normalize_sigmoid(
self.calculator.IERCCalculator, test_value
)
assert 0 <= normalized_sigmoid <= 1, "Normalización Sigmoide debe estar en [0, 1]"
logger.info(f" Normalización Sigmoide: {test_value} → {normalized_sigmoid:.3f}")

# Percentil
series = pd.Series([0.0, 0.25, 0.5, 0.75, 1.0])
normalized_percentile = self.calculator.IERCCalculator._normalize_percentile(
self.calculator.IERCCalculator, test_value, series
)
assert 0 <= normalized_percentile <= 1, "Normalización Percentil debe estar en [0, 1]"
logger.info(f" Normalización Percentil: {test_value} → {normalized_percentile:.3f}")

def test_monte_carlo_simulation(self):
"""Prueba simulación de Monte Carlo con datos sintéticos"""
logger.info(" Probando simulación de Monte Carlo")

# Scores base para prueba
base_scores = {
'amenaza': 0.85,
'exposicion': 0.60,
'sensibilidad': 0.75,
'dependencia': 0.80,
'valor_biocultural': 0.90,
'capacidad_adaptativa': 0.40
}

# Ejecutar simulación
result = self.calculator.IERCCalculator._simulate_monte_carlo(
self.calculator.IERCCalculator, base_scores
)

# Validar resultados
assert 'mean_IERC' in result, "Resultado debe contener mean_IERC"
assert 'confidence_dato' in result, "Resultado debe contener confidence_dato"
assert 'simulation_iterations' in result, "Resultado debe contener simulation_iterations"

# Validar rangos
assert 0 <= result['mean_IERC'] <= 100, "mean_IERC debe estar en [0, 100]"
assert 0 <= result['confidence_dato'] <= 1, "confidence_dato debe estar en [0, 1]"
assert result['simulation_iterations'] == 100, "Debe ejecutar 100 iteraciones"

logger.info(f" Monte Carlo completado: {result['simulation_iterations']} iteraciones")
logger.info(f"   - IERC promedio: {result['mean_IERC']:.2f}")
logger.info(f"   - Confianza: {result['confidence_dato']:.3f}")
logger.info(f"   - Nivel de incertidumbre: {result['uncertainty_level']}")

def test_ierc_calculation_pipeline(self):
"""Prueba pipeline completo de cálculo del IERC"""
logger.info(" Probando pipeline completo de cálculo del IERC")

# Crear calculador de prueba
calculator = self.calculator.IERCCalculator(None, self.config)

# Scores de prueba para una celda
test_scores = {
'h3_cell_id': 'test_cell_123',
'quincena': 5,
'score_amenaza': 0.85,
'score_exposicion': 0.60,
'score_sensibilidad': 0.75,
'score_dependencia': 0.80,
'score_biocultural': 0.90,
'score_capacidad_adaptativa': 0.40
}

# Calcular IERC para la celda
result = calculator.calculate_ierc_for_cell_quincena(
test_scores['h3_cell_id'],
test_scores['quincena']
)

# Validar resultado
assert 'IERC_total' in result, "Resultado debe contener IERC_total"
assert 'confidence_dato' in result, "Resultado debe contener confidence_dato"

# Validar rangos
assert 0 <= result['IERC_total'] <= 100, "IERC_total debe estar en [0, 100]"
assert 0 <= result['confidence_dato'] <= 1, "confidence_dato debe estar en [0, 1]"

logger.info(f" Pipeline de cálculo completado")
logger.info(f"   - IERC: {result['IERC_total']:.2f}")
logger.info(f"   - Confianza: {result['confidence_dato']:.3f}")

class TestMonteCarloEngine:
"""Pruebas unitarias para monte_carlo_engine.py"""

def setup_method(self):
"""Configuración inicial para cada prueba"""
logger.info(" Configurando pruebas para monte_carlo_engine.py")

# Importar módulo bajo prueba
sys.path.insert(0, '/home/gorops/ierc-gnl-project/src/engine')
import monte_carlo_engine
self.engine = monte_carlo_engine

def test_monte_carlo_distribution_params(self):
"""Prueba generación de parámetros de distribución"""
logger.info(" Probando generación de parámetros de distribución")

engine = self.engine.MonteCarloEngine(self.engine.MonteCarloConfig(iterations=10))

# Probar diferentes valores base
test_cases = [
(0.2, 'amenaza'),
(0.8, 'capacidad_adaptativa'),
(0.5, 'exposicion'),
]

for base_value, component in test_cases:
dist_type, param1, param2 = engine._generate_distribution_params(base_value, component)
assert dist_type in ['normal', 'beta', 'uniform'], "Tipo de distribución debe ser válido"
assert param1 >= 0, "Parámetros deben ser no negativos"
assert param2 >= 0, "Parámetros deben ser no negativos"
logger.info(f" Distribución para {component} ({base_value}): {dist_type}, params=({param1}, {param2})")

def test_monte_carlo_sampling(self):
"""Prueba muestreo de distribuciones"""
logger.info(" Probando muestreo de distribuciones")

engine = self.engine.MonteCarloEngine(self.engine.MonteCarloConfig(iterations=100))

# Probar diferentes distribuciones
test_cases = [
('normal', 0.5, 0.1),
('beta', 2.0, 5.0),
('uniform', 0.0, 1.0),
]

for dist_type, param1, param2 in test_cases:
for _ in range(10):
value = engine._sample_from_distribution(dist_type, param1, param2)
assert 0 <= value <= 1, f"Valor muestreado debe estar en [0, 1], obtenido {value}"
logger.info(f" Muestreo {dist_type} ({param1}, {param2}) → valores en [0, 1]")

def test_monte_carlo_uncertainty_consistency(self):
"""Prueba consistencia matemática de resultados de Monte Carlo"""
logger.info(" Probando consistencia matemática de Monte Carlo")

engine = self.engine.MonteCarloEngine(self.engine.MonteCarloConfig(iterations=1000))

# Scores base consistentes
base_scores = {
'amenaza': 0.85,
'exposicion': 0.60,
'sensibilidad': 0.75,
'dependencia': 0.80,
'valor_biocultural': 0.90,
'capacidad_adaptativa': 0.40
}

# Ejecutar múltiples simulaciones
results = []
for _ in range(5):
result = engine.simulate_uncertainty(base_scores)
results.append(result)

# Validar estructura de resultado
assert 'mean_IERC' in result
assert 'confidence_dato' in result
assert 'uncertainty_level' in result

# Validar rangos
assert 0 <= result['mean_IERC'] <= 100
assert 0 <= result['confidence_dato'] <= 1

# Validar consistencia entre simulaciones
mean_scores = [r['mean_IERC'] for r in results]
std_mean = np.std(mean_scores)

# La desviación estándar debe ser pequeña (simulaciones consistentes)
assert std_mean < 2.0, f"Simulaciones deben ser consistentes, desviación: {std_mean}"

logger.info(f" Simulaciones consistentes: desviación estándar = {std_mean:.3f}")
logger.info(f"   - Rango de IERC promedio: {min(mean_scores):.2f} - {max(mean_scores):.2f}")

def test_monte_carlo_confidence_calculation(self):
"""Prueba cálculo de confianza matemática"""
logger.info(" Probando cálculo de confianza matemática")

engine = self.engine.MonteCarloEngine(self.engine.MonteCarloConfig(iterations=1000))

# Scores base
base_scores = {
'amenaza': 0.5,
'exposicion': 0.5,
'sensibilidad': 0.5,
'dependencia': 0.5,
'valor_biocultural': 0.5,
'capacidad_adaptativa': 0.5
}

# Ejecutar simulación
result = engine.simulate_uncertainty(base_scores)

# Validar cálculo de confianza
ci_width = result['upper_bound_95CI'] - result['lower_bound_95CI']
expected_confidence = 1 - (ci_width / 2)

assert abs(result['confidence_dato'] - expected_confidence) < 0.01, "Cálculo de confianza debe ser preciso"

logger.info(f" Cálculo de confianza preciso: {result['confidence_dato']:.3f}")
logger.info(f"   - Intervalo de confianza: [{result['lower_bound_95CI']:.2f}, {result['upper_bound_95CI']:.2f}]")
logger.info(f"   - Ancho del intervalo: {ci_width:.2f}")

class TestDataIngestOpenSources:
"""Pruebas unitarias para data_ingest_open_sources.py"""

def setup_method(self):
"""Configuración inicial para cada prueba"""
logger.info(" Configurando pruebas para data_ingest_open_sources.py")

# Importar módulo bajo prueba
sys.path.insert(0, '/home/gorops/ierc-gnl-project/src/engine')
import data_ingest_open_sources
self.ingestor = data_ingest_open_sources

def test_validate_coordinates(self):
"""Prueba validación de coordenadas"""
logger.info(" Probando validación de coordenadas")

# Coordenadas válidas
valid_cases = [
(29.9000, -112.6833),
(27.9500, -110.9000),
(0.0, 0.0),
]

for lat, lon in valid_cases:
assert self.ingestor.validate_coordinates(lat, lon), f"Coordenadas válidas deben pasar: ({lat}, {lon})"

# Coordenadas inválidas
invalid_cases = [
(95.0, -112.6833),
(-95.0, -112.6833),
(29.9000, 200.0),
(29.9000, -200.0),
(None, -112.6833),
(29.9000, None),
]

for lat, lon in invalid_cases:
assert not self.ingestor.validate_coordinates(lat, lon), f"Coordenadas inválidas deben fallar: ({lat}, {lon})"

logger.info(" Validación de coordenadas funcionando correctamente")

def test_point_to_h3_with_zone(self):
"""Prueba conversión a H3 con determinación de zona"""
logger.info(" Probando conversión a H3 con zonas")

ingestor = self.ingestor.GulfOfCaliforniaDataIngestor(None)

# Coordenadas en diferentes zonas
test_cases = [
(29.9000, -112.6833, 8, "Puerto Libertad"),  # En zona portuaria
(27.9500, -110.9000, 8, "Guaymas"),        # En zona portuaria
(25.0000, -111.0000, 8, "Mar Abierto"),     # En mar abierto
(28.5000, -112.0000, 8, "Zona Costera"),    # En zona costera
]

for lat, lon, resolution, expected_zone in test_cases:
h3_index, zone = ingestor._point_to_h3_with_zone(lat, lon, resolution)
assert h3_index is not None, f"H3 debe ser válido para ({lat}, {lon})"
assert zone == expected_zone, f"Zona esperada: {expected_zone}, obtenida: {zone}"
logger.info(f" ({lat}, {lon}) → H3 {h3_index} en zona {zone}")

def test_add_gender_distribution_batch(self):
"""Prueba adición de distribución de género en batch"""
logger.info(" Probando adición de distribución de género")

ingestor = self.ingestor.GulfOfCaliforniaDataIngestor(None)

# DataFrame de prueba
df = pd.DataFrame({
'vessel_type': ['artesanal', 'industrial', 'metanero', 'unknown'],
'other_column': [1, 2, 3, 4]
})

# Añadir distribución de género
df_result = ingestor._add_gender_distribution_batch(df, 'vessel_type')

# Validar que se añadió la columna
assert 'gender_distribution' in df_result.columns, "Debe añadirse gender_distribution"

# Validar formato JSON
for gender_dist in df_result['gender_distribution']:
gender_dict = json.loads(gender_dist)
assert 'male' in gender_dict
assert 'female' in gender_dict
assert 'non_binary' in gender_dict
assert sum(gender_dict.values()) == 1.0, "Distribución debe sumar 1.0"

logger.info(" Distribución de género añadida correctamente")
logger.info(f"   - Tipos de pesca procesados: {df_result['vessel_type'].unique().tolist()}")

def test_date_to_quincena_batch(self):
"""Prueba conversión de fechas a quincenas en batch"""
logger.info(" Probando conversión de fechas a quincenas")

ingestor = self.ingestor.GulfOfCaliforniaDataIngestor(None)

# DataFrame de prueba con fechas
dates = pd.date_range('2024-01-01', '2024-12-31', freq='15D')
df = pd.DataFrame({
'sampling_date': dates,
'other_column': range(len(dates))
})

# Convertir a quincenas
df_result = ingestor._date_to_quincena_batch(df, 'sampling_date')

# Validar que se añadió la columna
assert 'quincena' in df_result.columns, "Debe añadirse columna quincena"

# Validar rangos de quincenas
quincenas = df_result['quincena'].unique()
assert all(1 <= q <= 24 for q in quincenas), "Todas las quincenas deben estar en 1-24"

# Validar que hay 24 quincenas únicas
assert len(quincenas) == 24, f"Deben haber 24 quincenas únicas, obtenidas {len(quincenas)}"

logger.info(f" Conversión a quincenas completada: {len(quincenas)} quincenas únicas")
logger.info(f"   - Quincenas: {sorted(quincenas)}")

# Suite de pruebas principales
class TestMainSuite:
"""Suite principal que ejecuta todas las pruebas"""

def test_all_suites(self):
"""Ejecuta todas las suites de pruebas"""
logger.info(" Ejecutando suite completa de pruebas unitarias")

# Ejecutar pruebas
test_h3 = TestH3Indexer()
test_h3.setup_method()
test_h3.test_point_to_h3_valid_coordinates()
test_h3.test_point_to_h3_invalid_coordinates()
test_h3.test_point_to_h3_outside_golfo_california()
test_h3.test_point_to_h3_different_resolutions()
test_h3.test_create_h3_cell_geometry()

test_ierc = TestIERCCalculator()
test_ierc.setup_method()
test_ierc.test_ierc_formula_algebraica()
test_ierc.test_ierc_formula_scores_out_of_range()
test_ierc.test_normalization_methods()
test_ierc.test_monte_carlo_simulation()
test_ierc.test_ierc_calculation_pipeline()

test_mc = TestMonteCarloEngine()
test_mc.setup_method()
test_mc.test_monte_carlo_distribution_params()
test_mc.test_monte_carlo_sampling()
test_mc.test_monte_carlo_uncertainty_consistency()
test_mc.test_monte_carlo_confidence_calculation()

test_ingest = TestDataIngestOpenSources()
test_ingest.setup_method()
test_ingest.test_validate_coordinates()
test_ingest.test_point_to_h3_with_zone()
test_ingest.test_add_gender_distribution_batch()
test_ingest.test_date_to_quincena_batch()

logger.info(" Todas las pruebas unitarias pasaron exitosamente")
return True

# Configuración de pytest
if __name__ == "__main__":
# Ejecutar pruebas
suite = TestMainSuite()
try:
result = suite.test_all_suites()
if result:
logger.info(" Suite de pruebas completada con éxito")
sys.exit(0)
else:
logger.error(" Suite de pruebas fallida")
sys.exit(1)
except Exception as e:
logger.error(f" Error en suite de pruebas: {e}")
import traceback
logger.error(f"Traceback: {traceback.format_exc()}")
sys.exit(1)
