# Índice Espacial de Riesgo Socioeconómico (IERC) para Infraestructura de GNL en el Golfo de California
## Nota Metodológica - Entregable E1 (Semana 1)

**Proyecto:** IERC-GNL  
**Versión:** 0.1  
**Fecha:** 27 de julio de 2026  
**Responsable:** Arquitecto de Software Senior y Científico de Datos Geoespaciales  
**Alcance:** Semana 1 - Definición de la fórmula algebraica y parametrización inicial

---

## 1. Introducción

El **Índice Espacial de Riesgo Socioeconómico (IERC)** es un modelo geoespacial multidimensional diseñado para evaluar la vulnerabilidad de comunidades costeras, ecosistemas pesqueros y patrimonio biocultural frente a megaproyectos de Gas Natural Licuado (GNL) en el Golfo de California. Este índice integra:

- **Amenazas antropogénicas** (infraestructura de GNL, tráfico marítimo, ruido acústico)
- **Exposición de los medios de vida** (pesquerías artesanales e industriales)
- **Sensibilidad ecosistémica y cultural** (especies clave, sitios sagrados, rutas ancestrales)
- **Dependencia socioeconómica** (medios de subsistencia, seguridad alimentaria)
- **Valor biocultural** (patrimonio inmaterial, conocimientos tradicionales)
- **Capacidad adaptativa y de gobernanza** (Matriz GAGE)

El IERC se calcula a nivel de **celda hexagonal H3** (resolución 8 para mar abierto, 9-11 para zonas portuarias) y temporalidad **quincenal** para capturar variaciones estacionales críticas en la pesca y el turismo.

---

## 2. Marco Teórico y Variables Clave

### 2.1 Dimensiones del IERC

El índice se compone de **6 dimensiones principales**, cada una con un peso específico basado en evidencia empírica y consulta con actores locales:

| Dimensión | Peso | Descripción | Variables Principales |
|-----------|------|-------------|----------------------|
| **Amenaza** | 20% | Intensidad y proximidad de infraestructura fósil | Distancia a terminales GNL, rutas de metaneros, zonas de exclusión, niveles de ruido acústico |
| **Exposición** | 20% | Nivel de traslape con actividades humanas críticas | Horas de esfuerzo pesquero, densidad de tráfico marítimo, presencia de comunidades costeras |
| **Sensibilidad** | 15% | Vulnerabilidad intrínseca de los ecosistemas | Diversidad de especies, presencia de especies endémicas/en peligro, sensibilidad acústica |
| **Dependencia** | 15% | Importancia socioeconómica de los recursos amenazados | Porcentaje de ingresos por pesca, seguridad alimentaria, empleo local |
| **Valor Biocultural** | 15% | Patrimonio inmaterial y conocimientos tradicionales | Sitios sagrados, rutas ancestrales, prácticas culturales vinculadas al mar |
| **Capacidad Adaptativa** | 15% | Resiliencia comunitaria y gobernanza | Matriz GAGE (50 indicadores), acceso a recursos, participación en toma de decisiones |

### 2.2 Matriz GAGE (Gobernanza y Equidad)

La **Matriz GAGE** evalúa 50 indicadores distribuidos en **7 principios de gobernanza comunitaria**:

1. **Inclusión** (3 indicadores): Participación equitativa en procesos de toma de decisiones
2. **Equidad** (3 indicadores): Distribución justa de beneficios y cargas (con enfoque de género)
3. **Autonomía** (3 indicadores): Reconocimiento legal y autogestión de recursos
4. **Transparencia** (3 indicadores): Acceso a información y rendición de cuentas
5. **Rendición de Cuentas** (3 indicadores): Mecanismos de responsabilidad y remediación
6. **Corresponsabilidad** (3 indicadores): Alianzas público-comunitarias y beneficios compartidos
7. **Incidencia** (3 indicadores): Capacidad de influir en políticas públicas y acciones legales

**Score GAGE Total:** Suma normalizada de los 21 indicadores principales (0-21 puntos).
**Score GAGE Extendido:** Incluye 29 indicadores adicionales para análisis detallado.

---

## 3. Fórmula Algebraica del IERC

### 3.1 Definición Formal

El IERC se expresa como una **función ponderada de componentes normalizados** (0-1):

