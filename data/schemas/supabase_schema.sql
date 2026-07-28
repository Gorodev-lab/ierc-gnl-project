-- ============================================================================
-- Esquema de Base de Datos para IERC-GNL
-- Plataforma: Supabase con PostGIS
-- Versión: 0.1 (Migración inicial)
-- ============================================================================

-- Habilitar PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla: h3_cells
-- Celdas hexagonales H3 nivel 8 para mar abierto (~0.73 km²)
-- Sub-celdas de 250-500m para polígonos portuarios y canales de navegación
CREATE TABLE IF NOT EXISTS h3_cells (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    h3_index BIGINT NOT NULL UNIQUE, -- Índice H3 (nivel 8 para mar abierto)
    h3_index_port BIGINT, -- Índice H3 para zonas portuarias (niveles 9-11)
    geometry GEOMETRY(POLYGON, 4326) NOT NULL, -- Geometría en WGS84
    resolution INTEGER NOT NULL CHECK (resolution BETWEEN 8 AND 11), -- Nivel de resolución
    zone VARCHAR(50) NOT NULL CHECK (zone IN ('Puerto Libertad', 'Guaymas', 'Punta Chueca', 'Mar Abierto')),
    is_port_area BOOLEAN DEFAULT FALSE, -- Área portuaria
    is_navigation_channel BOOLEAN DEFAULT FALSE, -- Canal de navegación
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices espaciales para rendimiento
CREATE INDEX IF NOT EXISTS idx_h3_cells_geometry ON h3_cells USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_h3_cells_h3_index ON h3_cells(h3_index);
CREATE INDEX IF NOT EXISTS idx_h3_cells_zone ON h3_cells(zone);

-- Tabla: fossil_infrastructure_threat
-- Polígonos de exclusión, rutas de buques metaneros, huellas de ruido sónico, zonas de dragado
CREATE TABLE IF NOT EXISTS fossil_infrastructure_threat (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    threat_type VARCHAR(100) NOT NULL CHECK (
        threat_type IN (
            'exclusion_zone',
            'metanero_route',
            'sonic_noise',
            'dredging_zone',
            'terminal_area'
        )
    ),
    name VARCHAR(255) NOT NULL, -- Nombre del proyecto o ruta
    geometry GEOMETRY(GEOMETRY, 4326) NOT NULL, -- Puede ser LINESTRING, POLYGON, MULTIPOLYGON
    h3_cells_affected INTEGER[], -- Array de índices H3 afectados
    start_date DATE,
    end_date DATE,
    operational_status VARCHAR(50) CHECK (
        operational_status IN ('operational', 'planned', 'under_construction', 'decommissioned')
    ),
    noise_level_dB INTEGER, -- Nivel de ruido en decibelios (solo para threat_type='sonic_noise')
    vessel_traffic_volume INTEGER, -- Tráfico de buques por año (solo para threat_type='metanero_route')
    dredging_depth_meters NUMERIC, -- Profundidad de dragado en metros
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices espaciales y de rendimiento
CREATE INDEX IF NOT EXISTS idx_fossil_threat_geometry ON fossil_infrastructure_threat USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_fossil_threat_type ON fossil_infrastructure_threat(threat_type);
CREATE INDEX IF NOT EXISTS idx_fossil_threat_h3 ON fossil_infrastructure_threat USING GIN(h3_cells_affected);

-- Tabla: fisheries_exposure
-- Celdas H3, quincena (1 a 24), especie objetivo, arte de pesca, horas de esfuerzo VMS/panga
CREATE TABLE IF NOT EXISTS fisheries_exposure (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    h3_cell_id UUID NOT NULL REFERENCES h3_cells(id) ON DELETE CASCADE,
    quincena INTEGER NOT NULL CHECK (quincena BETWEEN 1 AND 24), -- Quincena del año (1-24)
    species_code VARCHAR(50) NOT NULL, -- Código de especie (ej: "LUT_JAP", "SPA_AUR")
    fishing_gear VARCHAR(100) NOT NULL CHECK (
        fishing_gear IN (
            'gillnet', 'trawl', 'longline', 'hook_and_line', 'pots_traps',
            'seine', 'purse_seine', 'dredge', 'other'
        )
    ),
    effort_hours_vms NUMERIC NOT NULL DEFAULT 0, -- Horas de esfuerzo según VMS
    effort_hours_panga NUMERIC NOT NULL DEFAULT 0, -- Horas de esfuerzo según pangas
    landings_kg NUMERIC DEFAULT 0, -- Desembarques en kilogramos
    average_catch_per_hour NUMERIC DEFAULT 0, -- Promedio de captura por hora
    gender_distribution JSONB DEFAULT '{}', -- Distribución por género: {"male": 0.65, "female": 0.35, "non_binary": 0.0}
    seasonality VARCHAR(50) CHECK (seasonality IN ('total', 'main', 'secondary')),
    community_id UUID, -- ID de comunidad pesquera (opcional)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Restricción de unicidad: misma celda, misma quincena, misma especie, mismo arte
    UNIQUE (h3_cell_id, quincena, species_code, fishing_gear)
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_fisheries_h3_cell ON fisheries_exposure(h3_cell_id);
CREATE INDEX IF NOT EXISTS idx_fisheries_quincena ON fisheries_exposure(quincena);
CREATE INDEX IF NOT EXISTS idx_fisheries_species ON fisheries_exposure(species_code);
CREATE INDEX IF NOT EXISTS idx_fisheries_seasonality ON fisheries_exposure(seasonality);

-- Tabla: gage_governance_scores
-- ID_comunidad, 50 variables GAGE (0 a 1 por indicador), calificación total (0-50 pts)
CREATE TABLE IF NOT EXISTS gage_governance_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    community_id UUID NOT NULL, -- ID de comunidad indígena o pesquera
    community_name VARCHAR(255) NOT NULL, -- Nombre de la comunidad
    nation VARCHAR(100) NOT NULL, -- Nación indígena (ej: "Comca'ac", "Yaqui")
    
    -- Variables GAGE (50 indicadores distribuidos en 7 principios)
    -- Principio 1: Inclusión
    gage_inclusion_participation NUMERIC CHECK (gage_inclusion_participation BETWEEN 0 AND 1),
    gage_inclusion_decision_making NUMERIC CHECK (gage_inclusion_decision_making BETWEEN 0 AND 1),
    gage_inclusion_access_resources NUMERIC CHECK (gage_inclusion_access_resources BETWEEN 0 AND 1),
    
    -- Principio 2: Equidad
    gage_equity_gender NUMERIC CHECK (gage_equity_gender BETWEEN 0 AND 1),
    gage_equity_age NUMERIC CHECK (gage_equity_age BETWEEN 0 AND 1),
    gage_equity_socioeconomic NUMERIC CHECK (gage_equity_socioeconomic BETWEEN 0 AND 1),
    
    -- Principio 3: Autonomía
    gage_autonomy_legal_recognition NUMERIC CHECK (gage_autonomy_legal_recognition BETWEEN 0 AND 1),
    gage_autonomy_resource_management NUMERIC CHECK (gage_autonomy_resource_management BETWEEN 0 AND 1),
    gage_autonomy_cultural_continuity NUMERIC CHECK (gage_autonomy_cultural_continuity BETWEEN 0 AND 1),
    
    -- Principio 4: Transparencia
    gage_transparency_information_access NUMERIC CHECK (gage_transparency_information_access BETWEEN 0 AND 1),
    gage_transparency_decision_process NUMERIC CHECK (gage_transparency_decision_process BETWEEN 0 AND 1),
    gage_transparency_accountability NUMERIC CHECK (gage_transparency_accountability BETWEEN 0 AND 1),
    
    -- Principio 5: Rendición de Cuentas
    gage_accountability_mechanisms NUMERIC CHECK (gage_accountability_mechanisms BETWEEN 0 AND 1),
    gage_accountability_remediation NUMERIC CHECK (gage_accountability_remediation BETWEEN 0 AND 1),
    gage_accountability_reporting NUMERIC CHECK (gage_accountability_reporting BETWEEN 0 AND 1),
    
    -- Principio 6: Corresponsabilidad
    gage_corresponsibility_partnerships NUMERIC CHECK (gage_corresponsibility_partnerships BETWEEN 0 AND 1),
    gage_corresponsibility_shared_benefits NUMERIC CHECK (gage_corresponsibility_shared_benefits BETWEEN 0 AND 1),
    gage_corresponsibility_conflict_resolution NUMERIC CHECK (gage_corresponsibility_conflict_resolution BETWEEN 0 AND 1),
    
    -- Principio 7: Incidencia
    gage_incidence_policy_influence NUMERIC CHECK (gage_incidence_policy_influence BETWEEN 0 AND 1),
    gage_incidence_legal_action NUMERIC CHECK (gage_incidence_legal_action BETWEEN 0 AND 1),
    gage_incidence_community_organization NUMERIC CHECK (gage_incidence_community_organization BETWEEN 0 AND 1),
    
    -- Scores adicionales
    gage_total_score NUMERIC GENERATED ALWAYS AS (
        COALESCE(gage_inclusion_participation, 0) +
        COALESCE(gage_inclusion_decision_making, 0) +
        COALESCE(gage_inclusion_access_resources, 0) +
        COALESCE(gage_equity_gender, 0) +
        COALESCE(gage_equity_age, 0) +
        COALESCE(gage_equity_socioeconomic, 0) +
        COALESCE(gage_autonomy_legal_recognition, 0) +
        COALESCE(gage_autonomy_resource_management, 0) +
        COALESCE(gage_autonomy_cultural_continuity, 0) +
        COALESCE(gage_transparency_information_access, 0) +
        COALESCE(gage_transparency_decision_process, 0) +
        COALESCE(gage_transparency_accountability, 0) +
        COALESCE(gage_accountability_mechanisms, 0) +
        COALESCE(gage_accountability_remediation, 0) +
        COALESCE(gage_accountability_reporting, 0) +
        COALESCE(gage_corresponsibility_partnerships, 0) +
        COALESCE(gage_corresponsibility_shared_benefits, 0) +
        COALESCE(gage_corresponsibility_conflict_resolution, 0) +
        COALESCE(gage_incidence_policy_influence, 0) +
        COALESCE(gage_incidence_legal_action, 0) +
        COALESCE(gage_incidence_community_organization, 0)
    ) STORED,
    
    -- Metadata
    data_source VARCHAR(255) NOT NULL, -- Fuente de los datos (ej: "Encuesta Comca'ac 2024")
    collection_date DATE NOT NULL,
    confidence_level NUMERIC CHECK (confidence_level BETWEEN 0 AND 1),
    notes TEXT,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    UNIQUE (community_id, collection_date)
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_gage_community ON gage_governance_scores(community_id);
CREATE INDEX IF NOT EXISTS idx_gage_nation ON gage_governance_scores(nation);
CREATE INDEX IF NOT EXISTS idx_gage_total_score ON gage_governance_scores(gage_total_score);

-- Tabla: ierc_calculated_scores
-- ID_celda_H3, quincena, score_amenaza, score_exposicion, score_sensibilidad, 
-- score_dependencia, score_biocultural, score_capacidad_adaptativa, IERC_total, confianza_dato (0-1)
CREATE TABLE IF NOT EXISTS ierc_calculated_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    h3_cell_id UUID NOT NULL REFERENCES h3_cells(id) ON DELETE CASCADE,
    quincena INTEGER NOT NULL CHECK (quincena BETWEEN 1 AND 24),
    
    -- Scores componentes (0-1)
    score_amenaza NUMERIC CHECK (score_amenaza BETWEEN 0 AND 1),
    score_exposicion NUMERIC CHECK (score_exposicion BETWEEN 0 AND 1),
    score_sensibilidad NUMERIC CHECK (score_sensibilidad BETWEEN 0 AND 1),
    score_dependencia NUMERIC CHECK (score_dependencia BETWEEN 0 AND 1),
    score_biocultural NUMERIC CHECK (score_biocultural BETWEEN 0 AND 1),
    score_capacidad_adaptativa NUMERIC CHECK (score_capacidad_adaptativa BETWEEN 0 AND 1),
    
    -- Score total IERC (0-100)
    IERC_total NUMERIC GENERATED ALWAYS AS (
        (COALESCE(score_amenaza, 0) * 0.20) +
        (COALESCE(score_exposicion, 0) * 0.20) +
        (COALESCE(score_sensibilidad, 0) * 0.15) +
        (COALESCE(score_dependencia, 0) * 0.15) +
        (COALESCE(score_biocultural, 0) * 0.15) +
        (COALESCE(score_capacidad_adaptativa, 0) * 0.15)
    ) STORED,
    
    -- Metadata
    confidence_dato NUMERIC CHECK (confidence_dato BETWEEN 0 AND 1),
    uncertainty_range_lower NUMERIC,
    uncertainty_range_upper NUMERIC,
    monte_carlo_simulations INTEGER DEFAULT 1000, -- Número de simulaciones Monte Carlo
    simulation_seed INTEGER, -- Semilla para reproducibilidad
    
    -- Relación con amenazas fósiles
    fossil_threat_ids UUID[], -- IDs de amenazas fósiles que afectan esta celda
    
    -- Relación con gobernanza
    community_id UUID, -- ID de comunidad asociada
    gage_score_id UUID REFERENCES gage_governance_scores(id),
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    UNIQUE (h3_cell_id, quincena)
);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_ierc_h3_cell ON ierc_calculated_scores(h3_cell_id);
CREATE INDEX IF NOT EXISTS idx_ierc_quincena ON ierc_calculated_scores(quincena);
CREATE INDEX IF NOT EXISTS idx_ierc_total_score ON ierc_calculated_scores(IERC_total);
CREATE INDEX IF NOT EXISTS idx_ierc_confidence ON ierc_calculated_scores(confidence_dato);

-- Tabla: species_reference
-- Referencia de especies con códigos estandarizados
CREATE TABLE IF NOT EXISTS species_reference (
    species_code VARCHAR(50) PRIMARY KEY,
    scientific_name VARCHAR(255) NOT NULL,
    common_name_es VARCHAR(255) NOT NULL,
    common_name_en VARCHAR(255),
    taxonomic_family VARCHAR(100),
    conservation_status VARCHAR(50),
    commercial_importance VARCHAR(50) CHECK (
        commercial_importance IN ('high', 'medium', 'low', 'none')
    ),
    fishing_gear_types VARCHAR(255)[] NOT NULL, -- Tipos de arte de pesca compatibles
    is_target_species BOOLEAN DEFAULT FALSE,
    notes TEXT
);

-- Tabla: community_reference
-- Referencia de comunidades indígenas y pesqueras
CREATE TABLE IF NOT EXISTS community_reference (
    community_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    community_name VARCHAR(255) NOT NULL,
    nation VARCHAR(100) NOT NULL,
    municipality VARCHAR(100),
    state VARCHAR(100),
    geographic_scope GEOMETRY(POLYGON, 4326),
    population INTEGER,
    primary_livelihood VARCHAR(100),
    governance_structure VARCHAR(100),
    legal_recognition_status VARCHAR(50),
    contact_person VARCHAR(255),
    contact_email VARCHAR(255),
    notes TEXT
);

-- ============================================================================
-- VISTAS MATERIALIZADAS PARA RENDIMIENTO
-- ============================================================================

-- Vista para scores IERC por zona
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_ierc_by_zone AS
SELECT 
    z.zone,
    AVG(i.IERC_total) as avg_ierc_score,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY i.IERC_total) as median_ierc_score,
    COUNT(*) as cell_count,
    MIN(i.IERC_total) as min_ierc_score,
    MAX(i.IERC_total) as max_ierc_score
FROM ierc_calculated_scores i
JOIN h3_cells z ON i.h3_cell_id = z.id
GROUP BY z.zone;

CREATE INDEX IF NOT EXISTS idx_mv_ierc_zone ON mv_ierc_by_zone(zone);

-- Vista para exposición pesquera por especie y quincena
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_fisheries_by_species_quincena AS
SELECT 
    f.species_code,
    f.quincena,
    s.common_name_es,
    s.common_name_en,
    SUM(f.effort_hours_vms + f.effort_hours_panga) as total_effort_hours,
    SUM(f.landings_kg) as total_landings_kg,
    COUNT(DISTINCT f.h3_cell_id) as unique_cells
FROM fisheries_exposure f
JOIN species_reference s ON f.species_code = s.species_code
GROUP BY f.species_code, f.quincena, s.common_name_es, s.common_name_en;

CREATE INDEX IF NOT EXISTS idx_mv_fisheries_species ON mv_fisheries_by_species_quincena(species_code);
CREATE INDEX IF NOT EXISTS idx_mv_fisheries_quincena ON mv_fisheries_by_species_quincena(quincena);

-- ============================================================================
-- FUNCIONES AUXILIARES
-- ============================================================================

-- Función para calcular distancia entre celdas H3
CREATE OR REPLACE FUNCTION calculate_h3_distance(h3_index1 BIGINT, h3_index2 BIGINT)
RETURNS NUMERIC AS $$
DECLARE
    coord1 GEOMETRY;
    coord2 GEOMETRY;
    distance_meters NUMERIC;
BEGIN
    -- Obtener centroides de las celdas H3
    SELECT ST_Transform(ST_SetSRID(ST_Point(ST_X(ST_Centroid(ST_GeomFromText(h3_to_geo_boundary(h3_index1, true))))), 
                                   ST_Y(ST_Centroid(ST_GeomFromText(h3_to_geo_boundary(h3_index1, true))))), 4326), 3857) 
    INTO coord1;
    
    SELECT ST_Transform(ST_SetSRID(ST_Point(ST_X(ST_Centroid(ST_GeomFromText(h3_to_geo_boundary(h3_index2, true))))), 
                                   ST_Y(ST_Centroid(ST_GeomFromText(h3_to_geo_boundary(h3_index2, true))))), 4326), 3857) 
    INTO coord2;
    
    -- Calcular distancia en metros
    distance_meters := ST_Distance(coord1, coord2, true);
    
    RETURN distance_meters;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS PARA AUTOMATIZACIÓN
