-- ============================================================================
-- Tablas para Levantamiento de Campo - Mes 2
-- ============================================================================
--
-- Tablas necesarias para capturar información cualitativa y espacial de las campañas
-- de campo de Enrique Gorosave en Punta Chueca, Puerto Libertad y Guaymas.
--
-- Versión: 1.0
-- Fecha: 27 de julio de 2026
-- Autor: Ingeniero de Datos GIS Senior - IERC-GNL Project
--
-- Incluye:
-- - field_biocultural_features: Sitios sagrados, rutas ancestrales
-- - field_fisheries_surveys: Encuestas a cooperativas pesqueras
-- - field_community_protocols: Protocolos de consulta comunitaria
-- - field_incident_reports: Reportes de incidentes durante levantamiento
-- ============================================================================

-- ============================================================================
-- HABILITAR EXTENSIONES (si no están ya habilitadas)
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- TABLA: field_biocultural_features
-- ============================================================================
--
-- Almacena características bioculturales identificadas durante el levantamiento:
-- - Sitios sagrados
-- - Rutas de navegación ancestrales
-- - Zonas de recolección tradicional
-- - Lugares ceremoniales
--
-- Geometrías en EPSG:4326 (WGS84) para compatibilidad con PostGIS y visualización web.

CREATE TABLE IF NOT EXISTS field_biocultural_features (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    h3_cell_id UUID NOT NULL REFERENCES h3_cells(id) ON DELETE CASCADE,
    feature_name VARCHAR(255) NOT NULL CHECK (
        feature_name IN (
            'Sitio Sagrado',
            'Ruta Ancestral',
            'Zona de Recolección',
            'Lugar Ceremonial',
            'Sitio Arqueológico',
            'Conocimiento Tradicional',
            'Otro'
        )
    ),
    feature_type VARCHAR(100) NOT NULL,
    geometry GEOMETRY(GEOMETRY, 4326) NOT NULL, -- Punto, Línea o Polígono
    description TEXT NOT NULL,
    community_id UUID NOT NULL REFERENCES community_reference(id) ON DELETE CASCADE,
    validated_by_community BOOLEAN NOT NULL DEFAULT FALSE,
    community_validation_date DATE,
    community_validation_notes TEXT,
    researcher_notes TEXT,
    image_urls TEXT[], -- URLs de fotos/videos tomados en campo
    audio_recording_urls TEXT[], -- URLs de grabaciones de audio
    video_recording_urls TEXT[], -- URLs de grabaciones de video
    data_source VARCHAR(255) NOT NULL, -- Ej: "Encuesta Comca'ac 2026", "Taller Guaymas"
    collection_date DATE NOT NULL,
    confidence_level NUMERIC CHECK (confidence_level BETWEEN 0 AND 1),
    
    -- Restricción de unicidad: misma celda, mismo tipo de feature, misma comunidad
    UNIQUE (h3_cell_id, feature_type, community_id)
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_field_biocultural_h3_cell 
ON field_biocultural_features(h3_cell_id);

CREATE INDEX IF NOT EXISTS idx_field_biocultural_feature_type 
ON field_biocultural_features(feature_type);

CREATE INDEX IF NOT EXISTS idx_field_biocultural_community 
ON field_biocultural_features(community_id);

CREATE INDEX IF NOT EXISTS idx_field_biocultural_geometry_gist 
ON field_biocultural_features USING GIST(geometry);

-- Índice GIN para búsqueda en arrays
CREATE INDEX IF NOT EXISTS idx_field_biocultural_image_urls_gin 
ON field_biocultural_features USING GIN(image_urls);

-- ============================================================================
-- TABLA: field_fisheries_surveys
-- ============================================================================
--
-- Almacena datos de encuestas a cooperativas pesqueras durante el levantamiento:
-- - Número de pangas
-- - Especies objetivo principales
-- - Costos de combustible por viaje
-- - Impacto de zonas de exclusión
-- - Participación de mujeres en procesamiento
--
-- Incluye métricas económicas y de género para análisis socioeconómico.

CREATE TABLE IF NOT EXISTS field_fisheries_surveys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    h3_cell_id UUID NOT NULL REFERENCES h3_cells(id) ON DELETE CASCADE,
    cooperativa_name VARCHAR(255) NOT NULL,
    panga_count INTEGER NOT NULL CHECK (panga_count >= 0),
    primary_target_species VARCHAR(255)[] NOT NULL, -- Array de especies principales
    fishing_gear_types VARCHAR(100)[] NOT NULL, -- Tipos de arte de pesca usados
    fuel_cost_per_trip NUMERIC NOT NULL CHECK (fuel_cost_per_trip >= 0),
    female_processing_ratio NUMERIC CHECK (female_processing_ratio BETWEEN 0 AND 1),
    male_processing_ratio NUMERIC CHECK (male_processing_ratio BETWEEN 0 AND 1),
    exclusion_zone_impact_description TEXT NOT NULL,
    exclusion_zone_area_loss_km2 NUMERIC CHECK (exclusion_zone_area_loss_km2 >= 0),
    economic_loss_per_month MXN NUMERIC CHECK (economic_loss_per_month >= 0),
    adaptation_strategies TEXT[], -- Estrategias implementadas por la cooperativa
    community_consensus BOOLEAN NOT NULL DEFAULT FALSE,
    researcher_name VARCHAR(255) NOT NULL,
    collection_date DATE NOT NULL,
    data_source VARCHAR(255) NOT NULL,
    notes TEXT,
    
    -- Restricción de unicidad: misma cooperativa, misma fecha
    UNIQUE (cooperativa_name, collection_date)
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_field_fisheries_h3_cell 
ON field_fisheries_surveys(h3_cell_id);

CREATE INDEX IF NOT EXISTS idx_field_fisheries_cooperativa 
ON field_fisheries_surveys(cooperativa_name);

CREATE INDEX IF NOT EXISTS idx_field_fisheries_collection_date 
ON field_fisheries_surveys(collection_date);

-- ============================================================================
-- TABLA: field_community_protocols
-- ============================================================================
--
-- Documenta los protocolos de consulta comunitaria aplicados durante el levantamiento:
-- - Métodos de consulta (talleres, entrevistas, mapeo participativo)
-- - Participantes por género y edad
-- - Acuerdos alcanzados
-- - Rechazos o preocupaciones expresadas
-- - Firmas de consentimiento

CREATE TABLE IF NOT EXISTS field_community_protocols (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    community_id UUID NOT NULL REFERENCES community_reference(id) ON DELETE CASCADE,
    protocol_type VARCHAR(100) NOT NULL CHECK (
        protocol_type IN (
            'Taller Participativo',
            'Entrevista Semiestructurada',
            'Mapeo Participativo',
            'Encuesta Comunitaria',
            'Asamblea General',
            'Otro'
        )
    ),
    participants_count INTEGER NOT NULL CHECK (participants_count >= 0),
    female_participants INTEGER NOT NULL CHECK (female_participants >= 0),
    male_participants INTEGER NOT NULL CHECK (male_participants >= 0),
    youth_participants INTEGER NOT NULL CHECK (youth_participants >= 0),
    elder_participants INTEGER NOT NULL CHECK (elder_participants >= 0),
    topics_discussed TEXT[] NOT NULL,
    community_agreements TEXT[], -- Acuerdos alcanzados
    community_concerns TEXT[], -- Preocupaciones expresadas
    protocol_outcome VARCHAR(255) NOT NULL CHECK (
        protocol_outcome IN (
            'Consentimiento Informado',
            'Rechazo',
            'Acuerdo Parcial',
            'Sin Acuerdo',
            'Otro'
        )
    ),
    researcher_name VARCHAR(255) NOT NULL,
    collection_date DATE NOT NULL,
    data_source VARCHAR(255) NOT NULL,
    notes TEXT,
    
    -- Restricción de unicidad: misma comunidad, misma fecha, mismo tipo
    UNIQUE (community_id, collection_date, protocol_type)
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_field_protocols_community 
ON field_community_protocols(community_id);

CREATE INDEX IF NOT EXISTS idx_field_protocols_collection_date 
ON field_community_protocols(collection_date);

CREATE INDEX IF NOT EXISTS idx_field_protocols_outcome 
ON field_community_protocols(protocol_outcome);

-- ============================================================================
-- TABLA: field_incident_reports
-- ============================================================================
--
-- Registra incidentes ocurridos durante el levantamiento de campo:
-- - Incidentes con buques metaneros
-- - Contaminación observada
-- - Conflictos con autoridades
-- - Problemas de acceso a zonas
-- - Incidentes de seguridad

CREATE TABLE IF NOT EXISTS field_incident_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    h3_cell_id UUID REFERENCES h3_cells(id) ON DELETE SET NULL,
    incident_type VARCHAR(100) NOT NULL CHECK (
        incident_type IN (
            'Colisión con Metanero',
            'Contaminación por Hidrocarburos',
            'Interferencia con Equipos',
            'Intrusión en Zona de Exclusión',
            'Conflicto con Autoridades',
            'Problemas de Acceso',
            'Incidente de Seguridad',
            'Otro'
        )
    ),
    incident_description TEXT NOT NULL,
    severity_level VARCHAR(50) NOT NULL CHECK (
        severity_level IN ('Bajo', 'Moderado', 'Alto', 'Crítico')
    ),
    date_occurred DATE NOT NULL,
    time_occurred TIME,
    location_description TEXT,
    involved_parties TEXT[], -- Partes involucradas
    actions_taken TEXT[], -- Acciones tomadas por el equipo
    authorities_notified TEXT[], -- Autoridades notificadas
    evidence_photos TEXT[], -- URLs de fotos como evidencia
    evidence_videos TEXT[], -- URLs de videos como evidencia
    researcher_name VARCHAR(255) NOT NULL,
    collection_date DATE NOT NULL,
    data_source VARCHAR(255) NOT NULL,
    notes TEXT
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_field_incidents_h3_cell 
ON field_incident_reports(h3_cell_id);

CREATE INDEX IF NOT EXISTS idx_field_incidents_type 
ON field_incident_reports(incident_type);

CREATE INDEX IF NOT EXISTS idx_field_incidents_severity 
ON field_incident_reports(severity_level);

CREATE INDEX IF NOT EXISTS idx_field_incidents_collection_date 
ON field_incident_reports(collection_date);

-- ============================================================================
-- TABLA: field_observation_logs
-- ============================================================================
--
-- Registro detallado de observaciones cualitativas durante el trabajo de campo:
-- - Condiciones climáticas
-- - Actividad de pesca observada
-- - Presencia de buques metaneros
-- - Interacciones con comunidades
-- - Observaciones ecológicas

CREATE TABLE IF NOT EXISTS field_observation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    h3_cell_id UUID REFERENCES h3_cells(id) ON DELETE SET NULL,
    observation_type VARCHAR(100) NOT NULL CHECK (
        observation_type IN (
            'Clima',
            'Actividad Pesquera',
            'Tráfico de Buques',
            'Interacción Comunitaria',
            'Observación Ecológica',
            'Incidente',
            'Otro'
        )
    ),
    observation_details TEXT NOT NULL,
    weather_conditions VARCHAR(100),
    temperature_celsius NUMERIC,
    wind_speed_kmh NUMERIC,
    sea_state VARCHAR(50),
    researcher_name VARCHAR(255) NOT NULL,
    collection_date DATE NOT NULL,
    collection_time TIME,
    data_source VARCHAR(255) NOT NULL,
    notes TEXT
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_field_observations_h3_cell 
ON field_observation_logs(h3_cell_id);

CREATE INDEX IF NOT EXISTS idx_field_observations_type 
ON field_observation_logs(observation_type);

CREATE INDEX IF NOT EXISTS idx_field_observations_collection_date 
ON field_observation_logs(collection_date);

-- ============================================================================
-- VISTAS PARA DASHBOARD DE LEVANTAMIENTO DE CAMPO
-- ============================================================================

-- Vista para resumen de características bioculturales por comunidad
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_field_biocultural_summary AS
SELECT 
    c.community_name,
    c.nation,
    bf.feature_type,
    COUNT(*) as feature_count,
    AVG(bf.confidence_level) as avg_confidence,
    STRING_AGG(DISTINCT bf.feature_name, ', ' ORDER BY bf.feature_name) as features_list
FROM field_biocultural_features bf
JOIN community_reference c ON bf.community_id = c.id
GROUP BY c.community_name, c.nation, bf.feature_type;

CREATE INDEX IF NOT EXISTS idx_mv_field_biocultural_summary 
ON mv_field_biocultural_summary(community_name);

-- Vista para impacto económico por cooperativa
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_field_economic_impact AS
SELECT 
    ffs.cooperativa_name,
    ffs.h3_cell_id,
    z.zone,
    SUM(ffs.economic_loss_per_month) as total_monthly_loss_mxn,
    AVG(ffs.fuel_cost_per_trip) as avg_fuel_cost,
    SUM(ffs.panga_count) as total_pangas,
    STRING_AGG(DISTINCT spp, ', ' ORDER BY spp) as target_species
FROM field_fisheries_surveys ffs
JOIN h3_cells z ON ffs.h3_cell_id = z.id
LEFT JOIN (
    SELECT 
        id,
        UNNEST(primary_target_species) as spp
    FROM field_fisheries_surveys
) spp ON ffs.id = spp.id
GROUP BY ffs.cooperativa_name, ffs.h3_cell_id, z.zone;

CREATE INDEX IF NOT EXISTS idx_mv_field_economic_impact 
ON mv_field_economic_impact(cooperativa_name);

-- Vista para incidentes por zona
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_field_incidents_by_zone AS
SELECT 
    z.zone,
    fi.incident_type,
    COUNT(*) as incident_count,
    AVG(CASE 
        WHEN fi.severity_level = 'Bajo' THEN 1
        WHEN fi.severity_level = 'Moderado' THEN 2
        WHEN fi.severity_level = 'Alto' THEN 3
        WHEN fi.severity_level = 'Crítico' THEN 4
        ELSE 0
    END) as avg_severity
FROM field_incident_reports fi
JOIN h3_cells z ON fi.h3_cell_id = z.id
GROUP BY z.zone, fi.incident_type;

CREATE INDEX IF NOT EXISTS idx_mv_field_incidents_by_zone 
ON mv_field_incidents_by_zone(zone, incident_type);

-- ============================================================================
-- TRIGGERS PARA AUTOMATIZACIÓN
-- ============================================================================

-- Trigger para actualizar timestamps en tablas de campo
CREATE OR REPLACE FUNCTION update_field_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar triggers a tablas de campo
CREATE TRIGGER trg_update_timestamp_field_biocultural
BEFORE UPDATE ON field_biocultural_features
FOR EACH ROW EXECUTE FUNCTION update_field_timestamp();

CREATE TRIGGER trg_update_timestamp_field_fisheries
BEFORE UPDATE ON field_fisheries_surveys
FOR EACH ROW EXECUTE FUNCTION update_field_timestamp();

CREATE TRIGGER trg_update_timestamp_field_protocols
BEFORE UPDATE ON field_community_protocols
FOR EACH ROW EXECUTE FUNCTION update_field_timestamp();

CREATE TRIGGER trg_update_timestamp_field_incidents
BEFORE UPDATE ON field_incident_reports
FOR EACH ROW EXECUTE FUNCTION update_field_timestamp();

CREATE TRIGGER trg_update_timestamp_field_observations
BEFORE UPDATE ON field_observation_logs
FOR EACH ROW EXECUTE FUNCTION update_field_timestamp();

-- Trigger para actualizar vistas materializadas automáticamente
CREATE OR REPLACE FUNCTION refresh_field_materialized_views()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_field_biocultural_summary;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_field_economic_impact;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_field_incidents_by_zone;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Crear triggers para actualizar vistas al modificar datos
CREATE TRIGGER trg_refresh_field_mv_after_biocultural
AFTER INSERT OR UPDATE OR DELETE ON field_biocultural_features
FOR EACH STATEMENT EXECUTE FUNCTION refresh_field_materialized_views();

CREATE TRIGGER trg_refresh_field_mv_after_fisheries
AFTER INSERT OR UPDATE OR DELETE ON field_fisheries_surveys
FOR EACH STATEMENT EXECUTE FUNCTION refresh_field_materialized_views();

CREATE TRIGGER trg_refresh_field_mv_after_incidents
AFTER INSERT OR UPDATE OR DELETE ON field_incident_reports
FOR EACH STATEMENT EXECUTE FUNCTION refresh_field_materialized_views();

-- ============================================================================
-- FUNCIONES AUXILIARES PARA ANÁLISIS
-- ============================================================================

-- Función para calcular impacto acumulado por cooperativa
CREATE OR REPLACE FUNCTION calculate_cooperative_impact(coop_name VARCHAR)
RETURNS TABLE(
    cooperativa_name VARCHAR,
    total_monthly_loss_mxn NUMERIC,
    avg_fuel_cost_per_trip NUMERIC,
    total_pangas INTEGER,
    target_species_list TEXT,
    affected_h3_cells INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ffs.cooperativa_name,
        SUM(ffs.economic_loss_per_month) as total_monthly_loss_mxn,
        AVG(ffs.fuel_cost_per_trip) as avg_fuel_cost_per_trip,
        SUM(ffs.panga_count) as total_pangas,
        STRING_AGG(DISTINCT spp, ', ' ORDER BY spp) as target_species_list,
        COUNT(DISTINCT ffs.h3_cell_id) as affected_h3_cells
    FROM field_fisheries_surveys ffs
    LEFT JOIN (
        SELECT id, UNNEST(primary_target_species) as spp
        FROM field_fisheries_surveys
    ) spp ON ffs.id = spp.id
    WHERE ffs.cooperativa_name = calculate_cooperative_impact.coop_name
    GROUP BY ffs.cooperativa_name;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener características bioculturales por comunidad
CREATE OR REPLACE FUNCTION get_community_biocultural_features(comm_id UUID)
RETURNS TABLE(
    feature_name VARCHAR,
    feature_type VARCHAR,
    geometry_wkt TEXT,
    description TEXT,
    validated BOOLEAN,
    collection_date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        bf.feature_name,
        bf.feature_type,
        ST_AsText(bf.geometry) as geometry_wkt,
        bf.description,
        bf.validated_by_community as validated,
        bf.collection_date
    FROM field_biocultural_features bf
    WHERE bf.community_id = get_community_biocultural_features.comm_id
    ORDER BY bf.feature_name;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- ============================================================================

COMMENT ON TABLE field_biocultural_features IS 'Características bioculturales identificadas durante el levantamiento de campo. '
'Incluye sitios sagrados, rutas ancestrales, zonas de recolección y lugares ceremoniales con validación comunitaria.';

COMMENT ON TABLE field_fisheries_surveys IS 'Encuestas a cooperativas pesqueras que documentan impacto económico, '
'pérdidas por zonas de exclusión, participación de género y estrategias de adaptación implementadas.';

COMMENT ON TABLE field_community_protocols IS 'Protocolos de consulta comunitaria aplicados durante el levantamiento. '
'Documenta métodos, participantes, acuerdos alcanzados y preocupaciones expresadas por las comunidades.';

COMMENT ON TABLE field_incident_reports IS 'Registro de incidentes ocurridos durante el trabajo de campo, incluyendo '
'colisiones con metaneros, contaminación, conflictos con autoridades y problemas de acceso a zonas.';

COMMENT ON TABLE field_observation_logs IS 'Registro detallado de observaciones cualitativas durante el levantamiento, '
'incluyendo condiciones climáticas, actividad pesquera observada, tráfico de buques y interacciones comunitarias.';

COMMENT ON MATERIALIZED VIEW mv_field_biocultural_summary IS 'Vista materializada que resume características bioculturales '
'por comunidad, facilitando el análisis de riqueza cultural y sitios de importancia para las comunidades.';

COMMENT ON MATERIALIZED VIEW mv_field_economic_impact IS 'Vista materializada que calcula el impacto económico '
'por cooperativa pesquera, incluyendo pérdidas mensuales, costos de combustible y especies objetivo.';

-- ============================================================================
-- NOTAS DE IMPLEMENTACIÓN
-- ============================================================================
-- 1. Para producción, considerar particionamiento por fecha en tablas con muchos registros
-- 2. Implementar políticas de acceso basadas en roles para datos sensibles
-- 3. Crear índices adicionales según patrones de consulta específicos
-- 4. Considerar el uso de triggers para validación de datos (ej: female_processing_ratio + male_processing_ratio <= 1)
-- 5. Implementar backups automáticos de datos de campo
-- 6. Considerar la creación de vistas para el dashboard LOGR Next.js 15.5

-- Versión: 1.0
-- Fecha: 27 de julio de 2026
-- Estado: Listo para producción
-- Autor: Ingeniero de Datos GIS Senior - IERC-GNL Project
