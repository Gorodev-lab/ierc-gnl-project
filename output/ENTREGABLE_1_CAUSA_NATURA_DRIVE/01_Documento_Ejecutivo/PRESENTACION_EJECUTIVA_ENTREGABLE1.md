# Dossier de Presentación Oficial: Entregable 1 — Meta 1 (POA 2026)

**Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)  
**Organización:** Causa Natura Center / Causa Natura Data (POA 2026-2028)  
**Fecha de Presentación:** 19 de Agosto de 2026  
**Equipo de Trabajo:**
- **Juan Carlos Barrera (JCB):** Consultor Senior / Especialista Pesquero y Socioambiental
- **Enrique Gorosave (EG):** Analista de Datos y SIG

---

## 📌 Guion de Presentación Ejecutiva ante Causa Natura Center

### Bloque 1: Bienvenida, Alcance y Contexto de la Meta 1
**Presentadores:** JCB y EG  
- **Propósito de la Sesión:** Presentar el **1er Entregable del Proyecto IERC-GNL**, correspondiente a la **Meta 1 (Diseño e Instrumentación Metodológica y Repositorio SIG)**.
- **Clarificación de Alcance de Datos:** 
  > *Nota Aclaratoria:* La información presentada en este Entregable 1 constituye el **marco estructural de gabinete, la línea base histórica PANGAS (Dra. Marcia Moreno-Báez) y los instrumentos de captura**. Los datos primarios oficiales y el mapeo definitivo de proyectos de Gas Natural Licuado (obras, ductos, áreas de seguridad, tráfico marítimo y polígonos comunitarios) serán recolectados y georreferenciados en campo durante las **Semanas 5 a 8 (Meta 2 - Producto 1)** en Punta Chueca, Puerto Libertad y Guaymas.

---

### Bloque 2: Nota Metodológica Ajustada y Unidad Espacio-Temporal
**Presentador:** JCB  
- **Marco Conceptual:** Implementación del modelo de riesgo socioecológico $R_{i,t} = H_{i,t} \times V_{i,t}$ adaptado del IPCC/NOAA.
- **Unidad de Análisis Pesquero Estandarizada:**
  $$\text{Unidad} = \text{comunidad} - \text{actor} - \text{pesquería} - \text{arte} - \text{zona} - \text{temporada} - \text{ruta}$$
- **Protocolo de Confidencialidad:** Reglas de salvaguarda para el conocimiento pesquero tradicional y sitios bioculturales de la Nación Comca'ac (Punta Chueca).

---

### Bloque 3: Repositorio GeoPackage OGC v1.1 y Catálogo PANGAS con Basemaps Georreferenciados
**Presentador:** EG  
- **Demostración de la Base de Datos GeoPackage ([ierc_golfo_california.gpkg](file:///home/gorops/ierc-gnl-project/deliverables/v1_geopackage/ierc_golfo_california.gpkg)):**
  - Sistema de Referencia: `EPSG:4326 (WGS84)`.
  - Estructura de 7 capas vectoriales base (`proyectos_gnl`, `gasoductos_infraestructura_gnl`, `localidades_estudio_ierc`, `anp_habitats_criticos`, `zonas_pesqueras_pangas`, `grilla_h3_riesgo` Res 8/9 adaptativa, `riqueza_relativa_pesquera`).
  - Validación del atributo `uid_espaciotemporal` en Python (`src/engine/spatial_validator.py`).
- **Demostración del Catálogo y Visor Cartográfico PANGAS ([output/paquetes_capas_pangas/ATLAS_PAQUETES_COMPLETO.html](file:///home/gorops/ierc-gnl-project/output/paquetes_capas_pangas/ATLAS_PAQUETES_COMPLETO.html)):**
  - Muestra de los 7 paquetes por capa creados en `output/paquetes_capas_pangas/`.
  - Visualización de mapas JPG georreferenciados en Web Mercator (`EPSG:3857`) sobre **OpenStreetMap estándar (estilo QGIS)** e **imagen satelital Esri World Imagery**.
  - Fichas de metadatos `METADATOS_CAPA.md` con cita académica oficial a la **Dra. Marcia Moreno-Báez et al. (2011, 2012)**.

---

### Bloque 4: Matriz de Vacíos Geoespaciales e Instrumentos Piloto para el Campo
**Presentadores:** EG y JCB  
- **Matriz de Vacíos:** Identificación de información faltante a ser cubierta en campo (rutas pesqueras quincenales, zonas de contingencia, costos por viaje, calendarios por especie, interacción con metaneros).
- **Mapas Base y Formatos Piloto:** Presentación de las plantillas de digitalización y mapas base a varias escalas preparados para las jornadas en **Punta Chueca (Comca'ac)**, **Puerto Libertad** y **Guaymas**.

---

### Bloque 5: Dictamen de Auditoría y Próximos Pasos (Meta 2)
**Presentadores:** Auditor Técnico y Equipo JCB/EG  
- **Dictamen de Auditoría:** Presentación del expediente [docs/auditoria/AUDITORIA_META1_ENTREGABLE1.md](file:///home/gorops/ierc-gnl-project/docs/auditoria/AUDITORIA_META1_ENTREGABLE1.md) (Verificación de 3 Niveles aprobada).
- **Próximos Pasos:** Inicio de las salidas a campo en Punta Chueca (Semana 5), Puerto Libertad (Semana 6) y Guaymas (Semana 7).
