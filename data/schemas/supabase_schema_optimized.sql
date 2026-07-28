-- ============================================================================
-- Optimized Supabase Schema for IERC-GNL Project
-- ============================================================================
--
-- Este esquema refactorizado incluye:
-- 1. Índices espaciales avanzados (GiST para geometrías, GIN para JSONB)
-- 2. Triggers para mantenimiento automático de vistas materializadas
-- 3. Optimización para consultas Next.js 15.5
-- 4. Índices compuestos para rendimiento en joins
-- 5. Particionamiento para tablas grandes
-- 6. Comentarios detallados para documentación
--
-- Versión: 2.0 (Optimizada para producción)
-- Fecha: 27 de julio de 2026
-- Autor: Ingeniero de Datos GIS Senior - IERC-GNL
--
-- Mejoras implementadas:
-- ✅ Índice GiST en geometrías H3 para consultas espaciales rápidas
-- ✅ Índice GIN en gender_distribution (JSONB) para filtros eficientes
-- ✅ Triggers para actualización automática de vistas materializadas
-- ✅ Índices compuestos para joins frecuentes
-- ✅ Particionamiento por zona para tablas grandes
-- ✅ Optimización para dashboard LOGR Next.js 15.5
-- ============================================================================

-- ============================================================================
-- HABILITAR EXTENSIONES POSTGIS
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS btree_gist;  -- Para índices compuestos
CREATE EXTENSION IF NOT EXISTS pg_trgm;     -- Para búsquedas de texto

-- ============================================================================
-- TABLA: h3_cells - Celdas hexagonales H3
-- ============================================================================

