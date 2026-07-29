# Plan de Auditoría, Supervisión Técnica y Control de Calidad del Proyecto IERC-GNL

**Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)  
**Organización:** Causa Natura Center / Causa Natura Data (POA 2026-2028)  
**Rol:** Auditor y Supervisor Técnico del Proyecto  
**Responsables Ejecutores:** Juan Carlos Barrera (JCB - Consultor Senior) & Enrique Gorosave (EG - Analista GIS)  

---

## 1. Función de Auditoría y Marco de Control de Calidad

Como **Auditor y Supervisor Técnico**, mi función es auditar de manera continua e inexorable el grado de cumplimiento técnico, topológico, espacial y metodológico de los avances realizados por el Analista GIS (EG) y el Consultor Senior (JCB). Ningún entregable será considerado listo para ser enviado a Causa Natura Center sin haber superado el **Protocolo de Auditoría de 3 Niveles**.

### Protocolo de Auditoría de 3 Niveles
1. **Nivel 1 (Verificación Técnica y SIG):** Inspección de archivos de datos (`.gpkg`, GeoJSON, CSV), código Python, proyecciones (EPSG:4326 / EPSG:3857), topología, índices espaciales R-Tree y estricto cumplimiento de la guía de estilo (sin emoticones).
2. **Nivel 2 (Cotejo de Requisitos del POA y Manual Metodológico):** Verificación punto por punto contra los productos y metas comprometidas en el Plan Operativo Anual (POA 2026).
3. **Nivel 3 (Ficha de Dictamen y Empaquetado Ejecutivo):** Emisión del expediente formal de auditoría en `docs/auditoria/` y estructuración del paquete de presentación para Causa Natura Center.

---

## 2. Inventario de Avance Realizado por Enrique Gorosave (EG) — Meta 1

### Trabajos Completados y Auditados
- **Base de Datos GeoPackage OGC v1.1 (`ierc_golfo_california.gpkg`):**
  - Compilado en CRS EPSG:4326 con 7 capas vectoriales (`proyectos_gnl`, `gasoductos_infraestructura_gnl`, `localidades_estudio_ierc`, `anp_habitats_criticos`, `zonas_pesqueras_pangas`, `grilla_h3_riesgo` Res 8/9 adaptativa, `riqueza_relativa_pesquera`).
  - Estandarización de la clave primaria `uid_espaciotemporal` (`comunidad-actor-pesquería-arte-zona-temporada-ruta`) en Python (`src/engine/spatial_validator.py`).
- **Paquetes Cartográficos y Atribución a la Dra. Marcia Moreno-Báez:**
  - Extracción y reproyección a Web Mercator (EPSG:3857) de las 7 capas de `Fish_Zones_PANGAS.gdb`.
  - Generación de 14 mapas JPG georreferenciados (7 variante OpenStreetMap estilo QGIS + 7 variante Esri Satelital).
  - Estructuración de 7 carpetas de paquetes individuales en `output/paquetes_capas_pangas/` con sus archivos `METADATOS_CAPA.md` y cita oficial completa a Moreno-Báez et al. (2011, 2012).
  - Visor maestro HTML [ATLAS_PAQUETES_COMPLETO.html](file:///home/gorops/ierc-gnl-project/output/paquetes_capas_pangas/ATLAS_PAQUETES_COMPLETO.html).
- **Documentación Metodológica e Inventarios:**
  - `docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md`
  - `docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md`
  - `deliverables/v1_geopackage/GEOPACKAGE_METADATA.md`
- **Control de Versiones:**
  - Repositorio público sincronizado en GitHub: [Gorodev-lab/ierc-gnl-project](https://github.com/Gorodev-lab/ierc-gnl-project).

---

## 3. Plan Metodológico por Fases, Cronograma y Entregables (12 Semanas)

### FASE 1: Meta 1 — Diseño e Instrumentación Metodológica y Repositorio SIG (Semanas 1-4 | 23 Jul - 19 Aug 2026)
- **Hitos Semanales:**
  - Semana 1: Reunión inicial, definición de unidades de análisis y creación del GeoPackage base (EG).
  - Semana 2: Revisión documental (Moreno-Báez) y compilación de capas base de gabinete (EG).
  - Semana 3: Diseño de instrumentos de campo (JCB) y mapas base a varias escalas (EG).
  - Semana 4: Pilotaje de instrumentos y protocolo de campo aprobado.
- **Entregable 1:** Nota Metodológica + GeoPackage v1.1 + Catálogo PANGAS + Protocolo de Campo.
- **Estado de Auditoría:** APROBADO CON OBSERVACIONES MENORES (Expediente: `docs/auditoria/AUDITORIA_META1_ENTREGABLE1.md`).

---

### FASE 2: Meta 2 — Levantamiento de Campo Socioambiental y Base Georreferenciada (Semanas 5-8 | 20 Aug - 16 Sep 2026)
- **Hitos Semanales:**
  - Semana 5: Campo en Punta Chueca (JCB) y digitalización de rutas/sitios Comca'ac en SIG (EG).
  - Semana 6: Campo en Puerto Libertad (JCB) y superposición digital con infraestructura GNL/ductos (EG).
  - Semana 7: Campo en Guaymas (JCB) y digitalización de polígonos/rutas portuarias (EG).
  - Semana 8: Triangulación de datos campo vs gabinete (JCB) y construcción de grilla de hexágonos H3 (EG).
- **Entregable 2 (Producto 1):** Base Espacial Maestra en GeoPackage + Atlas Pesquero Preliminar.
- **Criterios de Auditoría Nivel 1:** 100% de mapas de campo digitalizados bajo `uid_espaciotemporal`, topología sin solapamientos inválidos y grilla H3 validada.

---

### FASE 3: Meta 3 — Cálculo del Índice IERC, Sensibilidad y Validación Social (Semanas 9-10 | 17 Sep - 07 Oct 2026)
- **Hitos Semanales:**
  - Semana 9: Cálculo de variables espaciales, normalización Min-Max, ponderación AHP y generación de escenarios (EG / JCB).
  - Semana 10: Validación comunitaria/técnica y cálculo de mapa de confianza Monte Carlo (EG / JCB).
- **Entregable 3 (Producto 2):** Versión Validada del Índice IERC + Integración en Plataforma LOGR (Next.js/Supabase).
- **Criterios de Auditoría Nivel 1:** Validación estadística de Monte Carlo, pruebas de estabilidad en sensibilidad y consulta limpia en API `/api/geopackage`.

---

### FASE 4: Meta 4 — Integración Final, Reporte Ejecutivo y Paquete de Difusión (Semanas 11-12 | 08 Oct - 19 Nov 2026)
- **Hitos Semanales:**
  - Semana 11: Redacción de hallazgos, cartografía final y gráficos comparativos (JCB / EG).
  - Semana 12: Paquete final de entregables, resumen ejecutivo y estrategia de difusión (JCB / EG).
- **Entregables 4 (Productos 3, 4 y 5):**
  - Producto 3: Material Gráfico y Atlas Espacio-Temporal.
  - Producto 4: Resumen Ejecutivo e Informe Final de Políticas Públicas.
  - Producto 5: Estrategia y Paquete de Difusión Diferenciada para Causa Natura Center, SEMARNAT, CONAPESCA y Comunidades.
- **Criterios de Auditoría Nivel 1:** Verificación completa de productos 1 a 5, compatibilidad OGC final y expediente de cierre.
