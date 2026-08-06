INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Terminal de Licuefacción y Almacenamiento LNG Amigo', 'Sonora',
            'Guaymas', 'Terminal GNL',
            'Amigo LNG, S.A. de C.V.', 'En evaluación',
            'ASEA', 7.8,
            27.9189, -110.9161, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.922, 27.915], [-110.91, 27.915], [-110.91, 27.923], [-110.922, 27.923], [-110.922, 27.915]]]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Sistema de Distribución de Gas Natural por Medio de Ductos en Los Cabos', 'Baja California Sur',
            'Los Cabos', 'Gasoducto distribución',
            'Gas Natural del Noroeste, S.A. de C.V.', 'En evaluación',
            'ASEA', NULL,
            22.8905, -109.9167, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-109.9167, 22.8905]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Vista Pacífico LNG', 'Sinaloa',
            'Topolobampo / Ahome', 'Terminal GNL',
            'Vista Pacífico LNG, S.A.P.I. de C.V.', 'En evaluación',
            'ASEA', 4.0,
            24.895, -108.012, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-108.02, 24.89], [-108.005, 24.89], [-108.005, 24.9], [-108.02, 24.9], [-108.02, 24.89]]]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Gasoducto Corredor Norte', 'Sinaloa',
            'Guasave/Ahome', 'Gasoducto',
            'Gasoducto Corredor Norte, S.A.P.I. de C.V.', 'En evaluación',
            'ASEA', NULL,
            25.4, -108.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-108.25, 25.4]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Construcción y Operación de Planta de Licuefacción GNL Cosalá', 'Sinaloa',
            'Cosalá', 'Planta Licuefacción GNL',
            'GNL Cosalá, S.A. de C.V.', 'En evaluación',
            'ASEA', 1.2,
            24.4133, -106.6908, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-106.6908, 24.4133]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Sistema de Transporte de Gas Natural Los Ramones Fase II Sur', 'Sonora/Baja California',
            'San Luis Río Colorado / Mexicali', 'Gasoducto transporte',
            'CENAGAS', 'En operación/Planificación',
            'ASEA Transparencia/CENAGAS', NULL,
            32.45, -114.8, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-114.8, 32.45]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'STGN Sierra Madre (Frontera-Puerto Libertad)', 'Sonora',
            'Pitiquito / Caborca', 'Gasoducto transporte',
            'CENAGAS', 'En operación/Planificación',
            'ASEA Transparencia/CENAGAS', NULL,
            29.9, -112.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-112.5, 29.9]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Terminal de Licuefacción LNG (proyecto Puerto Libertad)', 'Sonora',
            'Pitiquito', 'Terminal GNL',
            'México Pacific Limited / MPL', 'En evaluación',
            'SENER/Plan Quinquenal CENAGAS', 14.1,
            29.8972, -112.6869, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-112.695, 29.89], [-112.68, 29.89], [-112.68, 29.905], [-112.695, 29.905], [-112.695, 29.89]]]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Reconfiguración Estación de Compresión Cempoala', 'Veracruz',
            'Úrsulo Galván', 'Estación compresión',
            'CENAGAS', 'En ejecución',
            'Plan Quinquenal CENAGAS 2025-2029', NULL,
            19.45, -96.4, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-96.4, 19.45]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Gasoducto Naco-Hermosillo', 'Sonora',
            'Naco / Hermosillo', 'Gasoducto transporte',
            'CENAGAS', 'Planificado',
            'Plan Quinquenal CENAGAS 2025-2029', NULL,
            30.5, -110.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-110.5, 30.5]}'), 4326)
        );
INSERT INTO public.proyectos_gnl (
            nombre_proyecto, estado, municipio, tipo_infraestructura, empresa_promovente,
            estatus_permiso, fuente_oficial, capacidad_mtpa, latitud, longitud, geometry
        ) VALUES (
            'Gasoducto Puerto Libertad-Guaymas', 'Sonora',
            'Hermosillo / Guaymas', 'Gasoducto transporte',
            'CENAGAS', 'Planificado',
            'Plan Quinquenal CENAGAS 2025-2029', NULL,
            28.9, -111.8, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Point", "coordinates": [-111.8, 28.9]}'), 4326)
        );