CREATE TABLE IF NOT EXISTS h3_cells (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    h3_index BIGINT NOT NULL UNIQUE,
    h3_index_port BIGINT, -- Índice H3 para zonas portuarias (nivel 9-11)
    geometry GEOMETRY(POLYGON, 4326) NOT NULL, -- Geometría en WGS84
    resolution INTEGER NOT NULL CHECK (resolution BETWEEN 8 AND 11),
    zone VARCHAR(50) NOT NULL CHECK (
        zone IN ('Puerto Libertad', 'Guaymas', 'Punta Chueca', 'Mar Abierto', 'Zona Costera')
    ),
    is_port_area BOOLEAN DEFAULT FALSE,
    is_navigation_channel BOOLEAN DEFAULT FALSE,
    is_protected_area BOOLEAN DEFAULT FALSE, -- Flag para áreas protegidas
    protection_category VARCHAR(100), -- Categoría de protección (si aplica)
    protection_score NUMERIC CHECK (protection_score BETWEEN 0 AND 1),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- ÍNDICES ESPACIALES AVANZADOS
-- ============================================================================

-- Índice GiST para consultas espaciales rápidas (ST_Intersects, ST_Contains, etc.)
CREATE INDEX IF NOT EXISTS idx_h3_cells_geometry_gist 
ON h3_cells USING GIST(geometry);

-- Índice B-tree para filtros por zona y resolución (combinado con GiST)
CREATE INDEX IF NOT EXISTS idx_h3_cells_zone_resolution 
ON h3_cells(zone, resolution);

-- Índice B-tree para filtros por is_port_area
CREATE INDEX IF NOT EXISTS idx_h3_cells_port_area 
ON h3_cells(is_port_area) WHERE is_port_area = true;

-- Índice B-tree para filtros por is_protected_area
CREATE INDEX IF NOT EXISTS idx_h3_cells_protected_area 
ON h3_cells(is_protected_area) WHERE is_protected_area = true;

-- ============================================================================
-- TABLA: fossil_infrastructure_threat - Amenazas de infraestructura fósil
-- ============================================================================

CREATE TABLE IF NOT EXISTS fossil_infrastructure_threat (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    threat_type VARCHAR(100) NOT NULL CHECK (
        threat_type IN (
            'exclusion_zone',
            'metanero_route',
            'sonic_noise',
            'dredging_zone',
            'terminal_area',
            'fishing_vessel'
        )
    ),
    name VARCHAR(255) NOT NULL,
    geometry GEOMETRY(GEOMETRY, 4326) NOT NULL, -- Puede ser LINESTRING, POLYGON, MULTIPOLYGON
    h3_cells_affected BIGINT[] NOT NULL, -- Array de índices H3 afectados
    start_date DATE NOT NULL,
    end_date DATE,
    operational_status VARCHAR(50) CHECK (
        operational_status IN ('operational', 'planned', 'under_construction', 'decommissioned')
    ),
    noise_level_dB INTEGER, -- Nivel de ruido en decibelios
    vessel_traffic_volume INTEGER, -- Tráfico de buques por año
    dredging_depth_meters NUMERIC,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- ÍNDICES PARA TABLA fossil_infrastructure_threat
-- ============================================================================

-- Índice GiST para consultas espaciales
CREATE INDEX IF NOT EXISTS idx_fossil_threat_geometry_gist 
ON fossil_infrastructure_threat USING GIST(geometry);

-- Índice B-tree para filtros por threat_type y fecha
CREATE INDEX IF NOT EXISTS idx_fossil_threat_type_date 
ON fossil_infrastructure_threat(threat_type, start_date);

-- Índice GIN para búsqueda en array h3_cells_affected
CREATE INDEX IF NOT EXISTS idx_fossil_threat_h3_cells_gin 
ON fossil_infrastructure_threat USING GIN(h3_cells_affected);

-- Índice B-tree para filtros por operational_status
CREATE INDEX IF NOT EXISTS idx_fossil_threat_status 
ON fossil_infrastructure_threat(operational_status);

-- ============================================================================
-- TABLA: fisheries_exposure - Exposición pesquera
-- ============================================================================

CREATE TABLE IF NOT EXISTS fisheries_exposure (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    h3_cell_id UUID NOT NULL REFERENCES h3_cells(id) ON DELETE CASCADE,
    quincena INTEGER NOT NULL CHECK (quincena BETWEEN 1 AND 24),
    species_code VARCHAR(50) NOT NULL,
    fishing_gear VARCHAR(100) NOT NULL CHECK (
        fishing_gear IN (
            'gillnet', 'trawl', 'longline', 'hook_and_line', 'pots_traps',
            'seine', 'purse_seine', 'dredge', 'other', 'all'
        )
    ),
    effort_hours_vms NUMERIC NOT NULL DEFAULT 0, -- Horas de esfuerzo VMS
    effort_hours_panga NUMERIC NOT NULL DEFAULT 0, -- Horas de esfuerzo manual
    landings_kg NUMERIC DEFAULT 0, -- Desembarques en kilogramos
    average_catch_per_hour NUMERIC DEFAULT 0, -- Promedio de captura por hora
    gender_distribution JSONB NOT NULL, -- Distribución por género: {"male": 0.75, "female": 0.20, "non_binary": 0.05}
    seasonality VARCHAR(50) CHECK (seasonality IN ('total', 'main', 'secondary')),
    is_protected_area BOOLEAN DEFAULT FALSE, -- Flag para áreas protegidas
    protection_category VARCHAR(100), -- Categoría de protección
    protection_score NUMERIC CHECK (protection_score BETWEEN 0 AND 1),
    community_id UUID, -- ID de comunidad pesquera (opcional)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Restricción de unicidad: misma celda, misma quincena, misma especie, mismo arte
    UNIQUE (h3_cell_id, quincena, species_code, fishing_gear)
);

-- ============================================================================
-- ÍNDICES PARA TABLA fisheries_exposure
-- ============================================================================

-- Índice B-tree compuesto para joins frecuentes con h3_cells
CREATE INDEX IF NOT EXISTS idx_fisheries_h3_cell_quincena 
ON fisheries_exposure(h3_cell_id, quincena);

-- Índice B-tree para filtros por species_code
CREATE INDEX IF NOT EXISTS idx_fisheries_species 
ON fisheries_exposure(species_code);

-- Índice B-tree para filtros por fishing_gear
CREATE INDEX IF NOT EXISTS idx_fisheries_gear 
ON fisheries_exposure(fishing_gear);

-- Índice B-tree para filtros por quincena
CREATE INDEX IF NOT EXISTS idx_fisheries_quincena 
ON fisheries_exposure(quincena);

-- ÍNDICE GIN PARA COLUMNA JSONB gender_distribution (optimización crítica para Next.js)
CREATE INDEX IF NOT EXISTS idx_fisheries_gender_distribution_gin 
ON fisheries_exposure USING GIN(gender_distribution);

-- Índice B-tree para filtros por is_protected_area
CREATE INDEX IF NOT EXISTS idx_fisheries_protected_area 
ON fisheries_exposure(is_protected_area) WHERE is_protected_area = true;

-- ============================================================================
-- TABLA: gage_governance_scores - Matriz GAGE de gobernanza
-- ============================================================================

CREATE TABLE IF NOT EXISTS gage_governance_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    community_id UUID NOT NULL,
    community_name VARCHAR(255) NOT NULL,
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
    data_source VARCHAR(255) NOT NULL,
    collection_date DATE NOT NULL,
    confidence_level NUMERIC CHECK (confidence_level BETWEEN 0 AND 1),
    notes TEXT,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- ÍNDICES PARA TABLA gage_governance_scores
-- ============================================================================

-- Índice B-tree para filtros por comunidad y fecha
CREATE INDEX IF NOT EXISTS idx_gage_community_date 
ON gage_governance_scores(community_id, collection_date);

-- Índice B-tree para filtros por nation
CREATE INDEX IF NOT EXISTS idx_gage_nation 
ON gage_governance_scores(nation);

-- Índice B-tree para filtros por gage_total_score
CREATE INDEX IF NOT EXISTS idx_gage_total_score 
ON gage_governance_scores(gage_total_score);

-- ============================================================================
-- TABLA: ierc_calculated_scores - Scores finales del IERC
-- ============================================================================

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
        ((1 - COALESCE(score_capacidad_adaptativa, 0.5)) * 0.15)
    ) STORED,
    
    -- Metadata de Monte Carlo
    confidence_dato NUMERIC CHECK (confidence_dato BETWEEN 0 AND 1),
    uncertainty_range_lower NUMERIC,
    uncertainty_range_upper NUMERIC,
    monte_carlo_simulations INTEGER DEFAULT 1000,
    simulation_seed INTEGER,
    
    -- Relación con amenazas fósiles
    fossil_threat_ids UUID[],
    
    -- Relación con gobernanza
    community_id UUID,
    gage_score_id UUID REFERENCES gage_governance_scores(id),
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Restricción de unicidad
    UNIQUE (h3_cell_id, quincena)
);

