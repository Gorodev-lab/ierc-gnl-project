INSERT INTO public.anp_habitats_criticos (
            anp_id, nombre, categoria, administracion, superficie_ha, geometry
        ) VALUES (
            'APFF_ISLAS_GOLFO', 'Área de Protección de Flora y Fauna Islas del Golfo de California',
            'APFF Federal', 'CONANP',
            150000.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-112.5, 29.0], [-112.0, 29.0], [-112.0, 29.5], [-112.5, 29.5], [-112.5, 29.0]]]}'), 4326)
        );
INSERT INTO public.anp_habitats_criticos (
            anp_id, nombre, categoria, administracion, superficie_ha, geometry
        ) VALUES (
            'RB_ALTO_GOLFO', 'Reserva de la Biosfera Alto Golfo de California y Delta del Río Colorado',
            'Reserva de la Biosfera', 'CONANP',
            934756.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.8, 31.0], [-113.5, 31.0], [-113.5, 31.8], [-114.8, 31.8], [-114.8, 31.0]]]}'), 4326)
        );