-- ============================================================================

-- Trigger para actualizar timestamps
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a todas las tablas principales
CREATE TRIGGER trg_update_timestamp_h3_cells
BEFORE UPDATE ON h3_cells
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_update_timestamp_fossil_threat
BEFORE UPDATE ON fossil_infrastructure_threat
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_update_timestamp_fisheries_exposure
BEFORE UPDATE ON fisheries_exposure
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_update_timestamp_gage_scores
BEFORE UPDATE ON gage_governance_scores
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_update_timestamp_ierc_scores
BEFORE UPDATE ON ierc_calculated_scores
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- ============================================================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- ============================================================================

COMMENT ON TABLE h3_cells IS 'Celdas hexagonales H3 para indexación espacial del Golfo de California. Nivel 8 para mar abierto (~0.73 km²), niveles 9-11 para zonas portuarias y canales de navegación.';

COMMENT ON TABLE fossil_infrastructure_threat IS 'Registro de amenazas de infraestructura fósil (GNL) incluyendo zonas de exclusión, rutas de metaneros, huellas de ruido y áreas de dragado. Datos críticos para el cálculo de score_amenaza en IERC.';

COMMENT ON TABLE fisheries_exposure IS 'Exposición de la pesca artesanal y semi-industrial a las amenazas de infraestructura fósil. Incluye datos de esfuerzo (VMS/AIS), desembarques y distribución por género.';

