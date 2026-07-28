# Protocolos de Campo para IERC-GNL

**Proyecto:** Índice Espacial de Riesgo Socioeconómico (IERC) para Infraestructura de GNL en el Golfo de California  
**Responsable:** Consultor Senior Enrique Gorosave  
**Versión:** 1.0  
**Fecha:** 27 de julio de 2026  

---

## Tabla de Contenidos

1. [Protocolo Comunitario: Punta Chueca (Nación Comca'ac)](#protocolo-comunitario-punta-chueca-nación-comcaac)
2. [Protocolo Portuario: Puerto Libertad y Guaymas](#protocolo-portuario-puerto-libertad-y-guaymas)
3. [Guías Generales de Recolección de Datos](#guías-generales-de-recolección-de-datos)
4. [Formatos de Registro y Herramientas](#formatos-de-registro-y-herramientas)
5. [Protocolos de Seguridad y Ética](#protocolos-de-seguridad-y-ética)

---

## Protocolo Comunitario: Punta Chueca (Nación Comca'ac)

### Objetivo
Documentar la vulnerabilidad socioambiental y biocultural de la comunidad Comca'ac frente a proyectos de GNL, con enfoque en:
- Sitios sagrados y ceremoniales
- Rutas de navegación ancestrales
- Zonas de recolección tradicional
- Prácticas pesqueras y culturales

### Alcance Geográfico
- **Comunidad:** Punta Chueca, Sonora
- **Zona de estudio:** 20 km a la redonda desde la comunidad
- **Coordenadas centrales:** 29.8167° N, 112.4167° W
- **Área aproximada:** 1,256 km² (incluyendo marismas y zonas costeras)

### Metodología

#### 1. Mapeo Participativo de Sitios Sagrados

**Objetivo:** Identificar y georreferenciar sitios de importancia espiritual y cultural.

**Metodología:**
- **Talleres comunitarios:** 2 sesiones de 3 horas cada una
- **Entrevistas semiestructuradas:** 15-20 líderes comunitarios (hombres y mujeres)
- **Técnica de mapeo:** Uso de GPS portátil + aplicación móvil (ODK Collect o KoboToolbox)
- **Validación:** Cruzar información con ancianos y chamanes

**Variables a registrar:**
- Nombre del sitio (en lengua Comca'ac y español)
- Tipo de sitio (sagrado, ceremonial, de recolección, etc.)
- Coordenadas GPS (WGS84, precisión mínima 5m)
- Importancia cultural (escala 1-5)
- Temporada de uso (quincenas del año)
- Acceso (restringido, público, peligroso)
- Amenazas identificadas (infraestructura, contaminación, etc.)

**Herramientas requeridas:**
- GPS Garmin GPSMAP 66i o equivalente
- Tablet con aplicación de mapeo
- Cámara fotográfica (para registro visual)
- Cuaderno de campo y bolígrafos
- Consentimiento informado firmado

**Formato de registro:**
```markdown
# Ficha de Sitio Sagrado Comca'ac

**ID:** COMCAAC_SS_001  
**Nombre en Comca'ac:** [ ]  
**Nombre en español:** [ ]  
**Tipo:** [ ] Sagrado / [ ] Ceremonial / [ ] Recolección / [ ] Otro: _______  
**Coordenadas:** Lat: _______ Lon: _______  
**Precisión GPS:** [ ] <5m / [ ] 5-10m / [ ] >10m  
**Importancia cultural (1-5):** [ ] 1 / [ ] 2 / [ ] 3 / [ ] 4 / [ ] 5  
**Temporada de uso:** [ ] Quincena 1 / [ ] Quincena 2 / ... / [ ] Todo el año  
**Acceso:** [ ] Restringido / [ ] Público / [ ] Peligroso  
**Amenazas:** [ ] Infraestructura GNL / [ ] Contaminación / [ ] Turismo / [ ] Otro: _______  
**Notas:**
[ ]

**Fecha de registro:** _______  
**Registrado por:** _______  
**Validado por:** _______ (anciano/comunitario)
```

#### 2. Registro de Rutas de Navegación Ancestrales

**Objetivo:** Documentar las rutas tradicionales de navegación en canoas y pangas.

**Metodología:**
- **Trayectos guiados:** Acompañar a pescadores locales en sus salidas tradicionales
- **Registro GPS:** Seguimiento continuo de la ruta (cada 10 segundos)
- **Entrevistas:** Preguntar sobre:
  - Puntos de partida y llegada
  - Zonas de pesca tradicionales
  - Lugares de descanso y aprovisionamiento
  - Épocas del año de uso
  - Cambios recientes en las rutas

**Variables a registrar:**
- ID de la ruta
- Punto de inicio y fin
- Coordenadas de puntos clave (waypoints)
- Tipo de embarcación tradicional
- Temporada de uso
- Especies objetivo en cada tramo
- Amenazas identificadas
- Tiempo de navegación estimado

**Formato de registro:**
```markdown
# Ficha de Ruta Ancestral Comca'ac

**ID Ruta:** COMCAAC_RA_001  
**Nombre:** [ ]  
**Punto de inicio:** Lat: _______ Lon: _______  
**Punto final:** Lat: _______ Lon: _______  
**Tipo de embarcación:** [ ] Canoa / [ ] Panga tradicional / [ ] Otra: _______  
**Temporada de uso:** [ ] Quincena 1 / [ ] Quincena 2 / ... / [ ] Todo el año  
**Especies objetivo:**
- [ ] Sardina
- [ ] Corvina
- [ ] Pulpo
- [ ] Otro: _______

**Waypoints clave:**
1. WP1: Lat: _______ Lon: _______ - Descripción: _______
2. WP2: Lat: _______ Lon: _______ - Descripción: _______

**Amenazas en la ruta:**
- [ ] Tráfico de metaneros
- [ ] Zonas de exclusión
- [ ] Contaminación sonora
- [ ] Otro: _______

**Tiempo estimado:** _______ horas  
**Distancia total:** _______ km  

**Notas:**
[ ]

**Fecha de registro:** _______  
**Registrado por:** _______  
**Guía local:** _______
```

#### 3. Encuesta de Medios de Subsistencia y Dependencia

**Objetivo:** Cuantificar la dependencia económica y cultural de la comunidad respecto a los recursos marinos.

**Metodología:**
- **Encuestas estructuradas:** 30-40 hogares (muestra representativa)
- **Entrevistas a líderes:** Presidentes de cooperativas, ancianos, mujeres líderes
- **Grupos focales:** Separados por género y edad

**Variables a registrar:**

**Sección 1: Datos demográficos**
- Tamaño del hogar
- Edad y género de cada miembro
- Nivel educativo
- Tiempo de residencia en la comunidad

**Sección 2: Actividades económicas**
- Principal actividad económica del hogar
- Ingresos mensuales promedio por actividad
- Porcentaje de ingresos provenientes de la pesca
- Tipo de pesca (artesanal, semi-industrial, recolección)
- Especies objetivo principales
- Temporada de mayor actividad
- Acceso a mercados y precios

**Sección 3: Seguridad alimentaria**
- Porcentaje de dieta basado en recursos marinos
- Especies clave en la dieta
- Temporada de escasez
- Métodos de conservación tradicional

**Sección 4: Gobernanza y participación**
- Participación en toma de decisiones comunitarias
- Conocimiento de proyectos de GNL
- Percepción de riesgos
- Mecanismos de queja y denuncia

**Formato de encuesta:**
```markdown
# Encuesta de Medios de Subsistencia - Comunidad Comca'ac

**ID Encuesta:** COMCAAC_ENC_001  
**Fecha:** _______  
**Encuestador:** _______  

## Sección 1: Datos del Hogar
- **Tamaño del hogar:** _______ personas
- **Jefe del hogar:** [ ] Hombre / [ ] Mujer / [ ] Otro: _______
- **Edades:** 
  - <12 años: _______
  - 12-18 años: _______
  - 19-35 años: _______
  - 36-60 años: _______
  - >60 años: _______
- **Nivel educativo (promedio):**
  - [ ] Sin educación
  - [ ] Primaria
  - [ ] Secundaria
  - [ ] Bachillerato
  - [ ] Universidad

## Sección 2: Actividades Económicas
- **Principal actividad:**
  - [ ] Pesca artesanal
  - [ ] Recolección de moluscos
  - [ ] Turismo comunitario
  - [ ] Comercio local
  - [ ] Otro: _______
- **Ingresos mensuales promedio:** $_______ MXN
- **% ingresos de la pesca:** _______%
- **Tipo de pesca:**
  - [ ] Canoa tradicional
  - [ ] Panga con motor
  - [ ] Redes fijas
  - [ ] Línea y anzuelo
  - [ ] Otro: _______
- **Especies objetivo (top 3):**
  1. _______
  2. _______
  3. _______
- **Temporada de mayor actividad:**
  - [ ] Quincena 1-6
  - [ ] Quincena 7-12
  - [ ] Quincena 13-18
  - [ ] Quincena 19-24
  - [ ] Todo el año

## Sección 3: Seguridad Alimentaria
- **% dieta basada en mar:** _______%
- **Especies clave en dieta:**
  - [ ] Sardina
  - [ ] Corvina
  - [ ] Pulpo
  - [ ] Almeja
  - [ ] Otro: _______
- **Temporada de escasez:**
  - [ ] Quincena 1-6
  - [ ] Quincena 7-12
  - [ ] Quincena 13-18
  - [ ] Quincena 19-24
  - [ ] No hay escasez
- **Métodos de conservación:**
  - [ ] Secado al sol
  - [ ] Ahumado
  - [ ] Salado
  - [ ] Refrigeración
  - [ ] Otro: _______

## Sección 4: Gobernanza y Participación
- **Participa en asambleas comunitarias:**
  - [ ] Sí, regularmente
  - [ ] Sí, ocasionalmente
  - [ ] No
- **Sabe sobre proyectos de GNL:**
  - [ ] Sí, mucho
  - [ ] Sí, algo
  - [ ] No
- **Percepción de riesgos:**
  - [ ] Alto
  - [ ] Moderado
  - [ ] Bajo
  - [ ] No sabe
- **Mecanismos de denuncia:**
  - [ ] Asambleas
  - [ ] Autoridades locales
  - [ ] Organizaciones civiles
  - [ ] No conoce

**Notas del encuestador:**
[ ]

**Firma del entrevistado:** _______
```

#### 4. Registro de Prácticas Culturales Vinculadas al Mar

**Objetivo:** Documentar conocimientos tradicionales, rituales y prácticas culturales asociadas al mar.

**Metodología:**
- **Entrevistas a ancianos:** 5-8 personas mayores de 60 años
- **Observación participante:** Asistir a ceremonias y rituales
- **Recolección de testimonios:** Grabación de audio (con consentimiento)

**Variables a registrar:**
- Nombre de la práctica cultural
- Temporada de realización
- Especies o elementos naturales involucrados
- Significado cultural
- Cambios recientes en la práctica
- Amenazas identificadas

---

## Protocolo Portuario: Puerto Libertad y Guaymas

### Objetivo
Evaluar el impacto de proyectos de GNL en las operaciones pesqueras y la seguridad de las comunidades portuarias, con enfoque en:
- Cooperativas pesqueras y su relación con zonas de exclusión
- Traslape con rutas de buques metaneros
- Pérdidas económicas por exclusión de áreas de pesca
- Seguridad laboral y riesgos ocupacionales

### Alcance Geográfico

#### Puerto Libertad
- **Ubicación:** 29.9000° N, 112.6833° W
- **Zona de estudio:** 15 km a la redonda desde el puerto
- **Área aproximada:** 706 km²
- **Cooperativas principales:**
  - Cooperativa de Pescadores de Puerto Libertad
  - Cooperativa de Maricultura
  - Cooperativa de Buzos

#### Guaymas
- **Ubicación:** 27.9500° N, 110.9000° W
- **Zona de estudio:** 20 km a la redonda desde el puerto
- **Área aproximada:** 1,256 km²
- **Cooperativas principales:**
  - Cooperativa de Pescadores Ribereños
  - Cooperativa de Camaronicultores
  - Cooperativa de Pescadores de Altura

### Metodología

#### 1. Encuesta a Cooperativas Pesqueras

**Objetivo:** Cuantificar el impacto económico y operativo de las zonas de exclusión y el tráfico de metaneros.

**Metodología:**
- **Entrevistas a líderes:** Presidentes y secretarios de 5-8 cooperativas
- **Encuestas a pescadores:** 50-80 pescadores (muestra representativa)
- **Revisión de registros:** Libros de bitácora, ventas, gastos
- **Mapeo participativo:** Identificar zonas de pesca afectadas

**Variables a registrar:**

**Sección 1: Datos de la cooperativa**
- Nombre de la cooperativa
- Número de socios
- Tipo de pesca principal
- Año de fundación
- Área de operación principal

**Sección 2: Impacto de zonas de exclusión**
- Área total de pesca antes de zonas de exclusión (km²)
- Área perdida por zonas de exclusión (km² y %)
- Especies afectadas por la pérdida de área
- Temporada de mayor impacto
- Pérdida económica estimada (mensual/anual)
- Estrategias de adaptación implementadas

**Sección 3: Traslape con rutas de metaneros**
- Frecuencia de traslape con rutas de metaneros (semanal/mensual)
- Tipo de incidentes reportados:
  - [ ] Colisiones
  - [ ] Contaminación
  - [ ] Interferencia con equipos
  - [ ] Otro: _______
- Pérdida de tiempo de pesca por traslape (horas/semana)
- Costos adicionales por seguridad (ej: escoltas)

**Sección 4: Seguridad y riesgos**
- Conocimiento de protocolos de seguridad para metaneros
- Capacitación en manejo de emergencias
- Percepción de riesgo laboral
- Mecanismos de reporte de incidentes

**Formato de encuesta:**
```markdown
# Encuesta a Cooperativas Pesqueras - Impacto GNL

**ID Encuesta:** PORT_ENC_001  
**Fecha:** _______  
**Encuestador:** _______  
**Cooperativa:** _______

## Sección 1: Datos de la Cooperativa
- **Número de socios:** _______
- **Tipo de pesca principal:**
  - [ ] Artesanal costera
  - [ ] Semi-industrial
  - [ ] Industrial
  - [ ] Maricultura
  - [ ] Otro: _______
- **Año de fundación:** _______
- **Área de operación principal (km²):** _______

## Sección 2: Impacto de Zonas de Exclusión
- **Área total antes de zonas de exclusión:** _______ km²
- **Área perdida por zonas de exclusión:** _______ km² (_______%)
- **Especies afectadas (top 3):**
  1. _______
  2. _______
  3. _______
- **Temporada de mayor impacto:**
  - [ ] Quincena 1-6
  - [ ] Quincena 7-12
  - [ ] Quincena 13-18
  - [ ] Quincena 19-24
  - [ ] Todo el año
- **Pérdida económica estimada (mensual):** $_______ MXN
- **Estrategias de adaptación:**
  - [ ] Cambio de zonas de pesca
  - [ ] Cambio de especies objetivo
  - [ ] Diversificación de actividades
  - [ ] Otro: _______

## Sección 3: Traslape con Rutas de Metaneros
- **Frecuencia de traslape:**
  - [ ] Diario
  - [ ] 2-3 veces por semana
  - [ ] Semanal
  - [ ] Mensual
  - [ ] Ocasional
- **Tipo de incidentes reportados:**
  - [ ] Colisiones
  - [ ] Contaminación
  - [ ] Interferencia con equipos
  - [ ] Otro: _______
- **Pérdida de tiempo de pesca (horas/semana):** _______
- **Costos adicionales por seguridad:** $_______ MXN/mes

## Sección 4: Seguridad y Riesgos
- **Conoce protocolos de seguridad para metaneros:**
  - [ ] Sí
  - [ ] No
  - [ ] Parcialmente
- **Capacitación en manejo de emergencias:**
  - [ ] Sí, reciente
  - [ ] Sí, pero antigua
  - [ ] No
- **Percepción de riesgo laboral:**
  - [ ] Alto
  - [ ] Moderado
  - [ ] Bajo
- **Mecanismo de reporte de incidentes:**
  - [ ] Autoridades portuarias
  - [ ] SEMAR
  - [ ] Cooperativa
  - [ ] Otro: _______

**Notas del encuestador:**
[ ]

**Firma del entrevistado:** _______
```

#### 2. Registro de Incidentes y Accidentes

**Objetivo:** Documentar eventos relacionados con la operación de metaneros y zonas de exclusión.

**Metodología:**
- **Reporte diario:** Durante 30 días consecutivos
- **Entrevistas a testigos:** Pescadores, capitanes de puerto, autoridades
- **Revisión de registros oficiales:** Capitanía de Puerto, SEMAR, PROFEPA
- **Fotografía y video:** Registro visual de incidentes cuando sea posible

**Variables a registrar:**
- Fecha y hora del incidente
- Ubicación (coordenadas GPS)
- Tipo de incidente
- Embarcaciones involucradas
- Especies afectadas (si aplica)
- Daños reportados
- Acciones tomadas
- Autoridades notificadas

**Formato de reporte:**
```markdown
# Reporte de Incidente - Puerto [Libertad/Guaymas]

**ID Reporte:** INC_001  
**Fecha del incidente:** _______ / _______ / _______  
**Hora:** _______ : _______  
**Ubicación:** Lat: _______ Lon: _______  
**Tipo de incidente:**
- [ ] Colisión con buque metanero
- [ ] Contaminación por hidrocarburos
- [ ] Interferencia con equipos de pesca
- [ ] Intrusión en zona de exclusión
- [ ] Otro: _______

**Embarcaciones involucradas:**
- **Panga/Barco local:**
  - Nombre: _______
  - Tipo: _______
  - Dueño: _______
- **Buque metanero:**
  - Nombre: _______
  - Bandera: _______
  - Matrícula: _______

**Especies afectadas:**
- [ ] Sardina
- [ ] Corvina
- [ ] Camarón
- [ ] Otro: _______
- [ ] No aplica

**Daños reportados:**
- [ ] Daños materiales a embarcación
- [ ] Daños a equipos de pesca
- [ ] Contaminación de captura
- [ ] Lesiones a pescadores
- [ ] Otro: _______

**Acciones tomadas:**
- [ ] Notificación a autoridades
- [ ] Retirada del área
- [ ] Llamada a emergencias
- [ ] Otro: _______

**Autoridades notificadas:**
- [ ] SEMAR
- [ ] PROFEPA
- [ ] Capitanía de Puerto
- [ ] Cooperativa
- [ ] Otro: _______

**Testigos:**
- Nombre: _______ Teléfono: _______
- Nombre: _______ Teléfono: _______

**Fotos/videos adjuntos:** [ ] Sí / [ ] No  
**Nombres de archivos:** _______

**Notas:**
[ ]

**Reportado por:** _______  
**Fecha de reporte:** _______
```

#### 3. Mapeo de Zonas de Pesca Afectadas

**Objetivo:** Identificar y georreferenciar áreas de pesca que han sido afectadas por zonas de exclusión o tráfico de metaneros.

**Metodología:**
- **Talleres con pescadores:** 2 sesiones por puerto
- **Mapeo participativo:** Usar GPS y aplicación móvil
- **Entrevistas a capitanes:** 10-15 pescadores experimentados
- **Validación cruzada:** Comparar con datos de VMS/AIS cuando estén disponibles

**Variables a registrar:**
- ID de la zona afectada
- Coordenadas del polígono (mínimo 4 puntos)
- Tipo de afectación:
  - [ ] Zona de exclusión permanente
  - [ ] Zona de exclusión temporal
  - [ ] Tráfico intenso de metaneros
  - [ ] Contaminación
- Especies objetivo en la zona
- Temporada de uso
- Pérdida económica estimada
- Estrategias de adaptación

**Formato de registro:**
```markdown
# Ficha de Zona Afectada - Puerto [Libertad/Guaymas]

**ID Zona:** ZA_PORT_001  
**Nombre/localización:** _______

**Tipo de afectación:**
- [ ] Zona de exclusión permanente
- [ ] Zona de exclusión temporal
- [ ] Tráfico intenso de metaneros
- [ ] Contaminación
- [ ] Otro: _______

**Coordenadas (polígono):**
1. Lat: _______ Lon: _______
2. Lat: _______ Lon: _______
3. Lat: _______ Lon: _______
4. Lat: _______ Lon: _______

**Especies objetivo en la zona:**
- [ ] Sardina
- [ ] Corvina
- [ ] Camarón
- [ ] Pulpo
- [ ] Otro: _______

**Temporada de uso:**
- [ ] Quincena 1-6
- [ ] Quincena 7-12
- [ ] Quincena 13-18
- [ ] Quincena 19-24
- [ ] Todo el año

**Pérdida económica estimada:**
- **Área afectada:** _______ km²
- **Pérdida mensual:** $_______ MXN
- **% de ingresos perdidos:** _______%

**Estrategias de adaptación:**
- [ ] Cambio de zonas de pesca
- [ ] Cambio de especies objetivo
- [ ] Diversificación de actividades
- [ ] Otro: _______

**Notas:**
[ ]

**Fecha de registro:** _______  
**Registrado por:** _______  
**Validado por:** _______ (pescador local)
```

---

## Guías Generales de Recolección de Datos

### 1. Estándares de Precisión

**Coordenadas GPS:**
- **Precisión mínima requerida:** 5 metros
- **Sistema de referencia:** WGS84 (EPSG:4326)
- **Formato de registro:** Grados decimales (ej: 29.8167, -112.4167)
- **Dispositivos recomendados:**
  - GPS Garmin GPSMAP 66i
  - Teléfono inteligente con GPS de alta precisión
  - Tablet con receptor GNSS externo

**Fechas y horarios:**
- **Formato:** DD/MM/AAAA
- **Hora:** HH:MM (24 horas)
- **Zona horaria:** UTC-7 (Hora del Pacífico)

### 2. Registro Fotográfico y Visual

**Requisitos para fotos:**
- **Resolución mínima:** 12 MP
- **Formato:** JPEG o PNG
- **Metadatos:** Activar georreferenciación (EXIF)
- **Orientación:** Horizontal (paisaje) preferida
- **Enfoque:** En el sujeto principal
- **Contraste:** Adecuado para visualización

**Tipos de fotos a registrar:**
1. **Sitios sagrados:** Vista general y detalles
2. **Rutas de navegación:** Puntos clave y paisajes
3. **Embarcaciones tradicionales:** Vista lateral y frontal
4. **Infraestructura portuaria:** Terminales, zonas de exclusión
5. **Incidentes:** Antes y después (si aplica)
6. **Especies objetivo:** Capturas, artes de pesca
7. **Comunidades:** Hogares, cooperativas, autoridades

**Nomenclatura de archivos:**
```
[COMUNIDAD]_[TIPO]_[SECUENCIAL]_[FECHA]
Ejemplo:
COMCAAC_SS_001_20260727.jpg
PORT_LI_RA_002_20260728.jpg
```

### 3. Grabación de Audio y Video

**Requisitos:**
- **Formato:** MP3 o MP4
- **Resolución de video:** Mínimo 1080p
- **Duración máxima:** 10 minutos por clip
- **Consentimiento:** Obtener firma de consentimiento informado

**Contenido recomendado:**
- **Entrevistas:** Grabación completa de conversaciones
- **Testimonios:** Declaraciones espontáneas
- **Ceremonias:** Rituales y prácticas culturales
- **Explicaciones:** Guías locales describiendo sitios o prácticas

**Transcripción:**
- Realizar transcripción literal dentro de las 24 horas
- Incluir notas contextuales
- Guardar archivo de texto con el mismo nombre que el audio/video

### 4. Manejo de Datos Sensibles

**Información confidencial:**
- Datos personales de encuestados
- Ubicaciones exactas de sitios sagrados (solo compartir con consentimiento explícito)
- Información sobre litigios en curso
- Estrategias de adaptación comunitarias

**Protocolos:**
- **Anonimización:** Usar IDs en lugar de nombres en bases de datos
- **Acceso controlado:** Solo investigadores autorizados
- **Consentimiento informado:** Firmado antes de cualquier recolección
- **Destrucción segura:** Datos en papel deben ser triturados
- **Cifrado:** Datos digitales deben estar encriptados

**Formato de consentimiento informado:**
```markdown
# CONSENTIMIENTO INFORMADO PARA PARTICIPACIÓN EN ESTUDIO IERC-GNL

**Proyecto:** Índice Espacial de Riesgo Socioeconómico (IERC) para Infraestructura de GNL en el Golfo de California  
**Investigador principal:** Enrique Gorosave  
**Institución:** [Nombre de la institución o organización]

**Propósito del estudio:**
Documentar la vulnerabilidad socioambiental y biocultural de comunidades costeras frente a proyectos de GNL, con el fin de informar políticas públicas y estrategias de mitigación.

**Procedimientos:**
- Entrevistas semiestructuradas
- Encuestas estructuradas
- Mapeo participativo con GPS
- Registro fotográfico y de audio/video
- Observación participante

**Riesgos y beneficios:**
- **Riesgos mínimos:** Posible incomodidad al responder preguntas personales o compartir ubicaciones
- **Beneficios:** Los resultados del estudio pueden contribuir a la protección de medios de subsistencia y patrimonio cultural

**Confidencialidad:**
- Sus datos personales serán anonimizados
- Solo investigadores autorizados tendrán acceso
- Los resultados se presentarán de manera agregada
- No se compartirán ubicaciones exactas de sitios sagrados sin consentimiento explícito

**Participación voluntaria:**
- Su participación es completamente voluntaria
- Puede retirarse en cualquier momento sin consecuencias
- Puede negarse a responder cualquier pregunta

**Uso de la información:**
- Los datos recolectados se utilizarán únicamente para los fines del proyecto IERC-GNL
- Los resultados pueden publicarse en informes técnicos y artículos académicos
- No se venderá ni comercializará la información recolectada

**Consentimiento:**
- He leído y entendido la información proporcionada
- Mis preguntas han sido respondidas satisfactoriamente
- Consiento participar en este estudio

**Firma del participante:** _________________________  
**Nombre:** _________________________  
**Fecha:** _______ / _______ / _______  

**Firma del investigador:** _________________________  
**Nombre:** _________________________  
**Fecha:** _______ / _______ / _______
```

### 5. Control de Calidad de Datos

**Verificación en campo:**
- Revisar completitud de formularios al finalizar cada entrevista
- Confirmar que todas las coordenadas sean válidas (dentro del rango esperado)
- Validar que las fotos tengan georreferenciación
- Verificar consistencia entre respuestas (ej: ingresos vs. esfuerzo pesquero)

**Chequeo post-campo:**
- Revisar consistencia de IDs y formatos
- Validar que no haya datos faltantes críticos
- Confirmar que las transcripciones coincidan con las grabaciones
- Verificar que los metadatos de archivos sean correctos

**Herramientas de validación:**
- **ODK Validate:** Para formularios ODK Collect
- **QGIS:** Para validar geometrías y coordenadas
- **Python scripts:** Para validar consistencia de datos
- **Revisión por pares:** Validar con otro miembro del equipo

---

## Protocolos de Seguridad y Ética

### 1. Seguridad Personal

**En campo:**
- **Equipo básico:** Chaleco salvavidas, botas de agua, protección solar, repelente de insectos
- **Comunicación:** Radio portátil o teléfono satelital en zonas remotas
- **Transporte:** Usar embarcaciones seguras con motor en buen estado
- **Horarios:** Evitar navegación nocturna en zonas desconocidas
- **Clima:** Monitorear pronósticos y evitar salir con mal tiempo

**En comunidades:**
- **Presentación:** Mostrar credenciales y explicar el propósito de la visita
- **Acompañamiento:** Siempre ir acompañado de un miembro de la comunidad
- **Respeto:** Seguir normas culturales y protocolos comunitarios
- **Horarios:** Respetar horarios de descanso y actividades comunitarias

### 2. Seguridad de Datos

**Físicos:**
- **Almacenamiento:** Usar maletines con candado para documentos en papel
- **Transporte:** Llevar copias digitales en dispositivos cifrados
- **Backup:** Hacer copias de seguridad diarias en la nube y en disco externo
- **Destrucción:** Triturar documentos sensibles al finalizar el proyecto

**Digitales:**
- **Cifrado:** Usar VeraCrypt o similar para archivos sensibles
- **Contraseñas:** Usar contraseñas fuertes y gestores de contraseñas
- **Acceso remoto:** Usar VPN y autenticación de dos factores
- **Eliminación segura:** Usar herramientas como BleachBit para eliminar archivos

### 3. Ética de Investigación

**Principios:**
- **Beneficencia:** Maximizar beneficios y minimizar riesgos para participantes
- **Justicia:** Distribución equitativa de cargas y beneficios
- **Autonomía:** Respeto a la autodeterminación de los participantes
- **Integridad:** Honestidad y transparencia en el proceso de investigación

**Conducta profesional:**
- **Transparencia:** Explicar claramente el propósito y métodos del estudio
- **Consentimiento:** Obtener consentimiento informado antes de cualquier interacción
- **Confidencialidad:** Proteger la identidad y datos personales de los participantes
- **Retroalimentación:** Compartir resultados con las comunidades participantes
- **No maleficencia:** No causar daño físico, emocional o social

**Manejo de conflictos:**
- **Imparcialidad:** Evitar tomar partido en conflictos comunitarios
- **Neutralidad:** No promover agendas políticas o económicas
- **Transparencia:** Declarar posibles conflictos de interés
- **Denuncia:** Reportar cualquier irregularidad a las autoridades competentes

### 4. Protocolos de Emergencia

**Salud:**
- Llevar botiquín básico con medicamentos para mal de mar, alergias y heridas
- Tener contacto de servicios médicos locales
- En caso de enfermedad o lesión grave, evacuar inmediatamente

**Seguridad:**
- En caso de conflicto comunitario, retirarse y buscar refugio seguro
- En caso de amenaza de violencia, contactar a autoridades locales y retirarse
- En caso de accidente marítimo, activar protocolo de emergencia y usar equipo de flotación

**Ambientales:**
- En caso de derrame o contaminación, notificar inmediatamente a PROFEPA y SEMAR
- Documentar con fotos y videos para evidencia
- Evitar contacto con sustancias peligrosas

---

## Cronograma Recomendado

| Actividad | Duración | Responsable | Herramientas |
|-----------|----------|-------------|--------------|
| **Preparación** | 3 días | Investigador | Consentimientos, permisos, equipo |
| **Punta Chueca - Fase 1** | 5 días | Gorosave + equipo | Talleres, entrevistas, mapeo |
| **Punta Chueca - Fase 2** | 3 días | Gorosave + ancianos | Entrevistas profundas, rituales |
| **Puerto Libertad - Fase 1** | 4 días | Gorosave + equipo | Encuestas, mapeo, incidentes |
| **Puerto Libertad - Fase 2** | 2 días | Gorosave + cooperativas | Talleres, validación |
| **Guaymas - Fase 1** | 5 días | Gorosave + equipo | Encuestas, mapeo, incidentes |
| **Guaymas - Fase 2** | 3 días | Gorosave + cooperativas | Talleres, validación |
| **Análisis preliminar** | 3 días | Equipo técnico | QGIS, Python, Excel |
| **Redacción de informes** | 4 días | Gorosave + equipo | Documentos, mapas, dashboards |

**Total:** 32 días (6 semanas y 2 días)

---

## Equipo Requerido

### Equipo de Campo
- **Enrique Gorosave:** Investigador principal (especialista en comunidades indígenas)
- **1 Asistente de campo:** Apoyo en logística y grabación
- **1 Técnico en SIG:** Manejo de GPS y software de mapeo
- **1 Traductor:** Lengua Comca'ac (para Punta Chueca)
- **2 Guías locales:** Conocimiento de rutas y prácticas tradicionales

### Equipo Técnico
- **2 GPS de alta precisión** (Garmin GPSMAP 66i o equivalente)
- **2 Tablets** con aplicaciones de mapeo (ODK Collect, QField, KoboToolbox)
- **2 Cámaras fotográficas** (12 MP mínimo, con GPS integrado)
- **2 Grabadoras de audio digitales**
- **2 Teléfonos satelitales** (para zonas sin cobertura celular)
- **1 Computadora portátil** para procesamiento inicial
- **1 Disco duro externo** (1TB mínimo) para backups
- **Botiquín de primeros auxilios** completo
- **Equipo de seguridad marítima** (chalecos salvavidas, boyas, luces de emergencia)

### Software Requerido
- **ODK Collect** o **KoboToolbox** para formularios móviles
- **QGIS** con plugins de H3 para análisis espacial
- **Google Earth Pro** para visualización
- **Audacity** para edición de audio
- **VLC** para reproducción de video
- **7-Zip** o **VeraCrypt** para cifrado de datos
- **LibreOffice** o **Microsoft Office** para procesamiento de textos

---

## Presupuesto Estimado

| Concepto | Costo (MXN) | Notas |
|----------|-------------|-------|
| **Personal** | $45,000 | 32 días × 3 personas × $500/día |
| **Equipo de campo** | $12,000 | Compra/alquiler de GPS, tablets, cámaras |
| **Transporte** | $8,000 | Gasolina, peajes, transporte marítimo |
| **Alojamiento y alimentación** | $15,000 | 32 días × $500/día/persona |
| **Materiales** | $3,000 | Consentimientos, formularios, copias |
| **Software y licencias** | $2,000 | QGIS, ODK, antivirus |
| **Seguros** | $5,000 | Seguro médico y de equipo |
| **Backup y almacenamiento** | $1,000 | Discos duros, servicios en la nube |
| **Imprevistos** | $4,000 | 10% del total |
| **Total** | **$95,000** | |

---

## Contactos Clave

### Autoridades Locales
- **Presidente Municipal de Hermosillo:** [Nombre y contacto]
- **Capitanía de Puerto de Guaymas:** [Nombre y contacto]
- **Capitanía de Puerto de Puerto Libertad:** [Nombre y contacto]
- **Delegado de SEMARNAT en Sonora:** [Nombre y contacto]
- **Delegado de CONAPESCA en Sonora:** [Nombre y contacto]

### Organizaciones Comunitarias
- **Consejo de la Nación Comca'ac:** [Nombre y contacto]
- **Cooperativa de Pescadores de Puerto Libertad:** [Nombre y contacto]
- **Cooperativa de Pescadores Ribereños de Guaymas:** [Nombre y contacto]
- **Red de Cooperativas Pesqueras del Golfo:** [Nombre y contacto]

### Investigadores y Colaboradores
- **Dr. [Nombre]:** Investigador principal del proyecto PANGAS
- **Dra. [Nombre]:** Especialista en gobernanza comunitaria
- **Ing. [Nombre]:** Experto en SIG y análisis espacial
- **Lic. [Nombre]:** Asesor legal en derechos indígenas

---

## Anexos

### Anexo 1: Lista de Verificación Pre-Campo

- [ ] Consentimientos informados impresos y firmados
- [ ] Equipo de campo revisado y funcional
- [ ] Permisos de autoridades locales obtenidos
- [ ] Contactos clave confirmados
- [ ] Transporte reservado
- [ ] Alojamiento reservado
- [ ] Seguros contratados
- [ ] Copias de seguridad de datos iniciales
- [ ] Plan de emergencia comunicado a todo el equipo
- [ ] Cronograma impreso y distribuido

### Anexo 2: Lista de Verificación Post-Campo

- [ ] Todos los formularios completos y validados
- [ ] Datos digitalizados y respaldados
- [ ] Fotos y videos organizados y etiquetados
- [ ] Entrevistas transcritas
- [ ] Mapas generados y validados
- [ ] Informe preliminar redactado
- [ ] Datos sensibles almacenados de forma segura
- [ ] Equipo devuelto y revisado
- [ ] Agradecimientos enviados a participantes
- [ ] Plan de análisis futuro definido

### Anexo 3: Glosario de Términos Comca'ac

| Término en Comca'ac | Traducción al español | Significado cultural |
|---------------------|----------------------|---------------------|
| **Hant Comca'ac** | Pueblo Comca'ac | Nación indígena del Golfo de California |
| **Xepe** | Mar | Espacio vital y sagrado |
| **Maso** | Isla | Territorio ancestral |
| **Cmiique Iitom** | Conocimiento tradicional | Saberes ancestrales sobre el territorio |
| **Hapij** | Canoa | Embarcación tradicional |
| **Hant Ihi** | Jefe tradicional | Líder comunitario reconocido |
| **Ihí** | Casa | Espacio familiar y comunitario |
| **Cöihui** | Fiesta | Celebración ritual y comunitaria |

---

**Nota final:** Estos protocolos establecen el marco metodológico y ético para la recolección de datos en campo. Se requiere ajustar los detalles específicos según las condiciones reales en cada comunidad y puerto. La validación con actores locales es esencial para garantizar la calidad y pertinencia de los datos recolectados.

**Próxima revisión:** 15 de agosto de 2026 (tras primera ronda de recolección de datos)