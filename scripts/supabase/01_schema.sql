-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis SCHEMA extensions;

-- 1. Grilla H3 Riesgo
CREATE TABLE IF NOT EXISTS public.grilla_h3_riesgo (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    h3_index VARCHAR(20) UNIQUE NOT NULL,
    resolucion INT NOT NULL,
    latitud_centroide DOUBLE PRECISION,
    longitud_centroide DOUBLE PRECISION,
    ierc_score DOUBLE PRECISION,
    nivel_riesgo VARCHAR(50),
    amenaza_score DOUBLE PRECISION,
    exposicion_score DOUBLE PRECISION,
    sensibilidad_score DOUBLE PRECISION,
    dependencia_score DOUBLE PRECISION,
    biocultural_score DOUBLE PRECISION,
    capacidad_adaptativa_score DOUBLE PRECISION,
    distancia_proyecto_mas_cercano_km DOUBLE PRECISION,
    geometry extensions.geometry(Polygon, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Proyectos GNL
CREATE TABLE IF NOT EXISTS public.proyectos_gnl (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_proyecto TEXT NOT NULL,
    estado VARCHAR(100),
    municipio VARCHAR(100),
    tipo_infraestructura VARCHAR(100),
    empresa_promovente TEXT,
    estatus_permiso VARCHAR(100),
    fuente_oficial VARCHAR(100),
    capacidad_mtpa DOUBLE PRECISION,
    latitud DOUBLE PRECISION,
    longitud DOUBLE PRECISION,
    geometry extensions.geometry(Geometry, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Gasoductos e Infraestructura GNL
CREATE TABLE IF NOT EXISTS public.gasoductos_infraestructura_gnl (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ducto_id VARCHAR(100),
    nombre TEXT NOT NULL,
    operador TEXT,
    estatus VARCHAR(100),
    longitud_km DOUBLE PRECISION,
    geometry extensions.geometry(LineString, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Zonas Pesqueras PANGAS
CREATE TABLE IF NOT EXISTS public.zonas_pesqueras_pangas (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uid_espaciotemporal TEXT UNIQUE NOT NULL,
    sitio_code VARCHAR(50),
    nombre_sitio TEXT,
    comunidad TEXT,
    actor TEXT,
    pesqueria TEXT,
    arte TEXT,
    zona VARCHAR(50),
    temporada TEXT,
    ruta TEXT,
    habitat TEXT,
    total_registros_entrevista INT,
    riqueza_total_especies INT,
    especies_criticas_iucn_count INT,
    tiene_especies_amenazadas INT,
    geometry extensions.geometry(MultiPolygon, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. ANP y Hábitats Críticos
CREATE TABLE IF NOT EXISTS public.anp_habitats_criticos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    anp_id VARCHAR(50),
    nombre TEXT NOT NULL,
    categoria VARCHAR(100),
    administracion VARCHAR(100),
    superficie_ha DOUBLE PRECISION,
    geometry extensions.geometry(Polygon, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Localidades de Estudio IERC (Sensible / Protegida RLS)
CREATE TABLE IF NOT EXISTS public.localidades_estudio_ierc (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    localidad_id VARCHAR(50) UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    municipio VARCHAR(100),
    estado VARCHAR(100),
    tipo_comunidad TEXT,
    poblacion_pesquera_est INT,
    prioridad_poa TEXT,
    latitud DOUBLE PRECISION,
    longitud DOUBLE PRECISION,
    geometry extensions.geometry(Point, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Riqueza Relativa Pesquera
CREATE TABLE IF NOT EXISTS public.riqueza_relativa_pesquera (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    riqueza_absoluta DOUBLE PRECISION,
    shape_length DOUBLE PRECISION,
    shape_area DOUBLE PRECISION,
    geometry extensions.geometry(MultiPolygon, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Features Resumidas Lakehouse Gold
CREATE TABLE IF NOT EXISTS public.ierc_features_summary (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    h3_index VARCHAR(20) UNIQUE NOT NULL,
    chlor_a_mean DOUBLE PRECISION,
    sst_mean DOUBLE PRECISION,
    depth_mean DOUBLE PRECISION,
    bajos_count INT,
    coral_count INT,
    has_observed_data BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