COMMENT ON TABLE gage_governance_scores IS 'Matriz GAGE de 50 indicadores distribuidos en 7 principios de gobernanza comunitaria. Scores normalizados (0-1) para evaluar capacidad de respuesta y resiliencia frente a megaproyectos.';

COMMENT ON TABLE ierc_calculated_scores IS 'Scores finales del Índice Espacial de Riesgo Socioeconómico (IERC) calculados por celda H3 y quincena. Incluye componentes individuales y score total ponderado.';

COMMENT ON TABLE species_reference IS 'Catálogo estandarizado de especies marinas con códigos únicos para integración con datos de CONAPESCA, VMS y estudios locales (PANGAS/Moreno-Báez).';

COMMENT ON TABLE community_reference IS 'Registro de comunidades indígenas y pesqueras del Golfo de California con datos demográficos, geográficos y de gobernanza.';

-- ============================================================================
-- NOTAS DE IMPLEMENTACIÓN
-- ============================================================================
-- 1. Para producción, considerar particionamiento por zona y fecha en tablas grandes
-- 2. Implementar políticas de acceso basadas en roles para datos sensibles
-- 3. Crear funciones de agregación para cálculos complejos (ej: ponderación dinámica)
-- 4. Considerar el uso de PostGIS Topology para topología de redes (rutas de buques)
-- 5. Implementar triggers para recalcular scores automáticamente al actualizar datos base

-- Versión: 0.1
-- Fecha: 2026-07-27
-- Autor: Arquitecto de Software Senior - Proyecto IERC-GNL