```
IERC_total = (Amenaza × 0.20) + (Exposición × 0.20) + (Sensibilidad × 0.15) +
             (Dependencia × 0.15) + (Valor_Biocultural × 0.15) +
             ((1 - Capacidad_Adaptativa) × 0.15)
```

**Donde:**
- Cada componente se normaliza al rango [0, 1]
- La capacidad adaptativa se **inverte** (1 - score) porque mayor capacidad reduce el riesgo
- La suma ponderada produce un score final en el rango [0, 100]

### 3.2 Componentes Detallados

#### 3.2.1 Score de Amenaza (0-1)

```
Score_Amenaza = w_near × Amenaza_Cercanía + w_noise × Amenaza_Ruido + w_route × Amenaza_Ruta

Donde:
- Amenaza_Cercanía = 1 - (Distancia_Mínima / Distancia_Máxima_Referencia)
  * Distancia_Mínima: Distancia más cercana a infraestructura GNL en metros
  * Distancia_Máxima_Referencia: 50 km (umbral de influencia aceptable)

- Amenaza_Ruido = Nivel_Ruido_dB / 180 (ruido máximo teórico en dB)

- Amenaza_Ruta = Volumen_Tráfico / Volumen_Máximo_Referencia
  * Volumen_Máximo_Referencia: 1000 buques/año (estimación para terminales GNL)

Pesos:
- w_near = 0.50 (peso principal a la proximidad física)
- w_noise = 0.30 (impacto del ruido en fauna marina)
- w_route = 0.20 (riesgo de colisión y contaminación)
```

#### 3.2.2 Score de Exposición (0-1)

```
Score_Exposición = w_effort × Exposición_Esfuerzo + w_community × Exposición_Comunidad

Donde:
- Exposición_Esfuerzo = Horas_Esfuerzo_Celda / Horas_Esfuerzo_Máximo_Anual
  * Horas_Esfuerzo_Máximo_Anual: 8760 horas (1 año completo)

- Exposición_Comunidad = Población_Afectada / Población_Total_Zona
  * Población_Afectada: Número de personas en comunidades dentro de la celda H3

Pesos:
- w_effort = 0.60 (peso principal al esfuerzo pesquero directo)
- w_community = 0.40 (exposición de comunidades costeras)
```

#### 3.2.3 Score de Sensibilidad (0-1)

```
Score_Sensibilidad = w_species × Sensibilidad_Especies + w_endemic × Sensibilidad_Endémicas

Donde:
- Sensibilidad_Especies = (Número_Especies_Amenazadas / Número_Total_Especies) × Factor_Sensibilidad
  * Factor_Sensibilidad: 1.5 para especies en peligro crítico, 1.2 para amenazadas, 1.0 para otras

- Sensibilidad_Endémicas = Presencia_Endémicas / 1 (binario: 1 si hay especies endémicas, 0 si no)

Pesos:
- w_species = 0.70 (peso principal a la diversidad y estado de conservación)
- w_endemic = 0.30 (especies únicas del Golfo de California)
```

#### 3.2.4 Score de Dependencia (0-1)

```
Score_Dependencia = w_income × Dependencia_Ingresos + w_food × Dependencia_Alimentaria

Donde:
- Dependencia_Ingresos = (Porcentaje_Ingresos_Pesca / 100) × Factor_Económico
  * Factor_Económico: 1.0 si >50% ingresos, 0.8 si 30-50%, 0.5 si 10-30%, 0.2 si <10%

- Dependencia_Alimentaria = (Porcentaje_Dieta_Marina / 100) × Factor_Cultural
  * Factor_Cultural: 1.0 si dieta >70% marina, 0.7 si 40-70%, 0.4 si 10-40%, 0.1 si <10%

Pesos:
- w_income = 0.60 (dependencia económica directa)
- w_food = 0.40 (seguridad alimentaria y cultural)
```

#### 3.2.5 Score de Valor Biocultural (0-1)

