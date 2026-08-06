INSERT INTO public.gasoductos_infraestructura_gnl (
            ducto_id, nombre, operador, estatus, longitud_km, geometry
        ) VALUES (
            'DUC_SONORA_P_LIBERTAD', 'Gasoducto Samalayuca - Saguaro / Puerto Libertad',
            'Mexico Pacific / CFE', 'En construcción / Proyecto',
            800.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "LineString", "coordinates": [[-112.6835, 29.9107], [-111.0, 30.5], [-109.5, 31.3]]}'), 4326)
        );
INSERT INTO public.gasoductos_infraestructura_gnl (
            ducto_id, nombre, operador, estatus, longitud_km, geometry
        ) VALUES (
            'DUC_GUAYMAS_BRANCH', 'Ramal Gasoducto Guaymas - Sásabe',
            'IEnova / Sempra Infrastructure', 'En operación',
            505.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "LineString", "coordinates": [[-110.9039, 27.9179], [-110.5, 28.5], [-111.0, 30.0]]}'), 4326)
        );
INSERT INTO public.gasoductos_infraestructura_gnl (
            ducto_id, nombre, operador, estatus, longitud_km, geometry
        ) VALUES (
            'DUC_CORREDOR_NORTE', 'Gasoducto Corredor Norte Sinaloa',
            'Gasoducto Corredor Norte', 'En evaluación',
            320.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "LineString", "coordinates": [[-108.25, 25.4], [-108.01, 24.89]]}'), 4326)
        );