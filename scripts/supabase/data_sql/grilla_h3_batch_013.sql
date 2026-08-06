INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d93ffff', 9,
            27.91467, -110.88359,
            75.33, 'Alto',
            0.973, 0.804,
            0.403, 0.7,
            0.85, 0.3,
            2.68, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88254053877147, 27.91292446737429], [-110.88134490758358, 27.91460258278366], [-110.88239058583898, 27.91635216811092], [-110.88463192615954, 27.916423615088924], [-110.8858275248103, 27.91474547983065], [-110.88478181568018, 27.912995917443325], [-110.88254053877147, 27.91292446737429]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d83ffff', 9,
            27.9181, -110.88344,
            75.11, 'Alto',
            0.973, 0.793,
            0.403, 0.7,
            0.85, 0.3,
            2.7, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88239058583898, 27.91635216811092], [-110.88119491871056, 27.918030273114812], [-110.88224062443868, 27.91977984494333], [-110.88448202817466, 27.919851288830532], [-110.88567766276451, 27.91817316397997], [-110.88463192615954, 27.916423615088924], [-110.88239058583898, 27.91635216811092]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d8fffff', 9,
            27.92153, -110.88329,
            74.89, 'Moderado',
            0.973, 0.782,
            0.403, 0.7,
            0.85, 0.3,
            2.72, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88224062443868, 27.91977984494333], [-110.88104492136762, 27.921457939529457], [-110.8820906545699, 27.92320749784717], [-110.88433212172482, 27.923278938643808], [-110.88552779225591, 27.92160082421324], [-110.88448202817466, 27.919851288830532], [-110.88224062443868, 27.91977984494333]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d17ffff', 9,
            27.92496, -110.88314,
            74.66, 'Moderado',
            0.973, 0.771,
            0.403, 0.7,
            0.85, 0.3,
            2.74, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8820906545699, 27.92320749784717], [-110.88089491555402, 27.924885582003235], [-110.88194067623188, 27.926635126798082], [-110.8841822068093, 27.92670656450438], [-110.88537791328379, 27.92502846050611], [-110.88433212172482, 27.923278938643808], [-110.8820906545699, 27.92320749784717]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d07ffff', 9,
            27.92838, -110.88299,
            74.42, 'Moderado',
            0.972, 0.759,
            0.403, 0.7,
            0.85, 0.3,
            2.82, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88194067623188, 27.926635126798082], [-110.88074490126907, 27.928313200511795], [-110.88179068942392, 27.930062731771713], [-110.88403228342742, 27.930134166387916], [-110.88522802584741, 27.928456072834237], [-110.8841822068093, 27.92670656450438], [-110.88194067623188, 27.926635126798082]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d33ffff', 9,
            27.93021, -110.88627,
            74.34, 'Moderado',
            0.975, 0.753,
            0.402, 0.7,
            0.85, 0.3,
            2.52, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88522802584741, 27.928456072834237], [-110.88403228342742, 27.930134166387916], [-110.88507812994608, 27.931883661173245], [-110.88731974976277, 27.93195503947228], [-110.88851545963001, 27.930276926083398], [-110.88746958223591, 27.928527454230736], [-110.88522802584741, 27.928456072834237]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d37ffff', 9,
            27.93203, -110.88956,
            74.26, 'Moderado',
            0.977, 0.747,
            0.401, 0.7,
            0.85, 0.3,
            2.26, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88851545963001, 27.930276926083398], [-110.88731974976277, 27.93195503947228], [-110.888365654641, 27.933704497770822], [-110.89060730025672, 27.9337758197453], [-110.89180297756127, 27.932097686525996], [-110.89075704181539, 27.93034825116271], [-110.88851545963001, 27.930276926083398]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb72cbffff', 9,
            27.93385, -110.89285,
            74.17, 'Moderado',
            0.98, 0.741,
            0.4, 0.7,
            0.85, 0.3,
            2.04, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89180297756127, 27.932097686525996], [-110.89060730025672, 27.9337758197453], [-110.89165326349026, 27.93552524154488], [-110.89389493489082, 27.93559650718739], [-110.89509057962276, 27.933918354142456], [-110.89404458552936, 27.932168955280705], [-110.89180297756127, 27.932097686525996]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb72cfffff', 9,
            27.93567, -110.89614,
            74.08, 'Moderado',
            0.981, 0.735,
            0.4, 0.7,
            0.85, 0.3,
            1.86, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89509057962276, 27.933918354142456], [-110.89389493489082, 27.93559650718739], [-110.89494095647544, 27.93734589247583], [-110.89718265364665, 27.93741710177896], [-110.89837826579607, 27.935738928913178], [-110.89733221335938, 27.933989566565163], [-110.89509057962276, 27.933918354142456]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb721bffff', 9,
            27.93749, -110.89942,
            73.97, 'Moderado',
            0.982, 0.729,
            0.4, 0.7,
            0.85, 0.3,
            1.76, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89837826579607, 27.935738928913178], [-110.89718265364665, 27.93741710177896], [-110.89822873357812, 27.939166450544082], [-110.90047045650583, 27.939237603500462], [-110.90166603606275, 27.93755941081859], [-110.90061992528703, 27.93581008499648], [-110.89837826579607, 27.935738928913178]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7203ffff', 9,
            27.93931, -110.90271,
            73.85, 'Moderado',
            0.982, 0.723,
            0.4, 0.7,
            0.85, 0.3,
            1.76, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90166603606275, 27.93755941081859], [-110.90047045650583, 27.939237603500462], [-110.90151659477988, 27.940986915730072], [-110.9037583434499, 27.941058012332288], [-110.9049538904044, 27.93937979983912], [-110.9039077212939, 27.93763051055509], [-110.90166603606275, 27.93755941081859]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7217ffff', 9,
            27.9377, -110.90615,
            74.03, 'Moderado',
            0.985, 0.728,
            0.401, 0.7,
            0.85, 0.3,
            1.48, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90510323231145, 27.935952287603953], [-110.9039077212939, 27.93763051055509], [-110.9049538904044, 27.93937979983912], [-110.90719560136155, 27.93945084322143], [-110.9083910797682, 27.937772600461546], [-110.90734487983119, 27.936023334128148], [-110.90510323231145, 27.935952287603953]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb72bbffff', 9,
            27.93609, -110.90959,
            74.19, 'Moderado',
            0.987, 0.733,
            0.402, 0.7,
            0.85, 0.3,
            1.26, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90854032230443, 27.93434508092036], [-110.90734487983119, 27.936023334128148], [-110.9083910797682, 27.937772600461546], [-110.91063275299761, 27.937843590631516], [-110.91182816285146, 27.936165317617522], [-110.91078193209786, 27.934416074239806], [-110.90854032230443, 27.93434508092036]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb72b3ffff', 9,
            27.93449, -110.91302,
            74.35, 'Moderado',
            0.989, 0.739,
            0.403, 0.7,
            0.85, 0.3,
            1.08, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91197730602187, 27.932737790787964], [-110.91078193209786, 27.934416074239806], [-110.91182816285146, 27.936165317617522], [-110.91406979833829, 27.936236254582724], [-110.91526513963437, 27.934557951327225], [-110.91421887807414, 27.93280873091024], [-110.91197730602187, 27.932737790787964]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb704fffff', 9,
            27.93288, -110.91646,
            74.52, 'Moderado',
            0.991, 0.744,
            0.404, 0.7,
            0.85, 0.3,
            0.9, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91541418344397, 27.931130417226957], [-110.91421887807414, 27.93280873091024], [-110.91526513963437, 27.934557951327225], [-110.91750673736371, 27.93462883509523], [-110.91870201009712, 27.93295050161085], [-110.9176557177402, 27.93120130415962], [-110.91541418344397, 27.931130417226957]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7047ffff', 9,
            27.93127, -110.9199,
            74.69, 'Moderado',
            0.993, 0.75,
            0.406, 0.7,
            0.85, 0.3,
            0.72, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9188509545509, 27.92952296025751], [-110.9176557177402, 27.93120130415962], [-110.91870201009712, 27.93295050161085], [-110.92094357005413, 27.933021332189206], [-110.92213877421993, 27.931342968488558], [-110.92109245107623, 27.929593794008145], [-110.9188509545509, 27.92952296025751]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb700bffff', 9,
            27.92966, -110.92333,
            74.86, 'Moderado',
            0.995, 0.755,
            0.408, 0.7,
            0.85, 0.3,
            0.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9222876193229, 27.927915419899826], [-110.92109245107623, 27.929593794008145], [-110.92213877421993, 27.931342968488558], [-110.92438029638974, 27.93141374588486], [-110.925575431983, 27.92973535198056], [-110.92452907806248, 27.92798620047599], [-110.9222876193229, 27.927915419899826]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb701bffff', 9,
            27.92624, -110.92348,
            75.16, 'Alto',
            0.998, 0.767,
            0.408, 0.7,
            0.85, 0.3,
            0.17, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92243645602001, 27.924487847337986], [-110.92124132369034, 27.92616623184169], [-110.9222876193229, 27.927915419899826], [-110.92452907806248, 27.92798620047599], [-110.92572417774018, 27.926307796174065], [-110.92467785133289, 27.924558631094246], [-110.92243645602001, 27.924487847337986]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb70c7ffff', 9,
            27.92281, -110.92363,
            75.43, 'Alto',
            1.0, 0.778,
            0.408, 0.7,
            0.85, 0.3,
            0.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92258528431195, 27.921060250827388], [-110.92139018789713, 27.92273864571419], [-110.92243645602001, 27.924487847337986], [-110.92467785133289, 27.924558631094246], [-110.92587291509717, 27.922880216407], [-110.92482661620171, 27.92113103776399], [-110.92258528431195, 27.921060250827388]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb70d7ffff', 9,
            27.91938, -110.92378,
            75.65, 'Alto',
            1.0, 0.789,
            0.408, 0.7,
            0.85, 0.3,
            0.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92273410419944, 27.9176326303924], [-110.92153904369732, 27.91931103565], [-110.92258528431195, 27.921060250827388], [-110.92482661620171, 27.92113103776399], [-110.9260216440547, 27.91945261270371], [-110.92497537266964, 27.91770342050956], [-110.92273410419944, 27.9176326303924]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb746fffff', 9,
            27.91595, -110.92393,
            75.87, 'Alto',
            1.0, 0.8,
            0.408, 0.7,
            0.85, 0.3,
            0.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92288291568316, 27.914204986057356], [-110.92168789109165, 27.915883401673476], [-110.92273410419944, 27.9176326303924], [-110.92497537266964, 27.91770342050956], [-110.92617036461345, 27.916024985088544], [-110.92512412073735, 27.914275779355325], [-110.92288291568316, 27.914204986057356]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7463ffff', 9,
            27.91253, -110.92408,
            76.06, 'Alto',
            0.999, 0.811,
            0.408, 0.7,
            0.85, 0.3,
            0.13, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92303171876384, 27.910777317846637], [-110.9218367300808, 27.912455743808966], [-110.92288291568316, 27.914204986057356], [-110.92512412073735, 27.914275779355325], [-110.92631907677416, 27.91259733358585], [-110.9252728604056, 27.91084811432562], [-110.92303171876384, 27.910777317846637]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7473ffff', 9,
            27.9091, -110.92423,
            76.2, 'Alto',
            0.995, 0.821,
            0.408, 0.7,
            0.85, 0.3,
            0.48, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9231805134422, 27.90734962578457], [-110.92198556066549, 27.909028062080814], [-110.92303171876384, 27.910777317846637], [-110.9252728604056, 27.91084811432562], [-110.92646778053752, 27.909169658219998], [-110.92542159167509, 27.907420425444823], [-110.9231805134422, 27.90734962578457]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7447ffff', 9,
            27.90728, -110.92094,
            76.25, 'Alto',
            0.993, 0.827,
            0.406, 0.7,
            0.85, 0.3,
            0.66, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9198933302432, 27.905529500550365], [-110.91869834483158, 27.907207917032448], [-110.91974444465549, 27.908957209291675], [-110.92198556066549, 27.909028062080814], [-110.9231805134422, 27.90734962578457], [-110.92213438284644, 27.905600356513407], [-110.9198933302432, 27.905529500550365]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7443ffff', 9,
            27.90546, -110.91765,
            76.29, 'Alto',
            0.991, 0.832,
            0.405, 0.7,
            0.85, 0.3,
            0.86, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91660623095889, 27.903709282536937], [-110.91541121292232, 27.905387679200075], [-110.91645725446752, 27.907137007940545], [-110.91869834483158, 27.907207917032448], [-110.9198933302432, 27.905529500550365], [-110.9188472579183, 27.90378019479538], [-110.91660623095889, 27.903709282536937]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb745bffff', 9,
            27.90364, -110.91437,
            76.34, 'Alto',
            0.989, 0.838,
            0.403, 0.7,
            0.85, 0.3,
            1.07, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9133192156077, 27.901888971763878], [-110.91212416495608, 27.903567348603286], [-110.91317014821834, 27.905316713812805], [-110.91541121292232, 27.905387679200075], [-110.91660623095889, 27.903709282536937], [-110.91556021690916, 27.90195994031032], [-110.9133192156077, 27.901888971763878]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb292fffff', 9,
            27.90182, -110.91108,
            76.38, 'Alto',
            0.987, 0.843,
            0.402, 0.7,
            0.85, 0.3,
            1.27, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91003228420809, 27.90006856825074], [-110.90883720095135, 27.90174692526162], [-110.9098831259264, 27.90349632692803], [-110.91212416495608, 27.903567348603286], [-110.9133192156077, 27.901888971763878], [-110.91227325983738, 27.900139593077792], [-110.91003228420809, 27.90006856825074]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb292bffff', 9,
            27.9, -110.90779,
            76.43, 'Alto',
            0.985, 0.848,
            0.401, 0.7,
            0.85, 0.3,
            1.48, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90674543677846, 27.898248072017097], [-110.9055503209265, 27.899926409194684], [-110.9065961876101, 27.90167584730579], [-110.90883720095135, 27.90174692526162], [-110.91003228420809, 27.90006856825074], [-110.90898638672141, 27.898319153117377], [-110.90674543677846, 27.898248072017097]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2977ffff', 9,
            27.89818, -110.9045,
            76.48, 'Alto',
            0.983, 0.853,
            0.4, 0.7,
            0.85, 0.3,
            1.74, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9034586733372, 27.896427483082547], [-110.90226352489995, 27.898105800422044], [-110.90330933328788, 27.899855274965667], [-110.9055503209265, 27.899926409194684], [-110.90674543677846, 27.898248072017097], [-110.90569959757966, 27.896498620448636], [-110.9034586733372, 27.896427483082547]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2973ffff', 9,
            27.89636, -110.90122,
            76.51, 'Alto',
            0.979, 0.859,
            0.4, 0.7,
            0.85, 0.3,
            2.06, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90017199390275, 27.89460680146664], [-110.89897681289015, 27.896285098963272], [-110.90002256297812, 27.898034609927226], [-110.90226352489995, 27.898105800422044], [-110.9034586733372, 27.896427483082547], [-110.90241289243056, 27.894677995091158], [-110.90017199390275, 27.89460680146664]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb297bffff', 9,
            27.89796, -110.89778,
            76.41, 'Alto',
            0.979, 0.854,
            0.4, 0.7,
            0.85, 0.3,
            2.1, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89673587669927, 27.896213852210064], [-110.89554062720349, 27.897892119543], [-110.89658634646285, 27.899641653474482], [-110.89882734604922, 27.899712897105566], [-110.90002256297812, 27.898034609927226], [-110.89897681289015, 27.896285098963272], [-110.89673587669927, 27.896213852210064]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2bb7ffff', 9,
            27.89957, -110.89435,
            76.3, 'Alto',
            0.978, 0.849,
            0.4, 0.7,
            0.85, 0.3,
            2.22, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89329965336438, 27.897820819653546], [-110.89210433539036, 27.89949905681017], [-110.89315002381119, 27.901248613704134], [-110.8953910610472, 27.90131991047906], [-110.89658634646285, 27.899641653474482], [-110.89554062720349, 27.897892119543], [-110.89329965336438, 27.897820819653546]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2ba3ffff', 9,
            27.90118, -110.89091,
            76.17, 'Alto',
            0.976, 0.845,
            0.401, 0.7,
            0.85, 0.3,
            2.41, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88986332391788, 27.899427703776926], [-110.88866793747056, 27.90110591074462], [-110.88971359504295, 27.90285549059602], [-110.89195466991373, 27.902926840522348], [-110.89315002381119, 27.901248613704134], [-110.89210433539036, 27.89949905681017], [-110.88986332391788, 27.899427703776926]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2babffff', 9,
            27.90278, -110.88747,
            76.05, 'Alto',
            0.974, 0.84,
            0.401, 0.7,
            0.85, 0.3,
            2.62, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88642688837959, 27.901034504560023], [-110.8852314334639, 27.90271268132619], [-110.88627706017792, 27.904462284129966], [-110.88851817266861, 27.904533687215253], [-110.88971359504295, 27.90285549059602], [-110.88866793747056, 27.90110591074462], [-110.88642688837959, 27.901034504560023]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b07ffff', 9,
            27.90439, -110.88404,
            75.92, 'Alto',
            0.971, 0.835,
            0.403, 0.7,
            0.85, 0.3,
            2.88, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88299034676933, 27.902641221982666], [-110.88179482339021, 27.904319368534708], [-110.88284041923592, 27.906068994285814], [-110.88508156933166, 27.906140450537603], [-110.88627706017792, 27.904462284129966], [-110.8852314334639, 27.90271268132619], [-110.88299034676933, 27.902641221982666]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b0fffff', 9,
            27.906, -110.8806,
            75.78, 'Alto',
            0.968, 0.83,
            0.404, 0.7,
            0.85, 0.3,
            3.17, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87955369910688, 27.90424785602472], [-110.8783581072693, 27.905925972350012], [-110.87940367223678, 27.907675621043392], [-110.88164485992269, 27.907747130469247], [-110.88284041923592, 27.906068994285814], [-110.88179482339021, 27.904319368534708], [-110.87955369910688, 27.90424785602472]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b77ffff', 9,
            27.90943, -110.88045,
            75.59, 'Alto',
            0.969, 0.82,
            0.404, 0.7,
            0.85, 0.3,
            3.09, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87940367223678, 27.907675621043392], [-110.8782080444615, 27.90935372699003], [-110.87925363689533, 27.911103362218395], [-110.88149488798739, 27.91117486856035], [-110.88269048323687, 27.909496742757792], [-110.88164485992269, 27.907747130469247], [-110.87940367223678, 27.907675621043392]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b67ffff', 9,
            27.91285, -110.8803,
            75.39, 'Alto',
            0.969, 0.81,
            0.404, 0.7,
            0.85, 0.3,
            3.06, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87925363689533, 27.911103362218395], [-110.87805797318025, 27.912781457774084], [-110.87910359308182, 27.91453107952536], [-110.88134490758358, 27.91460258278366], [-110.88254053877147, 27.91292446737429], [-110.88149488798739, 27.91117486856035], [-110.87925363689533, 27.911103362218395]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d9bffff', 9,
            27.91628, -110.88015,
            75.17, 'Alto',
            0.969, 0.799,
            0.404, 0.7,
            0.85, 0.3,
            3.06, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87910359308182, 27.91453107952536], [-110.87790789342479, 27.916209164677817], [-110.87895354079554, 27.917958772939954], [-110.88119491871056, 27.918030273114812], [-110.88239058583898, 27.91635216811092], [-110.88134490758358, 27.91460258278366], [-110.87910359308182, 27.91453107952536]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d8bffff', 9,
            27.91971, -110.88,
            74.95, 'Moderado',
            0.969, 0.788,
            0.404, 0.7,
            0.85, 0.3,
            3.08, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87895354079554, 27.917958772939954], [-110.87775780519442, 27.91963684767686], [-110.87880348003577, 27.9213864424378], [-110.88104492136762, 27.921457939529457], [-110.88224062443868, 27.91977984494333], [-110.88119491871056, 27.918030273114812], [-110.87895354079554, 27.917958772939954]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d13ffff', 9,
            27.92314, -110.87985,
            74.73, 'Moderado',
            0.969, 0.777,
            0.404, 0.7,
            0.85, 0.3,
            3.1, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87880348003577, 27.9213864424378], [-110.87760770848844, 27.923064506746872], [-110.8786534108018, 27.924814087994545], [-110.88089491555402, 27.924885582003235], [-110.8820906545699, 27.92320749784717], [-110.88104492136762, 27.921457939529457], [-110.87880348003577, 27.9213864424378]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d03ffff', 9,
            27.92656, -110.8797,
            74.49, 'Moderado',
            0.969, 0.765,
            0.404, 0.7,
            0.85, 0.3,
            3.14, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8786534108018, 27.924814087994545], [-110.87745760330611, 27.926492141863505], [-110.87850333309292, 27.928241709585848], [-110.88074490126907, 27.928313200511795], [-110.88194067623188, 27.926635126798082], [-110.88089491555402, 27.924885582003235], [-110.8786534108018, 27.924814087994545]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d0fffff', 9,
            27.92999, -110.87955,
            74.25, 'Moderado',
            0.968, 0.754,
            0.404, 0.7,
            0.85, 0.3,
            3.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87850333309292, 27.928241709585848], [-110.87730748964674, 27.929919753002384], [-110.87835324690839, 27.93166930718734], [-110.88059487851204, 27.93174079503078], [-110.88179068942392, 27.930062731771713], [-110.88074490126907, 27.928313200511795], [-110.87850333309292, 27.928241709585848]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d3bffff', 9,
            27.93181, -110.88284,
            74.17, 'Moderado',
            0.971, 0.748,
            0.403, 0.7,
            0.85, 0.3,
            2.94, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88179068942392, 27.930062731771713], [-110.88059487851204, 27.93174079503078], [-110.88164069414532, 27.933490312743725], [-110.88388235157845, 27.933561744270044], [-110.88507812994608, 27.931883661173245], [-110.88403228342742, 27.930134166387916], [-110.88179068942392, 27.930062731771713]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d23ffff', 9,
            27.93363, -110.88612,
            74.08, 'Moderado',
            0.973, 0.742,
            0.402, 0.7,
            0.85, 0.3,
            2.68, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88507812994608, 27.931883661173245], [-110.88388235157845, 27.933561744270044], [-110.88492822557907, 27.9353112254988], [-110.88716990882754, 27.935382600700596], [-110.888365654641, 27.933704497770822], [-110.88731974976277, 27.93195503947228], [-110.88507812994608, 27.931883661173245]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d27ffff', 9,
            27.93545, -110.88941,
            73.99, 'Moderado',
            0.975, 0.736,
            0.401, 0.7,
            0.85, 0.3,
            2.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.888365654641, 27.933704497770822], [-110.88716990882754, 27.935382600700596], [-110.8882158411913, 27.937132045432957], [-110.89045755024091, 27.937203364302835], [-110.89165326349026, 27.93552524154488], [-110.89060730025672, 27.9337758197453], [-110.888365654641, 27.933704497770822]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7253ffff', 9,
            27.93727, -110.8927,
            73.89, 'Moderado',
            0.977, 0.729,
            0.4, 0.7,
            0.85, 0.3,
            2.27, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89165326349026, 27.93552524154488], [-110.89045755024091, 27.937203364302835], [-110.89150354096355, 27.93895277252665], [-110.89374527580013, 27.93902403505719], [-110.89494095647544, 27.93734589247583], [-110.89389493489082, 27.93559650718739], [-110.89165326349026, 27.93552524154488]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7257ffff', 9,
            27.9391, -110.89599,
            73.79, 'Moderado',
            0.979, 0.723,
            0.4, 0.7,
            0.85, 0.3,
            2.14, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89494095647544, 27.93734589247583], [-110.89374527580013, 27.93902403505719], [-110.8947913248774, 27.94077340676026], [-110.89703308548678, 27.94084461294407], [-110.89822873357812, 27.939166450544082], [-110.89718265364665, 27.93741710177896], [-110.89494095647544, 27.93734589247583]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb720bffff', 9,
            27.94092, -110.89927,
            73.67, 'Moderado',
            0.979, 0.717,
            0.4, 0.7,
            0.85, 0.3,
            2.09, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89822873357812, 27.939166450544082], [-110.89703308548678, 27.94084461294407], [-110.89807919291444, 27.94259394811423], [-110.90032097928243, 27.942665097943905], [-110.90151659477988, 27.940986915730072], [-110.90047045650583, 27.939237603500462], [-110.89822873357812, 27.939166450544082]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb720fffff', 9,
            27.94274, -110.90256,
            73.54, 'Moderado',
            0.979, 0.711,
            0.4, 0.7,
            0.85, 0.3,
            2.12, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90151659477988, 27.940986915730072], [-110.90032097928243, 27.942665097943905], [-110.90136714505624, 27.944414396568966], [-110.90360895716869, 27.944485490037124], [-110.90480454006229, 27.94280728801421], [-110.9037583434499, 27.941058012332288], [-110.90151659477988, 27.940986915730072]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7207ffff', 9,
            27.94113, -110.906,
            73.72, 'Moderado',
            0.981, 0.716,
            0.401, 0.7,
            0.85, 0.3,
            1.85, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9049538904044, 27.93937979983912], [-110.9037583434499, 27.941058012332288], [-110.90480454006229, 27.94280728801421], [-110.90704631446043, 27.942878328254874], [-110.90824182880259, 27.941200095955196], [-110.90719560136155, 27.93945084322143], [-110.9049538904044, 27.93937979983912]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb72abffff', 9,
            27.93952, -110.90944,
            73.88, 'Moderado',
            0.984, 0.722,
            0.402, 0.7,
            0.85, 0.3,
            1.64, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9083910797682, 27.937772600461546], [-110.90719560136155, 27.93945084322143], [-110.90824182880259, 27.941200095955196], [-110.91048356547157, 27.941271082975916], [-110.91167901125736, 27.93959282041207], [-110.91063275299761, 27.937843590631516], [-110.9083910797682, 27.937772600461546]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb72a3ffff', 9,
            27.93791, -110.91287,
            74.04, 'Moderado',
            0.985, 0.727,
            0.403, 0.7,
            0.85, 0.3,
            1.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91182816285146, 27.936165317617522], [-110.91063275299761, 27.937843590631516], [-110.91167901125736, 27.93959282041207], [-110.9139207101823, 27.939663754220412], [-110.91511608740677, 27.937985461405013], [-110.91406979833829, 27.936236254582724], [-110.91182816285146, 27.936165317617522]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb72b7ffff', 9,
            27.93631, -110.91631,
            74.21, 'Moderado',
            0.987, 0.733,
            0.404, 0.7,
            0.85, 0.3,
            1.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91526513963437, 27.934557951327225], [-110.91406979833829, 27.936236254582724], [-110.91511608740677, 27.937985461405013], [-110.91735774857281, 27.938056342008565], [-110.91855305723105, 27.93637801895421], [-110.91750673736371, 27.93462883509523], [-110.91526513963437, 27.934557951327225]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb707bffff', 9,
            27.9347, -110.91975,
            74.38, 'Moderado',
            0.989, 0.738,
            0.406, 0.7,
            0.85, 0.3,
            1.1, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91870201009712, 27.93295050161085], [-110.91750673736371, 27.93462883509523], [-110.91855305723105, 27.93637801895421], [-110.9207946806233, 27.93644884636053], [-110.92198992071036, 27.934770493079853], [-110.92094357005413, 27.933021332189206], [-110.91870201009712, 27.93295050161085]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7073ffff', 9,
            27.93309, -110.92319,
            74.55, 'Moderado',
            0.991, 0.744,
            0.408, 0.7,
            0.85, 0.3,
            0.93, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92213877421993, 27.931342968488558], [-110.92094357005413, 27.933021332189206], [-110.92198992071036, 27.934770493079853], [-110.92423150631397, 27.934841267296516], [-110.92542667782494, 27.933162883802108], [-110.92438029638974, 27.93141374588486], [-110.92213877421993, 27.931342968488558]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb700fffff', 9,
            27.93148, -110.92662,
            74.71, 'Moderado',
            0.992, 0.749,
            0.41, 0.7,
            0.85, 0.3,
            0.85, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.925575431983, 27.92973535198056], [-110.92438029638974, 27.93141374588486], [-110.92542667782494, 27.933162883802108], [-110.92766822562503, 27.93323360483669], [-110.92886332855497, 27.93155519114119], [-110.92781691635074, 27.92980607620236], [-110.925575431983, 27.92973535198056]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7003ffff', 9,
            27.92806, -110.92677,
            75.0, 'Alto',
            0.994, 0.76,
            0.41, 0.7,
            0.85, 0.3,
            0.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92572417774018, 27.926307796174065], [-110.92452907806248, 27.92798620047599], [-110.925575431983, 27.92973535198056], [-110.92781691635074, 27.92980607620236], [-110.92901198336655, 27.92812765210701], [-110.92796559867912, 27.926378523583338], [-110.92572417774018, 27.926307796174065]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7013ffff', 9,
            27.92463, -110.92692,
            75.27, 'Alto',
            0.997, 0.772,
            0.41, 0.7,
            0.85, 0.3,
            0.34, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92587291509717, 27.922880216407], [-110.92467785133289, 27.924558631094246], [-110.92572417774018, 27.926307796174065], [-110.92796559867912, 27.926378523583338], [-110.92916062978293, 27.92470008910043], [-110.92811427261087, 27.922950947003965], [-110.92587291509717, 27.922880216407]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb708bffff', 9,
            27.9212, -110.92707,
            75.5, 'Alto',
            0.997, 0.783,
            0.41, 0.7,
            0.85, 0.3,
            0.31, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9260216440547, 27.91945261270371], [-110.92482661620171, 27.92113103776399], [-110.92587291509717, 27.922880216407], [-110.92811427261087, 27.922950947003965], [-110.92930926780483, 27.92127250214579], [-110.92826293814672, 27.9195233464886], [-110.9260216440547, 27.91945261270371]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb709bffff', 9,
            27.91777, -110.92722,
            75.72, 'Alto',
            0.997, 0.794,
            0.41, 0.7,
            0.85, 0.3,
            0.33, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92617036461345, 27.916024985088544], [-110.92497537266964, 27.91770342050956], [-110.9260216440547, 27.91945261270371], [-110.92826293814672, 27.9195233464886], [-110.92945789743294, 27.917844891267453], [-110.92841159528734, 27.9160957220616], [-110.92617036461345, 27.916024985088544]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7467ffff', 9,
            27.91435, -110.92737,
            75.93, 'Alto',
            0.996, 0.805,
            0.411, 0.7,
            0.85, 0.3,
            0.36, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92631907677416, 27.91259733358585], [-110.92512412073735, 27.914275779355325], [-110.92617036461345, 27.916024985088544], [-110.92841159528734, 27.9160957220616], [-110.929606518668, 27.914417256489767], [-110.92856024403349, 27.912668073747305], [-110.92631907677416, 27.91259733358585]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7477ffff', 9,
            27.91092, -110.92751,
            76.11, 'Alto',
            0.995, 0.816,
            0.411, 0.7,
            0.85, 0.3,
            0.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92646778053752, 27.909169658219998], [-110.9252728604056, 27.91084811432562], [-110.92631907677416, 27.91259733358585], [-110.92856024403349, 27.912668073747305], [-110.92975513151066, 27.91098959783709], [-110.92870888438586, 27.909240401570074], [-110.92646778053752, 27.909169658219998]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb740fffff', 9,
            27.90749, -110.92766,
            76.27, 'Alto',
            0.992, 0.826,
            0.411, 0.7,
            0.85, 0.3,
            0.82, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92661647590424, 27.905741959015337], [-110.92542159167509, 27.907420425444823], [-110.92646778053752, 27.909169658219998], [-110.92870888438586, 27.909240401570074], [-110.9299037359617, 27.907561915333766], [-110.92885751634512, 27.905812705554265], [-110.92661647590424, 27.905741959015337]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb740bffff', 9,
            27.90567, -110.92438,
            76.33, 'Alto',
            0.991, 0.831,
            0.409, 0.7,
            0.85, 0.3,
            0.86, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92332929971896, 27.903921909895526], [-110.92213438284644, 27.905600356513407], [-110.9231805134422, 27.90734962578457], [-110.92542159167509, 27.907420425444823], [-110.92661647590424, 27.905741959015337], [-110.9255703145465, 27.90399271273727], [-110.92332929971896, 27.903921909895526]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7457ffff', 9,
            27.90385, -110.92109,
            76.38, 'Alto',
            0.99, 0.837,
            0.407, 0.7,
            0.85, 0.3,
            1.04, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9200422074243, 27.9021017679939], [-110.9188472579183, 27.90378019479538], [-110.9198933302432, 27.905529500550365], [-110.92213438284644, 27.905600356513407], [-110.92332929971896, 27.903921909895526], [-110.92228319662432, 27.90217262713107], [-110.9200422074243, 27.9021017679939]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7453ffff', 9,
            27.90203, -110.9178,
            76.42, 'Alto',
            0.988, 0.842,
            0.405, 0.7,
            0.85, 0.3,
            1.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91675519903868, 27.900281533330023], [-110.91556021690916, 27.90195994031032], [-110.91660623095889, 27.903709282536937], [-110.9188472579183, 27.90378019479538], [-110.9200422074243, 27.9021017679939], [-110.91899616259701, 27.90035244875522], [-110.91675519903868, 27.900281533330023]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2927ffff', 9,
            27.90021, -110.91451,
            76.46, 'Alto',
            0.986, 0.848,
            0.403, 0.7,
            0.85, 0.3,
            1.45, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91346827458052, 27.898461205923468], [-110.91227325983738, 27.900139593077792], [-110.9133192156077, 27.901888971763878], [-110.91556021690916, 27.90195994031032], [-110.91675519903868, 27.900281533330023], [-110.91570921248298, 27.898532177629306], [-110.91346827458052, 27.898461205923468]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2923ffff', 9,
            27.89839, -110.91123,
            76.51, 'Alto',
            0.984, 0.853,
            0.402, 0.7,
            0.85, 0.3,
            1.65, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91018143406825, 27.896640785793796], [-110.90898638672141, 27.898319153117377], [-110.91003228420809, 27.90006856825074], [-110.91227325983738, 27.900139593077792], [-110.91346827458052, 27.898461205923468], [-110.91242234630069, 27.896711813772892], [-110.91018143406825, 27.896640785793796]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb293bffff', 9,
            27.89657, -110.90794,
            76.55, 'Alto',
            0.981, 0.858,
            0.401, 0.7,
            0.85, 0.3,
            1.85, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90689467752027, 27.894820272960597], [-110.90569959757966, 27.896498620448636], [-110.90674543677846, 27.898248072017097], [-110.90898638672141, 27.898319153117377], [-110.91018143406825, 27.896640785793796], [-110.9091355640685, 27.89489135720554], [-110.90689467752027, 27.894820272960597]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb290fffff', 9,
            27.89475, -110.90465,
            76.6, 'Alto',
            0.979, 0.863,
            0.401, 0.7,
            0.85, 0.3,
            2.11, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90360800495503, 27.892999667443434], [-110.90241289243056, 27.894677995091158], [-110.9034586733372, 27.896427483082547], [-110.90569959757966, 27.896498620448636], [-110.90689467752027, 27.894820272960597], [-110.90584886580487, 27.89307080794683], [-110.90360800495503, 27.892999667443434]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb290bffff', 9,
            27.89293, -110.90137,
            76.63, 'Alto',
            0.976, 0.868,
            0.4, 0.7,
            0.85, 0.3,
            2.41, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90032141639088, 27.891178969261897], [-110.89912627129249, 27.89285727706451], [-110.90017199390275, 27.89460680146664], [-110.90241289243056, 27.894677995091158], [-110.90360800495503, 27.892999667443434], [-110.90256225152821, 27.89125016601635], [-110.90032141639088, 27.891178969261897]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2947ffff', 9,
            27.89454, -110.89793,
            76.54, 'Alto',
            0.976, 0.864,
            0.4, 0.7,
            0.85, 0.3,
            2.41, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8968853984935, 27.892786027188976], [-110.89569018491547, 27.894464304837953], [-110.89673587669927, 27.896213852210064], [-110.89897681289015, 27.896285098963272], [-110.90017199390275, 27.89460680146664], [-110.89912627129249, 27.89285727706451], [-110.8968853984935, 27.892786027188976]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb294fffff', 9,
            27.89614, -110.89449,
            76.44, 'Alto',
            0.975, 0.859,
            0.4, 0.7,
            0.85, 0.3,
            2.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89344927446969, 27.894393001833766], [-110.89225399241698, 27.89607124931649], [-110.89329965336438, 27.897820819653546], [-110.89554062720349, 27.897892119543], [-110.89673587669927, 27.896213852210064], [-110.89569018491547, 27.894464304837953], [-110.89344927446969, 27.894393001833766]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2bb3ffff', 9,
            27.89775, -110.89106,
            76.33, 'Alto',
            0.974, 0.855,
            0.401, 0.7,
            0.85, 0.3,
            2.63, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89001304433927, 27.895999893176096], [-110.8888176938168, 27.89767811047997], [-110.88986332391788, 27.899427703776926], [-110.89210433539036, 27.89949905681017], [-110.89329965336438, 27.897820819653546], [-110.89225399241698, 27.89607124931649], [-110.89001304433927, 27.895999893176096]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2bbbffff', 9,
            27.89936, -110.88762,
            76.21, 'Alto',
            0.972, 0.85,
            0.401, 0.7,
            0.85, 0.3,
            2.82, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88657670812204, 27.897606701195816], [-110.88538128913477, 27.899284888308223], [-110.88642688837959, 27.901034504560023], [-110.88866793747056, 27.90110591074462], [-110.88986332391788, 27.899427703776926], [-110.8888176938168, 27.89767811047997], [-110.88657670812204, 27.897606701195816]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b17ffff', 9,
            27.90096, -110.88419,
            76.09, 'Alto',
            0.97, 0.845,
            0.402, 0.7,
            0.85, 0.3,
            3.04, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8831402658378, 27.89921342587275], [-110.88194477839066, 27.90089158278109], [-110.88299034676933, 27.902641221982666], [-110.8852314334639, 27.90271268132619], [-110.88642688837959, 27.901034504560023], [-110.88538128913477, 27.899284888308223], [-110.8831402658378, 27.89921342587275]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b03ffff', 9,
            27.90257, -110.88075,
            75.96, 'Alto',
            0.967, 0.841,
            0.404, 0.7,
            0.85, 0.3,
            3.3, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87970371750637, 27.900820067186732], [-110.87850816160432, 27.90249819387839], [-110.87955369910688, 27.90424785602472], [-110.88179482339021, 27.904319368534708], [-110.88299034676933, 27.902641221982666], [-110.88194477839066, 27.90089158278109], [-110.87970371750637, 27.900820067186732]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b0bffff', 9,
            27.90418, -110.87731,
            75.83, 'Alto',
            0.964, 0.836,
            0.405, 0.7,
            0.85, 0.3,
            3.58, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87626706314758, 27.902426625117613], [-110.87507143879556, 27.904104721579987], [-110.8761169454121, 27.905854406665995], [-110.8783581072693, 27.905925972350012], [-110.87955369910688, 27.90424785602472], [-110.87850816160432, 27.90249819387839], [-110.87626706314758, 27.902426625117613]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b73ffff', 9,
            27.9076, -110.87716,
            75.65, 'Alto',
            0.965, 0.826,
            0.406, 0.7,
            0.85, 0.3,
            3.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8761169454121, 27.905854406665995], [-110.87492128512096, 27.90753249275195], [-110.8759668192003, 27.90928216438255], [-110.8782080444615, 27.90935372699003], [-110.87940367223678, 27.907675621043392], [-110.8783581072693, 27.905925972350012], [-110.8761169454121, 27.905854406665995]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b63ffff', 9,
            27.91103, -110.87701,
            75.45, 'Alto',
            0.966, 0.815,
            0.406, 0.7,
            0.85, 0.3,
            3.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8759668192003, 27.90928216438255], [-110.87477112296796, 27.91096024007978], [-110.87581668451148, 27.9127098982429], [-110.87805797318025, 27.912781457774084], [-110.87925363689533, 27.911103362218395], [-110.8782080444615, 27.90935372699003], [-110.8759668192003, 27.90928216438255]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b6fffff', 9,
            27.91446, -110.87686,
            75.24, 'Alto',
            0.966, 0.804,
            0.406, 0.7,
            0.85, 0.3,
            3.43, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87581668451148, 27.9127098982429], [-110.87462095233575, 27.914387963539124], [-110.8756665413449, 27.9161376082227], [-110.87790789342479, 27.916209164677817], [-110.87910359308182, 27.91453107952536], [-110.87805797318025, 27.912781457774084], [-110.87581668451148, 27.9127098982429]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0dd7ffff', 9,
            27.91789, -110.87671,
            75.02, 'Alto',
            0.966, 0.794,
            0.406, 0.7,
            0.85, 0.3,
            3.45, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8756665413449, 27.9161376082227], [-110.87447077322368, 27.917815663105618], [-110.87551638969984, 27.91956529429759], [-110.87775780519442, 27.91963684767686], [-110.87895354079554, 27.917958772939954], [-110.87790789342479, 27.916209164677817], [-110.8756665413449, 27.9161376082227]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0dc7ffff', 9,
            27.92131, -110.87656,
            74.8, 'Moderado',
            0.965, 0.783,
            0.406, 0.7,
            0.85, 0.3,
            3.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87551638969984, 27.91956529429759], [-110.87432058563097, 27.921243338754913], [-110.87536622957563, 27.922992956443213], [-110.87760770848844, 27.923064506746872], [-110.87880348003577, 27.9213864424378], [-110.87775780519442, 27.91963684767686], [-110.87551638969984, 27.91956529429759]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d1bffff', 9,
            27.92474, -110.87641,
            74.57, 'Moderado',
            0.965, 0.771,
            0.406, 0.7,
            0.85, 0.3,
            3.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87536622957563, 27.922992956443213], [-110.87417038955697, 27.924670990462637], [-110.8752160609715, 27.926420594635214], [-110.87745760330611, 27.926492141863505], [-110.8786534108018, 27.924814087994545], [-110.87760770848844, 27.923064506746872], [-110.87536622957563, 27.922992956443213]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d0bffff', 9,
            27.92817, -110.87626,
            74.33, 'Moderado',
            0.965, 0.76,
            0.406, 0.7,
            0.85, 0.3,
            3.54, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8752160609715, 27.926420594635214], [-110.87402018500093, 27.928098618204466], [-110.87506588388676, 27.929848208849243], [-110.87730748964674, 27.929919753002384], [-110.87850333309292, 27.928241709585848], [-110.87745760330611, 27.926492141863505], [-110.8752160609715, 27.926420594635214]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d73ffff', 9,
            27.9316, -110.87611,
            74.09, 'Moderado',
            0.964, 0.749,
            0.406, 0.7,
            0.85, 0.3,
            3.64, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87506588388676, 27.929848208849243], [-110.87386997196215, 27.931526221956013], [-110.87491569832069, 27.933275799060944], [-110.87715736750958, 27.93334734013918], [-110.87835324690839, 27.93166930718734], [-110.87730748964674, 27.929919753002384], [-110.87506588388676, 27.929848208849243]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d77ffff', 9,
            27.93342, -110.8794,
            74.0, 'Moderado',
            0.966, 0.743,
            0.404, 0.7,
            0.85, 0.3,
            3.36, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87835324690839, 27.93166930718734], [-110.87715736750958, 27.93334734013918], [-110.87820315224754, 27.93509688077469], [-110.88044484728222, 27.93516836553585], [-110.88164069414532, 27.933490312743725], [-110.88059487851204, 27.93174079503078], [-110.87835324690839, 27.93166930718734]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d2bffff', 9,
            27.93524, -110.88269,
            73.9, 'Moderado',
            0.969, 0.736,
            0.403, 0.7,
            0.85, 0.3,
            3.1, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88164069414532, 27.933490312743725], [-110.88044484728222, 27.93516836553585], [-110.88149069039534, 27.936917869689747], [-110.88373241126166, 27.936989298126434], [-110.88492822557907, 27.9353112254988], [-110.88388235157845, 27.933561744270044], [-110.88164069414532, 27.933490312743725]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d2fffff', 9,
            27.93706, -110.88597,
            73.81, 'Moderado',
            0.971, 0.73,
            0.402, 0.7,
            0.85, 0.3,
            2.88, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88492822557907, 27.9353112254988], [-110.88373241126166, 27.936989298126434], [-110.8847783127457, 27.938738765786546], [-110.88702005942947, 27.938810137891334], [-110.8882158411913, 27.937132045432957], [-110.88716990882754, 27.935382600700596], [-110.88492822557907, 27.9353112254988]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb725bffff', 9,
            27.93888, -110.88926,
            73.71, 'Moderado',
            0.973, 0.724,
            0.401, 0.7,
            0.85, 0.3,
            2.68, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8882158411913, 27.937132045432957], [-110.88702005942947, 27.938810137891334], [-110.88806601928019, 27.94055956904547], [-110.89030779176724, 27.940630884810965], [-110.89150354096355, 27.93895277252665], [-110.89045755024091, 27.937203364302835], [-110.8882158411913, 27.937132045432957]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7243ffff', 9,
            27.9407, -110.89255,
            73.6, 'Moderado',
            0.975, 0.718,
            0.4, 0.7,
            0.85, 0.3,
            2.53, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89150354096355, 27.93895277252665], [-110.89030779176724, 27.940630884810965], [-110.8913538099804, 27.942380279446954], [-110.89359560825658, 27.942451538865754], [-110.8947913248774, 27.94077340676026], [-110.89374527580013, 27.93902403505719], [-110.89150354096355, 27.93895277252665]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7247ffff', 9,
            27.94252, -110.89584,
            73.49, 'Moderado',
            0.976, 0.711,
            0.4, 0.7,
            0.85, 0.3,
            2.45, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8947913248774, 27.94077340676026], [-110.89359560825658, 27.942451538865754], [-110.89464168482792, 27.944200896971413], [-110.896883508879, 27.944272100036116], [-110.89807919291444, 27.94259394811423], [-110.89703308548678, 27.94084461294407], [-110.8947913248774, 27.94077340676026]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7273ffff', 9,
            27.94434, -110.89913,
            73.37, 'Moderado',
            0.976, 0.705,
            0.4, 0.7,
            0.85, 0.3,
            2.43, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89807919291444, 27.94259394811423], [-110.896883508879, 27.944272100036116], [-110.8979296438043, 27.946021421599262], [-110.90017149361616, 27.946092568302472], [-110.90136714505624, 27.944414396568966], [-110.90032097928243, 27.942665097943905], [-110.89807919291444, 27.94259394811423]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7277ffff', 9,
            27.94616, -110.90241,
            73.23, 'Moderado',
            0.975, 0.699,
            0.4, 0.7,
            0.85, 0.3,
            2.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90136714505624, 27.944414396568966], [-110.90017149361616, 27.946092568302472], [-110.90121768689114, 27.947841853310923], [-110.90345956244956, 27.947912943645257], [-110.9046551812844, 27.946234752104907], [-110.90360895716869, 27.944485490037124], [-110.90136714505624, 27.944414396568966]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb723bffff', 9,
            27.94456, -110.90585,
            73.4, 'Moderado',
            0.978, 0.704,
            0.401, 0.7,
            0.85, 0.3,
            2.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90480454006229, 27.94280728801421], [-110.90360895716869, 27.944485490037124], [-110.9046551812844, 27.946234752104907], [-110.90689701912709, 27.94630578920414], [-110.90809256940692, 27.94462756737695], [-110.90704631446043, 27.942878328254874], [-110.90480454006229, 27.94280728801421]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7233ffff', 9,
            27.94295, -110.90929,
            73.57, 'Moderado',
            0.98, 0.71,
            0.402, 0.7,
            0.85, 0.3,
            2.03, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90824182880259, 27.941200095955196], [-110.90704631446043, 27.942878328254874], [-110.90809256940692, 27.94462756737695], [-110.91033436951899, 27.944698551248656], [-110.91152985123888, 27.943020299147243], [-110.91048356547157, 27.941271082975916], [-110.90824182880259, 27.941200095955196]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb72afffff', 9,
            27.94134, -110.91273,
            73.73, 'Moderado',
            0.982, 0.716,
            0.403, 0.7,
            0.85, 0.3,
            1.84, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91167901125736, 27.93959282041207], [-110.91048356547157, 27.941271082975916], [-110.91152985123888, 27.943020299147243], [-110.9137716136055, 27.943091229798977], [-110.91496702676052, 27.941412947435943], [-110.9139207101823, 27.939663754220412], [-110.91167901125736, 27.93959282041207]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb72a7ffff', 9,
            27.93973, -110.91616,
            73.9, 'Moderado',
            0.983, 0.721,
            0.404, 0.7,
            0.85, 0.3,
            1.66, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91511608740677, 27.937985461405013], [-110.9139207101823, 27.939663754220412], [-110.91496702676052, 27.941412947435943], [-110.91720875136679, 27.941483824875288], [-110.91840409595198, 27.939805512263256], [-110.91735774857281, 27.938056342008565], [-110.91511608740677, 27.937985461405013]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb706bffff', 9,
            27.93813, -110.9196,
            74.07, 'Moderado',
            0.985, 0.727,
            0.406, 0.7,
            0.85, 0.3,
            1.48, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91855305723105, 27.93637801895421], [-110.91735774857281, 27.938056342008565], [-110.91840409595198, 27.939805512263256], [-110.92064578278304, 27.93987633649777], [-110.9218410587935, 27.938197993649343], [-110.9207946806233, 27.93644884636053], [-110.91855305723105, 27.93637801895421]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7063ffff', 9,
            27.93652, -110.92304,
            74.24, 'Moderado',
            0.987, 0.732,
            0.408, 0.7,
            0.85, 0.3,
            1.31, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92198992071036, 27.934770493079853], [-110.9207946806233, 27.93644884636053], [-110.9218410587935, 27.938197993649343], [-110.92408270783447, 27.938268764686605], [-110.92527791526527, 27.936590391614395], [-110.92423150631397, 27.934841267296516], [-110.92198992071036, 27.934770493079853]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7077ffff', 9,
            27.93491, -110.92647,
            74.41, 'Moderado',
            0.988, 0.737,
            0.41, 0.7,
            0.85, 0.3,
            1.19, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92542667782494, 27.933162883802108], [-110.92423150631397, 27.934841267296516], [-110.92527791526527, 27.936590391614395], [-110.92751952650127, 27.93666110946198], [-110.92871466534747, 27.934982706178612], [-110.92766822562503, 27.93323360483669], [-110.92542667782494, 27.933162883802108]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb703bffff', 9,
            27.9333, -110.92991,
            74.55, 'Moderado',
            0.988, 0.743,
            0.412, 0.7,
            0.85, 0.3,
            1.22, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92886332855497, 27.93155519114119], [-110.92766822562503, 27.93323360483669], [-110.92871466534747, 27.934982706178612], [-110.93095623876367, 27.93505337084407], [-110.93215130902034, 27.933374937362167], [-110.93110483853668, 27.931625859001247], [-110.92886332855497, 27.93155519114119]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7007ffff', 9,
            27.92988, -110.93006,
            74.83, 'Moderado',
            0.99, 0.754,
            0.413, 0.7,
            0.85, 0.3,
            0.96, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92901198336655, 27.92812765210701], [-110.92781691635074, 27.92980607620236], [-110.92886332855497, 27.93155519114119], [-110.93110483853668, 27.931625859001247], [-110.93229987288065, 27.929947415117258], [-110.93125342991735, 27.928198323161897], [-110.92901198336655, 27.92812765210701]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7017ffff', 9,
            27.92645, -110.93021,
            75.1, 'Alto',
            0.992, 0.766,
            0.413, 0.7,
            0.85, 0.3,
            0.76, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92916062978293, 27.92470008910043], [-110.92796559867912, 27.926378523583338], [-110.92901198336655, 27.92812765210701], [-110.93125342991735, 27.928198323161897], [-110.93244842835078, 27.92651986888811], [-110.93140201290637, 27.924770763350377], [-110.92916062978293, 27.92470008910043]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb708fffff', 9,
            27.92302, -110.93036,
            75.35, 'Alto',
            0.993, 0.777,
            0.413, 0.7,
            0.85, 0.3,
            0.68, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92930926780483, 27.92127250214579], [-110.92811427261087, 27.922950947003965], [-110.92916062978293, 27.92470008910043], [-110.93140201290637, 27.924770763350377], [-110.93259697543137, 27.9230922986991], [-110.93155058750449, 27.921343179591034], [-110.92930926780483, 27.92127250214579]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7083ffff', 9,
            27.91959, -110.9305,
            75.57, 'Alto',
            0.993, 0.788,
            0.413, 0.7,
            0.85, 0.3,
            0.7, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92945789743294, 27.917844891267453], [-110.92826293814672, 27.9195233464886], [-110.92930926780483, 27.92127250214579], [-110.93155058750449, 27.921343179591034], [-110.93274551412317, 27.91966470457455], [-110.93169915371234, 27.91791557190822], [-110.92945789743294, 27.917844891267453]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7093ffff', 9,
            27.91617, -110.93065,
            75.79, 'Alto',
            0.993, 0.799,
            0.413, 0.7,
            0.85, 0.3,
            0.71, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.929606518668, 27.914417256489767], [-110.92841159528734, 27.9160957220616], [-110.92945789743294, 27.917844891267453], [-110.93169915371234, 27.91791557190822], [-110.93289404442689, 27.916237086538832], [-110.93184771153071, 27.914487940326296], [-110.929606518668, 27.914417256489767]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb742bffff', 9,
            27.91274, -110.9308,
            75.99, 'Alto',
            0.992, 0.81,
            0.413, 0.7,
            0.85, 0.3,
            0.77, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92975513151066, 27.91098959783709], [-110.92856024403349, 27.912668073747305], [-110.929606518668, 27.914417256489767], [-110.93184771153071, 27.914487940326296], [-110.93304256634325, 27.91280944461628], [-110.93199626096029, 27.9110602848696], [-110.92975513151066, 27.91098959783709]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb743bffff', 9,
            27.90931, -110.93095,
            76.16, 'Alto',
            0.99, 0.82,
            0.413, 0.7,
            0.85, 0.3,
            0.97, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9299037359617, 27.907561915333766], [-110.92870888438586, 27.909240401570074], [-110.92975513151066, 27.91098959783709], [-110.93199626096029, 27.9110602848696], [-110.93319107987291, 27.90938177883126], [-110.93214480200174, 27.907632605562497], [-110.9299037359617, 27.907561915333766]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7407ffff', 9,
            27.90588, -110.9311,
            76.33, 'Alto',
            0.988, 0.831,
            0.413, 0.7,
            0.85, 0.3,
            1.2, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93005233202177, 27.904134209004162], [-110.92885751634512, 27.905812705554265], [-110.9299037359617, 27.907561915333766], [-110.93214480200174, 27.907632605562497], [-110.93333958501661, 27.90595408920813], [-110.93229333465582, 27.904204902429342], [-110.93005233202177, 27.904134209004162]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7403ffff', 9,
            27.90406, -110.92781,
            76.41, 'Alto',
            0.989, 0.836,
            0.411, 0.7,
            0.85, 0.3,
            1.15, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92676516287503, 27.90231423599622], [-110.9255703145465, 27.90399271273727], [-110.92661647590424, 27.905741959015337], [-110.92885751634512, 27.905812705554265], [-110.93005233202177, 27.904134209004162], [-110.92900613991202, 27.902384985724236], [-110.92676516287503, 27.90231423599622]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb741bffff', 9,
            27.90224, -110.92452,
            76.46, 'Alto',
            0.988, 0.842,
            0.409, 0.7,
            0.85, 0.3,
            1.24, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9234780775948, 27.900494170203864], [-110.92228319662432, 27.90217262713107], [-110.92332929971896, 27.903921909895526], [-110.9255703145465, 27.90399271273727], [-110.92676516287503, 27.90231423599622], [-110.92571902902057, 27.900564976227322], [-110.9234780775948, 27.900494170203864]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74cfffff', 9,
            27.90042, -110.92124,
            76.5, 'Alto',
            0.986, 0.847,
            0.407, 0.7,
            0.85, 0.3,
            1.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92019107619952, 27.898674011646648], [-110.91899616259701, 27.90035244875522], [-110.9200422074243, 27.9021017679939], [-110.92228319662432, 27.90217262713107], [-110.9234780775948, 27.900494170203864], [-110.92243200199988, 27.898744873958176], [-110.92019107619952, 27.898674011646648]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74cbffff', 9,
            27.8986, -110.91795,
            76.54, 'Alto',
            0.984, 0.852,
            0.405, 0.7,
            0.85, 0.3,
            1.63, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91690415870761, 27.896853760344143], [-110.91570921248298, 27.898532177629306], [-110.91675519903868, 27.900281533330023], [-110.91899616259701, 27.90035244875522], [-110.92019107619952, 27.898674011646648], [-110.91914505886841, 27.896924678936337], [-110.91690415870761, 27.896853760344143]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2937ffff', 9,
            27.89678, -110.91466,
            76.58, 'Alto',
            0.982, 0.857,
            0.403, 0.7,
            0.85, 0.3,
            1.83, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91361732513748, 27.895033416315925], [-110.91242234630069, 27.896711813772892], [-110.91346827458052, 27.898461205923468], [-110.91570921248298, 27.898532177629306], [-110.91690415870761, 27.896853760344143], [-110.91585819964453, 27.895104391181402], [-110.91361732513748, 27.895033416315925]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2933ffff', 9,
            27.89496, -110.91138,
            76.62, 'Alto',
            0.98, 0.862,
            0.402, 0.7,
            0.85, 0.3,
            2.03, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91033057550757, 27.893212979581563], [-110.9091355640685, 27.89489135720554], [-110.91018143406825, 27.896640785793796], [-110.91242234630069, 27.896711813772892], [-110.91361732513748, 27.895033416315925], [-110.91257142434671, 27.893284010712918], [-110.91033057550757, 27.893212979581563]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2907ffff', 9,
            27.89314, -110.90809,
            76.67, 'Alto',
            0.978, 0.867,
            0.401, 0.7,
            0.85, 0.3,
            2.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90704390983629, 27.89139245016063], [-110.90584886580487, 27.89307080794683], [-110.90689467752027, 27.894820272960597], [-110.9091355640685, 27.89489135720554], [-110.91033057550757, 27.893212979581563], [-110.90928473299336, 27.891463537550464], [-110.90704390983629, 27.89139245016063]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2903ffff', 9,
            27.89132, -110.9048,
            76.71, 'Alto',
            0.975, 0.872,
            0.401, 0.7,
            0.85, 0.3,
            2.48, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90375732814205, 27.8895718280727], [-110.90256225152821, 27.89125016601635], [-110.90360800495503, 27.892999667443434], [-110.90584886580487, 27.89307080794683], [-110.90704390983629, 27.89139245016063], [-110.90599812560288, 27.889642971713627], [-110.90375732814205, 27.8895718280727]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb291bffff', 9,
            27.8895, -110.90152,
            76.75, 'Alto',
            0.972, 0.877,
            0.4, 0.7,
            0.85, 0.3,
            2.76, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90047083044325, 27.887751113337362], [-110.89927572125691, 27.889429431433673], [-110.90032141639088, 27.891178969261897], [-110.90256225152821, 27.89125016601635], [-110.90375732814205, 27.8895718280727], [-110.90271160219368, 27.88782231322199], [-110.90047083044325, 27.887751113337362]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2957ffff', 9,
            27.89111, -110.89808,
            76.66, 'Alto',
            0.973, 0.873,
            0.4, 0.7,
            0.85, 0.3,
            2.74, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89703491184628, 27.88935817843556], [-110.89583973418387, 27.891036466388297], [-110.8968853984935, 27.892786027188976], [-110.89912627129249, 27.89285727706451], [-110.90032141639088, 27.891178969261897], [-110.89927572125691, 27.889429431433673], [-110.89703491184628, 27.88935817843556]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2943ffff', 9,
            27.89271, -110.89464,
            76.57, 'Alto',
            0.972, 0.869,
            0.4, 0.7,
            0.85, 0.3,
            2.78, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89359888712785, 27.89096516026913], [-110.89240364099432, 27.892643418065674], [-110.89344927446969, 27.894393001833766], [-110.89569018491547, 27.894464304837953], [-110.8968853984935, 27.892786027188976], [-110.89583973418387, 27.891036466388297], [-110.89359888712785, 27.89096516026913]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb294bffff', 9,
            27.89432, -110.89121,
            76.47, 'Alto',
            0.971, 0.864,
            0.401, 0.7,
            0.85, 0.3,
            2.88, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89016275630782, 27.8925720588179], [-110.88896744170809, 27.894250286445654], [-110.89001304433927, 27.895999893176096], [-110.89225399241698, 27.89607124931649], [-110.89344927446969, 27.894393001833766], [-110.89240364099432, 27.892643418065674], [-110.89016275630782, 27.8925720588179]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b87ffff', 9,
            27.89593, -110.88777,
            76.36, 'Alto',
            0.97, 0.86,
            0.401, 0.7,
            0.85, 0.3,
            3.04, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88672651940594, 27.894178874061712], [-110.88553113634495, 27.895857071508065], [-110.88657670812204, 27.897606701195816], [-110.8888176938168, 27.89767811047997], [-110.89001304433927, 27.895999893176096], [-110.88896744170809, 27.894250286445654], [-110.88672651940594, 27.894178874061712]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b8fffff', 9,
            27.89754, -110.88434,
            76.24, 'Alto',
            0.968, 0.855,
            0.402, 0.7,
            0.85, 0.3,
            3.24, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88329017644205, 27.895785605980397], [-110.88209472492477, 27.897463773232737], [-110.8831402658378, 27.89921342587275], [-110.88538128913477, 27.899284888308223], [-110.88657670812204, 27.897606701195816], [-110.88553113634495, 27.895857071508065], [-110.88329017644205, 27.895785605980397]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b13ffff', 9,
            27.89914, -110.8809,
            76.13, 'Alto',
            0.965, 0.851,
            0.404, 0.7,
            0.85, 0.3,
            3.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87985372743594, 27.897392254553793], [-110.8786582074673, 27.89907039159952], [-110.87970371750637, 27.900820067186732], [-110.88194477839066, 27.90089158278109], [-110.8831402658378, 27.89921342587275], [-110.88209472492477, 27.897463773232737], [-110.87985372743594, 27.897392254553793]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b1bffff', 9,
            27.90075, -110.87746,
            76.01, 'Alto',
            0.963, 0.846,
            0.405, 0.7,
            0.85, 0.3,
            3.71, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87641717240746, 27.89899881976175], [-110.87522158399238, 27.900676926588243], [-110.87626706314758, 27.902426625117613], [-110.87850816160432, 27.90249819387839], [-110.87970371750637, 27.900820067186732], [-110.8786582074673, 27.89907039159952], [-110.87641717240746, 27.89899881976175]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b57ffff', 9,
            27.90236, -110.87403,
            75.89, 'Alto',
            0.96, 0.841,
            0.407, 0.7,
            0.85, 0.3,
            4.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87298051137638, 27.90060530158409], [-110.87178485451986, 27.90228337817876], [-110.87283030278122, 27.904033099645225], [-110.87507143879556, 27.904104721579987], [-110.87626706314758, 27.902426625117613], [-110.87522158399238, 27.900676926588243], [-110.87298051137638, 27.90060530158409]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b47ffff', 9,
            27.90578, -110.87388,
            75.7, 'Alto',
            0.961, 0.831,
            0.407, 0.7,
            0.85, 0.3,
            3.9, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87283030278122, 27.904033099645225], [-110.87163460998418, 27.905711165865707], [-110.87268008570479, 27.90746087388636], [-110.87492128512096, 27.90753249275195], [-110.8761169454121, 27.905854406665995], [-110.87507143879556, 27.904104721579987], [-110.87283030278122, 27.904033099645225]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b7bffff', 9,
            27.90921, -110.87373,
            75.51, 'Alto',
            0.962, 0.821,
            0.407, 0.7,
            0.85, 0.3,
            3.83, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87268008570479, 27.90746087388636], [-110.8714843569651, 27.909138929720353], [-110.87252986014633, 27.910888624283128], [-110.87477112296796, 27.91096024007978], [-110.8759668192003, 27.90928216438255], [-110.87492128512096, 27.90753249275195], [-110.87268008570479, 27.90746087388636]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b6bffff', 9,
            27.91264, -110.87358,
            75.31, 'Alto',
            0.962, 0.81,
            0.408, 0.7,
            0.85, 0.3,
            3.8, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87252986014633, 27.910888624283128], [-110.87133409546183, 27.912566669718345], [-110.87237962610513, 27.914316350811173], [-110.87462095233575, 27.914387963539124], [-110.87581668451148, 27.9127098982429], [-110.87477112296796, 27.91096024007978], [-110.87252986014633, 27.910888624283128]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0dd3ffff', 9,
            27.91607, -110.87343,
            75.09, 'Alto',
            0.962, 0.799,
            0.408, 0.7,
            0.85, 0.3,
            3.81, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87237962610513, 27.914316350811173], [-110.87118382547372, 27.915994385835322], [-110.8722293835805, 27.917744053446143], [-110.87447077322368, 27.917815663105618], [-110.8756665413449, 27.9161376082227], [-110.87462095233575, 27.914387963539124], [-110.87237962610513, 27.914316350811173]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0dc3ffff', 9,
            27.91949, -110.87327,
            74.87, 'Moderado',
            0.962, 0.788,
            0.408, 0.7,
            0.85, 0.3,
            3.83, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8722293835805, 27.917744053446143], [-110.87103354700004, 27.919422078046928], [-110.87207913257171, 27.92117173216367], [-110.87432058563097, 27.921243338754913], [-110.87551638969984, 27.91956529429759], [-110.87447077322368, 27.917815663105618], [-110.8722293835805, 27.917744053446143]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0dcfffff', 9,
            27.92292, -110.87312,
            74.65, 'Moderado',
            0.962, 0.777,
            0.408, 0.7,
            0.85, 0.3,
            3.84, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87207913257171, 27.92117173216367], [-110.87088326004005, 27.9228497463288], [-110.87192887307805, 27.924599386939416], [-110.87417038955697, 27.924670990462637], [-110.87536622957563, 27.922992956443213], [-110.87432058563097, 27.921243338754913], [-110.87207913257171, 27.92117173216367]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d57ffff', 9,
            27.92635, -110.87297,
            74.42, 'Moderado',
            0.961, 0.766,
            0.408, 0.7,
            0.85, 0.3,
            3.88, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87192887307805, 27.924599386939416], [-110.87073296459305, 27.926277390656587], [-110.8717786050988, 27.928027017749006], [-110.87402018500093, 27.928098618204466], [-110.8752160609715, 27.926420594635214], [-110.87417038955697, 27.924670990462637], [-110.87192887307805, 27.924599386939416]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d47ffff', 9,
            27.92978, -110.87282,
            74.18, 'Moderado',
            0.96, 0.755,
            0.408, 0.7,
            0.85, 0.3,
            3.95, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8717786050988, 27.928027017749006], [-110.87058266065831, 27.929705011005943], [-110.87162832863324, 27.93145462456811], [-110.87386997196215, 27.931526221956013], [-110.87506588388676, 27.929848208849243], [-110.87402018500093, 27.928098618204466], [-110.8717786050988, 27.928027017749006]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d7bffff', 9,
            27.9332, -110.87267,
            73.93, 'Moderado',
            0.959, 0.743,
            0.408, 0.7,
            0.85, 0.3,
            4.06, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87162832863324, 27.93145462456811], [-110.87043234823513, 27.93313260735251], [-110.87147804368064, 27.93488220737236], [-110.87371975043989, 27.934953801692952], [-110.87491569832069, 27.933275799060944], [-110.87386997196215, 27.931526221956013], [-110.87162832863324, 27.93145462456811]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d63ffff', 9,
            27.93503, -110.87596,
            73.83, 'Moderado',
            0.962, 0.737,
            0.406, 0.7,
            0.85, 0.3,
            3.78, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87491569832069, 27.933275799060944], [-110.87371975043989, 27.934953801692952], [-110.87476550427257, 27.936703365245968], [-110.87700723689395, 27.93677490324953], [-110.87820315224754, 27.93509688077469], [-110.87715736750958, 27.93334734013918], [-110.87491569832069, 27.933275799060944]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d67ffff', 9,
            27.93685, -110.87925,
            73.73, 'Moderado',
            0.965, 0.731,
            0.404, 0.7,
            0.85, 0.3,
            3.52, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87820315224754, 27.93509688077469], [-110.87700723689395, 27.93677490324953], [-110.8780530491096, 27.938524430323525], [-110.8802948075789, 27.938595912002643], [-110.88149069039534, 27.936917869689747], [-110.88044484728222, 27.93516836553585], [-110.87820315224754, 27.93509688077469]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0993ffff', 9,
            27.93867, -110.88254,
            73.63, 'Moderado',
            0.967, 0.725,
            0.403, 0.7,
            0.85, 0.3,
            3.3, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88149069039534, 27.936917869689747], [-110.8802948075789, 27.938595912002643], [-110.88134067817327, 27.940345402585447], [-110.88358246247634, 27.940416827932715], [-110.8847783127457, 27.938738765786546], [-110.88373241126166, 27.936989298126434], [-110.88149069039534, 27.936917869689747]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0997ffff', 9,
            27.94049, -110.88582,
            73.53, 'Moderado',
            0.969, 0.718,
            0.402, 0.7,
            0.85, 0.3,
            3.1, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8847783127457, 27.938738765786546], [-110.88358246247634, 27.940416827932715], [-110.88462839144519, 27.94216628201213], [-110.88687020156786, 27.942237651020147], [-110.88806601928019, 27.94055956904547], [-110.88702005942947, 27.938810137891334], [-110.8847783127457, 27.938738765786546]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb724bffff', 9,
            27.94231, -110.88911,
            73.42, 'Moderado',
            0.971, 0.712,
            0.401, 0.7,
            0.85, 0.3,
            2.93, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88806601928019, 27.94055956904547], [-110.88687020156786, 27.942237651020147], [-110.88791618890694, 27.94398706858399], [-110.89015802483503, 27.944058381245355], [-110.8913538099804, 27.942380279446954], [-110.89030779176724, 27.940630884810965], [-110.88806601928019, 27.94055956904547]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb724fffff', 9,
            27.94413, -110.8924,
            73.31, 'Moderado',
            0.972, 0.706,
            0.4, 0.7,
            0.85, 0.3,
            2.82, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8913538099804, 27.942380279446954], [-110.89015802483503, 27.944058381245355], [-110.89120407054013, 27.945807762281454], [-110.89344593225944, 27.945879018588755], [-110.89464168482792, 27.944200896971413], [-110.89359560825658, 27.942451538865754], [-110.8913538099804, 27.942380279446954]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb727bffff', 9,
            27.94595, -110.89569,
            73.19, 'Moderado',
            0.972, 0.7,
            0.4, 0.7,
            0.85, 0.3,
            2.77, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89464168482792, 27.944200896971413], [-110.89344593225944, 27.945879018588755], [-110.89449203632627, 27.947628363084927], [-110.89673392382265, 27.94769956303077], [-110.8979296438043, 27.946021421599262], [-110.896883508879, 27.944272100036116], [-110.89464168482792, 27.944200896971413]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7263ffff', 9,
            27.94777, -110.89898,
            73.06, 'Moderado',
            0.972, 0.693,
            0.4, 0.7,
            0.85, 0.3,
            2.79, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8979296438043, 27.946021421599262], [-110.89673392382265, 27.94769956303077], [-110.897780086247, 27.94944887097483], [-110.90002199950625, 27.949520014551823], [-110.90121768689114, 27.947841853310923], [-110.90017149361616, 27.946092568302472], [-110.8979296438043, 27.946021421599262]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7267ffff', 9,
            27.94959, -110.90226,
            72.92, 'Moderado',
            0.971, 0.687,
            0.4, 0.7,
            0.85, 0.3,
            2.86, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90121768689114, 27.947841853310923], [-110.90002199950625, 27.949520014551823], [-110.90106822028385, 27.951269285931605], [-110.9033101592918, 27.951340373132332], [-110.90450581407, 27.94966219208683], [-110.90345956244956, 27.947912943645257], [-110.90121768689114, 27.947841853310923]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb722bffff', 9,
            27.94798, -110.9057,
            73.09, 'Moderado',
            0.974, 0.693,
            0.401, 0.7,
            0.85, 0.3,
            2.61, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9046551812844, 27.946234752104907], [-110.90345956244956, 27.947912943645257], [-110.90450581407, 27.94966219208683], [-110.9067477153608, 27.949733226044874], [-110.90794330158043, 27.948055014702472], [-110.90689701912709, 27.94630578920414], [-110.9046551812844, 27.946234752104907]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7223ffff', 9,
            27.94638, -110.90914,
            73.25, 'Moderado',
            0.976, 0.698,
            0.401, 0.7,
            0.85, 0.3,
            2.41, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90809256940692, 27.94462756737695], [-110.90689701912709, 27.94630578920414], [-110.90794330158043, 27.948055014702472], [-110.9101851651392, 27.948125995425393], [-110.91138068279531, 27.9464477537987], [-110.91033436951899, 27.944698551248656], [-110.90809256940692, 27.94462756737695]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7237ffff', 9,
            27.94477, -110.91258,
            73.42, 'Moderado',
            0.978, 0.704,
            0.403, 0.7,
            0.85, 0.3,
            2.22, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91152985123888, 27.943020299147243], [-110.91033436951899, 27.944698551248656], [-110.91138068279531, 27.9464477537987], [-110.91362250860716, 27.94651868129406], [-110.91481795769486, 27.944840409395685], [-110.9137716136055, 27.943091229798977], [-110.91152985123888, 27.943020299147243]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb73dbffff', 9,
            27.94316, -110.91601,
            73.59, 'Moderado',
            0.98, 0.709,
            0.404, 0.7,
            0.85, 0.3,
            2.04, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91496702676052, 27.941412947435943], [-110.9137716136055, 27.943091229798977], [-110.91481795769486, 27.944840409395685], [-110.91705974574491, 27.944911283671054], [-110.91825512625924, 27.943232981513624], [-110.91720875136679, 27.941483824875288], [-110.91496702676052, 27.941412947435943]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb73d3ffff', 9,
            27.94155, -110.91945,
            73.76, 'Moderado',
            0.981, 0.715,
            0.406, 0.7,
            0.85, 0.3,
            1.87, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91840409595198, 27.939805512263256], [-110.91720875136679, 27.941483824875288], [-110.91825512625924, 27.943232981513624], [-110.92049687653264, 27.943303802576565], [-110.92169218846864, 27.941625470172685], [-110.92064578278304, 27.93987633649777], [-110.91840409595198, 27.939805512263256]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb706fffff', 9,
            27.93995, -110.92289,
            73.93, 'Moderado',
            0.983, 0.72,
            0.408, 0.7,
            0.85, 0.3,
            1.69, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9218410587935, 27.938197993649343], [-110.92064578278304, 27.93987633649777], [-110.92169218846864, 27.941625470172685], [-110.92393390095052, 27.941696238030772], [-110.92512914430327, 27.940017875393067], [-110.92408270783447, 27.938268764686605], [-110.9218410587935, 27.938197993649343]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7067ffff', 9,
            27.93834, -110.92632,
            74.1, 'Moderado',
            0.984, 0.726,
            0.41, 0.7,
            0.85, 0.3,
            1.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92527791526527, 27.936590391614395], [-110.92408270783447, 27.938268764686605], [-110.92512914430327, 27.940017875393067], [-110.92737081897876, 27.94008859005387], [-110.92856599374336, 27.93841019719493], [-110.92751952650127, 27.93666110946198], [-110.92527791526527, 27.936590391614395]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb702bffff', 9,
            27.93673, -110.92976,
            74.26, 'Moderado',
            0.985, 0.731,
            0.412, 0.7,
            0.85, 0.3,
            1.52, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92871466534747, 27.934982706178612], [-110.92751952650127, 27.93666110946198], [-110.92856599374336, 27.93841019719493], [-110.9308076305976, 27.938480858666043], [-110.9320027367691, 27.936802435598494], [-110.93095623876367, 27.93505337084407], [-110.92871466534747, 27.934982706178612]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7023ffff', 9,
            27.93512, -110.9332,
            74.39, 'Moderado',
            0.984, 0.737,
            0.415, 0.7,
            0.85, 0.3,
            1.61, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93215130902034, 27.933374937362167], [-110.93095623876367, 27.93505337084407], [-110.9320027367691, 27.936802435598494], [-110.93424433578721, 27.93687304388747], [-110.9354393733607, 27.935194590623933], [-110.93439284460186, 27.93344554885309], [-110.93215130902034, 27.933374937362167]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7033ffff', 9,
            27.9317, -110.93335,
            74.67, 'Moderado',
            0.986, 0.748,
            0.415, 0.7,
            0.85, 0.3,
            1.38, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93229987288065, 27.929947415117258], [-110.93110483853668, 27.931625859001247], [-110.93215130902034, 27.933374937362167], [-110.93439284460186, 27.93344554885309], [-110.93558784626407, 27.931767085185253], [-110.93454134502916, 27.930018029810373], [-110.93229987288065, 27.929947415117258]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb70abffff', 9,
            27.92827, -110.93349,
            74.94, 'Moderado',
            0.988, 0.76,
            0.415, 0.7,
            0.85, 0.3,
            1.18, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93244842835078, 27.92651986888811], [-110.93125342991735, 27.928198323161897], [-110.93229987288065, 27.929947415117258], [-110.93454134502916, 27.930018029810373], [-110.93573631078226, 27.928339555750515], [-110.93468983706978, 27.926590486783663], [-110.93244842835078, 27.92651986888811]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb70bbffff', 9,
            27.92484, -110.93364,
            75.19, 'Alto',
            0.989, 0.771,
            0.416, 0.7,
            0.85, 0.3,
            1.06, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93259697543137, 27.9230922986991], [-110.93140201290637, 27.924770763350377], [-110.93244842835078, 27.92651986888811], [-110.93468983706978, 27.926590486783663], [-110.93588476691589, 27.92491200234407], [-110.93483832072448, 27.923162919797306], [-110.93259697543137, 27.9230922986991]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7087ffff', 9,
            27.92141, -110.93379,
            75.42, 'Alto',
            0.989, 0.782,
            0.416, 0.7,
            0.85, 0.3,
            1.06, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93274551412317, 27.91966470457455], [-110.93155058750449, 27.921343179591034], [-110.93259697543137, 27.9230922986991], [-110.93483832072448, 27.923162919797306], [-110.93603321466573, 27.921484424990272], [-110.93498679599392, 27.91973532887564], [-110.93274551412317, 27.91966470457455]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7097ffff', 9,
            27.91799, -110.93394,
            75.64, 'Alto',
            0.989, 0.793,
            0.416, 0.7,
            0.85, 0.3,
            1.08, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93289404442689, 27.916237086538832], [-110.93169915371234, 27.91791557190822], [-110.93274551412317, 27.91966470457455], [-110.93498679599392, 27.91973532887564], [-110.93618165403247, 27.918056823713467], [-110.93513526287886, 27.916307714043036], [-110.93289404442689, 27.916237086538832]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb742fffff', 9,
            27.91456, -110.93409,
            75.85, 'Alto',
            0.989, 0.804,
            0.416, 0.7,
            0.85, 0.3,
            1.09, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93304256634325, 27.91280944461628], [-110.93184771153071, 27.914487940326296], [-110.93289404442689, 27.916237086538832], [-110.93513526287886, 27.916307714043036], [-110.93633008501679, 27.914629198538012], [-110.93528372137996, 27.91288007532384], [-110.93304256634325, 27.91280944461628]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7423ffff', 9,
            27.91113, -110.93424,
            76.05, 'Alto',
            0.988, 0.815,
            0.416, 0.7,
            0.85, 0.3,
            1.19, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93319107987291, 27.90938177883126], [-110.93199626096029, 27.9110602848696], [-110.93304256634325, 27.91280944461628], [-110.93528372137996, 27.91288007532384], [-110.93647850761944, 27.911201549488254], [-110.93543217149796, 27.909452412742407], [-110.93319107987291, 27.90938177883126]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7433ffff', 9,
            27.9077, -110.93439,
            76.22, 'Alto',
            0.986, 0.825,
            0.416, 0.7,
            0.85, 0.3,
            1.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93333958501661, 27.90595408920813], [-110.93214480200174, 27.907632605562497], [-110.93319107987291, 27.90938177883126], [-110.93543217149796, 27.909452412742407], [-110.93662692184111, 27.907773876588553], [-110.93558061323355, 27.90602472632308], [-110.93333958501661, 27.90595408920813]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74abffff', 9,
            27.90428, -110.93453,
            76.38, 'Alto',
            0.984, 0.836,
            0.416, 0.7,
            0.85, 0.3,
            1.61, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93348808177507, 27.90252637577123], [-110.93229333465582, 27.904204902429342], [-110.93333958501661, 27.90595408920813], [-110.93558061323355, 27.90602472632308], [-110.93677532768251, 27.90434617986326], [-110.93572904658744, 27.90259701609024], [-110.93348808177507, 27.90252637577123]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7417ffff', 9,
            27.90246, -110.93125,
            76.47, 'Alto',
            0.985, 0.841,
            0.414, 0.7,
            0.85, 0.3,
            1.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93020091969163, 27.900706478872625], [-110.92900613991202, 27.902384985724236], [-110.93005233202177, 27.904134209004162], [-110.93229333465582, 27.904204902429342], [-110.93348808177507, 27.90252637577123], [-110.93244185892324, 27.900777175494486], [-110.93020091969163, 27.900706478872625]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7413ffff', 9,
            27.90064, -110.92796,
            76.54, 'Alto',
            0.985, 0.846,
            0.411, 0.7,
            0.85, 0.3,
            1.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9269138414506, 27.898886489187003], [-110.92571902902057, 27.900564976227322], [-110.92676516287503, 27.90231423599622], [-110.92900613991202, 27.902384985724236], [-110.93020091969163, 27.900706478872625], [-110.92915475508728, 27.898957242104345], [-110.9269138414506, 27.898886489187003]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74c7ffff', 9,
            27.89882, -110.92467,
            76.59, 'Alto',
            0.984, 0.852,
            0.409, 0.7,
            0.85, 0.3,
            1.62, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92362684707044, 27.897066406733924], [-110.92243200199988, 27.898744873958176], [-110.9234780775948, 27.900494170203864], [-110.92571902902057, 27.900564976227322], [-110.9269138414506, 27.898886489187003], [-110.925867735098, 27.897137215939345], [-110.92362684707044, 27.897066406733924]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74c3ffff', 9,
            27.897, -110.92139,
            76.62, 'Alto',
            0.982, 0.857,
            0.407, 0.7,
            0.85, 0.3,
            1.8, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92033993656955, 27.895246231532955], [-110.91914505886841, 27.896924678936337], [-110.92019107619952, 27.898674011646648], [-110.92243200199988, 27.898744873958176], [-110.92362684707044, 27.897066406733924], [-110.92258079897383, 27.895317097019063], [-110.92033993656955, 27.895246231532955]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74dbffff', 9,
            27.89518, -110.9181,
            76.66, 'Alto',
            0.98, 0.862,
            0.405, 0.7,
            0.85, 0.3,
            2.01, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91705310996636, 27.89342596360366], [-110.91585819964453, 27.895104391181402], [-110.91690415870761, 27.896853760344143], [-110.91914505886841, 27.896924678936337], [-110.92033993656955, 27.895246231532955], [-110.91929394673318, 27.89349688536308], [-110.91705310996636, 27.89342596360366]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29afffff', 9,
            27.89336, -110.91481,
            76.7, 'Alto',
            0.978, 0.867,
            0.403, 0.7,
            0.85, 0.3,
            2.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9137663672793, 27.891605602965626], [-110.91257142434671, 27.893284010712918], [-110.91361732513748, 27.895033416315925], [-110.91585819964453, 27.895104391181402], [-110.91705310996636, 27.89342596360366], [-110.9160071783945, 27.891676580990953], [-110.9137663672793, 27.891605602965626]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29abffff', 9,
            27.89153, -110.91153,
            76.74, 'Alto',
            0.976, 0.872,
            0.402, 0.7,
            0.85, 0.3,
            2.41, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91047970852678, 27.889785149638396], [-110.90928473299336, 27.891463537550464], [-110.91033057550757, 27.893212979581563], [-110.91257142434671, 27.893284010712918], [-110.9137663672793, 27.891605602965626], [-110.91272049397618, 27.88985618392224], [-110.91047970852678, 27.889785149638396]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2917ffff', 9,
            27.88971, -110.90824,
            76.78, 'Alto',
            0.974, 0.877,
            0.401, 0.7,
            0.85, 0.3,
            2.61, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90719313372722, 27.887964603641564], [-110.90599812560288, 27.889642971713627], [-110.90704390983629, 27.89139245016063], [-110.90928473299336, 27.891463537550464], [-110.91047970852678, 27.889785149638396], [-110.90943389349665, 27.888035694176533], [-110.90719313372722, 27.887964603641564]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2913ffff', 9,
            27.88789, -110.90495,
            76.82, 'Alto',
            0.972, 0.882,
            0.401, 0.7,
            0.85, 0.3,
            2.85, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90390664289902, 27.886143964994698], [-110.90271160219368, 27.88782231322199], [-110.90375732814205, 27.8895718280727], [-110.90599812560288, 27.889642971713627], [-110.90719313372722, 27.887964603641564], [-110.90614737697435, 27.8862151117734], [-110.90390664289902, 27.886143964994698]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29c7ffff', 9,
            27.88607, -110.90167,
            76.85, 'Alto',
            0.969, 0.886,
            0.4, 0.7,
            0.85, 0.3,
            3.12, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90062023606059, 27.884323233717392], [-110.89942516278415, 27.886001562095103], [-110.90047083044325, 27.887751113337362], [-110.90271160219368, 27.88782231322199], [-110.90390664289902, 27.886143964994698], [-110.90286094442763, 27.88439443673242], [-110.90062023606059, 27.884323233717392]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29cfffff', 9,
            27.88768, -110.89823,
            76.78, 'Alto',
            0.969, 0.882,
            0.4, 0.7,
            0.85, 0.3,
            3.08, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89718441675832, 27.885930305974178], [-110.89598927500938, 27.88760860421837], [-110.89703491184628, 27.88935817843556], [-110.89927572125691, 27.889429431433673], [-110.90047083044325, 27.887751113337362], [-110.89942516278415, 27.886001562095103], [-110.89718441675832, 27.885930305974178]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2953ffff', 9,
            27.88929, -110.89479,
            76.69, 'Alto',
            0.969, 0.878,
            0.4, 0.7,
            0.85, 0.3,
            3.09, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89374849133961, 27.887537294984], [-110.8925532811231, 27.889215563082075], [-110.89359888712785, 27.89096516026913], [-110.89583973418387, 27.891036466388297], [-110.89703491184628, 27.88935817843556], [-110.89598927500938, 27.88760860421837], [-110.89374849133961, 27.887537294984]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb295bffff', 9,
            27.89089, -110.89136,
            76.6, 'Alto',
            0.968, 0.874,
            0.401, 0.7,
            0.85, 0.3,
            3.16, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89031245982424, 27.889144200726694], [-110.88911718114511, 27.890822438666017], [-110.89016275630782, 27.8925720588179], [-110.89240364099432, 27.892643418065674], [-110.89359888712785, 27.89096516026913], [-110.8925532811231, 27.889215563082075], [-110.89031245982424, 27.889144200726694]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b97ffff', 9,
            27.8925, -110.88792,
            76.5, 'Alto',
            0.967, 0.869,
            0.401, 0.7,
            0.85, 0.3,
            3.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88687632223206, 27.890751023182073], [-110.88568097509523, 27.892429230950068], [-110.88672651940594, 27.894178874061712], [-110.88896744170809, 27.894250286445654], [-110.89016275630782, 27.8925720588179], [-110.88911718114511, 27.890822438666017], [-110.88687632223206, 27.890751023182073]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b83ffff', 9,
            27.89411, -110.88449,
            76.39, 'Alto',
            0.966, 0.865,
            0.402, 0.7,
            0.85, 0.3,
            3.45, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88344007858281, 27.89235776232999], [-110.88224466299323, 27.894035939914033], [-110.88329017644205, 27.895785605980397], [-110.88553113634495, 27.895857071508065], [-110.88672651940594, 27.894178874061712], [-110.88568097509523, 27.892429230950068], [-110.88344007858281, 27.89235776232999]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b8bffff', 9,
            27.89571, -110.88105,
            76.28, 'Alto',
            0.963, 0.86,
            0.404, 0.7,
            0.85, 0.3,
            3.65, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88000372889634, 27.893964418150272], [-110.87880824485894, 27.89564256553776], [-110.87985372743594, 27.897392254553793], [-110.88209472492477, 27.897463773232737], [-110.88329017644205, 27.895785605980397], [-110.88224466299323, 27.894035939914033], [-110.88000372889634, 27.893964418150272]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2bc7ffff', 9,
            27.89732, -110.87761,
            76.17, 'Alto',
            0.961, 0.856,
            0.405, 0.7,
            0.85, 0.3,
            3.88, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87656727319245, 27.895570990622762], [-110.87537172071221, 27.897249107801084], [-110.87641717240746, 27.89899881976175], [-110.8786582074673, 27.89907039159952], [-110.87985372743594, 27.897392254553793], [-110.87880824485894, 27.89564256553776], [-110.87656727319245, 27.895570990622762]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2bcfffff', 9,
            27.89893, -110.87418,
            76.06, 'Alto',
            0.959, 0.851,
            0.407, 0.7,
            0.85, 0.3,
            4.13, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87313071149097, 27.897177479727297], [-110.87193509057282, 27.89885556668386], [-110.87298051137638, 27.90060530158409], [-110.87522158399238, 27.900676926588243], [-110.87641717240746, 27.89899881976175], [-110.87537172071221, 27.897249107801084], [-110.87313071149097, 27.897177479727297]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b53ffff', 9,
            27.90053, -110.87074,
            75.94, 'Alto',
            0.956, 0.847,
            0.409, 0.7,
            0.85, 0.3,
            4.41, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86969404381172, 27.898783885443752], [-110.86849835446061, 27.90046194216594], [-110.86954374436257, 27.902211700000674], [-110.87178485451986, 27.90228337817876], [-110.87298051137638, 27.90060530158409], [-110.87193509057282, 27.89885556668386], [-110.86969404381172, 27.898783885443752]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b43ffff', 9,
            27.90396, -110.87059,
            75.76, 'Alto',
            0.957, 0.837,
            0.409, 0.7,
            0.85, 0.3,
            4.3, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86954374436257, 27.902211700000674], [-110.86834801906953, 27.903889746350906], [-110.86939343642717, 27.90563949074942], [-110.87163460998418, 27.905711165865707], [-110.87283030278122, 27.904033099645225], [-110.87178485451986, 27.90228337817876], [-110.86954374436257, 27.902211700000674]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b4fffff', 9,
            27.90739, -110.87044,
            75.57, 'Alto',
            0.958, 0.826,
            0.41, 0.7,
            0.85, 0.3,
            4.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86939343642717, 27.90563949074942], [-110.86819767519005, 27.907317526715403], [-110.86924312000478, 27.90906725766564], [-110.8714843569651, 27.909138929720353], [-110.87268008570479, 27.90746087388636], [-110.87163460998418, 27.905711165865707], [-110.86939343642717, 27.90563949074942]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0cb7ffff', 9,
            27.91082, -110.87029,
            75.37, 'Alto',
            0.958, 0.816,
            0.41, 0.7,
            0.85, 0.3,
            4.18, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86924312000478, 27.90906725766564], [-110.86804732282145, 27.910745283235087], [-110.86909279509467, 27.912495000724963], [-110.87133409546183, 27.912566669718345], [-110.87252986014633, 27.910888624283128], [-110.8714843569651, 27.909138929720353], [-110.86924312000478, 27.90906725766564]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0ca7ffff', 9,
            27.91424, -110.87014,
            75.16, 'Alto',
            0.958, 0.805,
            0.41, 0.7,
            0.85, 0.3,
            4.18, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86909279509467, 27.912495000724963], [-110.867896961963, 27.914173015885577], [-110.86894246169615, 27.91592271990305], [-110.87118382547372, 27.915994385835322], [-110.87237962610513, 27.914316350811173], [-110.87133409546183, 27.912566669718345], [-110.86909279509467, 27.912495000724963]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0ddbffff', 9,
            27.91767, -110.86999,
            74.95, 'Moderado',
            0.958, 0.794,
            0.41, 0.7,
            0.85, 0.3,
            4.19, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86894246169615, 27.91592271990305], [-110.86774659261401, 27.917600724642526], [-110.8687921198085, 27.919350415175522], [-110.87103354700004, 27.919422078046928], [-110.8722293835805, 27.917744053446143], [-110.87118382547372, 27.915994385835322], [-110.86894246169615, 27.91592271990305]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0dcbffff', 9,
            27.9211, -110.86984,
            74.72, 'Moderado',
            0.958, 0.783,
            0.41, 0.7,
            0.85, 0.3,
            4.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8687921198085, 27.919350415175522], [-110.86759621477373, 27.921028409481572], [-110.86864176943098, 27.922778086518043], [-110.87088326004005, 27.9228497463288], [-110.87207913257171, 27.92117173216367], [-110.87103354700004, 27.919422078046928], [-110.8687921198085, 27.919350415175522]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d53ffff', 9,
            27.92453, -110.86969,
            74.5, 'Moderado',
            0.958, 0.772,
            0.41, 0.7,
            0.85, 0.3,
            4.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86864176943098, 27.922778086518043], [-110.86744582844146, 27.924456070378376], [-110.86849141056291, 27.92620573390625], [-110.87073296459305, 27.926277390656587], [-110.87192887307805, 27.924599386939416], [-110.87088326004005, 27.9228497463288], [-110.86864176943098, 27.922778086518043]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d43ffff', 9,
            27.92796, -110.86954,
            74.26, 'Moderado',
            0.957, 0.761,
            0.41, 0.7,
            0.85, 0.3,
            4.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86849141056291, 27.92620573390625], [-110.8672954336165, 27.927883707308567], [-110.86834104320354, 27.929633357315787], [-110.87058266065831, 27.929705011005943], [-110.8717786050988, 27.928027017749006], [-110.87073296459305, 27.926277390656587], [-110.86849141056291, 27.92620573390625]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d4fffff', 9,
            27.93138, -110.86939,
            74.02, 'Moderado',
            0.956, 0.749,
            0.41, 0.7,
            0.85, 0.3,
            4.36, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86834104320354, 27.929633357315787], [-110.8671450302981, 27.931311320247797], [-110.86819066735217, 27.933060956722297], [-110.87043234823513, 27.93313260735251], [-110.87162832863324, 27.93145462456811], [-110.87058266065831, 27.929705011005943], [-110.86834104320354, 27.929633357315787]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb08b7ffff', 9,
            27.93481, -110.86924,
            73.77, 'Moderado',
            0.955, 0.738,
            0.41, 0.7,
            0.85, 0.3,
            4.47, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86819066735217, 27.933060956722297], [-110.86699461848556, 27.934738909171706], [-110.86804028300807, 27.936488532101436], [-110.87028202732279, 27.936560179671933], [-110.87147804368064, 27.93488220737236], [-110.87043234823513, 27.93313260735251], [-110.86819066735217, 27.933060956722297]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d6bffff', 9,
            27.93663, -110.87252,
            73.67, 'Moderado',
            0.958, 0.732,
            0.408, 0.7,
            0.85, 0.3,
            4.2, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87147804368064, 27.93488220737236], [-110.87028202732279, 27.936560179671933], [-110.8713277502403, 27.938309766137408], [-110.87356952043343, 27.938381357390917], [-110.87476550427257, 27.936703365245968], [-110.87371975043989, 27.934953801692952], [-110.87147804368064, 27.93488220737236]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d6fffff', 9,
            27.93845, -110.87581,
            73.56, 'Moderado',
            0.961, 0.725,
            0.406, 0.7,
            0.85, 0.3,
            3.94, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87476550427257, 27.936703365245968], [-110.87356952043343, 27.938381357390917], [-110.87461530174171, 27.940130907379963], [-110.8768570977991, 27.94020244230908], [-110.8780530491096, 27.938524430323525], [-110.87700723689395, 27.93677490324953], [-110.87476550427257, 27.936703365245968]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb099bffff', 9,
            27.94027, -110.8791,
            73.46, 'Moderado',
            0.963, 0.719,
            0.405, 0.7,
            0.85, 0.3,
            3.72, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8780530491096, 27.938524430323525], [-110.8768570977991, 27.94020244230908], [-110.87790293749389, 27.941951955809518], [-110.88014475940136, 27.942023434406817], [-110.88134067817327, 27.940345402585447], [-110.8802948075789, 27.938595912002643], [-110.8780530491096, 27.938524430323525]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0983ffff', 9,
            27.94209, -110.88239,
            73.35, 'Moderado',
            0.965, 0.713,
            0.403, 0.7,
            0.85, 0.3,
            3.51, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88134067817327, 27.940345402585447], [-110.88014475940136, 27.942023434406817], [-110.88119065747841, 27.94377291140646], [-110.88343250522178, 27.943844333664543], [-110.88462839144519, 27.94216628201213], [-110.88358246247634, 27.940416827932715], [-110.88134067817327, 27.940345402585447]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0987ffff', 9,
            27.94392, -110.88567,
            73.24, 'Moderado',
            0.967, 0.707,
            0.402, 0.7,
            0.85, 0.3,
            3.34, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88462839144519, 27.94216628201213], [-110.88343250522178, 27.943844333664543], [-110.88447846167688, 27.945593774151206], [-110.88672033524199, 27.945665140062687], [-110.88791618890694, 27.94398706858399], [-110.88687020156786, 27.942237651020147], [-110.88462839144519, 27.94216628201213]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb09b3ffff', 9,
            27.94574, -110.88896,
            73.13, 'Moderado',
            0.968, 0.7,
            0.401, 0.7,
            0.85, 0.3,
            3.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88791618890694, 27.94398706858399], [-110.88672033524199, 27.945665140062687], [-110.88776635007088, 27.947414544024184], [-110.89000824944353, 27.94748585358164], [-110.89120407054013, 27.945807762281454], [-110.89015802483503, 27.944058381245355], [-110.88791618890694, 27.94398706858399]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb09b7ffff', 9,
            27.94756, -110.89225,
            73.01, 'Moderado',
            0.969, 0.694,
            0.4, 0.7,
            0.85, 0.3,
            3.13, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89120407054013, 27.945807762281454], [-110.89000824944353, 27.94748585358164], [-110.89105432264199, 27.949235221005793], [-110.89329624780801, 27.94930647420183], [-110.89449203632627, 27.947628363084927], [-110.89344593225944, 27.945879018588755], [-110.89120407054013, 27.945807762281454]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb726bffff', 9,
            27.94938, -110.89554,
            72.88, 'Moderado',
            0.969, 0.688,
            0.4, 0.7,
            0.85, 0.3,
            3.11, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89449203632627, 27.947628363084927], [-110.89329624780801, 27.94930647420183], [-110.89434237937176, 27.951055805076464], [-110.89658433031698, 27.951127001903675], [-110.897780086247, 27.94944887097483], [-110.89673392382265, 27.94769956303077], [-110.89449203632627, 27.947628363084927]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb726fffff', 9,
            27.9512, -110.89883,
            72.75, 'Moderado',
            0.969, 0.681,
            0.4, 0.7,
            0.85, 0.3,
            3.15, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.897780086247, 27.94944887097483], [-110.89658433031698, 27.951127001903675], [-110.8976305202418, 27.9528762962166], [-110.89987249695203, 27.9529474366676], [-110.90106822028385, 27.951269285931605], [-110.90002199950625, 27.949520014551823], [-110.897780086247, 27.94944887097483]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb549bffff', 9,
            27.95302, -110.90211,
            72.61, 'Moderado',
            0.968, 0.675,
            0.4, 0.7,
            0.85, 0.3,
            3.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90106822028385, 27.951269285931605], [-110.89987249695203, 27.9529474366676], [-110.90091874523367, 27.954696694406653], [-110.90316074769471, 27.95476777847403], [-110.90435643841842, 27.95308960793565], [-110.9033101592918, 27.951340373132332], [-110.90106822028385, 27.951269285931605]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb5493ffff', 9,
            27.95141, -110.90555,
            72.77, 'Moderado',
            0.97, 0.681,
            0.401, 0.7,
            0.85, 0.3,
            2.99, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90450581407, 27.94966219208683], [-110.9033101592918, 27.951340373132332], [-110.90435643841842, 27.95308960793565], [-110.90659840316087, 27.953160638752745], [-110.90779402532246, 27.951482437907412], [-110.9067477153608, 27.949733226044874], [-110.90450581407, 27.94966219208683]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb722fffff', 9,
            27.9498, -110.90899,
            72.94, 'Moderado',
            0.972, 0.686,
            0.401, 0.7,
            0.85, 0.3,
            2.79, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90794330158043, 27.948055014702472], [-110.9067477153608, 27.949733226044874], [-110.90779402532246, 27.951482437907412], [-110.91003595233144, 27.951553415481776], [-110.91123150592594, 27.9498751843421], [-110.9101851651392, 27.948125995425393], [-110.90794330158043, 27.948055014702472]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7227ffff', 9,
            27.9482, -110.91243,
            73.1, 'Moderado',
            0.974, 0.692,
            0.403, 0.7,
            0.85, 0.3,
            2.6, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91138068279531, 27.9464477537987], [-110.9101851651392, 27.948125995425393], [-110.91123150592594, 27.9498751843421], [-110.91347339518659, 27.949946108681303], [-110.91466888020908, 27.948267847259896], [-110.91362250860716, 27.94651868129406], [-110.91138068279531, 27.9464477537987]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb73cbffff', 9,
            27.94659, -110.91586,
            73.27, 'Moderado',
            0.976, 0.697,
            0.404, 0.7,
            0.85, 0.3,
            2.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91481795769486, 27.944840409395685], [-110.91362250860716, 27.94651868129406], [-110.91466888020908, 27.948267847259896], [-110.9169107317065, 27.948338718371513], [-110.91810614815205, 27.94666042668097], [-110.91705974574491, 27.944911283671054], [-110.91481795769486, 27.944840409395685]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb73c3ffff', 9,
            27.94498, -110.9193,
            73.44, 'Moderado',
            0.978, 0.703,
            0.406, 0.7,
            0.85, 0.3,
            2.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91825512625924, 27.943232981513624], [-110.91705974574491, 27.944911283671054], [-110.91810614815205, 27.94666042668097], [-110.92034796187139, 27.94673124457258], [-110.92154330973506, 27.94505292262554], [-110.92049687653264, 27.943303802576565], [-110.91825512625924, 27.943232981513624]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb73d7ffff', 9,
            27.94337, -110.92274,
            73.62, 'Moderado',
            0.979, 0.709,
            0.407, 0.7,
            0.85, 0.3,
            2.07, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92169218846864, 27.941625470172685], [-110.92049687653264, 27.943303802576565], [-110.92154330973506, 27.94505292262554], [-110.92378508566141, 27.94512368730469], [-110.92498036493828, 27.943445335113758], [-110.92393390095052, 27.941696238030772], [-110.92169218846864, 27.941625470172685]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb739bffff', 9,
            27.94177, -110.92618,
            73.79, 'Moderado',
            0.981, 0.714,
            0.41, 0.7,
            0.85, 0.3,
            1.92, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92512914430327, 27.940017875393067], [-110.92393390095052, 27.941696238030772], [-110.92498036493828, 27.943445335113758], [-110.9272221030568, 27.94351604658803], [-110.92841731374193, 27.941837664165806], [-110.92737081897876, 27.94008859005387], [-110.92512914430327, 27.940017875393067]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7393ffff', 9,
            27.94016, -110.92961,
            73.95, 'Moderado',
            0.981, 0.72,
            0.412, 0.7,
            0.85, 0.3,
            1.86, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92856599374336, 27.93841019719493], [-110.92737081897876, 27.94008859005387], [-110.92841731374193, 27.941837664165806], [-110.93065901403776, 27.941908322442792], [-110.93185415612622, 27.9402299098019], [-110.9308076305976, 27.938480858666043], [-110.92856599374336, 27.93841019719493]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb702fffff', 9,
            27.93855, -110.93305,
            74.1, 'Moderado',
            0.981, 0.725,
            0.415, 0.7,
            0.85, 0.3,
            1.89, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9320027367691, 27.936802435598494], [-110.9308076305976, 27.938480858666043], [-110.93185415612622, 27.9402299098019], [-110.9340958185845, 27.94030051488915], [-110.93529089207138, 27.938622072042204], [-110.93424433578721, 27.93687304388747], [-110.9320027367691, 27.936802435598494]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7027ffff', 9,
            27.93694, -110.93649,
            74.23, 'Moderado',
            0.98, 0.731,
            0.418, 0.7,
            0.85, 0.3,
            2.01, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9354393733607, 27.935194590623933], [-110.93424433578721, 27.93687304388747], [-110.93529089207138, 27.938622072042204], [-110.93753251667721, 27.938692623947315], [-110.93872752155757, 27.937014150906936], [-110.93768093452783, 27.935265145738356], [-110.9354393733607, 27.935194590623933]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7037ffff', 9,
            27.93352, -110.93663,
            74.51, 'Moderado',
            0.982, 0.742,
            0.418, 0.7,
            0.85, 0.3,
            1.79, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93558784626407, 27.931767085185253], [-110.93439284460186, 27.93344554885309], [-110.9354393733607, 27.935194590623933], [-110.93768093452783, 27.935265145738356], [-110.93887590349837, 27.93358666229144], [-110.93782934399607, 27.931837643509226], [-110.93558784626407, 27.931767085185253]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb70afffff', 9,
            27.93009, -110.93678,
            74.78, 'Moderado',
            0.984, 0.754,
            0.418, 0.7,
            0.85, 0.3,
            1.6, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93573631078226, 27.928339555750515], [-110.93454134502916, 27.930018029810373], [-110.93558784626407, 27.931767085185253], [-110.93782934399607, 27.931837643509226], [-110.93902427705892, 27.930159149668064], [-110.93797774508263, 27.928410117284276], [-110.93573631078226, 27.928339555750515]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb70a3ffff', 9,
            27.92666, -110.93693,
            75.04, 'Alto',
            0.985, 0.765,
            0.418, 0.7,
            0.85, 0.3,
            1.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93588476691589, 27.92491200234407], [-110.93468983706978, 27.926590486783663], [-110.93573631078226, 27.928339555750515], [-110.93797774508263, 27.928410117284276], [-110.93917264223994, 27.92673161306115], [-110.93812613778826, 27.924982567087852], [-110.93588476691589, 27.92491200234407]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb70b3ffff', 9,
            27.92323, -110.93708,
            75.27, 'Alto',
            0.986, 0.776,
            0.419, 0.7,
            0.85, 0.3,
            1.43, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93603321466573, 27.921484424990272], [-110.93483832072448, 27.923162919797306], [-110.93588476691589, 27.92491200234407], [-110.93812613778826, 27.924982567087852], [-110.93932099904214, 27.923304052495055], [-110.93827452211363, 27.921554992944298], [-110.93603321466573, 27.921484424990272]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb754bffff', 9,
            27.91981, -110.93723,
            75.49, 'Alto',
            0.986, 0.787,
            0.419, 0.7,
            0.85, 0.3,
            1.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93618165403247, 27.918056823713467], [-110.93498679599392, 27.91973532887564], [-110.93603321466573, 27.921484424990272], [-110.93827452211363, 27.921554992944298], [-110.93946934746621, 27.919876467994126], [-110.93842289805944, 27.91812739487798], [-110.93618165403247, 27.918056823713467]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb755bffff', 9,
            27.91638, -110.93738,
            75.71, 'Alto',
            0.985, 0.798,
            0.419, 0.7,
            0.85, 0.3,
            1.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93633008501679, 27.914629198538012], [-110.93513526287886, 27.916307714043036], [-110.93618165403247, 27.918056823713467], [-110.93842289805944, 27.91812739487798], [-110.9396176875129, 27.91644885958273], [-110.93857126562645, 27.914699772913238], [-110.93633008501679, 27.914629198538012]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7427ffff', 9,
            27.91295, -110.93752,
            75.92, 'Alto',
            0.985, 0.809,
            0.419, 0.7,
            0.85, 0.3,
            1.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93647850761944, 27.911201549488254], [-110.93528372137996, 27.91288007532384], [-110.93633008501679, 27.914629198538012], [-110.93857126562645, 27.914699772913238], [-110.93976601918287, 27.913021227285185], [-110.9387196248153, 27.91127212707443], [-110.93647850761944, 27.911201549488254]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7437ffff', 9,
            27.90952, -110.93767,
            76.11, 'Alto',
            0.984, 0.82,
            0.419, 0.7,
            0.85, 0.3,
            1.61, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93662692184111, 27.907773876588553], [-110.93543217149796, 27.909452412742407], [-110.93647850761944, 27.911201549488254], [-110.9387196248153, 27.91127212707443], [-110.93991434247683, 27.90959357112589], [-110.93886797562674, 27.907844457385913], [-110.93662692184111, 27.907773876588553]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74afffff', 9,
            27.9061, -110.93782,
            76.28, 'Alto',
            0.982, 0.83,
            0.419, 0.7,
            0.85, 0.3,
            1.81, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93677532768251, 27.90434617986326], [-110.93558061323355, 27.90602472632308], [-110.93662692184111, 27.907773876588553], [-110.93886797562674, 27.907844457385913], [-110.94006265739552, 27.90616589112916], [-110.93901631806148, 27.90441676387203], [-110.93677532768251, 27.90434617986326]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74a3ffff', 9,
            27.90267, -110.93797,
            76.45, 'Alto',
            0.98, 0.84,
            0.419, 0.7,
            0.85, 0.3,
            2.02, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93692372514435, 27.900918459336733], [-110.93572904658744, 27.90259701609024], [-110.93677532768251, 27.90434617986326], [-110.93901631806148, 27.90441676387203], [-110.9402109639396, 27.90273818731937], [-110.93916465212018, 27.900989046557147], [-110.93692372514435, 27.900918459336733]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74bbffff', 9,
            27.90085, -110.93468,
            76.53, 'Alto',
            0.981, 0.846,
            0.416, 0.7,
            0.85, 0.3,
            1.88, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93363657014899, 27.899098638544935], [-110.93244185892324, 27.900777175494486], [-110.93348808177507, 27.90252637577123], [-110.93572904658744, 27.90259701609024], [-110.93692372514435, 27.900918459336733], [-110.93587747156035, 27.89916928206822], [-110.93363657014899, 27.899098638544935]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb748fffff', 9,
            27.89903, -110.9314,
            76.61, 'Alto',
            0.982, 0.851,
            0.414, 0.7,
            0.85, 0.3,
            1.83, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93034949897195, 27.897278724963517], [-110.92915475508728, 27.898957242104345], [-110.93020091969163, 27.900706478872625], [-110.93244185892324, 27.900777175494486], [-110.93363657014899, 27.899098638544935], [-110.93259037480466, 27.8973494247823], [-110.93034949897195, 27.897278724963517]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb748bffff', 9,
            27.89721, -110.92811,
            76.66, 'Alto',
            0.981, 0.856,
            0.411, 0.7,
            0.85, 0.3,
            1.87, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92706251163168, 27.89545871861204], [-110.925867735098, 27.897137215939345], [-110.9269138414506, 27.898886489187003], [-110.92915475508728, 27.898957242104345], [-110.93034949897195, 27.897278724963517], [-110.92930336187156, 27.895529474718934], [-110.92706251163168, 27.89545871861204]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74d7ffff', 9,
            27.89539, -110.92482,
            76.71, 'Alto',
            0.98, 0.861,
            0.409, 0.7,
            0.85, 0.3,
            2.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92377560814658, 27.893638619510085], [-110.92258079897383, 27.895317097019063], [-110.92362684707044, 27.897066406733924], [-110.925867735098, 27.897137215939345], [-110.92706251163168, 27.89545871861204], [-110.92601643277949, 27.89370943189769], [-110.92377560814658, 27.893638619510085]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74d3ffff', 9,
            27.89357, -110.92153,
            76.74, 'Alto',
            0.978, 0.866,
            0.407, 0.7,
            0.85, 0.3,
            2.19, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92048878853512, 27.891818427677197], [-110.91929394673318, 27.89349688536308], [-110.92033993656955, 27.895246231532955], [-110.92258079897383, 27.895317097019063], [-110.92377560814658, 27.893638619510085], [-110.92272958754685, 27.89188929633813], [-110.92048878853512, 27.891818427677197]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29a7ffff', 9,
            27.89175, -110.91825,
            76.77, 'Alto',
            0.976, 0.871,
            0.405, 0.7,
            0.85, 0.3,
            2.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91720205281568, 27.889998143132946], [-110.9160071783945, 27.891676580990953], [-110.91705310996636, 27.89342596360366], [-110.91929394673318, 27.89349688536308], [-110.92048878853512, 27.891818427677197], [-110.91944282619207, 27.890069068059823], [-110.91720205281568, 27.889998143132946]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29a3ffff', 9,
            27.88993, -110.91496,
            76.81, 'Alto',
            0.974, 0.876,
            0.403, 0.7,
            0.85, 0.3,
            2.59, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91391540100669, 27.88817776589691], [-110.91272049397618, 27.88985618392224], [-110.9137663672793, 27.891605602965626], [-110.9160071783945, 27.891676580990953], [-110.91720205281568, 27.889998143132946], [-110.91615614873359, 27.888248747082333], [-110.91391540100669, 27.88817776589691]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29bbffff', 9,
            27.88811, -110.91167,
            76.84, 'Alto',
            0.972, 0.881,
            0.402, 0.7,
            0.85, 0.3,
            2.79, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9106288331266, 27.886357295988653], [-110.90943389349665, 27.888035694176533], [-110.91047970852678, 27.889785149638396], [-110.91272049397618, 27.88985618392224], [-110.91391540100669, 27.88817776589691], [-110.9128695551898, 27.886428333425233], [-110.9106288331266, 27.886357295988653]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb298fffff', 9,
            27.88629, -110.90839,
            76.88, 'Alto',
            0.97, 0.886,
            0.401, 0.7,
            0.85, 0.3,
            2.99, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90734234919374, 27.884536733427762], [-110.90614737697435, 27.8862151117734], [-110.90719313372722, 27.887964603641564], [-110.90943389349665, 27.888035694176533], [-110.9106288331266, 27.886357295988653], [-110.90958304557914, 27.88460782710809], [-110.90734234919374, 27.884536733427762]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb298bffff', 9,
            27.88447, -110.9051,
            76.92, 'Alto',
            0.968, 0.89,
            0.401, 0.7,
            0.85, 0.3,
            3.22, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9040559492266, 27.882716078233802], [-110.90286094442763, 27.88439443673242], [-110.90390664289902, 27.886143964994698], [-110.90614737697435, 27.8862151117734], [-110.90734234919374, 27.884536733427762], [-110.90629661992001, 27.882787228150498], [-110.9040559492266, 27.882716078233802]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29d7ffff', 9,
            27.88264, -110.90182,
            76.95, 'Alto',
            0.965, 0.895,
            0.4, 0.7,
            0.85, 0.3,
            3.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90076963324356, 27.880895330426362], [-110.89957459587492, 27.882573669073178], [-110.90062023606059, 27.884323233717392], [-110.90286094442763, 27.88439443673242], [-110.9040559492266, 27.882716078233802], [-110.90301027823081, 27.88096653657202], [-110.90076963324356, 27.880895330426362]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29c3ffff', 9,
            27.88425, -110.89838,
            76.88, 'Alto',
            0.966, 0.891,
            0.4, 0.7,
            0.85, 0.3,
            3.43, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89733391323034, 27.88250240982923], [-110.89613880739275, 27.88418071835257], [-110.89718441675832, 27.885930305974178], [-110.89942516278415, 27.886001562095103], [-110.90062023606059, 27.884323233717392], [-110.89957459587492, 27.882573669073178], [-110.89733391323034, 27.88250240982923]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29cbffff', 9,
            27.88586, -110.89494,
            76.81, 'Alto',
            0.966, 0.887,
            0.4, 0.7,
            0.85, 0.3,
            3.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89389808710563, 27.88410940600277], [-110.89270291280403, 27.88578768439006], [-110.89374849133961, 27.887537294984], [-110.89598927500938, 27.88760860421837], [-110.89718441675832, 27.885930305974178], [-110.89613880739275, 27.88418071835257], [-110.89389808710563, 27.88410940600277]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2827ffff', 9,
            27.88747, -110.89151,
            76.72, 'Alto',
            0.965, 0.883,
            0.401, 0.7,
            0.85, 0.3,
            3.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89046215488926, 27.885716318926836], [-110.88926691212859, 27.887394567165455], [-110.89031245982424, 27.889144200726694], [-110.8925532811231, 27.889215563082075], [-110.89374849133961, 27.887537294984], [-110.89270291280403, 27.88578768439006], [-110.89046215488926, 27.885716318926836]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb282fffff', 9,
            27.88907, -110.88807,
            76.63, 'Alto',
            0.965, 0.878,
            0.401, 0.7,
            0.85, 0.3,
            3.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88702611660105, 27.88732314858126], [-110.88583080538623, 27.889001366658597], [-110.88687632223206, 27.890751023182073], [-110.88911718114511, 27.890822438666017], [-110.89031245982424, 27.889144200726694], [-110.88926691212859, 27.887394567165455], [-110.88702611660105, 27.88732314858126]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b93ffff', 9,
            27.89068, -110.88464,
            76.53, 'Alto',
            0.963, 0.874,
            0.402, 0.7,
            0.85, 0.3,
            3.68, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88358997226078, 27.88892989494587], [-110.88239459259677, 27.890608082849326], [-110.88344007858281, 27.89235776232999], [-110.88568097509523, 27.892429230950068], [-110.88687632223206, 27.890751023182073], [-110.88583080538623, 27.889001366658597], [-110.88358997226078, 27.88892989494587]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b9bffff', 9,
            27.89229, -110.8812,
            76.43, 'Alto',
            0.961, 0.87,
            0.404, 0.7,
            0.85, 0.3,
            3.86, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88015372188823, 27.890536558000512], [-110.87895827377999, 27.892214715717472], [-110.88000372889634, 27.893964418150272], [-110.88224466299323, 27.894035939914033], [-110.88344007858281, 27.89235776232999], [-110.88239459259677, 27.890608082849326], [-110.88015372188823, 27.890536558000512]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2bd7ffff', 9,
            27.89389, -110.87776,
            76.32, 'Alto',
            0.959, 0.865,
            0.405, 0.7,
            0.85, 0.3,
            4.07, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87671736550328, 27.892143137725014], [-110.87552184895573, 27.893821265242885], [-110.87656727319245, 27.895570990622762], [-110.87880824485894, 27.89564256553776], [-110.88000372889634, 27.893964418150272], [-110.87895827377999, 27.892214715717472], [-110.87671736550328, 27.892143137725014]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2bc3ffff', 9,
            27.8955, -110.87433,
            76.22, 'Alto',
            0.957, 0.861,
            0.407, 0.7,
            0.85, 0.3,
            4.29, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87328090312569, 27.893749634099247], [-110.87208531814379, 27.895427731405398], [-110.87313071149097, 27.897177479727297], [-110.87537172071221, 27.897249107801084], [-110.87656727319245, 27.895570990622762], [-110.87552184895573, 27.893821265242885], [-110.87328090312569, 27.893749634099247]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2bcbffff', 9,
            27.89711, -110.87089,
            76.11, 'Alto',
            0.955, 0.856,
            0.409, 0.7,
            0.85, 0.3,
            4.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86984433477531, 27.895356047103018], [-110.86864868136401, 27.89703411418486], [-110.86969404381172, 27.898783885443752], [-110.87193509057282, 27.89885556668386], [-110.87313071149097, 27.897177479727297], [-110.87208531814379, 27.895427731405398], [-110.86984433477531, 27.895356047103018]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2a27ffff', 9,
            27.89871, -110.86745,
            76.0, 'Alto',
            0.952, 0.852,
            0.412, 0.7,
            0.85, 0.3,
            4.82, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86640766047195, 27.896962376716196], [-110.86521193863618, 27.89864041356113], [-110.86625727017453, 27.900390207751933], [-110.86849835446061, 27.90046194216594], [-110.86969404381172, 27.898783885443752], [-110.86864868136401, 27.89703411418486], [-110.86640766047195, 27.896962376716196]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b5bffff', 9,
            27.90214, -110.8673,
            75.82, 'Alto',
            0.953, 0.842,
            0.412, 0.7,
            0.85, 0.3,
            4.71, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86625727017453, 27.900390207751933], [-110.86506151239541, 27.902068234227148], [-110.86610687138585, 27.903818014991334], [-110.86834801906953, 27.903889746350906], [-110.86954374436257, 27.902211700000674], [-110.86849835446061, 27.90046194216594], [-110.86625727017453, 27.900390207751933]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2b4bffff', 9,
            27.90557, -110.86715,
            75.64, 'Alto',
            0.954, 0.832,
            0.412, 0.7,
            0.85, 0.3,
            4.63, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86610687138585, 27.903818014991334], [-110.86491107766125, 27.90549603108453], [-110.86595646410521, 27.90724579841004], [-110.86819767519005, 27.907317526715403], [-110.86939343642717, 27.90563949074942], [-110.86834801906953, 27.903889746350906], [-110.86610687138585, 27.903818014991334]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0cb3ffff', 9,
            27.909, -110.867,
            75.45, 'Alto',
            0.954, 0.821,
            0.412, 0.7,
            0.85, 0.3,
            4.57, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86595646410521, 27.90724579841004], [-110.86476063443298, 27.90892380410893], [-110.86580604833189, 27.91067355798369], [-110.86804732282145, 27.910745283235087], [-110.86924312000478, 27.90906725766564], [-110.86819767519005, 27.907317526715403], [-110.86595646410521, 27.90724579841004]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0ca3ffff', 9,
            27.91242, -110.86685,
            75.24, 'Alto',
            0.955, 0.811,
            0.412, 0.7,
            0.85, 0.3,
            4.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86580604833189, 27.91067355798369], [-110.8646101827099, 27.912351553275975], [-110.86565562406518, 27.91410129368792], [-110.867896961963, 27.914173015885577], [-110.86909279509467, 27.912495000724963], [-110.86804732282145, 27.910745283235087], [-110.86580604833189, 27.91067355798369]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0cafffff', 9,
            27.91585, -110.8667,
            75.03, 'Alto',
            0.954, 0.8,
            0.412, 0.7,
            0.85, 0.3,
            4.56, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86565562406518, 27.91410129368792], [-110.8644597224913, 27.915779278561303], [-110.86550519130436, 27.917529005498377], [-110.86774659261401, 27.917600724642526], [-110.86894246169615, 27.91592271990305], [-110.867896961963, 27.914173015885577], [-110.86565562406518, 27.91410129368792]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0c37ffff', 9,
            27.91928, -110.86655,
            74.81, 'Moderado',
            0.954, 0.789,
            0.412, 0.7,
            0.85, 0.3,
            4.57, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86550519130436, 27.917529005498377], [-110.86430925377644, 27.919206979940572], [-110.86535475004871, 27.920956693390707], [-110.86759621477373, 27.921028409481572], [-110.8687921198085, 27.919350415175522], [-110.86774659261401, 27.917600724642526], [-110.86550519130436, 27.917529005498377]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0c27ffff', 9,
            27.92271, -110.8664,
            74.58, 'Moderado',
            0.954, 0.778,
            0.413, 0.7,
            0.85, 0.3,
            4.59, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86535475004871, 27.920956693390707], [-110.86415877656461, 27.922634657389416], [-110.8652043002975, 27.924384357340557], [-110.86744582844146, 27.924456070378376], [-110.86864176943098, 27.922778086518043], [-110.86759621477373, 27.921028409481572], [-110.86535475004871, 27.920956693390707]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d5bffff', 9,
            27.92613, -110.86625,
            74.35, 'Moderado',
            0.954, 0.767,
            0.413, 0.7,
            0.85, 0.3,
            4.62, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8652043002975, 27.924384357340557], [-110.8640082908551, 27.92606231088348], [-110.86505384205003, 27.927811997323566], [-110.8672954336165, 27.927883707308567], [-110.86849141056291, 27.92620573390625], [-110.86744582844146, 27.924456070378376], [-110.8652043002975, 27.924384357340557]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb0d4bffff', 9,
            27.92956, -110.8661,
            74.11, 'Moderado',
            0.953, 0.755,
            0.413, 0.7,
            0.85, 0.3,
            4.68, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86505384205003, 27.927811997323566], [-110.86385779664717, 27.92948994039842], [-110.86490337530557, 27.931239613315377], [-110.8671450302981, 27.931311320247797], [-110.86834104320354, 27.929633357315787], [-110.8672954336165, 27.927883707308567], [-110.86505384205003, 27.927811997323566]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb08b3ffff', 9,
            27.93299, -110.86595,
            73.87, 'Moderado',
            0.952, 0.744,
            0.413, 0.7,
            0.85, 0.3,
            4.77, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86490337530557, 27.931239613315377], [-110.86370729394012, 27.932917545909866], [-110.86475290006342, 27.934667205291642], [-110.86699461848556, 27.934738909171706], [-110.86819066735217, 27.933060956722297], [-110.8671450302981, 27.931311320247797], [-110.86490337530557, 27.931239613315377]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb08a3ffff', 9,
            27.93642, -110.8658,
            73.61, 'Moderado',
            0.951, 0.732,
            0.413, 0.7,
            0.85, 0.3,
            4.89, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86475290006342, 27.934667205291642], [-110.86355678273324, 27.93634512739348], [-110.86460241632284, 27.938094773228023], [-110.86684419817814, 27.938166474055972], [-110.86804028300807, 27.936488532101436], [-110.86699461848556, 27.934738909171706], [-110.86475290006342, 27.934667205291642]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb08a7ffff', 9,
            27.93824, -110.86909,
            73.51, 'Moderado',
            0.954, 0.726,
            0.411, 0.7,
            0.85, 0.3,
            4.62, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.86804028300807, 27.936488532101436], [-110.86684419817814, 27.938166474055972], [-110.86788989017053, 27.939916083428855], [-110.87013169792057, 27.93998772793986], [-110.8713277502403, 27.938309766137408], [-110.87028202732279, 27.936560179671933], [-110.86804028300807, 27.936488532101436]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb09d3ffff', 9,
            27.94006, -110.87237,
            73.4, 'Moderado',
            0.956, 0.72,
            0.408, 0.7,
            0.85, 0.3,
            4.36, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8713277502403, 27.938309766137408], [-110.87013169792057, 27.93998772793986], [-110.87117744831151, 27.94173730083891], [-110.87341928194209, 27.941808889025555], [-110.87461530174171, 27.940130907379963], [-110.87356952043343, 27.938381357390917], [-110.8713277502403, 27.938309766137408]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb09d7ffff', 9,
            27.94188, -110.87566,
            73.29, 'Moderado',
            0.959, 0.714,
            0.406, 0.7,
            0.85, 0.3,
            4.14, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87461530174171, 27.940130907379963], [-110.87341928194209, 27.941808889025555], [-110.87446509072736, 27.943558425438585], [-110.87670695022433, 27.943629957293485], [-110.87790293749389, 27.941951955809518], [-110.8768570977991, 27.94020244230908], [-110.87461530174171, 27.940130907379963]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb098bffff', 9,
            27.9437, -110.87895,
            73.18, 'Moderado',
            0.961, 0.707,
            0.405, 0.7,
            0.85, 0.3,
            3.93, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.87790293749389, 27.941951955809518], [-110.87670695022433, 27.943629957293485], [-110.87775281739965, 27.9453794572083], [-110.87999470274886, 27.94545093272402], [-110.88119065747841, 27.94377291140646], [-110.88014475940136, 27.942023434406817], [-110.87790293749389, 27.941951955809518]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb098fffff', 9,
            27.94552, -110.88224,
            73.07, 'Moderado',
            0.963, 0.701,
            0.403, 0.7,
            0.85, 0.3,
            3.75, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88119065747841, 27.94377291140646], [-110.87999470274886, 27.94545093272402], [-110.88104062831003, 27.947200396128434], [-110.88328253949727, 27.947271815297587], [-110.88447846167688, 27.945593774151206], [-110.88343250522178, 27.943844333664543], [-110.88119065747841, 27.94377291140646]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb09bbffff', 9,
            27.94734, -110.88552,
            72.95, 'Moderado',
            0.964, 0.695,
            0.402, 0.7,
            0.85, 0.3,
            3.61, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88447846167688, 27.945593774151206], [-110.88328253949727, 27.947271815297587], [-110.88432852344003, 27.949021242179438], [-110.88657046045114, 27.949092604994608], [-110.88776635007088, 27.947414544024184], [-110.88672033524199, 27.945665140062687], [-110.88447846167688, 27.945593774151206]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb09a3ffff', 9,
            27.94916, -110.88881,
            72.83, 'Moderado',
            0.965, 0.688,
            0.401, 0.7,
            0.85, 0.3,
            3.51, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.88776635007088, 27.947414544024184], [-110.88657046045114, 27.949092604994608], [-110.88761650277125, 27.950841995341694], [-110.88985846559204, 27.950913301795474], [-110.89105432264199, 27.949235221005793], [-110.89000824944353, 27.94748585358164], [-110.88776635007088, 27.947414544024184]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb09a7ffff', 9,
            27.95098, -110.8921,
            72.71, 'Moderado',
            0.965, 0.682,
            0.4, 0.7,
            0.85, 0.3,
            3.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89105432264199, 27.949235221005793], [-110.88985846559204, 27.950913301795474], [-110.89090456628527, 27.95266265559564], [-110.89314655490158, 27.95273390568063], [-110.89434237937176, 27.951055805076464], [-110.89329624780801, 27.94930647420183], [-110.89105432264199, 27.949235221005793]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb54d3ffff', 9,
            27.95281, -110.89539,
            72.58, 'Moderado',
            0.965, 0.676,
            0.4, 0.7,
            0.85, 0.3,
            3.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.89434237937176, 27.951055805076464], [-110.89314655490158, 27.95273390568063], [-110.89419271396368, 27.954483222921667], [-110.89643472836129, 27.954554416630486], [-110.8976305202418, 27.9528762962166], [-110.89658433031698, 27.951127001903675], [-110.89434237937176, 27.951055805076464]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb54d7ffff', 9,
            27.95463, -110.89868,
            72.44, 'Moderado',
            0.965, 0.669,
            0.4, 0.7,
            0.85, 0.3,
            3.51, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.8976305202418, 27.9528762962166], [-110.89643472836129, 27.954554416630486], [-110.897480945788, 27.95630369730023], [-110.89972298595276, 27.956374834625457], [-110.90091874523367, 27.954696694406653], [-110.89987249695203, 27.9529474366676], [-110.8976305202418, 27.9528762962166]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb548bffff', 9,
            27.95645, -110.90197,
            72.29, 'Moderado',
            0.964, 0.663,
            0.4, 0.7,
            0.85, 0.3,
            3.61, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90091874523367, 27.954696694406653], [-110.89972298595276, 27.956374834625457], [-110.90076926173985, 27.958124078711737], [-110.90301132765755, 27.958195159645985], [-110.90420705432892, 27.95651699962703], [-110.90316074769471, 27.95476777847403], [-110.90091874523367, 27.954696694406653]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb5483ffff', 9,
            27.95484, -110.9054,
            72.46, 'Moderado',
            0.966, 0.669,
            0.401, 0.7,
            0.85, 0.3,
            3.37, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90435643841842, 27.95308960793565], [-110.90316074769471, 27.95476777847403], [-110.90420705432892, 27.95651699962703], [-110.9064490825266, 27.95658802730339], [-110.90764474063225, 27.95490983696742], [-110.90659840316087, 27.953160638752745], [-110.90435643841842, 27.95308960793565]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb5497ffff', 9,
            27.95323, -110.90884,
            72.62, 'Moderado',
            0.968, 0.674,
            0.401, 0.7,
            0.85, 0.3,
            3.17, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90779402532246, 27.951482437907412], [-110.90659840316087, 27.953160638752745], [-110.90764474063225, 27.95490983696742], [-110.90988673109504, 27.95498081139347], [-110.91108232063006, 27.953302590753093], [-110.91003595233144, 27.951553415481776], [-110.90779402532246, 27.951482437907412]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb735bffff', 9,
            27.95162, -110.91228,
            72.79, 'Moderado',
            0.97, 0.68,
            0.402, 0.7,
            0.85, 0.3,
            2.98, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91123150592594, 27.9498751843421], [-110.91003595233144, 27.951553415481776], [-110.91108232063006, 27.953302590753093], [-110.91332427334304, 27.953373511936377], [-110.91451979430248, 27.951695261004215], [-110.91347339518659, 27.949946108681303], [-110.91123150592594, 27.9498751843421]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7353ffff', 9,
            27.95002, -110.91572,
            72.96, 'Moderado',
            0.972, 0.685,
            0.404, 0.7,
            0.85, 0.3,
            2.8, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91466888020908, 27.948267847259896], [-110.91347339518659, 27.949946108681303], [-110.91451979430248, 27.951695261004215], [-110.91676170925082, 27.951766128952315], [-110.91795716162974, 27.950087847740974], [-110.9169107317065, 27.948338718371513], [-110.91466888020908, 27.948267847259896]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb73cfffff', 9,
            27.94841, -110.91915,
            73.13, 'Moderado',
            0.974, 0.691,
            0.405, 0.7,
            0.85, 0.3,
            2.63, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91810614815205, 27.94666042668097], [-110.9169107317065, 27.948338718371513], [-110.91795716162974, 27.950087847740974], [-110.92019903879854, 27.950158662461465], [-110.92139442259203, 27.948480350983548], [-110.92034796187139, 27.94673124457258], [-110.91810614815205, 27.94666042668097]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb73c7ffff', 9,
            27.9468, -110.92259,
            73.3, 'Moderado',
            0.976, 0.697,
            0.407, 0.7,
            0.85, 0.3,
            2.45, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92154330973506, 27.94505292262554], [-110.92034796187139, 27.94673124457258], [-110.92139442259203, 27.948480350983548], [-110.92363626196644, 27.94855111248399], [-110.92483157716954, 27.946872770752126], [-110.92378508566141, 27.94512368730469], [-110.92154330973506, 27.94505292262554]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb738bffff', 9,
            27.94519, -110.92603,
            73.48, 'Moderado',
            0.977, 0.702,
            0.41, 0.7,
            0.85, 0.3,
            2.29, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92498036493828, 27.943445335113758], [-110.92378508566141, 27.94512368730469], [-110.92483157716954, 27.946872770752126], [-110.92707337873466, 27.9469434790401], [-110.92826862534245, 27.94526510706689], [-110.9272221030568, 27.94351604658803], [-110.92498036493828, 27.943445335113758]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7383ffff', 9,
            27.94359, -110.92946,
            73.65, 'Moderado',
            0.978, 0.708,
            0.412, 0.7,
            0.85, 0.3,
            2.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92841731374193, 27.941837664165806], [-110.9272221030568, 27.94351604658803], [-110.92826862534245, 27.94526510706689], [-110.93051038908345, 27.945335762149966], [-110.93170556709102, 27.94365735994803], [-110.93065901403776, 27.941908322442792], [-110.92841731374193, 27.941837664165806]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7397ffff', 9,
            27.94198, -110.9329,
            73.8, 'Moderado',
            0.978, 0.713,
            0.415, 0.7,
            0.85, 0.3,
            2.2, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93185415612622, 27.9402299098019], [-110.93065901403776, 27.941908322442792], [-110.93170556709102, 27.94365735994803], [-110.933947292993, 27.943727961833794], [-110.9351424023954, 27.942049529415737], [-110.9340958185845, 27.94030051488915], [-110.93185415612622, 27.9402299098019]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb715bffff', 9,
            27.94037, -110.93634,
            73.94, 'Moderado',
            0.977, 0.719,
            0.418, 0.7,
            0.85, 0.3,
            2.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93529089207138, 27.938622072042204], [-110.9340958185845, 27.94030051488915], [-110.9351424023954, 27.942049529415737], [-110.9373840904435, 27.94212007811176], [-110.93857913123583, 27.940441615490208], [-110.93753251667721, 27.938692623947315], [-110.93529089207138, 27.938622072042204]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7153ffff', 9,
            27.93876, -110.93977,
            74.07, 'Moderado',
            0.976, 0.724,
            0.421, 0.7,
            0.85, 0.3,
            2.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93872752155757, 27.937014150906936], [-110.93753251667721, 27.938692623947315], [-110.93857913123583, 27.940441615490208], [-110.94082078141521, 27.940512111004058], [-110.94201575359253, 27.938833618191637], [-110.94096910829614, 27.93708464963747], [-110.93872752155757, 27.937014150906936]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb71cbffff', 9,
            27.93534, -110.93992,
            74.35, 'Moderado',
            0.978, 0.736,
            0.421, 0.7,
            0.85, 0.3,
            2.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93887590349837, 27.93358666229144], [-110.93768093452783, 27.935265145738356], [-110.93872752155757, 27.937014150906936], [-110.94096910829614, 27.93708464963747], [-110.94216404456508, 27.935406146416273], [-110.94111742679968, 27.933657164238884], [-110.93887590349837, 27.93358666229144]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb71dbffff', 9,
            27.93191, -110.94007,
            74.62, 'Moderado',
            0.98, 0.748,
            0.422, 0.7,
            0.85, 0.3,
            2.01, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93902427705892, 27.930159149668064], [-110.93782934399607, 27.931837643509226], [-110.93887590349837, 27.93358666229144], [-110.94111742679968, 27.933657164238884], [-110.94231232716236, 27.93197865062121], [-110.94126573692652, 27.93022965483265], [-110.93902427705892, 27.930159149668064]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb70a7ffff', 9,
            27.92848, -110.94022,
            74.88, 'Moderado',
            0.981, 0.759,
            0.422, 0.7,
            0.85, 0.3,
            1.87, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93917264223994, 27.92673161306115], [-110.93797774508263, 27.928410117284276], [-110.93902427705892, 27.930159149668064], [-110.94126573692652, 27.93022965483265], [-110.94246060138508, 27.928551130830794], [-110.94141403867741, 27.926802121443124], [-110.93917264223994, 27.92673161306115]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb70b7ffff', 9,
            27.92505, -110.94037,
            75.13, 'Alto',
            0.982, 0.77,
            0.422, 0.7,
            0.85, 0.3,
            1.8, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93932099904214, 27.923304052495055], [-110.93812613778826, 27.924982567087852], [-110.93917264223994, 27.92673161306115], [-110.94141403867741, 27.926802121443124], [-110.94260886723399, 27.925123587069358], [-110.94156233205301, 27.92337456409465], [-110.93932099904214, 27.923304052495055]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb754fffff', 9,
            27.92163, -110.94052,
            75.35, 'Alto',
            0.982, 0.782,
            0.422, 0.7,
            0.85, 0.3,
            1.81, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93946934746621, 27.919876467994126], [-110.93827452211363, 27.921554992944298], [-110.93932099904214, 27.923304052495055], [-110.94156233205301, 27.92337456409465], [-110.94275712470974, 27.921696019361274], [-110.94171061705407, 27.91994698281157], [-110.93946934746621, 27.919876467994126]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7543ffff', 9,
            27.9182, -110.94066,
            75.57, 'Alto',
            0.982, 0.793,
            0.422, 0.7,
            0.85, 0.3,
            1.82, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9396176875129, 27.91644885958273], [-110.93842289805944, 27.91812739487798], [-110.93946934746621, 27.919876467994126], [-110.94171061705407, 27.91994698281157], [-110.94290537381309, 27.91826842773088], [-110.94185889368127, 27.916519377618243], [-110.9396176875129, 27.91644885958273]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7553ffff', 9,
            27.91477, -110.94081,
            75.79, 'Alto',
            0.982, 0.804,
            0.422, 0.7,
            0.85, 0.3,
            1.84, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93976601918287, 27.913021227285185], [-110.93857126562645, 27.914699772913238], [-110.9396176875129, 27.91644885958273], [-110.94185889368127, 27.916519377618243], [-110.94305361454471, 27.91484081220253], [-110.94200716193534, 27.913091748539014], [-110.93976601918287, 27.913021227285185]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb75cbffff', 9,
            27.91134, -110.94096,
            75.99, 'Alto',
            0.981, 0.814,
            0.422, 0.7,
            0.85, 0.3,
            1.9, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93991434247683, 27.90959357112589], [-110.9387196248153, 27.91127212707443], [-110.93976601918287, 27.913021227285185], [-110.94200716193534, 27.913091748539014], [-110.94320184690532, 27.911413172800575], [-110.94215542181698, 27.90966409559826], [-110.93991434247683, 27.90959357112589]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb75dbffff', 9,
            27.90792, -110.94111,
            76.18, 'Alto',
            0.98, 0.825,
            0.423, 0.7,
            0.85, 0.3,
            2.03, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.94006265739552, 27.90616589112916], [-110.93886797562674, 27.907844457385913], [-110.93991434247683, 27.90959357112589], [-110.94215542181698, 27.90966409559826], [-110.94335007089563, 27.907985509549373], [-110.94230367332686, 27.906236418820306], [-110.94006265739552, 27.90616589112916]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74a7ffff', 9,
            27.90449, -110.94126,
            76.35, 'Alto',
            0.978, 0.835,
            0.423, 0.7,
            0.85, 0.3,
            2.22, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.9402109639396, 27.90273818731937], [-110.93901631806148, 27.90441676387203], [-110.94006265739552, 27.90616589112916], [-110.94230367332686, 27.906236418820306], [-110.94349828651634, 27.904557822473272], [-110.94245191646574, 27.902808718229515], [-110.9402109639396, 27.90273818731937]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74b7ffff', 9,
            27.90106, -110.94141,
            76.51, 'Alto',
            0.976, 0.845,
            0.423, 0.7,
            0.85, 0.3,
            2.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.94035926210985, 27.89931045972087], [-110.93916465212018, 27.900989046557147], [-110.9402109639396, 27.90273818731937], [-110.94245191646574, 27.902808718229515], [-110.94364649376816, 27.901130111596636], [-110.9426001512343, 27.899380993850265], [-110.94035926210985, 27.89931045972087]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb74b3ffff', 9,
            27.89924, -110.93812,
            76.6, 'Alto',
            0.977, 0.85,
            0.42, 0.7,
            0.85, 0.3,
            2.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93707211422733, 27.89749071503333], [-110.93587747156035, 27.89916928206822], [-110.93692372514435, 27.900918459336733], [-110.93916465212018, 27.900989046557147], [-110.94035926210985, 27.89931045972087], [-110.93931297780361, 27.897561305465622], [-110.93707211422733, 27.89749071503333]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7487ffff', 9,
            27.89742, -110.93483,
            76.67, 'Alto',
            0.978, 0.856,
            0.417, 0.7,
            0.85, 0.3,
            2.19, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93378505013906, 27.895670877553584], [-110.93259037480466, 27.8973494247823], [-110.93363657014899, 27.899098638544935], [-110.93587747156035, 27.89916928206822], [-110.93707211422733, 27.89749071503333], [-110.93602588815298, 27.89574152428139], [-110.93378505013906, 27.895670877553584]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb7483ffff', 9,
            27.8956, -110.93154,
            76.73, 'Alto',
            0.978, 0.861,
            0.414, 0.7,
            0.85, 0.3,
            2.17, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.93049806986345, 27.8938509473012], [-110.92930336187156, 27.895529474718934], [-110.93034949897195, 27.897278724963517], [-110.93259037480466, 27.8973494247823], [-110.93378505013906, 27.895670877553584], [-110.93273888230084, 27.89392165031712], [-110.93049806986345, 27.8938509473012]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb749bffff', 9,
            27.89378, -110.92826,
            76.78, 'Alto',
            0.978, 0.866,
            0.411, 0.7,
            0.85, 0.3,
            2.24, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92721117341894, 27.892030924295703], [-110.92601643277949, 27.89370943189769], [-110.92706251163168, 27.89545871861204], [-110.92930336187156, 27.895529474718934], [-110.93049806986345, 27.8938509473012], [-110.92945196026561, 27.89210168359238], [-110.92721117341894, 27.892030924295703]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8948094da6fffff', 9,
            27.89196, -110.92497,
            76.82, 'Alto',
            0.976, 0.871,
            0.409, 0.7,
            0.85, 0.3,
            2.38, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92392436082396, 27.890210808556695], [-110.92272958754685, 27.89188929633813], [-110.92377560814658, 27.893638619510085], [-110.92601643277949, 27.89370943189769], [-110.92721117341894, 27.892030924295703], [-110.92616512206575, 27.89028162412672], [-110.92392436082396, 27.890210808556695]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8948094da6bffff', 9,
            27.89014, -110.92168,
            76.85, 'Alto',
            0.974, 0.876,
            0.407, 0.7,
            0.85, 0.3,
            2.57, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.92063763209691, 27.88839060010372], [-110.91944282619207, 27.890069068059823], [-110.92048878853512, 27.891818427677197], [-110.92272958754685, 27.89188929633813], [-110.92392436082396, 27.890210808556695], [-110.92287836771966, 27.88846147193971], [-110.92063763209691, 27.88839060010372]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29b7ffff', 9,
            27.88832, -110.9184,
            76.88, 'Alto',
            0.972, 0.88,
            0.405, 0.7,
            0.85, 0.3,
            2.77, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91735098725624, 27.886570298956343], [-110.91615614873359, 27.888248747082333], [-110.91720205281568, 27.889998143132946], [-110.91944282619207, 27.890069068059823], [-110.92063763209691, 27.88839060010372], [-110.91959169724578, 27.886641227050912], [-110.91735098725624, 27.886570298956343]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb29b3ffff', 9,
            27.8865, -110.91511,
            76.91, 'Alto',
            0.97, 0.885,
            0.404, 0.7,
            0.85, 0.3,
            2.97, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91406442632037, 27.884749905134154], [-110.9128695551898, 27.886428333425233], [-110.91391540100669, 27.88817776589691], [-110.91615614873359, 27.888248747082333], [-110.91735098725624, 27.886570298956343], [-110.91630511066252, 27.8848208894799], [-110.91406442632037, 27.884749905134154]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2987ffff', 9,
            27.88468, -110.91182,
            76.95, 'Alto',
            0.968, 0.89,
            0.402, 0.7,
            0.85, 0.3,
            3.17, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.91077794930769, 27.8829294186567], [-110.90958304557914, 27.88460782710809], [-110.9106288331266, 27.886357295988653], [-110.9128695551898, 27.886428333425233], [-110.91406442632037, 27.884749905134154], [-110.91301860798829, 27.88300045924624], [-110.91077794930769, 27.8829294186567]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2983ffff', 9,
            27.88286, -110.90854,
            76.98, 'Alto',
            0.966, 0.894,
            0.401, 0.7,
            0.85, 0.3,
            3.37, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90749155623661, 27.881108839543582], [-110.90629661992001, 27.882787228150498], [-110.90734234919374, 27.884536733427762], [-110.90958304557914, 27.88460782710809], [-110.91077794930769, 27.8829294186567], [-110.90973218924151, 27.881179936369513], [-110.90749155623661, 27.881108839543582]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb299bffff', 9,
            27.88104, -110.90525,
            77.02, 'Alto',
            0.964, 0.899,
            0.401, 0.7,
            0.85, 0.3,
            3.6, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90420524712556, 27.879288167814366], [-110.90301027823081, 27.88096653657202], [-110.9040559492266, 27.882716078233802], [-110.90629661992001, 27.882787228150498], [-110.90749155623661, 27.881108839543582], [-110.90644585444056, 27.87935932086928], [-110.90420524712556, 27.879288167814366]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '89480bb2d6fffff', 9,
            27.87922, -110.90196,
            77.05, 'Alto',
            0.961, 0.903,
            0.4, 0.7,
            0.85, 0.3,
            3.86, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-110.90091902199293, 27.877467403488637], [-110.89972402052993, 27.87914575239225], [-110.90076963324356, 27.880895330426362], [-110.90301027823081, 27.88096653657202], [-110.90420524712556, 27.879288167814366], [-110.90315960360391, 27.877538612765154], [-110.90091902199293, 27.877467403488637]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;