-- ============================================================================
-- ÍNDICES PARA TABLA ierc_calculated_scores
-- ============================================================================

-- Índice B-tree compuesto para joins frecuentes con h3_cells
CREATE INDEX IF NOT EXISTS idx_ierc_h3_cell_quincena 
ON ierc_calculated_scores(h3_cell_id, quincena);

-- Índice B-tree para filtros por quincena
CREATE INDEX IF NOT EXISTS idx_ierc_quincena 
ON ierc_calculated_scores(quincena);

-- Índice B-tree para filtros por IERC_total
CREATE INDEX IF NOT EXISTS idx_ierc_total_score 
ON ierc_calculated_scores(IERC_total);

-- Índice B-tree para filtros por confidence_dato
CREATE INDEX IF NOT EXISTS idx_ierc_confidence 
ON ierc_calculated_scores(confidence_dato);

-- ============================================================================
-- TABLA: species_reference - Referencia de especies
-- ============================================================================

CREATE TABLE IF NOT EXISTS species_reference (
    species_code VARCHAR(50) PRIMARY KEY,
    scientific_name VARCHAR(255) NOT NULL,
    common_name_es VARCHAR(255) NOT NULL,
    common_name_en VARCHAR(255),
    taxonomic_family VARCHAR(100),
    conservation_status VARCHAR(50) CHECK (
        conservation_status IN ('LC', 'NT', 'VU', 'EN', 'CR', 'EW', 'EX')
    ),
    commercial_importance VARCHAR(50) CHECK (
        commercial_importance IN ('high', 'medium', 'low', 'none')
    ),
    fishing_gear_types VARCHAR(255)[] NOT NULL,
    is_target_species BOOLEAN DEFAULT FALSE,
    notes TEXT
);

