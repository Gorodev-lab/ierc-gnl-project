-- Spatial GiST Indexes for Map Queries
CREATE INDEX IF NOT EXISTS idx_grilla_h3_geom ON public.grilla_h3_riesgo USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_grilla_h3_riesgo_level ON public.grilla_h3_riesgo (nivel_riesgo);
CREATE INDEX IF NOT EXISTS idx_proyectos_gnl_geom ON public.proyectos_gnl USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_gasoductos_geom ON public.gasoductos_infraestructura_gnl USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_pangas_geom ON public.zonas_pesqueras_pangas USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_anp_geom ON public.anp_habitats_criticos USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_localidades_geom ON public.localidades_estudio_ierc USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_riqueza_geom ON public.riqueza_relativa_pesquera USING GIST (geometry);

-- Enable Row Level Security (RLS) on all tables
ALTER TABLE public.grilla_h3_riesgo ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.proyectos_gnl ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gasoductos_infraestructura_gnl ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.zonas_pesqueras_pangas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.anp_habitats_criticos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.localidades_estudio_ierc ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.riqueza_relativa_pesquera ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ierc_features_summary ENABLE ROW LEVEL SECURITY;

-- Create Policies for Public Access (Read-Only via Anon Key)
DROP POLICY IF EXISTS "Public Read Grilla H3" ON public.grilla_h3_riesgo;
CREATE POLICY "Public Read Grilla H3" ON public.grilla_h3_riesgo FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Public Read Proyectos GNL" ON public.proyectos_gnl;
CREATE POLICY "Public Read Proyectos GNL" ON public.proyectos_gnl FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Public Read Gasoductos" ON public.gasoductos_infraestructura_gnl;
CREATE POLICY "Public Read Gasoductos" ON public.gasoductos_infraestructura_gnl FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Public Read Pangas" ON public.zonas_pesqueras_pangas;
CREATE POLICY "Public Read Pangas" ON public.zonas_pesqueras_pangas FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Public Read ANP" ON public.anp_habitats_criticos;
CREATE POLICY "Public Read ANP" ON public.anp_habitats_criticos FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Public Read Riqueza" ON public.riqueza_relativa_pesquera;
CREATE POLICY "Public Read Riqueza" ON public.riqueza_relativa_pesquera FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Public Read Features Summary" ON public.ierc_features_summary;
CREATE POLICY "Public Read Features Summary" ON public.ierc_features_summary FOR SELECT TO anon, authenticated USING (true);

-- PROTECTED POLICY: Localidades (Comunidades Indígenas / Sensible) -> Require authenticated / service_role
DROP POLICY IF EXISTS "Restricted Read Localidades" ON public.localidades_estudio_ierc;
CREATE POLICY "Restricted Read Localidades" ON public.localidades_estudio_ierc FOR SELECT TO authenticated USING (true);