```
Score_Biocultural = w_sacred × Valor_Sitios_Sagrados + w_routes × Valor_Rutas_Ancestrales

Donde:
- Valor_Sitios_Sagrados = Número_Sitios_Sagrados / Máximo_Sitios_Región
  * Máximo_Sitios_Región: 10 (estimación para el Golfo de California)

- Valor_Rutas_Ancestrales = Longitud_Rutas / Longitud_Total_Región
  * Longitud_Total_Región: 500 km (estimación de rutas tradicionales)

Pesos:
- w_sacred = 0.60 (peso principal a sitios de importancia espiritual)
- w_routes = 0.40 (rutas de navegación ancestral)
```

#### 3.2.6 Score de Capacidad Adaptativa (0-1)

**Nota:** Este score se invierte en la fórmula final (1 - score) porque mayor capacidad reduce el riesgo.

```
Score_Capacidad_Adaptativa = (GAGE_Total / 21) × w_gage + w_traditional × Capacidad_Tradicional

Donde:
- GAGE_Total: Score normalizado de la Matriz GAGE (0-21)
- w_gage = 0.70 (peso principal a la gobernanza estructurada)
- w_traditional = 0.30 (conocimientos tradicionales y redes comunitarias)
```

---

## 4. Parametrización Temporal: Criticidad Quincenal

### 4.1 Estructura Temporal

El IERC se calcula para **24 quincenas anuales** (1-24), con distinción entre:

- **Temporada Total:** Todas las quincenas del año
- **Temporada Principal de Pesca:** Quincenas con mayor actividad pesquera (generalmente 1-12 y 21-24 para especies costeras)

### 4.2 Ajuste Estacional

```
Score_Quincenal = Score_Base × Factor_Quincena

Donde:
- Factor_Quincena = 1.0 para temporada principal
- Factor_Quincena = 0.7 para temporada secundaria
- Factor_Quincena = 1.3 para temporada crítica (ej: temporada de desove de especies clave)
```

**Ejemplo:**
- Temporada principal (quincena 5): Score = Score_Base × 1.0
- Temporada secundaria (quincena 15): Score = Score_Base × 0.7
- Temporada crítica (quincena 22): Score = Score_Base × 1.3

### 4.3 Variabilidad Interanual

Para análisis de tendencias, se recomienda calcular el IERC para **múltiples años** (2020-2026) y evaluar:
- Tendencias de aumento/reducción de riesgo
- Impacto de eventos climáticos (El Niño, huracanes)
- Efectos de políticas públicas (vedas, regulaciones pesqueras)

---

## 5. Análisis de Incertidumbre y Monte Carlo

### 5.1 Fuentes de Incertidumbre

1. **Datos de entrada:**
   - Precisión de coordenadas GPS (error ±5-20m)
   - Exactitud de datos de esfuerzo pesquero (VMS vs. registros manuales)
   - Estimaciones de población comunitaria

2. **Modelos:**
   - Ponderaciones subjetivas de componentes
   - Umbrales de normalización (ej: distancia máxima de referencia)
   - Factores estacionales

3. **Contexto:**
   - Cambios regulatorios futuros
   - Nuevos megaproyectos no mapeados
   - Variabilidad climática

### 5.2 Simulación de Monte Carlo

**Metodología:**

1. **Variables estocásticas:**
   - Ponderaciones de componentes: Distribución uniforme [0.15, 0.25] para cada peso
   - Umbrales de normalización: Distribución normal (μ=valor_base, σ=10%)
   - Datos de entrada: Distribución normal (μ=valor_observado, σ=incertidumbre_base)

2. **Parámetros de simulación:**
   - Número de simulaciones: 1000 (equilibrio entre precisión y costo computacional)
   - Semilla aleatoria: Fija para reproducibilidad
   - Rango de confianza: 95% (percentiles 2.5 y 97.5)

3. **Salidas:**
   - Distribución del IERC_total
   - Intervalo de confianza para cada celda H3
   - Sensibilidad de cada componente al score final
   - Mapa de incertidumbre espacial

**Fórmula de propagación:**

```
Para cada simulación k:
  - Generar valores estocásticos para todas las variables
  - Calcular IERC_total(k) usando la misma fórmula algebraica
  - Registrar resultado

Resultado final:
  - IERC_medio = Media(IERC_total(k) para k=1..1000)
  - IERC_IC_2.5 = Percentil_2.5(IERC_total(k))
  - IERC_IC_97.5 = Percentil_97.5(IERC_total(k))
  - confidence_dato = 1 - (IERC_IC_97.5 - IERC_IC_2.5) / 2
```