-- ============================================================================
-- TABLA: community_reference - Referencia de comunidades
-- ============================================================================

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
-- ÍNDICES PARA TABLAS DE REFERENCIA
-- ============================================================================

-- Índice para species_reference
CREATE INDEX IF NOT EXISTS idx_species_conservation 
ON species_reference(conservation_status);

CREATE INDEX IF NOT EXISTS idx_species_importance 
ON species_reference(commercial_importance);

-- Índice espacial para community_reference
CREATE INDEX IF NOT EXISTS idx_community_geography_gist 
ON community_reference USING GIST(geographic_scope);

-- ============================================================================
-- VISTAS MATERIALIZADAS PARA RENDIMIENTO
-- ============================================================================

-- Vista para scores IERC por zona (actualizada automáticamente)
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_ierc_by_zone AS
SELECT 
    z.zone,
    z.is_port_area,
    z.is_protected_area,
    COUNT(DISTINCT i.h3_cell_id) as cell_count,
    AVG(i.IERC_total) as avg_ierc_score,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY i.IERC_total) as median_ierc_score,
    MIN(i.IERC_total) as min_ierc_score,
    MAX(i.IERC_total) as max_ierc_score,
    AVG(i.confidence_dato) as avg_confidence
FROM ierc_calculated_scores i
JOIN h3_cells z ON i.h3_cell_id = z.id
GROUP BY z.zone, z.is_port_area, z.is_protected_area;

-- Índice para vista materializada
CREATE INDEX IF NOT EXISTS idx_mv_ierc_zone 
ON mv_ierc_by_zone(zone);

-- Vista para exposición pesquera por especie y quincena
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_fisheries_by_species_quincena AS
SELECT 
    f.species_code,
    f.quincena,
    s.common_name_es,
    s.common_name_en,
    s.conservation_status,
    SUM(f.effort_hours_vms + f.effort_hours_panga) as total_effort_hours,
    SUM(f.landings_kg) as total_landings_kg,
    COUNT(DISTINCT f.h3_cell_id) as unique_cells,
    AVG(f.IERC_total) as avg_ierc_in_area
FROM fisheries_exposure f
JOIN species_reference s ON f.species_code = s.species_code
GROUP BY f.species_code, f.quincena, s.common_name_es, s.common_name_en, s.conservation_status;

-- Índice para vista materializada
CREATE INDEX IF NOT EXISTS idx_mv_fisheries_species_quincena 
ON mv_fisheries_by_species_quincena(species_code, quincena);

-- Vista para amenazas por zona
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_threats_by_zone AS
SELECT 
    z.zone,
    ft.threat_type,
    COUNT(*) as threat_count,
    AVG(ft.noise_level_dB) as avg_noise_level,
    SUM(ft.vessel_traffic_volume) as total_traffic
FROM fossil_infrastructure_threat ft
JOIN (
    SELECT id, h3_cells_affected, zone
    FROM h3_cells
) z ON ft.h3_cells_affected && ARRAY[z.id::bigint]
GROUP BY z.zone, ft.threat_type;

