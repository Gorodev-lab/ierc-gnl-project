INSERT INTO public.localidades_estudio_ierc (
            localidad_id, nombre, municipio, estado, tipo_comunidad,
            poblacion_pesquera_est, prioridad_poa, latitud, longitud, geometry
        ) VALUES (
            'PUNTA_CHUECA_COMCAAC', 'Punta Chueca (Socaaix)',
            'Hermosillo', 'Sonora',
            'Comunidad Indígena Comca''ac / Pesquera', 600,
            'Meta 1 - Campo Agosto 2026', 28.9886,
            -112.1603, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-112.1603, 28.9886]}'), 4326)
        ) ON CONFLICT (localidad_id) DO NOTHING;
INSERT INTO public.localidades_estudio_ierc (
            localidad_id, nombre, municipio, estado, tipo_comunidad,
            poblacion_pesquera_est, prioridad_poa, latitud, longitud, geometry
        ) VALUES (
            'PUERTO_LIBERTAD', 'Puerto Libertad',
            'Pitiquito', 'Sonora',
            'Localidad Pesquera / Interfaz GNL (Mexico Pacific)', 1200,
            'Meta 1 - Campo Agosto 2026', 29.9107,
            -112.6835, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-112.6835, 29.9107]}'), 4326)
        ) ON CONFLICT (localidad_id) DO NOTHING;
INSERT INTO public.localidades_estudio_ierc (
            localidad_id, nombre, municipio, estado, tipo_comunidad,
            poblacion_pesquera_est, prioridad_poa, latitud, longitud, geometry
        ) VALUES (
            'GUAYMAS_PORTUARIO', 'Guaymas (Cooperativas Pesqueras)',
            'Guaymas', 'Sonora',
            'Puerto Pesquero - Industrial / Terminal GNL', 4500,
            'Meta 1 - Campo Septiembre 2026', 27.9179,
            -110.9039, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-110.9039, 27.9179]}'), 4326)
        ) ON CONFLICT (localidad_id) DO NOTHING;