### 5.3 Interpretación de Resultados

| Nivel de Incertidumbre | Intervalo de Confianza | Acción Recomendada |
|------------------------|------------------------|-------------------|
| **Bajo** (<0.1) | IC < 5 puntos | Resultados robustos, priorizar intervención |
| **Moderado** (0.1-0.3) | 5 ≤ IC < 15 puntos | Validar con datos adicionales, considerar monitoreo intensivo |
| **Alto** (>0.3) | IC ≥ 15 puntos | Recolectar más datos, revisar metodología, priorizar investigación |

---

## 6. Implementación Técnica

### 6.1 Arquitectura de Cálculo

```
┌─────────────────────────────────────────────────────────────┐
│                    IERC Calculation Engine                   │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Data Layer    │  Engine Layer   │    Output Layer         │
├─────────────────┼─────────────────┼─────────────────────────┤
│ - h3_cells      │ - Weight Engine │ - ierc_calculated_scores│
│ - fossil_threat │ - Normalization │ - mv_ierc_by_zone       │
│ - fisheries_exp │ - Monte Carlo   │ - mv_fisheries_by_spp   │
│ - gage_scores   │ - Aggregation   │ - Alertas tempranas     │
│ - species_ref   │ - Validation    │                         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### 6.2 Flujo de Procesamiento

1. **Preprocesamiento:**
   - Indexación espacial con H3 (nivel 8 para mar abierto)
   - Limpieza y normalización de datos (VMS, AIS, CONAPESCA)
   - Cálculo de métricas base (esfuerzo, desembarques, diversidad)

2. **Cálculo de componentes:**
   - Amenaza: Proximidad a infraestructura + ruido + tráfico
   - Exposición: Traslape con pesca + comunidades
   - Sensibilidad: Biodiversidad + especies endémicas
   - Dependencia: Ingresos + seguridad alimentaria
   - Valor Biocultural: Sitios sagrados + rutas ancestrales
   - Capacidad Adaptativa: Matriz GAGE

3. **Integración temporal:**
   - Aplicación de factores estacionales
   - Cálculo de scores quincenales

4. **Análisis de incertidumbre:**
   - Simulación Monte Carlo
   - Cálculo de intervalos de confianza

5. **Generación de outputs:**
   - Tabla ierc_calculated_scores
   - Vistas materializadas para dashboards
   - Mapas de calor y alertas tempranas

### 6.3 Tecnologías Clave

- **Base de datos:** Supabase con PostGIS (esquema definido en `/data/schemas/supabase_schema.sql`)
- **Indexación espacial:** Uber H3 (nivel 8 para mar abierto, 9-11 para zonas portuarias)
- **Cálculo:** Python (pandas, geopandas, numpy, scipy para Monte Carlo)
- **Visualización:** LOGR (Next.js 15.5 + MapLibre GL JS)
- **Integración IA:** TONL framework para síntesis y alertas automáticas

---

## 7. Validación y Calibración

### 7.1 Fuentes de Validación

1. **Datos históricos:**
   - Línea base PANGAS/Moreno-Báez (2012) para especies y esfuerzo
   - Registros de CONAPESCA para desembarques
   - Estudios de impacto ambiental de proyectos existentes

2. **Consulta con actores locales:**
   - Talleres con comunidades Comca'ac, Yaqui, Seri
   - Entrevistas con cooperativas pesqueras
   - Validación con autoridades ambientales (SEMARNAT, CONANP)

3. **Benchmarking:**
   - Comparación con índices similares (ej: Índice de Vulnerabilidad Costera de la UNESCO)
   - Análisis de correlación con datos de conflictos sociales y ambientales

### 7.2 Métricas de Calibración

| Métrica | Valor Esperado | Acción si no se cumple |
|---------|----------------|-----------------------|
| Correlación IERC vs. conflictos reportados | r > 0.7 | Revisar ponderaciones de Amenaza y Exposición |
| Sensibilidad del modelo a cambios en datos de entrada | ΔIERC < 5% para Δ10% en datos | Ajustar factores de normalización |
| Cobertura espacial | >90% de celdas H3 con datos | Completar datos faltantes o ajustar resolución |
| Consistencia temporal | Tendencias estables en años sin cambios estructurales | Revisar factores estacionales |

---

## 8. Limitaciones y Supuestos

### 8.1 Supuestos Críticos

1. **Datos disponibles:**
   - Se asume que los datos de VMS/AIS y CONAPESCA son representativos de la actividad pesquera real
   - Se asume que las comunidades reportan con precisión sus medios de subsistencia

2. **Modelo espacial:**
   - Las celdas H3 nivel 8 (~0.73 km²) son adecuadas para capturar variaciones espaciales en el Golfo de California
   - La proximidad a infraestructura es un proxy válido para riesgo de impacto

3. **Temporalidad:**
   - La quincena es una unidad temporal adecuada para capturar variaciones estacionales
   - No se modelan eventos puntuales (ej: derrames, accidentes) por falta de datos históricos

### 8.2 Limitaciones

1. **Datos faltantes:**
   - Información detallada sobre rutas de navegación ancestrales
   - Datos de ruido acústico submarino (solo estimaciones basadas en tráfico de buques)
   - Información socioeconómica desagregada por género en algunas comunidades

2. **Resolución espacial:**
   - Limitaciones en la precisión de coordenadas GPS en datos históricos
   - Dificultad para diferenciar actividades pesqueras dentro de una misma celda H3

3. **Dinámica compleja:**
   - No se modelan interacciones entre componentes (ej: cómo la capacidad adaptativa modula la exposición)
   - Efectos acumulativos a largo plazo no capturados en el análisis quincenal

4. **Contexto político:**
   - Cambios regulatorios futuros pueden invalidar supuestos del modelo
   - Litigios en curso (10 juicios de amparo) pueden alterar el panorama de amenazas

---

## 9. Próximos Pasos (Semana 2-4)

1. **Implementación técnica:**
   - Desarrollar módulo `/src/engine/ierc_calculator.py`
   - Implementar funciones de normalización y ponderación
   - Desarrollar pipeline de Monte Carlo

2. **Preparación de datos:**
   - Procesar datos crudos de VMS/AIS/CONAPESCA
   - Indexar con H3 nivel 8 y 9-11
   - Validar y limpiar datos de línea base (PANGAS/Moreno-Báez)

3. **Consulta comunitaria:**
   - Validar componentes y ponderaciones con comunidades
   - Ajustar factores estacionales según conocimiento local
   - Identificar sitios sagrados y rutas ancestrales no mapeados

4. **Desarrollo de prototipo:**
   - Calcular IERC para 3-5 celdas piloto
   - Generar mapas de calor y dashboards preliminares
   - Validar resultados con expertos locales

5. **Documentación:**
   - Actualizar esta nota metodológica con hallazgos de validación
   - Desarrollar manual de usuario para LOGR
   - Crear guías de interpretación de resultados

---

## 10. Referencias Clave

1. **Línea base ecológica y pesquera:**
   - PANGAS Project (2012). *Baseline assessment of small-scale fisheries in the Gulf of California*
   - Moreno-Báez, M. et al. (2012). *Spatial and temporal patterns of small-scale fisheries in the Gulf of California*

2. **Metodologías de riesgo socioeconómico:**
   - IPCC (2014). *Climate Change 2014: Impacts, Adaptation, and Vulnerability*
   - Turner, B.L. et al. (2003). *A framework for vulnerability analysis in sustainability science*

3. **Gobernanza comunitaria:**
   - Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action*
   - Agrawal, A. & Gibson, C. (1999). *Enchantment and Disenchantment: The Role of Community in Natural Resource Conservation*

4. **Indexación espacial:**
   - Uber H3 Documentation. *Hexagonal hierarchical spatial index*
   - Bardin, A. et al. (2019). *Spatial analysis of marine protected areas using H3*

5. **Análisis de incertidumbre:**
   - Saltelli, A. et al. (2008). *Global Sensitivity Analysis: The Primer*
   - Helton, J.C. & Davis, F.J. (2003). *Latin Hypercube Sampling and the Propagation of Uncertainty in Analyses of Complex Systems*

---

## 11. Glosario

| Término | Definición |
|---------|------------|
| **IERC** | Índice Espacial de Riesgo Socioeconómico |
| **GNL** | Gas Natural Licuado |
| **H3** | Sistema de indexación espacial hexagonal de Uber |
| **VMS** | Vessel Monitoring System (sistema de monitoreo de buques) |
| **AIS** | Automatic Identification System (sistema de identificación automática) |
| **CONAPESCA** | Comisión Nacional de Acuacultura y Pesca |
| **GAGE** | Gobernanza, Autonomía, Gobernanza, Equidad (matriz de 50 indicadores) |
| **Quincena** | Período de 15 días para análisis temporal |
| **Celda H3** | Unidad hexagonal de indexación espacial |
| **Score** | Valor normalizado entre 0 y 1 (o 0 y 100) |
| **Monte Carlo** | Método de simulación estocástica para análisis de incertidumbre |

---

## 12. Anexos

### Anexo A: Ejemplo de Cálculo

**Celda H3:** 8928308280fffff (Nivel 8, Golfo de California)  
**Quincena:** 5 (Temporada Principal)  
**Datos base:**
- Distancia a terminal GNL: 8 km
- Nivel de ruido estimado: 160 dB
- Volumen de tráfico: 800 buques/año
- Horas de esfuerzo pesquero: 1200 horas
- Número de especies amenazadas: 8 (de 43 totales)
- Especies endémicas: 2
- Porcentaje de ingresos por pesca: 65%
- Porcentaje de dieta marina: 80%
- Sitios sagrados en celda: 1
- Score GAGE: 14/21

**Cálculo manual:**

1. **Score_Amenaza:**
   - Amenaza_Cercanía = 1 - (8000/50000) = 0.84
   - Amenaza_Ruido = 160/180 = 0.89
   - Amenaza_Ruta = 800/1000 = 0.80
   - Score_Amenaza = (0.84×0.50) + (0.89×0.30) + (0.80×0.20) = 0.84

2. **Score_Exposición:**
   - Exposición_Esfuerzo = 1200/8760 = 0.14
   - Exposición_Comunidad = 150/1000 = 0.15 (estimación)
   - Score_Exposición = (0.14×0.60) + (0.15×0.40) = 0.14

3. **Score_Sensibilidad:**
   - Sensibilidad_Especies = (8/43) × 1.2 = 0.22
   - Sensibilidad_Endémicas = 1
   - Score_Sensibilidad = (0.22×0.70) + (1×0.30) = 0.45

4. **Score_Dependencia:**
   - Dependencia_Ingresos = 0.65 × 1.0 = 0.65
   - Dependencia_Alimentaria = 0.80 × 1.0 = 0.80
   - Score_Dependencia = (0.65×0.60) + (0.80×0.40) = 0.71

5. **Score_Biocultural:**
   - Valor_Sitios_Sagrados = 1/10 = 0.10
   - Valor_Rutas_Ancestrales = 5/500 = 0.01
   - Score_Biocultural = (0.10×0.60) + (0.01×0.40) = 0.06

6. **Score_Capacidad_Adaptativa:**
   - Score = (14/21) × 0.70 + 0.30 = 0.77

7. **IERC_Total:**
   - IERC = (0.84×0.20) + (0.14×0.20) + (0.45×0.15) + (0.71×0.15) + (0.06×0.15) + ((1-0.77)×0.15)
   - IERC = 0.168 + 0.028 + 0.0675 + 0.1065 + 0.009 + 0.0345 = **0.413**

**Resultado:** IERC = 41.3 (riesgo moderado-alto)

### Anexo B: Pesos por Especie (Ejemplo)

| Especie | Código | Peso en Exposición | Notas |
|---------|--------|-------------------|-------|
| Sardina monterrey | SARD_MON | 0.8 | Especie clave en cadena trófica |
| Corvina golfina | CORV_GOL | 0.7 | Importante para pesca artesanal |
| Totoaba | TOTOABA | 1.2 | En peligro crítico, alto valor biocultural |
| Camarón | CAMARON | 0.9 | Alta dependencia económica |
| Pulpo | PULPO | 0.6 | Pesca estacional |

---

**Nota final:** Este documento establece la base metodológica para el IERC-GNL. Se requiere validación con datos reales y consulta con actores locales para ajustar parámetros y ponderaciones antes de la implementación completa en la Semana 4.

**Próxima revisión:** 10 de agosto de 2026 (tras primera ronda de validación comunitaria)