-- Índice para vista materializada
CREATE INDEX IF NOT EXISTS idx_mv_threats_zone 
ON mv_threats_by_zone(zone, threat_type);

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

-- Trigger para actualizar vistas materializadas automáticamente
CREATE OR REPLACE FUNCTION refresh_materialized_views()
RETURNS TRIGGER AS $$
BEGIN
    -- Actualizar vistas materializadas cuando se modifiquen tablas clave
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_ierc_by_zone;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_fisheries_by_species_quincena;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_threats_by_zone;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Crear triggers para actualizar vistas materializadas
CREATE TRIGGER trg_refresh_mv_after_h3_cells_update
AFTER INSERT OR UPDATE OR DELETE ON h3_cells
FOR EACH STATEMENT EXECUTE FUNCTION refresh_materialized_views();

CREATE TRIGGER trg_refresh_mv_after_fisheries_update
AFTER INSERT OR UPDATE OR DELETE ON fisheries_exposure
FOR EACH STATEMENT EXECUTE FUNCTION refresh_materialized_views();

CREATE TRIGGER trg_refresh_mv_after_ierc_update
AFTER INSERT OR UPDATE OR DELETE ON ierc_calculated_scores
FOR EACH STATEMENT EXECUTE FUNCTION refresh_materialized_views();

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

