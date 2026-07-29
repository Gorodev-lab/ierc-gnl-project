# Nota Metodológica Ajustada: Diseño del Índice Espacial de Riesgo Socioeconómico (IERC) para Infraestructura de GNL

**Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades Pesqueras ante Proyectos de GNL en el Golfo de California  
**Organización:** Causa Natura Data (POA 2026-2028)  
**Entregable:** Meta 1 — Producto 1 (Nota Metodológica Ajustada + Repositorio SIG)  
**Autores del Equipo Técnico:**
- **Juan Carlos Barrera (JCB):** Consultor Senior / Especialista Pesquero y Socioambiental
- **Enrique Gorosave (EG):** Analista de Datos y SIG

---

## 1. Introducción y Justificación Metodológica

El presente documento constituye la **Nota Metodológica Ajustada** para el diseño del Índice Espacial de Riesgo Socioeconómico (IERC). Integra la línea base histórica pesquera de **Moreno-Báez et al. (2011, 2012)**, la plataforma de inteligencia marítima **LOGR**, los indicadores de gobernanza de la **Matriz GAGE** y la estructura conceptual multicriterio del IPCC/NOAA.

El objetivo central es medir la exposición, vulnerabilidad y capacidad adaptativa de las comunidades pesqueras artesanales del Golfo de California ante el desarrollo de infraestructura de Gas Natural Licuado (GNL) en **Punta Chueca (Comca'ac)**, **Puerto Libertad** y **Guaymas**.

---

## 2. Unidad de Análisis Espacio-Temporal

Para asegurar la defendibilidad científica y la ingesta estandarizada en el Sistema de Información Geográfica (SIG), cada entidad de análisis pesquero adopta la unidad estructurada:

$$\text{Unidad de Análisis} = \text{comunidad} - \text{actor} - \text{pesquería} - \text{arte} - \text{zona} - \text{temporada} - \text{ruta}$$

* **`comunidad`**: Localidad de origen (ej. `Punta_Chueca`, `Puerto_Libertad`, `Guaymas`).
* **`actor`**: Grupo o categoría social (ej. `Pescadores_artesanales`, `Mujeres_desconchadoras`, `Cooperativa`).
* **`pesquería`**: Especie objetivo o recurso (ej. `Jaiba`, `Camarón`, `Escama`, `Calamar`).
* **`arte`**: Arte de pesca utilizado (ej. `PANGAS`, `Chinchorro`, `Redes_manta`, `Trampas`, `Buceo`).
* **`zona`**: Delimitación espacial primaria (uso frecuente) o secundaria (contingencia/histórica).
* **`temporada`**: Periodo quincenal/mensual o estado de veda.
* **`ruta`**: Trayectoria de navegación entre el puerto de desembarque y la zona de pesca.

---

## 3. Formulación Matemática del Índice IERC

El riesgo integral ($R_{i,t}$) por celda ($i$) y periodo ($t$) se evalúa mediante el producto de la amenaza espacial ($H_{i,t}$) y la vulnerabilidad socioecológica ($V_{i,t}$):

$$R_{i,t} = H_{i,t} \times V_{i,t}$$

Donde la **Amenaza y Exposición Espacio-Temporal ($H_{i,t}$)** se define como:
$$H_{i,t} = (0.50 \times \text{Densidad Esfuerzo}) + (0.30 \times \text{Proximidad GNL}) + (0.20 \times \text{Intersección Rutas})$$

Y la **Vulnerabilidad Socioeconómica y Gobernanza ($V_{i,t}$)** integra las 5 dimensiones clave:
$$V_{i,t} = (0.25 \times \text{Sensibilidad Especies}) + (0.25 \times \text{Dependencia Ingreso}) + (0.20 \times \text{Patrimonio Biocultural}) + (0.15 \times \text{Género/Postcaptura}) + (0.15 \times [1 - \text{Capacidad Adaptativa}])$$

---

## 4. Estructura de la Grilla Hexagonal Adaptativa (Uber H3)

Para la evaluación continua, el espacio marino y costero se discretiza en una grilla hexagonal **Uber H3**:
1. **Mar Abierto / Zonas Pesqueras:** H3 Resolución 8 (~0.73 km² por celda).
2. **Zonas Portuarias e Interfaz Industrial (Puerto Libertad y Guaymas):** H3 Resolución 9 (~0.10 km² por celda).

---

## 5. Protocolo de Confidencialidad de Datos Comunitarios

En cumplimiento de los principios de justicia ambiental y gobernanza indígena Comca'ac:
1. **Protección de Sitios Bioculturales y Sagrados:** Los polígonos de valor espiritual o conocimiento pesquero tradicional no público se agregan o anonimizan a nivel de grilla H3.
2. **Propiedad Intelectual Comunal:** Toda la información recolectada en Punta Chueca requiere consentimiento previo, libre e informado (CPLI) de las autoridades de la Nación Comca'ac.