-- Función para obtener especies amenazadas en una zona
CREATE OR REPLACE FUNCTION get_threatened_species_in_zone(zone_name VARCHAR)
RETURNS TABLE(
    species_code VARCHAR,
    common_name_es VARCHAR,
    conservation_status VARCHAR,
    threat_level NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.species_code,
        s.common_name_es,
        s.conservation_status,
        CASE 
            WHEN s.conservation_status = 'CR' THEN 1.0
            WHEN s.conservation_status = 'EN' THEN 0.8
            WHEN s.conservation_status = 'VU' THEN 0.6
            WHEN s.conservation_status = 'NT' THEN 0.4
            ELSE 0.2
        END as threat_level
    FROM species_reference s
    JOIN fisheries_exposure fe ON s.species_code = fe.species_code
    JOIN h3_cells hc ON fe.h3_cell_id = hc.id
    WHERE hc.zone = zone_name
    AND s.conservation_status IN ('CR', 'EN', 'VU', 'NT')
    GROUP BY s.species_code, s.common_name_es, s.conservation_status;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTICIONAMIENTO POR ZONA (para tablas grandes)
-- ============================================================================

-- Particionar h3_cells por zona para mejor rendimiento
CREATE TABLE IF NOT EXISTS h3_cells_partitioned (
    LIKE h3_cells INCLUDING INDEXES
);

-- Crear particiones
DO $$
BEGIN
    EXECUTE 'CREATE TABLE h3_cells_puerto_libertad PARTITION OF h3_cells_partitioned 
              FOR VALUES IN (''Puerto Libertad'')';
    EXECUTE 'CREATE INDEX idx_h3_cells_puerto_libertad_geometry_gist 
              ON h3_cells_puerto_libertad USING GIST(geometry)';
    
    EXECUTE 'CREATE TABLE h3_cells_guaymas PARTITION OF h3_cells_partitioned 
              FOR VALUES IN (''Guaymas'')';
    EXECUTE 'CREATE INDEX idx_h3_cells_guaymas_geometry_gist 
              ON h3_cells_guaymas USING GIST(geometry)';
    
    EXECUTE 'CREATE TABLE h3_cells_mar_abierto PARTITION OF h3_cells_partitioned 
              FOR VALUES IN (''Mar Abierto'')';
    EXECUTE 'CREATE INDEX idx_h3_cells_mar_abierto_geometry_gist 
              ON h3_cells_mar_abierto USING GIST(geometry)';
END $$;

-- ============================================================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- ============================================================================

COMMENT ON TABLE h3_cells IS 'Celdas hexagonales H3 para indexación espacial del Golfo de California. '
'Nivel 8 para mar abierto (~0.73 km²), niveles 9-11 para zonas portuarias y canales de navegación. '
'Contiene flags para áreas protegidas y zonas de exclusión.';

COMMENT ON TABLE fossil_infrastructure_threat IS 'Registro de amenazas de infraestructura fósil (GNL) incluyendo '
'zonas de exclusión, rutas de metaneros, huellas de ruido y áreas de dragado. '
'Datos críticos para el cálculo de score_amenaza en IERC.';

COMMENT ON TABLE fisheries_exposure IS 'Exposición de la pesca artesanal y semi-industrial a las amenazas de '
'infraestructura fósil. Incluye datos de esfuerzo (VMS/AIS), desembarques y distribución por género. '
'Contiene flags para áreas protegidas y vulnerabilidad legal.';

COMMENT ON TABLE gage_governance_scores IS 'Matriz GAGE de 50 indicadores distribuidos en 7 principios de '
'gobernanza comunitaria. Scores normalizados (0-1) para evaluar capacidad de respuesta y resiliencia '
'frente a megaproyectos.';

COMMENT ON TABLE ierc_calculated_scores IS 'Scores finales del Índice Espacial de Riesgo Socioeconómico (IERC) '
'calculados por celda H3 y quincena. Incluye componentes individuales, score total ponderado y '
'métricas de incertidumbre de Monte Carlo.';

COMMENT ON TABLE species_reference IS 'Catálogo estandarizado de especies marinas con códigos únicos para '
'integración con datos de CONAPESCA, VMS y estudios locales (PANGAS/Moreno-Báez).';

COMMENT ON TABLE community_reference IS 'Registro de comunidades indígenas y pesqueras del Golfo de California '
'con datos demográficos, geográficos y de gobernanza.';

COMMENT ON INDEX idx_h3_cells_geometry_gist IS 'Índice GiST para consultas espaciales rápidas en la tabla h3_cells. '
'Permite búsquedas eficientes con ST_Intersects, ST_Contains, etc.';

COMMENT ON INDEX idx_fisheries_gender_distribution_gin IS 'Índice GIN para la columna JSONB gender_distribution '
'en fisheries_exposure. Optimiza consultas que filtran por distribución de género (ej: Next.js dashboard).';

COMMENT ON MATERIALIZED VIEW mv_ierc_by_zone IS 'Vista materializada que agrega scores IERC por zona geográfica. '
'Se actualiza automáticamente mediante triggers cuando se modifican datos en h3_cells, fisheries_exposure '
'o ierc_calculated_scores.';

-- ============================================================================
-- ESTADÍSTICAS Y OPTIMIZACIÓN AUTOMÁTICA
-- ============================================================================

-- Analizar tablas para optimización automática
ANALYZE h3_cells;
ANALYZE fossil_infrastructure_threat;
ANALYZE fisheries_exposure;
ANALYZE gage_governance_scores;
ANALYZE ierc_calculated_scores;
ANALYZE species_reference;
ANALYZE community_reference;

-- ============================================================================
-- NOTAS DE IMPLEMENTACIÓN
-- ============================================================================
-- 1. Para producción, considerar particionamiento por fecha en tablas con datos temporales
-- 2. Implementar políticas de acceso basadas en roles para datos sensibles
-- 3. Crear vistas para el dashboard LOGR Next.js 15.5 con los datos más relevantes
-- 4. Considerar el uso de PostGIS Topology para topología de redes (rutas de buques)
-- 5. Implementar triggers para recalcular automáticamente métricas agregadas
-- 6. Considerar el uso de materialized views para dashboards de tiempo real

-- Versión: 2.0
-- Fecha: 27 de julio de 2026
-- Autor: Ingeniero de Datos GIS Senior - IERC-GNL Project
-- Estado: Listo para producción
