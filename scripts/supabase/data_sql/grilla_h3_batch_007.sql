INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92d5fffff', 8,
            30.52103, -113.97011,
            50.42, 'Moderado',
            0.0, 0.49,
            0.458, 0.7,
            0.85, 0.3,
            156.54, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.969063586555, 30.51593661313423], [-113.96444525095053, 30.519304541253838], [-113.965488025231, 30.52440265686118], [-113.97114953530685, 30.52613272264338], [-113.97576786119046, 30.52276462904017], [-113.97472468675008, 30.51766663515301], [-113.969063586555, 30.51593661313423]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92d7fffff', 8,
            30.52786, -113.97681,
            49.85, 'Bajo',
            0.0, 0.469,
            0.448, 0.7,
            0.85, 0.3,
            157.54, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97576786119046, 30.52276462904017], [-113.97114953530685, 30.52613272264338], [-113.97219264041533, 30.5312306015572], [-113.9778544715777, 30.53296026509055], [-113.98247278759025, 30.529592006034413], [-113.9814292823425, 30.5244942489125], [-113.97576786119046, 30.52276462904017]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9299fffff', 8,
            30.53469, -113.98352,
            49.3, 'Bajo',
            0.0, 0.449,
            0.439, 0.7,
            0.85, 0.3,
            158.54, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98247278759025, 30.529592006034413], [-113.9778544715777, 30.53296026509055], [-113.978897907545, 30.538057907090256], [-113.98456005967448, 30.539787168184823], [-113.98917836566572, 30.53641874370645], [-113.98813452957984, 30.53132122357036], [-113.98247278759025, 30.529592006034413]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512da5fffff', 8,
            30.53305, -113.9938,
            49.21, 'Bajo',
            0.0, 0.454,
            0.426, 0.7,
            0.85, 0.3,
            159.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9927523561659, 30.52795264043325], [-113.98813452957984, 30.53132122357036], [-113.98917836566572, 30.53641874370645], [-113.9948404283734, 30.538147558716144], [-113.99945824470981, 30.53477881014103], [-113.99841400861926, 30.529681412008838], [-113.9927523561659, 30.52795264043325]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512da1fffff', 8,
            30.53141, -114.00408,
            49.15, 'Bajo',
            0.0, 0.458,
            0.416, 0.7,
            0.85, 0.3,
            160.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00303134552937, 30.52631250496807], [-113.99841400861926, 30.529681412008838], [-113.99945824470981, 30.53477881014103], [-114.0051202176322, 30.536507179102994], [-114.00973754406441, 30.533138106608554], [-114.00869290808318, 30.528040830620448], [-114.00303134552937, 30.52631250496807]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dabfffff', 8,
            30.52977, -114.01435,
            49.13, 'Bajo',
            0.0, 0.463,
            0.408, 0.7,
            0.85, 0.3,
            161.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01330975506801, 30.524671599853445], [-114.00869290808318, 30.528040830620448], [-114.00973754406441, 30.533138106608554], [-114.01539942683816, 30.534866029560007], [-114.02001626311687, 30.53149663332368], [-114.01897122735903, 30.52639947961983], [-114.01330975506801, 30.524671599853445]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d87fffff', 8,
            30.52813, -114.02463,
            49.15, 'Bajo',
            0.0, 0.468,
            0.403, 0.7,
            0.85, 0.3,
            162.34, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0235875841694, 30.523029925304044], [-114.01897122735903, 30.52639947961983], [-114.02001626311687, 30.53149663332368], [-114.02567805537872, 30.53322411030192], [-114.03029440125479, 30.529854390501242], [-114.02924896583443, 30.524757359221816], [-114.0235875841694, 30.523029925304044]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d81fffff', 8,
            30.51966, -114.0282,
            49.65, 'Bajo',
            0.0, 0.494,
            0.402, 0.7,
            0.85, 0.3,
            162.31, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02715835690276, 30.514562944596474], [-114.0225424795038, 30.517932656752198], [-114.0235875841694, 30.523029925304044], [-114.02924896583443, 30.524757359221816], [-114.03386483222133, 30.52138748153478], [-114.03281932798636, 30.51629033547588], [-114.02715835690276, 30.514562944596474]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d89fffff', 8,
            30.51119, -114.03177,
            50.18, 'Moderado',
            0.0, 0.521,
            0.401, 0.7,
            0.85, 0.3,
            162.27, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03072858141552, 30.50609569165795], [-114.026113183371, 30.509465561414054], [-114.02715835690276, 30.514562944596474], [-114.03281932798636, 30.51629033547588], [-114.03743471494104, 30.512920300142028], [-114.03638914193307, 30.507823039521103], [-114.03072858141552, 30.50609569165795]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dc3fffff', 8,
            30.50273, -114.03534,
            50.73, 'Moderado',
            0.0, 0.549,
            0.4, 0.7,
            0.85, 0.3,
            162.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03429825780616, 30.49762816694551], [-114.02968333905915, 30.500998194062436], [-114.03072858141552, 30.50609569165795], [-114.03638914193307, 30.507823039521103], [-114.04100404951251, 30.504452846779994], [-114.03995840777309, 30.49935547181451], [-114.03429825780616, 30.49762816694551]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dcbfffff', 8,
            30.49426, -114.03891,
            51.3, 'Moderado',
            0.0, 0.578,
            0.4, 0.7,
            0.85, 0.3,
            162.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03786738617323, 30.48916037091626], [-114.03325294666678, 30.4925305551544], [-114.03429825780616, 30.49762816694551], [-114.03995840777309, 30.49935547181451], [-114.04457283603429, 30.495985121905726], [-114.04352712560494, 30.490887632813173], [-114.03786738617323, 30.48916037091626]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dc9fffff', 8,
            30.48743, -114.03221,
            51.79, 'Moderado',
            0.0, 0.601,
            0.401, 0.7,
            0.85, 0.3,
            161.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03116258618495, 30.48233498097444], [-114.02654813558348, 30.485704999510972], [-114.02759311615337, 30.490802847907148], [-114.03325294666678, 30.4925305551544], [-114.03786738617323, 30.48916037091626], [-114.03682200629237, 30.484062645147063], [-114.03116258618495, 30.48233498097444]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c27fffff', 8,
            30.48061, -114.0255,
            52.29, 'Moderado',
            0.0, 0.625,
            0.403, 0.7,
            0.85, 0.3,
            160.26, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02445843615855, 30.475508952490582], [-114.01984397461229, 30.478878805294585], [-114.02088862464322, 30.483976890075184], [-114.02654813558348, 30.485704999510972], [-114.03116258618495, 30.48233498097444], [-114.03011753682205, 30.47723701874922], [-114.02445843615855, 30.475508952490582]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c25fffff', 8,
            30.47378, -114.0188,
            52.81, 'Moderado',
            0.0, 0.649,
            0.405, 0.7,
            0.85, 0.3,
            159.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01775493618311, 30.468682285875122], [-114.01314046384215, 30.47205197291569], [-114.01418478336478, 30.477150293860007], [-114.01984397461229, 30.478878805294585], [-114.02445843615855, 30.475508952490582], [-114.02341371728306, 30.470410754030006], [-114.01775493618311, 30.468682285875122]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d53fffff', 8,
            30.46695, -114.0121,
            53.35, 'Moderado',
            0.0, 0.673,
            0.41, 0.7,
            0.85, 0.3,
            158.3, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01105208634755, 30.46185498153861], [-114.00643760336204, 30.465224502784878], [-114.00748159240696, 30.47032305967216], [-114.01314046384215, 30.47205197291569], [-114.01775493618311, 30.468682285875122], [-114.01671054776445, 30.4635838513999], [-114.01105208634755, 30.46185498153861]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d51fffff', 8,
            30.46013, -114.00539,
            53.9, 'Moderado',
            0.0, 0.696,
            0.415, 0.7,
            0.85, 0.3,
            157.31, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00434988674075, 30.45502703989177], [-113.99973539326075, 30.45839639531286], [-114.00077905185861, 30.4634951879223], [-114.00643760336204, 30.465224502784878], [-114.01105208634755, 30.46185498153861], [-114.01000802835512, 30.456756311269555], [-114.00434988674075, 30.45502703989177]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d55fffff', 8,
            30.46177, -113.99512,
            53.93, 'Moderado',
            0.0, 0.691,
            0.425, 0.7,
            0.85, 0.3,
            156.34, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99407716180848, 30.456666679021218], [-113.98946217921004, 30.46003571174431], [-113.99050543829955, 30.46513462655387], [-113.99616407952682, 30.466864386454823], [-114.00077905185861, 30.4634951879223], [-113.99973539326075, 30.45839639531286], [-113.99407716180848, 30.456666679021218]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d09fffff', 8,
            30.4634, -113.98485,
            54.0, 'Moderado',
            0.0, 0.685,
            0.437, 0.7,
            0.85, 0.3,
            155.36, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98380385828256, 30.458305550501805], [-113.97918838681467, 30.46167426034964], [-113.98023124628209, 30.466773297218992], [-113.98588997687042, 30.46850350219534], [-113.99050543829955, 30.46513462655387], [-113.98946217921004, 30.46003571174431], [-113.98380385828256, 30.458305550501805]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d0dfffff', 8,
            30.46504, -113.97457,
            54.11, 'Moderado',
            0.0, 0.679,
            0.451, 0.7,
            0.85, 0.3,
            154.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9735299767747, 30.45994365411935], [-113.9689140166865, 30.463312040914726], [-113.96995647641815, 30.468411199703556], [-113.9756152960047, 30.470141849792164], [-113.98023124628209, 30.466773297218992], [-113.97918838681467, 30.46167426034964], [-113.9735299767747, 30.45994365411935]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d63fffff', 8,
            30.46668, -113.9643,
            54.24, 'Moderado',
            0.0, 0.674,
            0.468, 0.7,
            0.85, 0.3,
            153.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.96325551789687, 30.461580989659836], [-113.95863906943762, 30.464949053225624], [-113.95968112931992, 30.470048333793557], [-113.96534003754176, 30.47177942903123], [-113.96995647641815, 30.468411199703556], [-113.9689140166865, 30.463312040914726], [-113.96325551789687, 30.461580989659836]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d29fffff', 8,
            30.47515, -113.96072,
            53.74, 'Moderado',
            0.0, 0.644,
            0.474, 0.7,
            0.85, 0.3,
            153.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95968112931992, 30.470048333793557], [-113.95506420209384, 30.47341623969861], [-113.9561061925635, 30.47851540654194], [-113.96176551023255, 30.480246545784333], [-113.9663824279538, 30.476878474164035], [-113.96534003754176, 30.47177942903123], [-113.95968112931992, 30.470048333793557]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d21fffff', 8,
            30.48361, -113.95715,
            53.25, 'Moderado',
            0.0, 0.614,
            0.481, 0.7,
            0.85, 0.3,
            153.47, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9561061925635, 30.47851540654194], [-113.95148878651402, 30.48188315454661], [-113.95253070752936, 30.48698220744767], [-113.95819043466061, 30.488713390716747], [-113.96280783128336, 30.485345477043435], [-113.96176551023255, 30.480246545784333], [-113.9561061925635, 30.47851540654194]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d27fffff', 8,
            30.49208, -113.95357,
            52.76, 'Moderado',
            0.0, 0.585,
            0.487, 0.7,
            0.85, 0.3,
            153.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95253070752936, 30.48698220744767], [-113.94791282259985, 30.490349797312312], [-113.94895467411925, 30.49544873605345], [-113.95461481072763, 30.497179963371206], [-113.95923268630854, 30.493812207884503], [-113.95819043466061, 30.488713390716747], [-113.95253070752936, 30.48698220744767]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92cdfffff', 8,
            30.50055, -113.95,
            52.29, 'Moderado',
            0.0, 0.556,
            0.494, 0.7,
            0.85, 0.3,
            153.54, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94895467411925, 30.49544873605345], [-113.94433631025308, 30.49881616753849], [-113.94537809223482, 30.5039149919021], [-113.95103863833528, 30.505646263290537], [-113.95565699293098, 30.502278666230023], [-113.95461481072763, 30.497179963371206], [-113.94895467411925, 30.49544873605345]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92c5fffff', 8,
            30.50901, -113.94642,
            51.83, 'Moderado',
            0.0, 0.528,
            0.501, 0.7,
            0.85, 0.3,
            153.59, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94537809223482, 30.5039149919021], [-113.9407592493754, 30.507282264767927], [-113.9418009617778, 30.512380974536445], [-113.94746191738523, 30.514112290017547], [-113.95208075105236, 30.51074485162281], [-113.95103863833528, 30.505646263290537], [-113.94537809223482, 30.5039149919021]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92c7fffff', 8,
            30.51584, -113.95312,
            51.19, 'Moderado',
            0.0, 0.506,
            0.488, 0.7,
            0.85, 0.3,
            154.59, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95208075105236, 30.51074485162281], [-113.94746191738523, 30.514112290017547], [-113.94850396057437, 30.51921076360577], [-113.9541652377558, 30.520941677305853], [-113.95878406208054, 30.517574073412803], [-113.95774161859721, 30.512475721332628], [-113.95208075105236, 30.51074485162281]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9289fffff', 8,
            30.52267, -113.95983,
            50.58, 'Moderado',
            0.0, 0.485,
            0.476, 0.7,
            0.85, 0.3,
            155.59, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95878406208054, 30.517574073412803], [-113.9541652377558, 30.520941677305853], [-113.9552076117626, 30.52603991449304], [-113.96086921039881, 30.527770426221963], [-113.965488025231, 30.52440265686118], [-113.96444525095053, 30.519304541253838], [-113.95878406208054, 30.517574073412803]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e928bfffff', 8,
            30.5295, -113.96653,
            49.99, 'Bajo',
            0.0, 0.464,
            0.464, 0.7,
            0.85, 0.3,
            156.6, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.965488025231, 30.52440265686118], [-113.96086921039881, 30.527770426221963], [-113.96191191525419, 30.5328684267874], [-113.96757383522585, 30.534598536355087], [-113.97219264041533, 30.5312306015572], [-113.97114953530685, 30.52613272264338], [-113.965488025231, 30.52440265686118]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e929dfffff', 8,
            30.53633, -113.97324,
            49.43, 'Bajo',
            0.0, 0.444,
            0.453, 0.7,
            0.85, 0.3,
            157.6, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97219264041533, 30.5312306015572], [-113.96757383522585, 30.534598536355087], [-113.9686168709607, 30.539696300078138], [-113.9742791121485, 30.541426007294593], [-113.978897907545, 30.538057907090256], [-113.9778544715777, 30.53296026509055], [-113.97219264041533, 30.5312306015572]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9291fffff', 8,
            30.54316, -113.97994,
            48.91, 'Bajo',
            0.0, 0.425,
            0.443, 0.7,
            0.85, 0.3,
            158.6, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.978897907545, 30.538057907090256], [-113.9742791121485, 30.541426007294593], [-113.97532247879366, 30.54652353395468], [-113.98098504107817, 30.54825283862999], [-113.98560382653145, 30.54488457304984], [-113.98456005967448, 30.539787168184823], [-113.978897907545, 30.538057907090256]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e929bfffff', 8,
            30.54152, -113.99022,
            48.8, 'Bajo',
            0.0, 0.43,
            0.43, 0.7,
            0.85, 0.3,
            159.54, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98917836566572, 30.53641874370645], [-113.98456005967448, 30.539787168184823], [-113.98560382653145, 30.54488457304984], [-113.99126629950855, 30.546613431515784], [-113.99588459532819, 30.54324484164584], [-113.9948404283734, 30.538147558716144], [-113.98917836566572, 30.53641874370645]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512da7fffff', 8,
            30.53988, -114.0005,
            48.72, 'Bajo',
            0.0, 0.434,
            0.419, 0.7,
            0.85, 0.3,
            160.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99945824470981, 30.53477881014103], [-113.9948404283734, 30.538147558716144], [-113.99588459532819, 30.54324484164584], [-114.00154697863437, 30.544973253939517], [-114.00616478457087, 30.541604339957164], [-114.0051202176322, 30.536507179102994], [-113.99945824470981, 30.53477881014103]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512da3fffff', 8,
            30.53824, -114.01078,
            48.68, 'Bajo',
            0.0, 0.439,
            0.41, 0.7,
            0.85, 0.3,
            161.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00973754406441, 30.533138106608554], [-114.0051202176322, 30.536507179102994], [-114.00616478457087, 30.541604339957164], [-114.01182707784265, 30.543332306115772], [-114.01644439364665, 30.539963068198436], [-114.01539942683816, 30.534866029560007], [-114.00973754406441, 30.533138106608554]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dbdfffff', 8,
            30.53659, -114.02106,
            48.68, 'Bajo',
            0.0, 0.443,
            0.404, 0.7,
            0.85, 0.3,
            162.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02001626311687, 30.53149663332368], [-114.01539942683816, 30.534866029560007], [-114.01644439364665, 30.539963068198436], [-114.02210659652064, 30.5416905882593], [-114.02672342194289, 30.538321026584498], [-114.02567805537872, 30.53322411030192], [-114.02001626311687, 30.53149663332368]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512db9fffff', 8,
            30.53495, -114.03134,
            48.72, 'Bajo',
            0.0, 0.448,
            0.401, 0.7,
            0.85, 0.3,
            163.34, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03029440125479, 30.529854390501242], [-114.02567805537872, 30.53322411030192], [-114.02672342194289, 30.538321026584498], [-114.03238553405582, 30.540048100584993], [-114.03700186884723, 30.53667821533029], [-114.03595610264152, 30.53158142154371], [-114.03029440125479, 30.529854390501242]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d83fffff', 8,
            30.52648, -114.03491,
            49.21, 'Bajo',
            0.0, 0.473,
            0.4, 0.7,
            0.85, 0.3,
            163.3, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03386483222133, 30.52138748153478], [-114.02924896583443, 30.524757359221816], [-114.03029440125479, 30.529854390501242], [-114.03595610264152, 30.53158142154371], [-114.04057195786598, 30.528211378356257], [-114.03952612289726, 30.52311446964135], [-114.03386483222133, 30.52138748153478]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d8bfffff', 8,
            30.51802, -114.03848,
            49.73, 'Bajo',
            0.0, 0.499,
            0.4, 0.7,
            0.85, 0.3,
            163.27, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03743471494104, 30.512920300142028], [-114.03281932798636, 30.51629033547588], [-114.03386483222133, 30.52138748153478], [-114.03952612289726, 30.52311446964135], [-114.04414149861178, 30.519744268760665], [-114.04309559492164, 30.514647245334835], [-114.03743471494104, 30.512920300142028]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dd5fffff', 8,
            30.50955, -114.04205,
            50.28, 'Moderado',
            0.0, 0.526,
            0.4, 0.7,
            0.85, 0.3,
            163.24, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04100404951251, 30.504452846779994], [-114.03638914193307, 30.507823039521103], [-114.03743471494104, 30.512920300142028], [-114.04309559492164, 30.514647245334835], [-114.04771049118322, 30.511276887000466], [-114.0466645188132, 30.506179749081145], [-114.04100404951251, 30.504452846779994]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dddfffff', 8,
            30.50108, -114.04562,
            50.85, 'Moderado',
            0.0, 0.555,
            0.4, 0.7,
            0.85, 0.3,
            163.22, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04457283603429, 30.495985121905726], [-114.03995840777309, 30.49935547181451], [-114.04100404951251, 30.504452846779994], [-114.0466645188132, 30.506179749081145], [-114.0512789356789, 30.502809233532666], [-114.05023289467053, 30.497711981337297], [-114.04457283603429, 30.495985121905726]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c37fffff', 8,
            30.49261, -114.04919,
            51.43, 'Moderado',
            0.0, 0.583,
            0.401, 0.7,
            0.85, 0.3,
            163.2, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04814107460489, 30.487517125976304], [-114.04352712560494, 30.490887632813173], [-114.04457283603429, 30.495985121905726], [-114.05023289467053, 30.497711981337297], [-114.05484683219733, 30.4943413088143], [-114.05380072259216, 30.489243942560403], [-114.04814107460489, 30.487517125976304]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c35fffff', 8,
            30.48579, -114.04248,
            51.89, 'Moderado',
            0.0, 0.607,
            0.4, 0.7,
            0.85, 0.3,
            162.22, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04143596661521, 30.480692304027322], [-114.03682200629237, 30.484062645147063], [-114.03786738617323, 30.48916037091626], [-114.04352712560494, 30.490887632813173], [-114.04814107460489, 30.487517125976304], [-114.04709529552713, 30.482419522974215], [-114.04143596661521, 30.480692304027322]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c23fffff', 8,
            30.47896, -114.03578,
            52.37, 'Moderado',
            0.0, 0.631,
            0.4, 0.7,
            0.85, 0.3,
            161.24, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03473150831758, 30.47386684337758], [-114.03011753682205, 30.47723701874922], [-114.03116258618495, 30.48233498097444], [-114.03682200629237, 30.484062645147063], [-114.04143596661521, 30.480692304027322], [-114.0403905180344, 30.47559446449763], [-114.03473150831758, 30.47386684337758]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c21fffff', 8,
            30.47214, -114.02907,
            52.86, 'Moderado',
            0.0, 0.655,
            0.401, 0.7,
            0.85, 0.3,
            160.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0280276998011, 30.467040744437398], [-114.02341371728306, 30.470410754030006], [-114.02445843615855, 30.475508952490582], [-114.03011753682205, 30.47723701874922], [-114.03473150831758, 30.47386684337758], [-114.03368639020319, 30.468768767540922], [-114.0280276998011, 30.467040744437398]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c2dfffff', 8,
            30.46531, -114.02237,
            53.38, 'Moderado',
            0.0, 0.678,
            0.404, 0.7,
            0.85, 0.3,
            159.27, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02132454115488, 30.460214007617278], [-114.01671054776445, 30.4635838513999], [-114.01775493618311, 30.468682285875122], [-114.02341371728306, 30.470410754030006], [-114.0280276998011, 30.467040744437398], [-114.02698291212262, 30.46194243251448], [-114.02132454115488, 30.460214007617278]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d5bfffff', 8,
            30.45849, -114.01567,
            53.9, 'Moderado',
            0.0, 0.702,
            0.407, 0.7,
            0.85, 0.3,
            158.29, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01462203246786, 30.45338663332783], [-114.01000802835512, 30.456756311269555], [-114.01105208634755, 30.46185498153861], [-114.01671054776445, 30.4635838513999], [-114.02132454115488, 30.460214007617278], [-114.02028008388173, 30.455115459828843], [-114.01462203246786, 30.45338663332783]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d59fffff', 8,
            30.45166, -114.00896,
            54.44, 'Moderado',
            0.0, 0.726,
            0.412, 0.7,
            0.85, 0.3,
            157.32, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00792017382894, 30.446558621979744], [-114.00330615914395, 30.449928134049703], [-114.00434988674075, 30.45502703989177], [-114.01000802835512, 30.456756311269555], [-114.01462203246786, 30.45338663332783], [-114.01357790556948, 30.448287849894683], [-114.00792017382894, 30.446558621979744]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d5dfffff', 8,
            30.4533, -113.99869,
            54.46, 'Moderado',
            0.0, 0.72,
            0.421, 0.7,
            0.85, 0.3,
            156.33, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99764833745151, 30.44819846134543], [-113.99303383362702, 30.45156765091048], [-113.99407716180848, 30.456666679021218], [-113.99973539326075, 30.45839639531286], [-114.00434988674075, 30.45502703989177], [-114.00330615914395, 30.449928134049703], [-113.99764833745151, 30.44819846134543]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d43fffff', 8,
            30.45494, -113.98842,
            54.52, 'Moderado',
            0.0, 0.714,
            0.432, 0.7,
            0.85, 0.3,
            155.35, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98737592234527, 30.44983753337984], [-113.98276092963017, 30.453206400262694], [-113.98380385828256, 30.458305550501805], [-113.98946217921004, 30.46003571174431], [-113.99407716180848, 30.456666679021218], [-113.99303383362702, 30.45156765091048], [-113.98737592234527, 30.44983753337984]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d47fffff', 8,
            30.45658, -113.97815,
            54.62, 'Moderado',
            0.0, 0.709,
            0.446, 0.7,
            0.85, 0.3,
            154.38, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97710292912173, 30.451475837868756], [-113.97248744776508, 30.454844381892197], [-113.9735299767747, 30.45994365411935], [-113.97918838681467, 30.46167426034964], [-113.98380385828256, 30.458305550501805], [-113.98276092963017, 30.453206400262694], [-113.97710292912173, 30.451475837868756]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d6bfffff', 8,
            30.45821, -113.96787,
            54.74, 'Moderado',
            0.0, 0.703,
            0.462, 0.7,
            0.85, 0.3,
            153.4, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.96682935839267, 30.453113374598136], [-113.96221338864362, 30.456481595585018], [-113.96325551789687, 30.461580989659836], [-113.9689140166865, 30.463312040914726], [-113.9735299767747, 30.45994365411935], [-113.97248744776508, 30.454844381892197], [-113.96682935839267, 30.453113374598136]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d61fffff', 8,
            30.45985, -113.9576,
            54.9, 'Moderado',
            0.0, 0.697,
            0.48, 0.7,
            0.85, 0.3,
            152.43, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95655521077008, 30.454750143354087], [-113.95193875287791, 30.458118041127342], [-113.95298048226125, 30.463217556909424], [-113.95863906943762, 30.464949053225624], [-113.96325551789687, 30.461580989659836], [-113.96221338864362, 30.456481595585018], [-113.95655521077008, 30.454750143354087]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d67fffff', 8,
            30.46832, -113.95402,
            54.41, 'Moderado',
            0.0, 0.668,
            0.486, 0.7,
            0.85, 0.3,
            152.45, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95298048226125, 30.463217556909424], [-113.94836354568035, 30.466585297068573], [-113.94940520559972, 30.471684699275194], [-113.95506420209384, 30.47341623969861], [-113.95968112931992, 30.470048333793557], [-113.95863906943762, 30.464949053225624], [-113.95298048226125, 30.463217556909424]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d2dfffff', 8,
            30.47678, -113.95045,
            53.92, 'Moderado',
            0.0, 0.638,
            0.493, 0.7,
            0.85, 0.3,
            152.48, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94940520559972, 30.471684699275194], [-113.94478779027348, 30.47505228158057], [-113.94582938068717, 30.48015156999402], [-113.95148878651402, 30.48188315454661], [-113.9561061925635, 30.47851540654194], [-113.95506420209384, 30.47341623969861], [-113.94940520559972, 30.471684699275194]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d25fffff', 8,
            30.48525, -113.94687,
            53.43, 'Moderado',
            0.0, 0.609,
            0.5, 0.7,
            0.85, 0.3,
            152.51, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94582938068717, 30.48015156999402], [-113.94121148655904, 30.483518994206012], [-113.9422530074254, 30.488618168608607], [-113.94791282259985, 30.490349797312312], [-113.95253070752936, 30.48698220744767], [-113.95148878651402, 30.48188315454661], [-113.94582938068717, 30.48015156999402]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e921bfffff', 8,
            30.49372, -113.94329,
            52.96, 'Moderado',
            0.0, 0.58,
            0.508, 0.7,
            0.85, 0.3,
            152.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9422530074254, 30.488618168608607], [-113.93763463443881, 30.491985434487585], [-113.93867608571614, 30.497084494661678], [-113.94433631025308, 30.49881616753849], [-113.94895467411925, 30.49544873605345], [-113.94791282259985, 30.490349797312312], [-113.9422530074254, 30.488618168608607]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9213fffff', 8,
            30.50218, -113.93972,
            52.49, 'Moderado',
            0.0, 0.551,
            0.515, 0.7,
            0.85, 0.3,
            152.59, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93867608571614, 30.497084494661678], [-113.9340572338145, 30.500451601968027], [-113.93509861546109, 30.50555054769601], [-113.9407592493754, 30.507282264767927], [-113.94537809223482, 30.5039149919021], [-113.94433631025308, 30.49881616753849], [-113.93867608571614, 30.497084494661678]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92e9fffff', 8,
            30.51065, -113.93614,
            52.05, 'Moderado',
            0.0, 0.523,
            0.523, 0.7,
            0.85, 0.3,
            152.65, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93509861546109, 30.50555054769601], [-113.93047928458783, 30.50891749619018], [-113.93152059656195, 30.514016327254485], [-113.93718163986851, 30.515748088543496], [-113.9418009617778, 30.512380974536445], [-113.9407592493754, 30.507282264767927], [-113.93509861546109, 30.50555054769601]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92ebfffff', 8,
            30.51748, -113.94284,
            51.4, 'Moderado',
            0.0, 0.501,
            0.509, 0.7,
            0.85, 0.3,
            153.65, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9418009617778, 30.512380974536445], [-113.93718163986851, 30.515748088543496], [-113.93822328264982, 30.52084668349936], [-113.94388464777916, 30.522578043095187], [-113.94850396057437, 30.51921076360577], [-113.94746191738523, 30.514112290017547], [-113.9418009617778, 30.512380974536445]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e928dfffff', 8,
            30.52431, -113.94955,
            50.77, 'Moderado',
            0.0, 0.48,
            0.495, 0.7,
            0.85, 0.3,
            154.65, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94850396057437, 30.51921076360577], [-113.94388464777916, 30.522578043095187], [-113.94492662139862, 30.527676401721816], [-113.95058830823159, 30.52940735943424], [-113.9552076117626, 30.52603991449304], [-113.9541652377558, 30.520941677305853], [-113.94850396057437, 30.51921076360577]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9281fffff', 8,
            30.53114, -113.95625,
            50.17, 'Moderado',
            0.0, 0.459,
            0.482, 0.7,
            0.85, 0.3,
            155.65, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9552076117626, 30.52603991449304], [-113.95058830823159, 30.52940735943424], [-113.95163061272015, 30.534505481510934], [-113.95729262113754, 30.536236037149813], [-113.96191191525419, 30.5328684267874], [-113.96086921039881, 30.527770426221963], [-113.9552076117626, 30.52603991449304]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9283fffff', 8,
            30.53797, -113.96295,
            49.59, 'Bajo',
            0.0, 0.44,
            0.47, 0.7,
            0.85, 0.3,
            156.66, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.96191191525419, 30.5328684267874], [-113.95729262113754, 30.536236037149813], [-113.95833525652611, 30.541333922455905], [-113.96399758640862, 30.543064075831186], [-113.9686168709607, 30.539696300078138], [-113.96757383522585, 30.534598536355087], [-113.96191191525419, 30.5328684267874]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9295fffff', 8,
            30.54479, -113.96966,
            49.05, 'Bajo',
            0.0, 0.421,
            0.459, 0.7,
            0.85, 0.3,
            157.66, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9686168709607, 30.539696300078138], [-113.96399758640862, 30.543064075831186], [-113.96504055272815, 30.548161724146052], [-113.97070320395643, 30.549891475067724], [-113.97532247879366, 30.54652353395468], [-113.9742791121485, 30.541426007294593], [-113.9686168709607, 30.539696300078138]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9297fffff', 8,
            30.55162, -113.97637,
            48.55, 'Bajo',
            0.0, 0.403,
            0.449, 0.7,
            0.85, 0.3,
            158.67, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97532247879366, 30.54652353395468], [-113.97070320395643, 30.549891475067724], [-113.97174650123777, 30.554988886170825], [-113.9774094736924, 30.556718234448997], [-113.98202873866451, 30.553350128006578], [-113.98098504107817, 30.54825283862999], [-113.97532247879366, 30.54652353395468]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9293fffff', 8,
            30.54998, -113.98665,
            48.42, 'Bajo',
            0.0, 0.408,
            0.435, 0.7,
            0.85, 0.3,
            159.61, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98560382653145, 30.54488457304984], [-113.98098504107817, 30.54825283862999], [-113.98202873866451, 30.553350128006578], [-113.98769162192623, 30.55507902995088], [-113.99231039728596, 30.5517105990256], [-113.99126629950855, 30.546613431515784], [-113.98560382653145, 30.54488457304984]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e974dfffff', 8,
            30.54834, -113.99693,
            48.32, 'Bajo',
            0.0, 0.412,
            0.423, 0.7,
            0.85, 0.3,
            160.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99588459532819, 30.54324484164584], [-113.99126629950855, 30.546613431515784], [-113.99231039728596, 30.5517105990256], [-113.99797319099113, 30.55343905467313], [-114.00259147648883, 30.550070299442353], [-114.00154697863437, 30.544973253939517], [-113.99588459532819, 30.54324484164584]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9749fffff', 8,
            30.5467, -114.00721,
            48.27, 'Bajo',
            0.0, 0.416,
            0.413, 0.7,
            0.85, 0.3,
            161.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00616478457087, 30.541604339957164], [-114.00154697863437, 30.544973253939517], [-114.00259147648883, 30.550070299442353], [-114.00825418027391, 30.551798308830282], [-114.01287197566013, 30.54842922947144], [-114.01182707784265, 30.543332306115772], [-114.00616478457087, 30.541604339957164]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512db5fffff', 8,
            30.54506, -114.01749,
            48.25, 'Bajo',
            0.0, 0.42,
            0.406, 0.7,
            0.85, 0.3,
            162.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01644439364665, 30.539963068198436], [-114.01182707784265, 30.543332306115772], [-114.01287197566013, 30.54842922947144], [-114.01853458916162, 30.550156792637065], [-114.02315189418704, 30.546787389327633], [-114.02210659652064, 30.5416905882593], [-114.01644439364665, 30.539963068198436]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512db1fffff', 8,
            30.54342, -114.02777,
            48.27, 'Bajo',
            0.0, 0.425,
            0.402, 0.7,
            0.85, 0.3,
            163.38, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02672342194289, 30.538321026584498], [-114.02210659652064, 30.5416905882593], [-114.02315189418704, 30.546787389327633], [-114.02881441704154, 30.548514506308326], [-114.03343123145694, 30.545144779225883], [-114.03238553405582, 30.540048100584993], [-114.02672342194289, 30.538321026584498]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dbbfffff', 8,
            30.54177, -114.03805,
            48.33, 'Bajo',
            0.0, 0.429,
            0.4, 0.7,
            0.85, 0.3,
            164.34, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03700186884723, 30.53667821533029], [-114.03238553405582, 30.540048100584993], [-114.03343123145694, 30.545144779225883], [-114.03909366330113, 30.546871450059133], [-114.04370998685748, 30.543501399381288], [-114.04266388983585, 30.53840484330793], [-114.03700186884723, 30.53667821533029]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d95fffff', 8,
            30.53331, -114.04162,
            48.81, 'Bajo',
            0.0, 0.453,
            0.4, 0.7,
            0.85, 0.3,
            164.29, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04057195786598, 30.528211378356257], [-114.03595610264152, 30.53158142154371], [-114.03700186884723, 30.53667821533029], [-114.04266388983585, 30.53840484330793], [-114.04727973374749, 30.53503463465097], [-114.04623356801447, 30.529937963500455], [-114.04057195786598, 30.528211378356257]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d9dfffff', 8,
            30.52484, -114.04519,
            49.31, 'Bajo',
            0.0, 0.478,
            0.4, 0.7,
            0.85, 0.3,
            164.26, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04414149861178, 30.519744268760665], [-114.03952612289726, 30.52311446964135], [-114.04057195786598, 30.528211378356257], [-114.04623356801447, 30.529937963500455], [-114.05084893233845, 30.52656759710388], [-114.04980269793562, 30.521470811093568], [-114.04414149861178, 30.519744268760665]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dd7fffff', 8,
            30.51637, -114.04876,
            49.85, 'Bajo',
            0.0, 0.504,
            0.401, 0.7,
            0.85, 0.3,
            164.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04771049118322, 30.511276887000466], [-114.04309559492164, 30.514647245334835], [-114.04414149861178, 30.519744268760665], [-114.04980269793562, 30.521470811093568], [-114.05441758272899, 30.518100287196916], [-114.05337127969788, 30.513003386544217], [-114.04771049118322, 30.511276887000466]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dd1fffff', 8,
            30.50791, -114.05233,
            50.41, 'Moderado',
            0.0, 0.532,
            0.402, 0.7,
            0.85, 0.3,
            164.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0512789356789, 30.502809233532666], [-114.0466645188132, 30.506179749081145], [-114.04771049118322, 30.511276887000466], [-114.05337127969788, 30.513003386544217], [-114.05798568501773, 30.509632705387023], [-114.05693931339988, 30.504535690309368], [-114.0512789356789, 30.502809233532666]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dd9fffff', 8,
            30.49944, -114.05589,
            51.0, 'Moderado',
            0.0, 0.56,
            0.403, 0.7,
            0.85, 0.3,
            164.19, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05484683219733, 30.4943413088143], [-114.05023289467053, 30.497711981337297], [-114.0512789356789, 30.502809233532666], [-114.05693931339988, 30.504535690309368], [-114.06155323930324, 30.50116485213121], [-114.06050679914017, 30.49606772284605], [-114.05484683219733, 30.4943413088143]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c33fffff', 8,
            30.49097, -114.05946,
            51.6, 'Moderado',
            0.0, 0.589,
            0.405, 0.7,
            0.85, 0.3,
            164.18, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05841418083709, 30.485873113302443], [-114.05380072259216, 30.489243942560403], [-114.05484683219733, 30.4943413088143], [-114.06050679914017, 30.49606772284605], [-114.06512024568411, 30.492696727886514], [-114.06407373701734, 30.487599484611355], [-114.05841418083709, 30.485873113302443]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c31fffff', 8,
            30.48415, -114.05275,
            52.03, 'Moderado',
            0.0, 0.613,
            0.402, 0.7,
            0.85, 0.3,
            163.2, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05170876532281, 30.479048859448863], [-114.04709529552713, 30.482419522974215], [-114.04814107460489, 30.487517125976304], [-114.05380072259216, 30.489243942560403], [-114.05841418083709, 30.485873113302443], [-114.05736800267663, 30.480775633207553], [-114.05170876532281, 30.479048859448863]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c3dfffff', 8,
            30.47732, -114.04605,
            52.49, 'Moderado',
            0.0, 0.636,
            0.4, 0.7,
            0.85, 0.3,
            162.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04500399923059, 30.472223966735903], [-114.0403905180344, 30.47559446449763], [-114.04143596661521, 30.480692304027322], [-114.04709529552713, 30.482419522974215], [-114.05170876532281, 30.479048859448863], [-114.05066291763818, 30.473951142754828], [-114.04500399923059, 30.472223966735903]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c2bfffff', 8,
            30.4705, -114.03935,
            52.96, 'Moderado',
            0.0, 0.66,
            0.4, 0.7,
            0.85, 0.3,
            161.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0382998826497, 30.4653984355738], [-114.03368639020319, 30.468768767540922], [-114.03473150831758, 30.47386684337758], [-114.0403905180344, 30.47559446449763], [-114.04500399923059, 30.472223966735903], [-114.04395848199134, 30.467126013663304], [-114.0382998826497, 30.4653984355738]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c29fffff', 8,
            30.46367, -114.03264,
            53.44, 'Moderado',
            0.0, 0.684,
            0.401, 0.7,
            0.85, 0.3,
            160.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0315964156693, 30.458572266372947], [-114.02698291212262, 30.46194243251448], [-114.0280276998011, 30.467040744437398], [-114.03368639020319, 30.468768767540922], [-114.0382998826497, 30.4653984355738], [-114.03725469582535, 30.460300246343333], [-114.0315964156693, 30.458572266372947]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c67fffff', 8,
            30.45684, -114.02594,
            53.94, 'Moderado',
            0.0, 0.708,
            0.402, 0.7,
            0.85, 0.3,
            159.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02489359837847, 30.451745459543847], [-114.02028008388173, 30.455115459828843], [-114.02132454115488, 30.460214007617278], [-114.02698291212262, 30.46194243251448], [-114.0315964156693, 30.458572266372947], [-114.03055155922934, 30.45347384120533], [-114.02489359837847, 30.451745459543847]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c65fffff', 8,
            30.45002, -114.01924,
            54.45, 'Moderado',
            0.0, 0.731,
            0.405, 0.7,
            0.85, 0.3,
            158.3, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01819143086624, 30.444918015497166], [-114.01357790556948, 30.448287849894683], [-114.01462203246786, 30.45338663332783], [-114.02028008388173, 30.455115459828843], [-114.02489359837847, 30.451745459543847], [-114.02384907229238, 30.44664679865989], [-114.01819143086624, 30.444918015497166]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f33fffff', 8,
            30.44319, -114.01253,
            54.97, 'Moderado',
            0.0, 0.754,
            0.409, 0.7,
            0.85, 0.3,
            157.32, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01148991322147, 30.438089934643653], [-114.00687637727472, 30.44145960312279], [-114.00792017382894, 30.446558621979744], [-114.01357790556948, 30.448287849894683], [-114.01819143086624, 30.444918015497166], [-114.01714723510344, 30.439819119117693], [-114.01148991322147, 30.438089934643653]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f37fffff', 8,
            30.44483, -114.00226,
            54.99, 'Moderado',
            0.0, 0.749,
            0.417, 0.7,
            0.85, 0.3,
            156.34, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00121896532691, 30.43972997398395], [-113.99660494021965, 30.443099320151234], [-113.99764833745151, 30.44819846134543], [-114.00330615914395, 30.449928134049703], [-114.00792017382894, 30.446558621979744], [-114.00687637727472, 30.44145960312279], [-114.00121896532691, 30.43972997398395]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d4bfffff', 8,
            30.44647, -113.99199,
            55.04, 'Moderado',
            0.0, 0.743,
            0.428, 0.7,
            0.85, 0.3,
            155.35, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99094743856847, 30.441369246310554], [-113.98633292454952, 30.444738269988715], [-113.98737592234527, 30.44983753337984], [-113.99303383362702, 30.45156765091048], [-113.99764833745151, 30.44819846134543], [-113.99660494021965, 30.443099320151234], [-113.99094743856847, 30.441369246310554]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d41fffff', 8,
            30.44811, -113.98172,
            55.12, 'Moderado',
            0.0, 0.738,
            0.441, 0.7,
            0.85, 0.3,
            154.37, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9806753335575, 30.443007751409226], [-113.97606033087574, 30.44637645242103], [-113.97710292912173, 30.451475837868756], [-113.98276092963017, 30.453206400262694], [-113.98737592234527, 30.44983753337984], [-113.98633292454952, 30.444738269988715], [-113.9806753335575, 30.443007751409226]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d45fffff', 8,
            30.44974, -113.97145,
            55.24, 'Moderado',
            0.0, 0.732,
            0.456, 0.7,
            0.85, 0.3,
            153.4, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97040265090554, 30.444645489065877], [-113.96578715981006, 30.448013867234167], [-113.96682935839267, 30.453113374598136], [-113.97248744776508, 30.454844381892197], [-113.97710292912173, 30.451475837868756], [-113.97606033087574, 30.44637645242103], [-113.97040265090554, 30.444645489065877]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d69fffff', 8,
            30.45138, -113.96117,
            55.38, 'Moderado',
            0.0, 0.727,
            0.473, 0.7,
            0.85, 0.3,
            152.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.96012939122438, 30.44628245906661], [-113.95551341196439, 30.44965051421427], [-113.95655521077008, 30.454750143354087], [-113.96221338864362, 30.456481595585018], [-113.96682935839267, 30.453113374598136], [-113.96578715981006, 30.448013867234167], [-113.96012939122438, 30.44628245906661]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d6dfffff', 8,
            30.45302, -113.9509,
            55.56, 'Moderado',
            0.0, 0.721,
            0.492, 0.7,
            0.85, 0.3,
            151.45, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94985555512599, 30.44791866119765], [-113.94523908795082, 30.451286393147686], [-113.94628048686612, 30.45638614392291], [-113.95193875287791, 30.458118041127342], [-113.95655521077008, 30.454750143354087], [-113.95551341196439, 30.44965051421427], [-113.94985555512599, 30.44791866119765]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d65fffff', 8,
            30.46149, -113.94732,
            55.08, 'Moderado',
            0.0, 0.692,
            0.5, 0.7,
            0.85, 0.3,
            151.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94628048686612, 30.45638614392291], [-113.94166354108029, 30.459753718305507], [-113.94270487048024, 30.46485335565443], [-113.94836354568035, 30.466585297068573], [-113.95298048226125, 30.463217556909424], [-113.95193875287791, 30.458118041127342], [-113.94628048686612, 30.45638614392291]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e925bfffff', 8,
            30.46995, -113.94375,
            54.6, 'Moderado',
            0.0, 0.662,
            0.507, 0.7,
            0.85, 0.3,
            151.48, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94270487048024, 30.46485335565443], [-113.9380874460272, 30.468220772229916], [-113.93912870587016, 30.473320295934798], [-113.94478779027348, 30.47505228158057], [-113.94940520559972, 30.471684699275194], [-113.94836354568035, 30.466585297068573], [-113.94270487048024, 30.46485335565443]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9253fffff', 8,
            30.47842, -113.94017,
            54.11, 'Moderado',
            0.0, 0.633,
            0.514, 0.7,
            0.85, 0.3,
            151.51, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93912870587016, 30.473320295934798], [-113.93451080269338, 30.476687554463524], [-113.93555199293766, 30.481786964306643], [-113.94121148655904, 30.483518994206012], [-113.94582938068717, 30.48015156999402], [-113.94478779027348, 30.47505228158057], [-113.93912870587016, 30.473320295934798]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9219fffff', 8,
            30.48689, -113.93659,
            53.64, 'Moderado',
            0.0, 0.603,
            0.522, 0.7,
            0.85, 0.3,
            151.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93555199293766, 30.481786964306643], [-113.93093361098062, 30.485154064548993], [-113.93197473158448, 30.490253360312675], [-113.93763463443881, 30.491985434487585], [-113.9422530074254, 30.488618168608607], [-113.94121148655904, 30.483518994206012], [-113.93555199293766, 30.481786964306643]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9211fffff', 8,
            30.49535, -113.93302,
            53.17, 'Moderado',
            0.0, 0.574,
            0.53, 0.7,
            0.85, 0.3,
            151.59, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93197473158448, 30.490253360312675], [-113.92735587079063, 30.493620302029008], [-113.9283969217124, 30.49871948349561], [-113.9340572338145, 30.500451601968027], [-113.93867608571614, 30.497084494661678], [-113.93763463443881, 30.491985434487585], [-113.93197473158448, 30.490253360312675]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9217fffff', 8,
            30.50382, -113.92944,
            52.72, 'Moderado',
            0.0, 0.545,
            0.537, 0.7,
            0.85, 0.3,
            151.64, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9283969217124, 30.49871948349561], [-113.92377758202522, 30.50208626644635], [-113.92481856322316, 30.507185333398265], [-113.93047928458783, 30.50891749619018], [-113.93509861546109, 30.50555054769601], [-113.9340572338145, 30.500451601968027], [-113.9283969217124, 30.49871948349561]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92edfffff', 8,
            30.51228, -113.92586,
            52.28, 'Moderado',
            0.0, 0.517,
            0.545, 0.7,
            0.85, 0.3,
            151.7, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92481856322316, 30.507185333398265], [-113.92019874458609, 30.51055195734381], [-113.92123965601844, 30.515650909563462], [-113.92690078666053, 30.51738311669688], [-113.93152059656195, 30.514016327254485], [-113.93047928458783, 30.50891749619018], [-113.92481856322316, 30.507185333398265]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92e1fffff', 8,
            30.51912, -113.93256,
            51.62, 'Moderado',
            0.0, 0.496,
            0.531, 0.7,
            0.85, 0.3,
            152.7, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93152059656195, 30.514016327254485], [-113.92690078666053, 30.51738311669688], [-113.92794202892043, 30.522481832879958], [-113.9336034816341, 30.52421363840808], [-113.93822328264982, 30.52084668349936], [-113.93718163986851, 30.515748088543496], [-113.93152059656195, 30.514016327254485]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92e3fffff', 8,
            30.52595, -113.93927,
            50.98, 'Moderado',
            0.0, 0.475,
            0.516, 0.7,
            0.85, 0.3,
            153.71, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93822328264982, 30.52084668349936], [-113.9336034816341, 30.52421363840808], [-113.93464505475255, 30.529312118333802], [-113.94030682941867, 30.53104352206637], [-113.94492662139862, 30.527676401721816], [-113.94388464777916, 30.522578043095187], [-113.93822328264982, 30.52084668349936]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9285fffff', 8,
            30.53277, -113.94597,
            50.37, 'Moderado',
            0.0, 0.454,
            0.502, 0.7,
            0.85, 0.3,
            154.71, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94492662139862, 30.527676401721816], [-113.94030682941867, 30.53104352206637], [-113.94134873342672, 30.536141765513964], [-113.94701082992617, 30.537872767260783], [-113.95163061272015, 30.534505481510934], [-113.95058830823159, 30.52940735943424], [-113.94492662139862, 30.527676401721816]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9287fffff', 8,
            30.5396, -113.95267,
            49.79, 'Bajo',
            0.0, 0.435,
            0.489, 0.7,
            0.85, 0.3,
            155.72, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95163061272015, 30.534505481510934], [-113.94701082992617, 30.537872767260783], [-113.94805306485475, 30.542970774009554], [-113.9537154830683, 30.54470137358047], [-113.95833525652611, 30.541333922455905], [-113.95729262113754, 30.536236037149813], [-113.95163061272015, 30.534505481510934]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92b9fffff', 8,
            30.54643, -113.95938,
            49.23, 'Bajo',
            0.0, 0.417,
            0.477, 0.7,
            0.85, 0.3,
            156.73, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95833525652611, 30.541333922455905], [-113.9537154830683, 30.54470137358047], [-113.95475804894836, 30.549799143409814], [-113.96042078875671, 30.551529340614763], [-113.96504055272815, 30.548161724146052], [-113.96399758640862, 30.543064075831186], [-113.95833525652611, 30.541333922455905]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92bbfffff', 8,
            30.55326, -113.96608,
            48.71, 'Bajo',
            0.0, 0.399,
            0.465, 0.7,
            0.85, 0.3,
            157.73, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.96504055272815, 30.548161724146052], [-113.96042078875671, 30.551529340614763], [-113.9614636856192, 30.55662687330409], [-113.96712674690299, 30.558356667953113], [-113.97174650123777, 30.554988886170825], [-113.97070320395643, 30.549891475067724], [-113.96504055272815, 30.548161724146052]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e976dfffff', 8,
            30.56009, -113.97279,
            48.23, 'Bajo',
            0.0, 0.383,
            0.454, 0.7,
            0.85, 0.3,
            158.74, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97174650123777, 30.554988886170825], [-113.96712674690299, 30.558356667953113], [-113.9681699747788, 30.563453963281876], [-113.97383335741864, 30.56518335518506], [-113.97845310196642, 30.561815408119823], [-113.9774094736924, 30.556718234448997], [-113.97174650123777, 30.554988886170825]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9769fffff', 8,
            30.55845, -113.98307,
            48.08, 'Bajo',
            0.0, 0.387,
            0.439, 0.7,
            0.85, 0.3,
            159.67, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98202873866451, 30.553350128006578], [-113.9774094736924, 30.556718234448997], [-113.97845310196642, 30.561815408119823], [-113.98411639552792, 30.563544353564644], [-113.98873565048456, 30.560176081823496], [-113.98769162192623, 30.55507902995088], [-113.98202873866451, 30.553350128006578]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9745fffff', 8,
            30.55681, -113.99335,
            47.97, 'Bajo',
            0.0, 0.391,
            0.426, 0.7,
            0.85, 0.3,
            160.61, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99231039728596, 30.5517105990256], [-113.98769162192623, 30.55507902995088], [-113.98873565048456, 30.560176081823496], [-113.99439885460396, 30.561904580847035], [-113.99901761971975, 30.558535984607314], [-113.99797319099113, 30.55343905467313], [-113.99231039728596, 30.5517105990256]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9741fffff', 8,
            30.55517, -114.00364,
            47.89, 'Bajo',
            0.0, 0.395,
            0.416, 0.7,
            0.85, 0.3,
            161.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00259147648883, 30.550070299442353], [-113.99797319099113, 30.55343905467313], [-113.99901761971975, 30.558535984607314], [-114.00468073403341, 30.56026403724672], [-114.0092990090588, 30.55689511668585], [-114.00825418027391, 30.551798308830282], [-114.00259147648883, 30.550070299442353]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e974bfffff', 8,
            30.55353, -114.01392,
            47.85, 'Bajo',
            0.0, 0.399,
            0.408, 0.7,
            0.85, 0.3,
            162.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01287197566013, 30.54842922947144], [-114.00825418027391, 30.551798308830282], [-114.0092990090588, 30.55689511668585], [-114.01496203320309, 30.558622722978395], [-114.01957981788863, 30.55525347827384], [-114.01853458916162, 30.550156792637065], [-114.01287197566013, 30.54842922947144]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512db7fffff', 8,
            30.55188, -114.0242,
            47.85, 'Bajo',
            0.0, 0.403,
            0.403, 0.7,
            0.85, 0.3,
            163.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02315189418704, 30.546787389327633], [-114.01853458916162, 30.550156792637065], [-114.01957981788863, 30.55525347827384], [-114.0252427515001, 30.556980638256896], [-114.02986004559651, 30.553611069586204], [-114.02881441704154, 30.548514506308326], [-114.02315189418704, 30.546787389327633]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512db3fffff', 8,
            30.55024, -114.03448,
            47.89, 'Bajo',
            0.0, 0.407,
            0.4, 0.7,
            0.85, 0.3,
            164.38, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03343123145694, 30.545144779225883], [-114.02881441704154, 30.548514506308326], [-114.02986004559651, 30.553611069586204], [-114.0355228883117, 30.55533778329723], [-114.04013969156982, 30.551967890837997], [-114.03909366330113, 30.546871450059133], [-114.03343123145694, 30.545144779225883]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e966dfffff', 8,
            30.5486, -114.04476,
            47.98, 'Bajo',
            0.0, 0.411,
            0.4, 0.7,
            0.85, 0.3,
            165.33, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04370998685748, 30.543501399381288], [-114.03909366330113, 30.546871450059133], [-114.04013969156982, 30.551967890837997], [-114.04580244302542, 30.55369415831456], [-114.05041875519623, 30.55032394224448], [-114.04937232732814, 30.54522762410467], [-114.04370998685748, 30.543501399381288]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d97fffff', 8,
            30.54013, -114.04833,
            48.43, 'Bajo',
            0.0, 0.434,
            0.401, 0.7,
            0.85, 0.3,
            165.29, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04727973374749, 30.53503463465097], [-114.04266388983585, 30.53840484330793], [-114.04370998685748, 30.543501399381288], [-114.04937232732814, 30.54522762410467], [-114.05398815977651, 30.54185725000912], [-114.05294166324866, 30.53676081664336], [-114.04727973374749, 30.53503463465097]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d91fffff', 8,
            30.53166, -114.0519,
            48.93, 'Bajo',
            0.0, 0.458,
            0.402, 0.7,
            0.85, 0.3,
            165.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05084893233845, 30.52656759710388], [-114.04623356801447, 30.529937963500455], [-114.04727973374749, 30.53503463465097], [-114.05294166324866, 30.53676081664336], [-114.0575570160317, 30.533390284761825], [-114.05651045088565, 30.528293736387443], [-114.05084893233845, 30.52656759710388]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d99fffff', 8,
            30.5232, -114.05546,
            49.46, 'Bajo',
            0.0, 0.483,
            0.403, 0.7,
            0.85, 0.3,
            165.22, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05441758272899, 30.518100287196916], [-114.04980269793562, 30.521470811093568], [-114.05084893233845, 30.52656759710388], [-114.05651045088565, 30.528293736387443], [-114.06112532406044, 30.52492304695945], [-114.06007869033776, 30.519826383793802], [-114.05441758272899, 30.518100287196916]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512dd3fffff', 8,
            30.51473, -114.05903,
            50.01, 'Moderado',
            0.0, 0.51,
            0.405, 0.7,
            0.85, 0.3,
            165.19, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05798568501773, 30.509632705387023], [-114.05337127969788, 30.513003386544217], [-114.05441758272899, 30.518100287196916], [-114.06007869033776, 30.519826383793802], [-114.0646930839614, 30.516455537058896], [-114.06364638170362, 30.511358759319375], [-114.05798568501773, 30.509632705387023]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ddbfffff', 8,
            30.50626, -114.0626,
            50.59, 'Moderado',
            0.0, 0.537,
            0.406, 0.7,
            0.85, 0.3,
            165.17, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06155323930324, 30.50116485213121], [-114.05693931339988, 30.504535690309368], [-114.05798568501773, 30.509632705387023], [-114.06364638170362, 30.511358759319375], [-114.06826029583318, 30.507987755517092], [-114.0672135250818, 30.50289086342114], [-114.06155323930324, 30.50116485213121]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ce5fffff', 8,
            30.49779, -114.06617,
            51.19, 'Moderado',
            0.0, 0.566,
            0.409, 0.7,
            0.85, 0.3,
            165.16, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06512024568411, 30.492696727886514], [-114.06050679914017, 30.49606772284605], [-114.06155323930324, 30.50116485213121], [-114.0672135250818, 30.50289086342114], [-114.07182695977441, 30.49951970279106], [-114.07078012057093, 30.494422696556143], [-114.06512024568411, 30.492696727886514]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512cedfffff', 8,
            30.48933, -114.06973,
            51.81, 'Moderado',
            0.0, 0.595,
            0.411, 0.7,
            0.85, 0.3,
            165.15, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06868670425892, 30.484228333110025], [-114.06407373701734, 30.487599484611355], [-114.06512024568411, 30.492696727886514], [-114.07078012057093, 30.494422696556143], [-114.0753930758837, 30.491051379337843], [-114.07434616826959, 30.48595425918144], [-114.06868670425892, 30.484228333110025]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c3bfffff', 8,
            30.4825, -114.06303,
            52.22, 'Moderado',
            0.0, 0.618,
            0.407, 0.7,
            0.85, 0.3,
            164.17, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06198098169675, 30.47740464745428], [-114.05736800267663, 30.480775633207553], [-114.05841418083709, 30.485873113302443], [-114.06407373701734, 30.487599484611355], [-114.06868670425892, 30.484228333110025], [-114.06764012712992, 30.479130976062393], [-114.06198098169675, 30.47740464745428]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c39fffff', 8,
            30.47568, -114.05632,
            52.64, 'Moderado',
            0.0, 0.642,
            0.403, 0.7,
            0.85, 0.3,
            163.19, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05527590828659, 30.470580322780638], [-114.05066291763818, 30.473951142754828], [-114.05170876532281, 30.479048859448863], [-114.05736800267663, 30.480775633207553], [-114.06198098169675, 30.47740464745428], [-114.06093473502246, 30.47230705373596], [-114.05527590828659, 30.470580322780638]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c07fffff', 8,
            30.46885, -114.04962,
            53.09, 'Moderado',
            0.0, 0.666,
            0.401, 0.7,
            0.85, 0.3,
            162.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04857148411783, 30.46375535949925], [-114.04395848199134, 30.467126013663304], [-114.04500399923059, 30.472223966735903], [-114.05066291763818, 30.473951142754828], [-114.05527590828659, 30.470580322780638], [-114.05422999203658, 30.46548249261222], [-114.04857148411783, 30.46375535949925]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c05fffff', 8,
            30.46203, -114.04291,
            53.55, 'Moderado',
            0.0, 0.69,
            0.4, 0.7,
            0.85, 0.3,
            161.24, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04186770927976, 30.456929758020404], [-114.03725469582535, 30.460300246343333], [-114.0382998826497, 30.4653984355738], [-114.04395848199134, 30.467126013663304], [-114.04857148411783, 30.46375535949925], [-114.04752589826167, 30.45865729310138], [-114.04186770927976, 30.456929758020404]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c63fffff', 8,
            30.4552, -114.03621,
            54.02, 'Moderado',
            0.0, 0.714,
            0.4, 0.7,
            0.85, 0.3,
            160.26, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03516458386153, 30.45010351875454], [-114.03055155922934, 30.45347384120533], [-114.0315964156693, 30.458572266372947], [-114.03725469582535, 30.460300246343333], [-114.04186770927976, 30.456929758020404], [-114.04082245378694, 30.451831455613792], [-114.03516458386153, 30.45010351875454]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c61fffff', 8,
            30.44838, -114.02951,
            54.51, 'Moderado',
            0.0, 0.737,
            0.401, 0.7,
            0.85, 0.3,
            159.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0284621079523, 30.443276642112203], [-114.02384907229238, 30.44664679865989], [-114.02489359837847, 30.451745459543847], [-114.03055155922934, 30.45347384120533], [-114.03516458386153, 30.45010351875454], [-114.03411965870163, 30.44500498055995], [-114.0284621079523, 30.443276642112203]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c6dfffff', 8,
            30.44155, -114.0228,
            55.0, 'Moderado',
            0.0, 0.76,
            0.404, 0.7,
            0.85, 0.3,
            158.31, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02176028164102, 30.436449128504073], [-114.01714723510344, 30.439819119117693], [-114.01819143086624, 30.444918015497166], [-114.02384907229238, 30.44664679865989], [-114.0284621079523, 30.443276642112203], [-114.02741751309475, 30.43817786835044], [-114.02176028164102, 30.436449128504073]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f3bfffff', 8,
            30.43472, -114.0161,
            55.5, 'Moderado',
            0.0, 0.782,
            0.407, 0.7,
            0.85, 0.3,
            157.34, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01505910501666, 30.429620978340964], [-114.01044604775139, 30.432990802989572], [-114.01148991322147, 30.438089934643653], [-114.01714723510344, 30.439819119117693], [-114.02176028164102, 30.436449128504073], [-114.02071601705534, 30.431350119396022], [-114.01505910501666, 30.429620978340964]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f31fffff', 8,
            30.43636, -114.00583,
            55.5, 'Moderado',
            0.0, 0.777,
            0.414, 0.7,
            0.85, 0.3,
            156.35, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.004789045533, 30.431261217394223], [-114.00017549908624, 30.43463071992407], [-114.00121896532691, 30.43972997398395], [-114.00687637727472, 30.44145960312279], [-114.01148991322147, 30.438089934643653], [-114.01044604775139, 30.432990802989572], [-114.004789045533, 30.431261217394223]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f35fffff', 8,
            30.438, -113.99556,
            55.54, 'Moderado',
            0.0, 0.771,
            0.424, 0.7,
            0.85, 0.3,
            155.36, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99451840705049, 30.4329006897514], [-113.98990437167093, 30.43626986998519], [-113.99094743856847, 30.441369246310554], [-113.99660494021965, 30.443099320151234], [-114.00121896532691, 30.43972997398395], [-114.00017549908624, 30.43463071992407], [-113.99451840705049, 30.4329006897514]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d49fffff', 8,
            30.43964, -113.98529,
            55.62, 'Moderado',
            0.0, 0.766,
            0.436, 0.7,
            0.85, 0.3,
            154.38, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98424719018027, 30.434539395198204], [-113.97963266611676, 30.437908252958685], [-113.9806753335575, 30.443007751409226], [-113.98633292454952, 30.444738269988715], [-113.99094743856847, 30.441369246310554], [-113.98990437167093, 30.43626986998519], [-113.98424719018027, 30.434539395198204]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d4dfffff', 8,
            30.44128, -113.97502,
            55.72, 'Moderado',
            0.0, 0.761,
            0.451, 0.7,
            0.85, 0.3,
            153.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9739753955337, 30.436177333520533], [-113.96936038303521, 30.439545868630535], [-113.97040265090554, 30.444645489065877], [-113.97606033087574, 30.44637645242103], [-113.9806753335575, 30.443007751409226], [-113.97963266611676, 30.437908252958685], [-113.9739753955337, 30.436177333520533]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512893fffff', 8,
            30.44291, -113.96475,
            55.86, 'Moderado',
            0.0, 0.755,
            0.467, 0.7,
            0.85, 0.3,
            152.41, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.96370302372239, 30.437814504504434], [-113.95908752303798, 30.441182716786845], [-113.96012939122438, 30.44628245906661], [-113.96578715981006, 30.448013867234167], [-113.97040265090554, 30.444645489065877], [-113.96936038303521, 30.439545868630535], [-113.96370302372239, 30.437814504504434]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512897fffff', 8,
            30.44455, -113.95447,
            56.03, 'Moderado',
            0.0, 0.75,
            0.486, 0.7,
            0.85, 0.3,
            151.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95343007535809, 30.439450907936134], [-113.94881408673703, 30.442818797213906], [-113.94985555512599, 30.44791866119765], [-113.95551341196439, 30.44965051421427], [-113.96012939122438, 30.44628245906661], [-113.95908752303798, 30.441182716786845], [-113.95343007535809, 30.439450907936134]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128bbfffff', 8,
            30.44619, -113.9442,
            56.22, 'Moderado',
            0.0, 0.744,
            0.506, 0.7,
            0.85, 0.3,
            150.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94315655105282, 30.441086543601987], [-113.9385400747445, 30.44445410969815], [-113.93958114322261, 30.449554095245443], [-113.94523908795082, 30.451286393147686], [-113.94985555512599, 30.44791866119765], [-113.94881408673703, 30.442818797213906], [-113.94315655105282, 30.441086543601987]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128b3fffff', 8,
            30.45465, -113.94062,
            55.76, 'Moderado',
            0.0, 0.715,
            0.513, 0.7,
            0.85, 0.3,
            150.47, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93958114322261, 30.449554095245443], [-113.93496418838173, 30.45292150382086], [-113.9360051872932, 30.45802137609105], [-113.94166354108029, 30.459753718305507], [-113.94628048686612, 30.45638614392291], [-113.94523908795082, 30.451286393147686], [-113.93958114322261, 30.449554095245443]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9259fffff', 8,
            30.46312, -113.93705,
            55.28, 'Moderado',
            0.0, 0.686,
            0.521, 0.7,
            0.85, 0.3,
            150.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9360051872932, 30.45802137609105], [-113.93138775386328, 30.461388626906036], [-113.9324286831664, 30.466488385681338], [-113.9380874460272, 30.468220772229916], [-113.94270487048024, 30.46485335565443], [-113.94166354108029, 30.459753718305507], [-113.9360051872932, 30.45802137609105]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9251fffff', 8,
            30.47159, -113.93347,
            54.81, 'Moderado',
            0.0, 0.657,
            0.529, 0.7,
            0.85, 0.3,
            150.52, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9324286831664, 30.466488385681338], [-113.92781077109093, 30.46985547849623], [-113.92885163074405, 30.474955123558896], [-113.93451080269338, 30.476687554463524], [-113.93912870587016, 30.473320295934798], [-113.9380874460272, 30.468220772229916], [-113.9324286831664, 30.466488385681338]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9257fffff', 8,
            30.48005, -113.92989,
            54.33, 'Moderado',
            0.0, 0.627,
            0.536, 0.7,
            0.85, 0.3,
            150.56, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92885163074405, 30.474955123558896], [-113.92423323996653, 30.47832205813405], [-113.92527402992792, 30.483421589266367], [-113.93093361098062, 30.485154064548993], [-113.93555199293766, 30.481786964306643], [-113.93451080269338, 30.476687554463524], [-113.92885163074405, 30.474955123558896]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e921dfffff', 8,
            30.48852, -113.92631,
            53.87, 'Moderado',
            0.0, 0.597,
            0.544, 0.7,
            0.85, 0.3,
            150.6, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92527402992792, 30.483421589266367], [-113.92065516039183, 30.486788365362163], [-113.92169588061978, 30.49188778234646], [-113.92735587079063, 30.493620302029008], [-113.93197473158448, 30.490253360312675], [-113.93093361098062, 30.485154064548993], [-113.92527402992792, 30.483421589266367]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9215fffff', 8,
            30.49699, -113.92274,
            53.41, 'Moderado',
            0.0, 0.568,
            0.553, 0.7,
            0.85, 0.3,
            150.64, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92169588061978, 30.49188778234646], [-113.91707653226865, 30.49525439972326], [-113.91811718272142, 30.500353702341894], [-113.92377758202522, 30.50208626644635], [-113.9283969217124, 30.49871948349561], [-113.92735587079063, 30.493620302029008], [-113.92169588061978, 30.49188778234646]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e923bfffff', 8,
            30.50545, -113.91916,
            52.96, 'Moderado',
            0.0, 0.54,
            0.561, 0.7,
            0.85, 0.3,
            150.7, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91811718272142, 30.500353702341894], [-113.91349735549876, 30.503720160760132], [-113.9145379361346, 30.508819348795477], [-113.92019874458609, 30.51055195734381], [-113.92481856322316, 30.507185333398265], [-113.92377758202522, 30.50208626644635], [-113.91811718272142, 30.500353702341894]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9233fffff', 8,
            30.51392, -113.91558,
            52.53, 'Moderado',
            0.0, 0.512,
            0.569, 0.7,
            0.85, 0.3,
            150.76, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9145379361346, 30.508819348795477], [-113.90991762998392, 30.512185648015553], [-113.91095814076107, 30.51728472125005], [-113.916619358375, 30.519017374264276], [-113.92123965601844, 30.515650909563462], [-113.92019874458609, 30.51055195734381], [-113.9145379361346, 30.508819348795477]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92e5fffff', 8,
            30.52075, -113.92228,
            51.87, 'Moderado',
            0.0, 0.491,
            0.554, 0.7,
            0.85, 0.3,
            151.76, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92123965601844, 30.515650909563462], [-113.916619358375, 30.519017374264276], [-113.9176602, 30.5241162115341], [-113.92332173993428, 30.52584846303104], [-113.92794202892043, 30.522481832879958], [-113.92690078666053, 30.51738311669688], [-113.92123965601844, 30.515650909563462]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92e7fffff', 8,
            30.52758, -113.92898,
            51.22, 'Moderado',
            0.0, 0.47,
            0.538, 0.7,
            0.85, 0.3,
            152.77, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92794202892043, 30.522481832879958], [-113.92332173993428, 30.52584846303104], [-113.92436291243821, 30.530947064115384], [-113.93002477457377, 30.53267891390468], [-113.93464505475255, 30.529312118333802], [-113.9336034816341, 30.52421363840808], [-113.92794202892043, 30.522481832879958]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92a9fffff', 8,
            30.53441, -113.93569,
            50.6, 'Moderado',
            0.0, 0.45,
            0.524, 0.7,
            0.85, 0.3,
            153.78, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93464505475255, 30.529312118333802], [-113.93002477457377, 30.53267891390468], [-113.93106627798767, 30.53777727858275], [-113.93672846220545, 30.539508726474136], [-113.94134873342672, 30.536141765513964], [-113.94030682941867, 30.53104352206637], [-113.93464505475255, 30.529312118333802]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92abfffff', 8,
            30.54124, -113.94239,
            50.0, 'Moderado',
            0.0, 0.43,
            0.51, 0.7,
            0.85, 0.3,
            154.78, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94134873342672, 30.536141765513964], [-113.93672846220545, 30.539508726474136], [-113.93777029656033, 30.544606854525234], [-113.94343280274116, 30.54633790032851], [-113.94805306485475, 30.542970774009554], [-113.94701082992617, 30.537872767260783], [-113.94134873342672, 30.536141765513964]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92bdfffff', 8,
            30.54807, -113.9491,
            49.44, 'Bajo',
            0.0, 0.412,
            0.496, 0.7,
            0.85, 0.3,
            155.79, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94805306485475, 30.542970774009554], [-113.94343280274116, 30.54633790032851], [-113.94447496806801, 30.55143579153197], [-113.95013779609266, 30.553166435057015], [-113.95475804894836, 30.549799143409814], [-113.9537154830683, 30.54470137358047], [-113.94805306485475, 30.542970774009554]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92b1fffff', 8,
            30.5549, -113.9558,
            48.91, 'Bajo',
            0.0, 0.395,
            0.483, 0.7,
            0.85, 0.3,
            156.8, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95475804894836, 30.549799143409814], [-113.95013779609266, 30.553166435057015], [-113.95118029242246, 30.55826408919223], [-113.95684344217165, 30.559994330248998], [-113.9614636856192, 30.55662687330409], [-113.96042078875671, 30.551529340614763], [-113.95475804894836, 30.549799143409814]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92b3fffff', 8,
            30.56172, -113.96251,
            48.41, 'Bajo',
            0.0, 0.38,
            0.471, 0.7,
            0.85, 0.3,
            157.81, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9614636856192, 30.55662687330409], [-113.95684344217165, 30.559994330248998], [-113.95788626953535, 30.565091747095423], [-113.96354974088973, 30.56682158549393], [-113.9681699747788, 30.563453963281876], [-113.96712674690299, 30.558356667953113], [-113.9614636856192, 30.55662687330409]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9765fffff', 8,
            30.56855, -113.96921,
            47.95, 'Bajo',
            0.0, 0.365,
            0.46, 0.7,
            0.85, 0.3,
            158.82, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9681699747788, 30.563453963281876], [-113.96354974088973, 30.56682158549393], [-113.96459289931825, 30.571918764831057], [-113.97025669215837, 30.573648200381417], [-113.97487691633864, 30.570280412932814], [-113.97383335741864, 30.56518335518506], [-113.9681699747788, 30.563453963281876]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9761fffff', 8,
            30.56691, -113.9795,
            47.78, 'Bajo',
            0.0, 0.368,
            0.444, 0.7,
            0.85, 0.3,
            159.75, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97845310196642, 30.561815408119823], [-113.97383335741864, 30.56518335518506], [-113.97487691633864, 30.570280412932814], [-113.98054062021502, 30.572009401900328], [-113.98516035482545, 30.56864128958275], [-113.98411639552792, 30.563544353564644], [-113.97845310196642, 30.561815408119823]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e976bfffff', 8,
            30.56527, -113.98978,
            47.65, 'Bajo',
            0.0, 0.372,
            0.431, 0.7,
            0.85, 0.3,
            160.68, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98873565048456, 30.560176081823496], [-113.98411639552792, 30.563544353564644], [-113.98516035482545, 30.56864128958275], [-113.99082396937428, 30.570369832004463], [-113.99544321416506, 30.567001394995263], [-113.99439885460396, 30.561904580847035], [-113.98873565048456, 30.560176081823496]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9747fffff', 8,
            30.56363, -114.00006,
            47.55, 'Bajo',
            0.0, 0.375,
            0.419, 0.7,
            0.85, 0.3,
            161.62, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99901761971975, 30.558535984607314], [-113.99439885460396, 30.561904580847035], [-113.99544321416506, 30.567001394995263], [-114.00110673902252, 30.56872949090832], [-114.005725493744, 30.56536072938488], [-114.00468073403341, 30.56026403724672], [-113.99901761971975, 30.558535984607314]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9743fffff', 8,
            30.56199, -114.01034,
            47.49, 'Bajo',
            0.0, 0.379,
            0.411, 0.7,
            0.85, 0.3,
            162.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0092990090588, 30.55689511668585], [-114.00468073403341, 30.56026403724672], [-114.005725493744, 30.56536072938488], [-114.01138892854642, 30.567088378826544], [-114.01600719294906, 30.56371929296631], [-114.01496203320309, 30.558622722978395], [-114.0092990090588, 30.55689511668585]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e975dfffff', 8,
            30.56035, -114.02063,
            47.47, 'Bajo',
            0.0, 0.383,
            0.405, 0.7,
            0.85, 0.3,
            163.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01957981788863, 30.55525347827384], [-114.01496203320309, 30.558622722978395], [-114.01600719294906, 30.56371929296631], [-114.02167053733287, 30.56544649597392], [-114.02628831116725, 30.562077085954446], [-114.0252427515001, 30.556980638256896], [-114.01957981788863, 30.55525347827384]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9759fffff', 8,
            30.55871, -114.03091,
            47.49, 'Bajo',
            0.0, 0.386,
            0.401, 0.7,
            0.85, 0.3,
            164.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02986004559651, 30.553611069586204], [-114.0252427515001, 30.556980638256896], [-114.02628831116725, 30.562077085954446], [-114.0319515647689, 30.56380384256545], [-114.03656884778583, 30.5604341085643], [-114.0355228883117, 30.55533778329723], [-114.02986004559651, 30.553611069586204]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9665fffff', 8,
            30.55706, -114.04119,
            47.56, 'Bajo',
            0.0, 0.39,
            0.4, 0.7,
            0.85, 0.3,
            165.38, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04013969156982, 30.551967890837997], [-114.0355228883117, 30.55533778329723], [-114.03656884778583, 30.5604341085643], [-114.04223201024189, 30.562160418816234], [-114.04684880219222, 30.558790361011113], [-114.04580244302542, 30.55369415831456], [-114.04013969156982, 30.551967890837997]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9661fffff', 8,
            30.55542, -114.05147,
            47.66, 'Bajo',
            0.0, 0.394,
            0.402, 0.7,
            0.85, 0.3,
            166.33, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05041875519623, 30.55032394224448], [-114.04580244302542, 30.55369415831456], [-114.04684880219222, 30.558790361011113], [-114.0525118731393, 30.56051622494162], [-114.05712817377406, 30.557145843510227], [-114.05608141502898, 30.55204976352423], [-114.05041875519623, 30.55032394224448]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9669fffff', 8,
            30.54695, -114.05503,
            48.1, 'Bajo',
            0.0, 0.415,
            0.403, 0.7,
            0.85, 0.3,
            166.29, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05398815977651, 30.54185725000912], [-114.04937232732814, 30.54522762410467], [-114.05041875519623, 30.55032394224448], [-114.05608141502898, 30.55204976352423], [-114.06069723586361, 30.54867922402104], [-114.05965040851042, 30.54358302866031], [-114.05398815977651, 30.54185725000912]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d93fffff', 8,
            30.53849, -114.0586,
            48.58, 'Bajo',
            0.0, 0.438,
            0.404, 0.7,
            0.85, 0.3,
            166.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0575570160317, 30.533390284761825], [-114.05294166324866, 30.53676081664336], [-114.05398815977651, 30.54185725000912], [-114.05965040851042, 30.54358302866031], [-114.06426574960207, 30.540212331324813], [-114.06321885368234, 30.535116020806658], [-114.0575570160317, 30.533390284761825]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512d9bfffff', 8,
            30.53002, -114.06217,
            49.09, 'Bajo',
            0.0, 0.462,
            0.406, 0.7,
            0.85, 0.3,
            166.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06112532406044, 30.52492304695945], [-114.05651045088565, 30.528293736387443], [-114.0575570160317, 30.533390284761825], [-114.06321885368234, 30.535116020806658], [-114.06783371508813, 30.531745165878345], [-114.0667867506434, 30.5266487404201], [-114.06112532406044, 30.52492304695945]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ca5fffff', 8,
            30.52155, -114.06574,
            49.64, 'Bajo',
            0.0, 0.488,
            0.408, 0.7,
            0.85, 0.3,
            166.18, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0646930839614, 30.516455537058896], [-114.06007869033776, 30.519826383793802], [-114.06112532406044, 30.52492304695945], [-114.0667867506434, 30.5266487404201], [-114.07140113242042, 30.52327772813849], [-114.07035409949226, 30.5181811879575], [-114.0646930839614, 30.516455537058896]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512cadfffff', 8,
            30.51308, -114.06931,
            50.21, 'Moderado',
            0.0, 0.515,
            0.411, 0.7,
            0.85, 0.3,
            166.16, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06826029583318, 30.507987755517092], [-114.06364638170362, 30.511358759319375], [-114.0646930839614, 30.516455537058896], [-114.07035409949226, 30.5181811879575], [-114.07496800169766, 30.51481001856214], [-114.07392090032755, 30.509713363875807], [-114.06826029583318, 30.507987755517092]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ce7fffff', 8,
            30.50462, -114.07287,
            50.81, 'Moderado',
            0.0, 0.543,
            0.414, 0.7,
            0.85, 0.3,
            166.15, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07182695977441, 30.49951970279106], [-114.0672135250818, 30.50289086342114], [-114.06826029583318, 30.507987755517092], [-114.07392090032755, 30.509713363875807], [-114.07853432301846, 30.506342037606256], [-114.07748715324789, 30.501245268632005], [-114.07182695977441, 30.49951970279106]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ce1fffff', 8,
            30.49615, -114.07644,
            51.42, 'Moderado',
            0.0, 0.571,
            0.417, 0.7,
            0.85, 0.3,
            166.14, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0753930758837, 30.491051379337843], [-114.07078012057093, 30.494422696556143], [-114.07182695977441, 30.49951970279106], [-114.07748715324789, 30.501245268632005], [-114.08210009648147, 30.497873785727826], [-114.08105285835191, 30.492776902683136], [-114.0753930758837, 30.491051379337843]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ce9fffff', 8,
            30.48768, -114.08001,
            52.06, 'Moderado',
            0.0, 0.6,
            0.42, 0.7,
            0.85, 0.3,
            166.13, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07895864425959, 30.482582785614543], [-114.07434616826959, 30.48595425918144], [-114.0753930758837, 30.491051379337843], [-114.08105285835191, 30.492776902683136], [-114.08566532218529, 30.489405263383922], [-114.0846180157382, 30.484308266486277], [-114.07895864425959, 30.482582785614543]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c17fffff', 8,
            30.48086, -114.0733,
            52.44, 'Moderado',
            0.0, 0.624,
            0.414, 0.7,
            0.85, 0.3,
            165.15, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07225261512622, 30.475759668258906], [-114.06764012712992, 30.479130976062393], [-114.06868670425892, 30.484228333110025], [-114.07434616826959, 30.48595425918144], [-114.07895864425959, 30.482582785614543], [-114.07791166827634, 30.47748555175419], [-114.07225261512622, 30.475759668258906]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c15fffff', 8,
            30.47403, -114.06659,
            52.84, 'Moderado',
            0.0, 0.648,
            0.409, 0.7,
            0.85, 0.3,
            164.18, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06554723487477, 30.46893591172699], [-114.06093473502246, 30.47230705373596], [-114.06198098169675, 30.47740464745428], [-114.06764012712992, 30.479130976062393], [-114.07225261512622, 30.475759668258906], [-114.07120596957648, 30.47066219765638], [-114.06554723487477, 30.46893591172699]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c03fffff', 8,
            30.46721, -114.05989,
            53.26, 'Moderado',
            0.0, 0.672,
            0.405, 0.7,
            0.85, 0.3,
            163.2, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05884250359469, 30.462111516428827], [-114.05422999203658, 30.46548249261222], [-114.05527590828659, 30.470580322780638], [-114.06093473502246, 30.47230705373596], [-114.06554723487477, 30.46893591172699], [-114.06450091972815, 30.46383820460283], [-114.05884250359469, 30.462111516428827]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c01fffff', 8,
            30.46038, -114.05318,
            53.7, 'Moderado',
            0.0, 0.696,
            0.402, 0.7,
            0.85, 0.3,
            162.22, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0521384213754, 30.455286482774632], [-114.04752589826167, 30.45865729310138], [-114.04857148411783, 30.46375535949925], [-114.05422999203658, 30.46548249261222], [-114.05884250359469, 30.462111516428827], [-114.0577965188208, 30.457013573003678], [-114.0521384213754, 30.455286482774632]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c0dfffff', 8,
            30.45356, -114.04648,
            54.14, 'Moderado',
            0.0, 0.719,
            0.401, 0.7,
            0.85, 0.3,
            161.25, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04543498830618, 30.448460811174733], [-114.04082245378694, 30.451831455613792], [-114.04186770927976, 30.456929758020404], [-114.04752589826167, 30.45865729310138], [-114.0521384213754, 30.455286482774632], [-114.05109276694378, 30.450188303269172], [-114.04543498830618, 30.448460811174733]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c6bfffff', 8,
            30.44673, -114.03978,
            54.6, 'Moderado',
            0.0, 0.742,
            0.4, 0.7,
            0.85, 0.3,
            160.27, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03873220447622, 30.441634502039584], [-114.03411965870163, 30.44500498055995], [-114.03516458386153, 30.45010351875454], [-114.04082245378694, 30.451831455613792], [-114.04543498830618, 30.448460811174733], [-114.04438966418643, 30.443362395809682], [-114.03873220447622, 30.441634502039584]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c69fffff', 8,
            30.43991, -114.03307,
            55.06, 'Moderado',
            0.0, 0.765,
            0.401, 0.7,
            0.85, 0.3,
            159.3, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03203006997468, 30.434807555779777], [-114.02741751309475, 30.43817786835044], [-114.0284621079523, 30.443276642112203], [-114.03411965870163, 30.44500498055995], [-114.03873220447622, 30.441634502039584], [-114.03768721063787, 30.43653585103574], [-114.03203006997468, 30.434807555779777]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f17fffff', 8,
            30.43308, -114.02637,
            55.53, 'Moderado',
            0.0, 0.787,
            0.402, 0.7,
            0.85, 0.3,
            158.33, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02532858489056, 30.427979972806046], [-114.02071601705534, 30.431350119396022], [-114.02176028164102, 30.436449128504073], [-114.02741751309475, 30.43817786835044], [-114.03203006997468, 30.434807555779777], [-114.0309854063872, 30.429708669358], [-114.02532858489056, 30.427979972806046]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f15fffff', 8,
            30.42625, -114.01967,
            56.01, 'Moderado',
            0.0, 0.809,
            0.405, 0.7,
            0.85, 0.3,
            157.36, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01862774931281, 30.421151753529216], [-114.01401517067225, 30.42452173410754], [-114.01505910501666, 30.429620978340964], [-114.02071601705534, 30.431350119396022], [-114.02532858489056, 30.427979972806046], [-114.02428425152348, 30.422880851187223], [-114.01862774931281, 30.421151753529216]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f39fffff', 8,
            30.42789, -114.0094,
            56.0, 'Moderado',
            0.0, 0.804,
            0.411, 0.7,
            0.85, 0.3,
            156.37, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00835857816804, 30.42279219203382], [-114.00374551032506, 30.42616185068648], [-114.004789045533, 30.431261217394223], [-114.01044604775139, 30.432990802989572], [-114.01505910501666, 30.429620978340964], [-114.01401517067225, 30.42452173410754], [-114.00835857816804, 30.42279219203382]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f3dfffff', 8,
            30.42953, -113.99913,
            56.03, 'Moderado',
            0.0, 0.799,
            0.42, 0.7,
            0.85, 0.3,
            155.37, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99808882788956, 30.42443186415993], [-113.99347527109272, 30.427801200709613], [-113.99451840705049, 30.4329006897514], [-114.00017549908624, 30.43463071992407], [-114.004789045533, 30.431261217394223], [-114.00374551032506, 30.42616185068648], [-113.99808882788956, 30.42443186415993]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f23fffff', 8,
            30.43117, -113.98886,
            56.1, 'Moderado',
            0.0, 0.794,
            0.432, 0.7,
            0.85, 0.3,
            154.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98781849908828, 30.42607076969325], [-113.98320445358635, 30.429439783962682], [-113.98424719018027, 30.434539395198204], [-113.98990437167093, 30.43626986998519], [-113.99451840705049, 30.4329006897514], [-113.99347527109272, 30.427801200709613], [-113.98781849908828, 30.42607076969325]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f27fffff', 8,
            30.43281, -113.97859,
            56.2, 'Moderado',
            0.0, 0.788,
            0.445, 0.7,
            0.85, 0.3,
            153.4, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97754759237542, 30.42770890841964], [-113.97293305841724, 30.431077600231625], [-113.9739753955337, 30.436177333520533], [-113.97963266611676, 30.437908252958685], [-113.98424719018027, 30.434539395198204], [-113.98320445358635, 30.429439783962682], [-113.97754759237542, 30.42770890841964]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '884851289bfffff', 8,
            30.43445, -113.96832,
            56.33, 'Moderado',
            0.0, 0.783,
            0.461, 0.7,
            0.85, 0.3,
            152.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9672761083623, 30.429346280125102], [-113.9626610861969, 30.432714649302532], [-113.96370302372239, 30.437814504504434], [-113.96936038303521, 30.439545868630535], [-113.9739753955337, 30.436177333520533], [-113.97293305841724, 30.431077600231625], [-113.9672761083623, 30.429346280125102]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512891fffff', 8,
            30.43608, -113.95805,
            56.49, 'Moderado',
            0.0, 0.778,
            0.479, 0.7,
            0.85, 0.3,
            151.43, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95700404766056, 30.430982884595842], [-113.95238853753708, 30.434350930961653], [-113.95343007535809, 30.439450907936134], [-113.95908752303798, 30.441182716786845], [-113.96370302372239, 30.437814504504434], [-113.9626610861969, 30.432714649302532], [-113.95700404766056, 30.430982884595842]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512895fffff', 8,
            30.43772, -113.94777,
            56.68, 'Moderado',
            0.0, 0.772,
            0.499, 0.7,
            0.85, 0.3,
            150.45, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.946731410882, 30.432618721618187], [-113.94211541304969, 30.43598644499539], [-113.94315655105282, 30.441086543601987], [-113.94881408673703, 30.442818797213906], [-113.95343007535809, 30.439450907936134], [-113.95238853753708, 30.434350930961653], [-113.946731410882, 30.432618721618187]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128b9fffff', 8,
            30.43935, -113.9375,
            56.89, 'Moderado',
            0.0, 0.767,
            0.52, 0.7,
            0.85, 0.3,
            149.48, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93645819863862, 30.434253790978676], [-113.93184171334696, 30.43762119119034], [-113.93288245141882, 30.442721411288574], [-113.9385400747445, 30.44445410969815], [-113.94315655105282, 30.441086543601987], [-113.94211541304969, 30.43598644499539], [-113.93645819863862, 30.434253790978676]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128b1fffff', 8,
            30.44782, -113.93392,
            56.44, 'Moderado',
            0.0, 0.739,
            0.528, 0.7,
            0.85, 0.3,
            149.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93288245141882, 30.442721411288574], [-113.92826548767275, 30.44608865402621], [-113.92930615612666, 30.45118876099655], [-113.93496418838173, 30.45292150382086], [-113.93958114322261, 30.449554095245443], [-113.9385400747445, 30.44445410969815], [-113.93288245141882, 30.442721411288574]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128b7fffff', 8,
            30.45629, -113.93035,
            55.98, 'Moderado',
            0.0, 0.71,
            0.535, 0.7,
            0.85, 0.3,
            149.51, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92930615612666, 30.45118876099655], [-113.9246887138697, 30.45455584602046], [-113.92572931266396, 30.459655839645105], [-113.93138775386328, 30.461388626906036], [-113.9360051872932, 30.45802137609105], [-113.93496418838173, 30.45292150382086], [-113.92930615612666, 30.45118876099655]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e925dfffff', 8,
            30.46476, -113.92677,
            55.51, 'Moderado',
            0.0, 0.68,
            0.543, 0.7,
            0.85, 0.3,
            149.53, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92572931266396, 30.459655839645105], [-113.92111139183966, 30.463022766715614], [-113.9221519209326, 30.468122646776777], [-113.92781077109093, 30.46985547849623], [-113.9324286831664, 30.466488385681338], [-113.93138775386328, 30.461388626906036], [-113.92572931266396, 30.459655839645105]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9255fffff', 8,
            30.47322, -113.92319,
            55.04, 'Moderado',
            0.0, 0.651,
            0.552, 0.7,
            0.85, 0.3,
            149.56, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9221519209326, 30.468122646776777], [-113.9175335214845, 30.471489415654215], [-113.9185739808344, 30.476589181934155], [-113.92423323996653, 30.47832205813405], [-113.92885163074405, 30.474955123558896], [-113.92781077109093, 30.46985547849623], [-113.9221519209326, 30.468122646776777]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e920bfffff', 8,
            30.48169, -113.91961,
            54.57, 'Moderado',
            0.0, 0.621,
            0.56, 0.7,
            0.85, 0.3,
            149.6, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9185739808344, 30.476589181934155], [-113.91395510270603, 30.479955792378885], [-113.91499549227117, 30.485055444659903], [-113.92065516039183, 30.486788365362163], [-113.92527402992792, 30.483421589266367], [-113.92423323996653, 30.47832205813405], [-113.9185739808344, 30.476589181934155]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9203fffff', 8,
            30.49015, -113.91604,
            54.11, 'Moderado',
            0.0, 0.592,
            0.568, 0.7,
            0.85, 0.3,
            149.65, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91499549227117, 30.485055444659903], [-113.91037613540607, 30.488421896432296], [-113.91141645514472, 30.493521434496696], [-113.91707653226865, 30.49525439972326], [-113.92169588061978, 30.49188778234646], [-113.92065516039183, 30.486788365362163], [-113.91499549227117, 30.485055444659903]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9239fffff', 8,
            30.49862, -113.91246,
            53.66, 'Moderado',
            0.0, 0.563,
            0.577, 0.7,
            0.85, 0.3,
            149.7, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91141645514472, 30.493521434496696], [-113.90679661948643, 30.496887727357144], [-113.90783686935681, 30.50198715098728], [-113.91349735549876, 30.503720160760132], [-113.91811718272142, 30.500353702341894], [-113.91707653226865, 30.49525439972326], [-113.91141645514472, 30.493521434496696]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9231fffff', 8,
            30.50709, -113.90888,
            53.22, 'Moderado',
            0.0, 0.534,
            0.585, 0.7,
            0.85, 0.3,
            149.76, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.90783686935681, 30.50198715098728], [-113.9032165548489, 30.505353284696202], [-113.90425673480927, 30.510452593674465], [-113.90991762998392, 30.512185648015553], [-113.9145379361346, 30.508819348795477], [-113.91349735549876, 30.503720160760132], [-113.90783686935681, 30.50198715098728]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9237fffff', 8,
            30.51555, -113.9053,
            52.8, 'Moderado',
            0.0, 0.507,
            0.594, 0.7,
            0.85, 0.3,
            149.82, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.90425673480927, 30.510452593674465], [-113.89963594139525, 30.513818567992296], [-113.90067605140382, 30.518917762101093], [-113.90633735562587, 30.520650861032447], [-113.91095814076107, 30.51728472125005], [-113.90991762998392, 30.512185648015553], [-113.90425673480927, 30.510452593674465]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9059fffff', 8,
            30.52238, -113.912,
            52.13, 'Moderado',
            0.0, 0.485,
            0.578, 0.7,
            0.85, 0.3,
            150.83, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91095814076107, 30.51728472125005], [-113.90633735562587, 30.520650861032447], [-113.90737779650254, 30.52574981924852], [-113.91303942329364, 30.527482516750645], [-113.9176602, 30.5241162115341], [-113.916619358375, 30.519017374264276], [-113.91095814076107, 30.51728472125005]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e905bfffff', 8,
            30.52921, -113.9187,
            51.48, 'Moderado',
            0.0, 0.465,
            0.562, 0.7,
            0.85, 0.3,
            151.84, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9176602, 30.5241162115341], [-113.91303942329364, 30.527482516750645], [-113.91408019506953, 30.53258123885314], [-113.91974214431075, 30.534313534735617], [-113.92436291243821, 30.530947064115384], [-113.92332173993428, 30.52584846303104], [-113.9176602, 30.5241162115341]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92adfffff', 8,
            30.53605, -113.9254,
            50.85, 'Moderado',
            0.0, 0.445,
            0.547, 0.7,
            0.85, 0.3,
            152.84, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92436291243821, 30.530947064115384], [-113.91974214431075, 30.534313534735617], [-113.92078324701694, 30.539412020503736], [-113.92644551858923, 30.541143914576246], [-113.93106627798767, 30.53777727858275], [-113.93002477457377, 30.53267891390468], [-113.92436291243821, 30.530947064115384]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92a1fffff', 8,
            30.54288, -113.93211,
            50.24, 'Moderado',
            0.0, 0.426,
            0.532, 0.7,
            0.85, 0.3,
            153.85, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93106627798767, 30.53777727858275], [-113.92644551858923, 30.541143914576246], [-113.9274869522568, 30.54624216378925], [-113.93314954604107, 30.547973655861522], [-113.93777029656033, 30.544606854525234], [-113.93672846220545, 30.539508726474136], [-113.93106627798767, 30.53777727858275]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92a3fffff', 8,
            30.5497, -113.93881,
            49.67, 'Bajo',
            0.0, 0.408,
            0.517, 0.7,
            0.85, 0.3,
            154.86, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93777029656033, 30.544606854525234], [-113.93314954604107, 30.547973655861522], [-113.93419131070101, 30.553071668298717], [-113.93985422657812, 30.554802758180557], [-113.94447496806801, 30.55143579153197], [-113.94343280274116, 30.54633790032851], [-113.93777029656033, 30.544606854525234]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92b5fffff', 8,
            30.55653, -113.94552,
            49.13, 'Bajo',
            0.0, 0.392,
            0.503, 0.7,
            0.85, 0.3,
            155.87, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94447496806801, 30.55143579153197], [-113.93985422657812, 30.554802758180557], [-113.9408963222615, 30.55990053362132], [-113.94655956011218, 30.561631221122607], [-113.95118029242246, 30.55826408919223], [-113.95013779609266, 30.553166435057015], [-113.94447496806801, 30.55143579153197]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92b7fffff', 8,
            30.56336, -113.95222,
            48.62, 'Bajo',
            0.0, 0.376,
            0.49, 0.7,
            0.85, 0.3,
            156.88, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95118029242246, 30.55826408919223], [-113.94655956011218, 30.561631221122607], [-113.94760198684996, 30.566728759346365], [-113.95326554655497, 30.568459044277063], [-113.95788626953535, 30.565091747095423], [-113.95684344217165, 30.559994330248998], [-113.95118029242246, 30.55826408919223]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e90d9fffff', 8,
            30.57019, -113.95893,
            48.15, 'Bajo',
            0.0, 0.362,
            0.477, 0.7,
            0.85, 0.3,
            157.89, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95788626953535, 30.565091747095423], [-113.95326554655497, 30.568459044277063], [-113.95430830437815, 30.573556345063277], [-113.95997218581809, 30.57528622723343], [-113.96459289931825, 30.571918764831057], [-113.96354974088973, 30.56682158549393], [-113.95788626953535, 30.565091747095423]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e90dbfffff', 8,
            30.57702, -113.96564,
            47.71, 'Bajo',
            0.0, 0.349,
            0.466, 0.7,
            0.85, 0.3,
            158.91, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.96459289931825, 30.571918764831057], [-113.95997218581809, 30.57528622723343], [-113.96101527475759, 30.580383290361667], [-113.96667947781306, 30.582112769581368], [-113.97130018168264, 30.57874514198883], [-113.97025669215837, 30.573648200381417], [-113.96459289931825, 30.571918764831057]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9767fffff', 8,
            30.57538, -113.97592,
            47.53, 'Bajo',
            0.0, 0.352,
            0.449, 0.7,
            0.85, 0.3,
            159.83, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97487691633864, 30.570280412932814], [-113.97025669215837, 30.573648200381417], [-113.97130018168264, 30.57874514198883], [-113.97696429588903, 30.5804741745012], [-113.9815845102101, 30.577106221846655], [-113.98054062021502, 30.572009401900328], [-113.97487691633864, 30.570280412932814]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9763fffff', 8,
            30.57374, -113.9862,
            47.37, 'Bajo',
            0.0, 0.355,
            0.435, 0.7,
            0.85, 0.3,
            160.76, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98516035482545, 30.56864128958275], [-113.98054062021502, 30.572009401900328], [-113.9815845102101, 30.577106221846655], [-113.98724853520348, 30.578834807688725], [-113.99186825972615, 30.575466530149477], [-113.99082396937428, 30.570369832004463], [-113.98516035482545, 30.56864128958275]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e970dfffff', 8,
            30.5721, -113.99649,
            47.26, 'Bajo',
            0.0, 0.358,
            0.423, 0.7,
            0.85, 0.3,
            161.69, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99544321416506, 30.567001394995263], [-113.99082396937428, 30.570369832004463], [-113.99186825972615, 30.575466530149477], [-113.99753219514265, 30.57719466935838], [-114.00215142961714, 30.57382606711181], [-114.00110673902252, 30.56872949090832], [-113.99544321416506, 30.567001394995263]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9709fffff', 8,
            30.57046, -114.00677,
            47.18, 'Bajo',
            0.0, 0.361,
            0.414, 0.7,
            0.85, 0.3,
            162.62, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.005725493744, 30.56536072938488], [-114.00110673902252, 30.56872949090832], [-114.00215142961714, 30.57382606711181], [-114.00781527509298, 30.575553759724777], [-114.01243401926969, 30.572184832948327], [-114.01138892854642, 30.567088378826544], [-114.005725493744, 30.56536072938488]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9755fffff', 8,
            30.56882, -114.01705,
            47.14, 'Bajo',
            0.0, 0.365,
            0.406, 0.7,
            0.85, 0.3,
            163.56, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01600719294906, 30.56371929296631], [-114.01138892854642, 30.567088378826544], [-114.01243401926969, 30.572184832948327], [-114.01809777444117, 30.573912079002685], [-114.02271602807059, 30.570542827873886], [-114.02167053733287, 30.56544649597392], [-114.01600719294906, 30.56371929296631]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9751fffff', 8,
            30.56717, -114.02733,
            47.14, 'Bajo',
            0.0, 0.368,
            0.402, 0.7,
            0.85, 0.3,
            164.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02628831116725, 30.562077085954446], [-114.02167053733287, 30.56544649597392], [-114.02271602807059, 30.570542827873886], [-114.02837969257408, 30.572269627407064], [-114.03299745540686, 30.568900052103466], [-114.0319515647689, 30.56380384256545], [-114.02628831116725, 30.562077085954446]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e975bfffff', 8,
            30.56553, -114.03761,
            47.18, 'Bajo',
            0.0, 0.371,
            0.4, 0.7,
            0.85, 0.3,
            165.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03656884778583, 30.5604341085643], [-114.0319515647689, 30.56380384256545], [-114.03299745540686, 30.568900052103466], [-114.03866102887882, 30.570626405152993], [-114.04327830066576, 30.56725650585228], [-114.04223201024189, 30.562160418816234], [-114.03656884778583, 30.5604341085643]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9667fffff', 8,
            30.56389, -114.0479,
            47.26, 'Bajo',
            0.0, 0.375,
            0.401, 0.7,
            0.85, 0.3,
            166.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04684880219222, 30.558790361011113], [-114.04223201024189, 30.562160418816234], [-114.04327830066576, 30.56725650585228], [-114.0489417827427, 30.568982412455753], [-114.05355856323474, 30.565612189335624], [-114.0525118731393, 30.56051622494162], [-114.04684880219222, 30.558790361011113]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9663fffff', 8,
            30.56224, -114.05818,
            47.38, 'Bajo',
            0.0, 0.378,
            0.404, 0.7,
            0.85, 0.3,
            167.33, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05712817377406, 30.557145843510227], [-114.0525118731393, 30.56051622494162], [-114.05355856323474, 30.565612189335624], [-114.0592219535533, 30.567337649530803], [-114.0638382425015, 30.56396710276902], [-114.0627911528489, 30.55887126115706], [-114.05712817377406, 30.557145843510227]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e966bfffff', 8,
            30.55378, -114.06174,
            47.8, 'Bajo',
            0.0, 0.398,
            0.406, 0.7,
            0.85, 0.3,
            167.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06069723586361, 30.54867922402104], [-114.05608141502898, 30.55204976352423], [-114.05712817377406, 30.557145843510227], [-114.0627911528489, 30.55887126115706], [-114.06740696191929, 30.555500556277188], [-114.06635980371028, 30.55040459914175], [-114.06069723586361, 30.54867922402104]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9645fffff', 8,
            30.54531, -114.06531,
            48.26, 'Bajo',
            0.0, 0.42,
            0.408, 0.7,
            0.85, 0.3,
            167.24, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06426574960207, 30.540212331324813], [-114.05965040851042, 30.54358302866031], [-114.06069723586361, 30.54867922402104], [-114.06635980371028, 30.55040459914175], [-114.07097513296004, 30.54703373638325], [-114.06992790623617, 30.541937663941614], [-114.06426574960207, 30.540212331324813]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e964dfffff', 8,
            30.53684, -114.06888,
            48.76, 'Bajo',
            0.0, 0.443,
            0.41, 0.7,
            0.85, 0.3,
            167.2, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06783371508813, 30.531745165878345], [-114.06321885368234, 30.535116020806658], [-114.06426574960207, 30.540212331324813], [-114.06992790623617, 30.541937663941614], [-114.07454275572246, 30.53856664354397], [-114.07349546052528, 30.53347045601343], [-114.06783371508813, 30.531745165878345]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ca7fffff', 8,
            30.52837, -114.07245,
            49.29, 'Bajo',
            0.0, 0.467,
            0.413, 0.7,
            0.85, 0.3,
            167.17, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07140113242042, 30.52327772813849], [-114.0667867506434, 30.5266487404201], [-114.06783371508813, 30.531745165878345], [-114.07349546052528, 30.53347045601343], [-114.07810983030524, 30.530099278216145], [-114.07706246667628, 30.525002975814022], [-114.07140113242042, 30.52327772813849]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ca1fffff', 8,
            30.51991, -114.07602,
            49.86, 'Bajo',
            0.0, 0.493,
            0.416, 0.7,
            0.85, 0.3,
            167.15, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07496800169766, 30.51481001856214], [-114.07035409949226, 30.5181811879575], [-114.07140113242042, 30.52327772813849], [-114.07706246667628, 30.525002975814022], [-114.08167635680708, 30.521631640856633], [-114.08062892478782, 30.516535223800293], [-114.07496800169766, 30.51481001856214]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ca9fffff', 8,
            30.51144, -114.07958,
            50.45, 'Moderado',
            0.0, 0.52,
            0.42, 0.7,
            0.85, 0.3,
            167.13, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07853432301846, 30.506342037606256], [-114.07392090032755, 30.509713363875807], [-114.07496800169766, 30.51481001856214], [-114.08062892478782, 30.516535223800293], [-114.08524233532665, 30.513163731922347], [-114.08419483495861, 30.508067200429174], [-114.07853432301846, 30.506342037606256]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ce3fffff', 8,
            30.50297, -114.08315,
            51.06, 'Moderado',
            0.0, 0.548,
            0.423, 0.7,
            0.85, 0.3,
            167.12, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.08210009648147, 30.497873785727826], [-114.07748715324789, 30.501245268632005], [-114.07853432301846, 30.506342037606256], [-114.08419483495861, 30.508067200429174], [-114.08880776596264, 30.504695551870217], [-114.08776019728727, 30.499598906157654], [-114.08210009648147, 30.497873785727826]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512cebfffff', 8,
            30.4945, -114.08671,
            51.69, 'Moderado',
            0.0, 0.577,
            0.427, 0.7,
            0.85, 0.3,
            167.11, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.08566532218529, 30.489405263383922], [-114.08105285835191, 30.492776902683136], [-114.08210009648147, 30.497873785727826], [-114.08776019728727, 30.499598906157654], [-114.09237264881368, 30.496227101157263], [-114.09132501187244, 30.49113034144277], [-114.08566532218529, 30.489405263383922]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512cc5fffff', 8,
            30.48603, -114.09028,
            52.34, 'Moderado',
            0.0, 0.606,
            0.431, 0.7,
            0.85, 0.3,
            167.11, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.08923000022853, 30.480936471031647], [-114.0846180157382, 30.484308266486277], [-114.08566532218529, 30.489405263383922], [-114.09132501187244, 30.49113034144277], [-114.09593698397839, 30.48775838024055], [-114.09488927881274, 30.482661506741614], [-114.08923000022853, 30.480936471031647]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c13fffff', 8,
            30.47921, -114.08357,
            52.7, 'Moderado',
            0.0, 0.63,
            0.424, 0.7,
            0.85, 0.3,
            166.14, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.08252366500068, 30.474113922078303], [-114.07791166827634, 30.47748555175419], [-114.07895864425959, 30.482582785614543], [-114.0846180157382, 30.484308266486277], [-114.08923000022853, 30.480936471031647], [-114.08818262550538, 30.475839360498576], [-114.08252366500068, 30.474113922078303]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c11fffff', 8,
            30.47239, -114.07686,
            53.08, 'Moderado',
            0.0, 0.654,
            0.417, 0.7,
            0.85, 0.3,
            165.16, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07581797838455, 30.467290733790378], [-114.07120596957648, 30.47066219765638], [-114.07225261512622, 30.475759668258906], [-114.07791166827634, 30.47748555175419], [-114.08252366500068, 30.474113922078303], [-114.08147662068976, 30.469016574731576], [-114.07581797838455, 30.467290733790378]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c1dfffff', 8,
            30.46556, -114.07016,
            53.47, 'Moderado',
            0.0, 0.678,
            0.411, 0.7,
            0.85, 0.3,
            164.18, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06911294046971, 30.460466906577818], [-114.06450091972815, 30.46383820460283], [-114.06554723487477, 30.46893591172699], [-114.07120596957648, 30.47066219765638], [-114.07581797838455, 30.467290733790378], [-114.0747712644555, 30.462193149850524], [-114.06911294046971, 30.460466906577818]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c0bfffff', 8,
            30.45874, -114.06345,
            53.88, 'Moderado',
            0.0, 0.701,
            0.407, 0.7,
            0.85, 0.3,
            163.21, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06240855134563, 30.45364244085075], [-114.0577965188208, 30.457013573003678], [-114.05884250359469, 30.462111516428827], [-114.06450091972815, 30.46383820460283], [-114.06911294046971, 30.460466906577818], [-114.0680665568922, 30.455369086265463], [-114.06240855134563, 30.45364244085075]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c09fffff', 8,
            30.45192, -114.05675,
            54.3, 'Moderado',
            0.0, 0.725,
            0.404, 0.7,
            0.85, 0.3,
            162.24, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05570481110175, 30.44681733701943], [-114.05109276694378, 30.450188303269172], [-114.0521384213754, 30.455286482774632], [-114.0577965188208, 30.457013573003678], [-114.06240855134563, 30.45364244085075], [-114.06136249808928, 30.44854438438654], [-114.05570481110175, 30.44681733701943]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c47fffff', 8,
            30.44509, -114.05005,
            54.73, 'Moderado',
            0.0, 0.748,
            0.401, 0.7,
            0.85, 0.3,
            161.26, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04900171982739, 30.439991595494178], [-114.04438966418643, 30.443362395809682], [-114.04543498830618, 30.448460811174733], [-114.05109276694378, 30.450188303269172], [-114.05570481110175, 30.44681733701943], [-114.05465908813616, 30.441719044624048], [-114.04900171982739, 30.439991595494178]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c45fffff', 8,
            30.43826, -114.04334,
            55.16, 'Moderado',
            0.0, 0.771,
            0.4, 0.7,
            0.85, 0.3,
            160.29, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04229927761173, 30.43316521668552], [-114.03768721063787, 30.43653585103574], [-114.03873220447622, 30.441634502039584], [-114.04438966418643, 30.443362395809682], [-114.04900171982739, 30.439991595494178], [-114.04795632712214, 30.43489306738841], [-114.04229927761173, 30.43316521668552]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f13fffff', 8,
            30.43144, -114.03664,
            55.61, 'Moderado',
            0.0, 0.793,
            0.4, 0.7,
            0.85, 0.3,
            159.32, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03559748454398, 30.42633820100407], [-114.0309854063872, 30.429708669358], [-114.03203006997468, 30.434807555779777], [-114.03768721063787, 30.43653585103574], [-114.04229927761173, 30.43316521668552], [-114.04125421513639, 30.4280664530902], [-114.03559748454398, 30.42633820100407]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f11fffff', 8,
            30.42461, -114.02994,
            56.05, 'Moderado',
            0.0, 0.814,
            0.401, 0.7,
            0.85, 0.3,
            158.35, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02889634071316, 30.41951054886061], [-114.02428425152348, 30.422880851187223], [-114.02532858489056, 30.427979972806046], [-114.0309854063872, 30.429708669358], [-114.03559748454398, 30.42633820100407], [-114.03455275226806, 30.421239202140075], [-114.02889634071316, 30.41951054886061]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f1dfffff', 8,
            30.41778, -114.02324,
            56.5, 'Moderado',
            0.0, 0.835,
            0.403, 0.7,
            0.85, 0.3,
            157.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02219584620823, 30.41268226066601], [-114.01758374613557, 30.416052396934322], [-114.01862774931281, 30.421151753529216], [-114.02428425152348, 30.422880851187223], [-114.02889634071316, 30.41951054886061], [-114.02785193860618, 30.41441131494885], [-114.02219584620823, 30.41268226066601]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f03fffff', 8,
            30.41942, -114.01297,
            56.48, 'Moderado',
            0.0, 0.83,
            0.409, 0.7,
            0.85, 0.3,
            156.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01192756333032, 30.414322898360286], [-114.00731497403434, 30.41769271289602], [-114.00835857816804, 30.42279219203382], [-114.01401517067225, 30.42452173410754], [-114.01862774931281, 30.421151753529216], [-114.01758374613557, 30.416052396934322], [-114.01192756333032, 30.414322898360286]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f07fffff', 8,
            30.42106, -114.0027,
            56.51, 'Moderado',
            0.0, 0.825,
            0.417, 0.7,
            0.85, 0.3,
            155.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00165870118393, 30.415962769993712], [-113.99704562291312, 30.419332262619534], [-113.99808882788956, 30.42443186415993], [-114.00374551032506, 30.42616185068648], [-114.00835857816804, 30.42279219203382], [-114.00731497403434, 30.41769271289602], [-114.00165870118393, 30.415962769993712]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f2bfffff', 8,
            30.4227, -113.99243,
            56.56, 'Moderado',
            0.0, 0.82,
            0.428, 0.7,
            0.85, 0.3,
            154.4, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99138926037978, 30.417601875351917], [-113.98677569338275, 30.420971045890564], [-113.98781849908828, 30.42607076969325], [-113.99347527109272, 30.427801200709613], [-113.99808882788956, 30.42443186415993], [-113.99704562291312, 30.419332262619534], [-113.99138926037978, 30.417601875351917]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f21fffff', 8,
            30.42434, -113.98216,
            56.66, 'Moderado',
            0.0, 0.815,
            0.44, 0.7,
            0.85, 0.3,
            153.41, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98111924152884, 30.419240214220746], [-113.9765051860544, 30.422609062495], [-113.97754759237542, 30.42770890841964], [-113.98320445358635, 30.429439783962682], [-113.98781849908828, 30.42607076969325], [-113.98677569338275, 30.420971045890564], [-113.98111924152884, 30.419240214220746]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f25fffff', 8,
            30.42598, -113.97189,
            56.78, 'Moderado',
            0.0, 0.81,
            0.455, 0.7,
            0.85, 0.3,
            152.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97084864524233, 30.42087778638617], [-113.96623410153934, 30.4242463122189], [-113.9672761083623, 30.429346280125102], [-113.97293305841724, 30.431077600231625], [-113.97754759237542, 30.42770890841964], [-113.9765051860544, 30.422609062495], [-113.97084864524233, 30.42087778638617]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512899fffff', 8,
            30.42761, -113.96162,
            56.94, 'Moderado',
            0.0, 0.805,
            0.473, 0.7,
            0.85, 0.3,
            151.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9605774721316, 30.422514591634354], [-113.95596244044913, 30.425882794848494], [-113.95700404766056, 30.430982884595842], [-113.9626610861969, 30.432714649302532], [-113.9672761083623, 30.429346280125102], [-113.96623410153934, 30.4242463122189], [-113.9605774721316, 30.422514591634354]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '884851289dfffff', 8,
            30.42925, -113.95135,
            57.12, 'Moderado',
            0.0, 0.8,
            0.492, 0.7,
            0.85, 0.3,
            150.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95030572280827, 30.424150629751615], [-113.94569020339551, 30.427518510170135], [-113.946731410882, 30.432618721618187], [-113.95238853753708, 30.434350930961653], [-113.95700404766056, 30.430982884595842], [-113.95596244044913, 30.425882794848494], [-113.95030572280827, 30.424150629751615]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512883fffff', 8,
            30.43089, -113.94107,
            57.32, 'Moderado',
            0.0, 0.795,
            0.512, 0.7,
            0.85, 0.3,
            149.47, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94003339788419, 30.42578590052443], [-113.93541739099045, 30.429153457970404], [-113.93645819863862, 30.434253790978676], [-113.94211541304969, 30.43598644499539], [-113.946731410882, 30.432618721618187], [-113.94569020339551, 30.427518510170135], [-113.94003339788419, 30.42578590052443]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512887fffff', 8,
            30.43252, -113.9308,
            57.55, 'Moderado',
            0.0, 0.789,
            0.534, 0.7,
            0.85, 0.3,
            148.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92976049797139, 30.427420403739436], [-113.92514400384616, 30.430787638035998], [-113.92618441154269, 30.43588809246398], [-113.93184171334696, 30.43762119119034], [-113.93645819863862, 30.434253790978676], [-113.93541739099045, 30.429153457970404], [-113.92976049797139, 30.427420403739436]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128bdfffff', 8,
            30.44099, -113.92722,
            57.12, 'Moderado',
            0.0, 0.762,
            0.542, 0.7,
            0.85, 0.3,
            148.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92618441154269, 30.43588809246398], [-113.92156743904121, 30.43925516933324], [-113.92260777706852, 30.444355510782593], [-113.92826548767275, 30.44608865402621], [-113.93288245141882, 30.442721411288574], [-113.93184171334696, 30.43762119119034], [-113.92618441154269, 30.43588809246398]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128b5fffff', 8,
            30.44946, -113.92365,
            56.67, 'Moderado',
            0.0, 0.733,
            0.551, 0.7,
            0.85, 0.3,
            148.52, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92260777706852, 30.444355510782593], [-113.91799032613434, 30.447722429984857], [-113.91903059445075, 30.45282265823772], [-113.9246887138697, 30.45455584602046], [-113.92930615612666, 30.45118876099655], [-113.92826548767275, 30.44608865402621], [-113.92260777706852, 30.444355510782593]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e924bfffff', 8,
            30.45792, -113.92007,
            56.21, 'Moderado',
            0.0, 0.704,
            0.559, 0.7,
            0.85, 0.3,
            148.54, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91903059445075, 30.45282265823772], [-113.91441266502746, 30.456189419533292], [-113.91545286359124, 30.461289534371872], [-113.92111139183966, 30.463022766715614], [-113.92572931266396, 30.459655839645105], [-113.9246887138697, 30.45455584602046], [-113.91903059445075, 30.45282265823772]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9243fffff', 8,
            30.46639, -113.91649,
            55.75, 'Moderado',
            0.0, 0.675,
            0.567, 0.7,
            0.85, 0.3,
            148.57, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91545286359124, 30.461289534371872], [-113.9108344556224, 30.46465613752107], [-113.91187458439187, 30.46975613872758], [-113.9175335214845, 30.471489415654215], [-113.9221519209326, 30.468122646776777], [-113.92111139183966, 30.463022766715614], [-113.91545286359124, 30.461289534371872]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9209fffff', 8,
            30.47486, -113.91291,
            55.29, 'Moderado',
            0.0, 0.645,
            0.576, 0.7,
            0.85, 0.3,
            148.6, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91187458439187, 30.46975613872758], [-113.90725569782107, 30.473122583490756], [-113.90829575675447, 30.47822247084745], [-113.91395510270603, 30.479955792378885], [-113.9185739808344, 30.476589181934155], [-113.9175335214845, 30.471489415654215], [-113.91187458439187, 30.46975613872758]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9201fffff', 8,
            30.48332, -113.90934,
            54.82, 'Moderado',
            0.0, 0.615,
            0.584, 0.7,
            0.85, 0.3,
            148.65, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.90829575675447, 30.47822247084745], [-113.9036763915253, 30.48158875698495], [-113.90471638058088, 30.48668853027412], [-113.91037613540607, 30.488421896432296], [-113.91499549227117, 30.485055444659903], [-113.91395510270603, 30.479955792378885], [-113.90829575675447, 30.47822247084745]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9207fffff', 8,
            30.49179, -113.90576,
            54.37, 'Moderado',
            0.0, 0.586,
            0.593, 0.7,
            0.85, 0.3,
            148.7, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.90471638058088, 30.48668853027412], [-113.9000965366369, 30.490054657546338], [-113.90113645577293, 30.4951543165503], [-113.90679661948643, 30.496887727357144], [-113.91141645514472, 30.493521434496696], [-113.91037613540607, 30.488421896432296], [-113.90471638058088, 30.48668853027412]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e923dfffff', 8,
            30.50025, -113.90218,
            53.92, 'Moderado',
            0.0, 0.557,
            0.602, 0.7,
            0.85, 0.3,
            148.75, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.90113645577293, 30.4951543165503], [-113.89651613305772, 30.498520284717635], [-113.89755598223243, 30.503619829218728], [-113.9032165548489, 30.505353284696202], [-113.90783686935681, 30.50198715098728], [-113.90679661948643, 30.496887727357144], [-113.90113645577293, 30.4951543165503]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9235fffff', 8,
            30.50872, -113.8986,
            53.49, 'Moderado',
            0.0, 0.529,
            0.611, 0.7,
            0.85, 0.3,
            148.82, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.89755598223243, 30.503619829218728], [-113.89293518068959, 30.506985638041595], [-113.89397495986117, 30.512085067822216], [-113.89963594139525, 30.513818567992296], [-113.90425673480927, 30.510452593674465], [-113.9032165548489, 30.505353284696202], [-113.89755598223243, 30.503619829218728]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e904bfffff', 8,
            30.51718, -113.89501,
            53.08, 'Moderado',
            0.0, 0.502,
            0.619, 0.7,
            0.85, 0.3,
            148.89, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.89397495986117, 30.512085067822216], [-113.8893536794343, 30.515450717061054], [-113.89039338856095, 30.520550031903625], [-113.89605477902728, 30.52228357678828], [-113.90067605140382, 30.518917762101093], [-113.89963594139525, 30.513818567992296], [-113.89397495986117, 30.512085067822216]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e905dfffff', 8,
            30.52402, -113.90172,
            52.4, 'Moderado',
            0.0, 0.48,
            0.603, 0.7,
            0.85, 0.3,
            149.89, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.90067605140382, 30.518917762101093], [-113.89605477902728, 30.52228357678828], [-113.89709481904222, 30.527382655810083], [-113.90275653232634, 30.529115799353665], [-113.90737779650254, 30.52574981924852], [-113.90633735562587, 30.520650861032447], [-113.90067605140382, 30.518917762101093]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9051fffff', 8,
            30.53085, -113.90842,
            51.75, 'Moderado',
            0.0, 0.46,
            0.586, 0.7,
            0.85, 0.3,
            150.9, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.90737779650254, 30.52574981924852], [-113.90275653232634, 30.529115799353665], [-113.90379690326074, 30.534214642333836], [-113.90945893924373, 30.53594738434586], [-113.91408019506953, 30.53258123885314], [-113.91303942329364, 30.527482516750645], [-113.90737779650254, 30.52574981924852]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9053fffff', 8,
            30.53768, -113.91512,
            51.11, 'Moderado',
            0.0, 0.44,
            0.57, 0.7,
            0.85, 0.3,
            151.91, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91408019506953, 30.53258123885314], [-113.90945893924373, 30.53594738434586], [-113.91049964112871, 30.541045991063562], [-113.91616199969162, 30.542778331353635], [-113.92078324701694, 30.539412020503736], [-113.91974214431075, 30.534313534735617], [-113.91408019506953, 30.53258123885314]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92a5fffff', 8,
            30.54451, -113.92182,
            50.51, 'Moderado',
            0.0, 0.422,
            0.555, 0.7,
            0.85, 0.3,
            152.92, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92078324701694, 30.539412020503736], [-113.91616199969162, 30.542778331353635], [-113.91720303255829, 30.5478767015881], [-113.9228657135821, 30.549608639965893], [-113.9274869522568, 30.54624216378925], [-113.92644551858923, 30.541143914576246], [-113.92078324701694, 30.539412020503736]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e92a7fffff', 8,
            30.55134, -113.92853,
            49.92, 'Bajo',
            0.0, 0.404,
            0.539, 0.7,
            0.85, 0.3,
            153.93, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9274869522568, 30.54624216378925], [-113.9228657135821, 30.549608639965893], [-113.92390707746152, 30.554706773496417], [-113.92957008082713, 30.55643830977165], [-113.93419131070101, 30.553071668298717], [-113.93314954604107, 30.547973655861522], [-113.9274869522568, 30.54624216378925]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e90c9fffff', 8,
            30.55817, -113.93523,
            49.37, 'Bajo',
            0.0, 0.388,
            0.525, 0.7,
            0.85, 0.3,
            154.94, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93419131070101, 30.553071668298717], [-113.92957008082713, 30.55643830977165], [-113.93061177575039, 30.561536206377575], [-113.93627510133864, 30.563267340360074], [-113.9408963222615, 30.55990053362132], [-113.93985422657812, 30.554802758180557], [-113.93419131070101, 30.553071668298717]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e90cbfffff', 8,
            30.565, -113.94194,
            48.86, 'Bajo',
            0.0, 0.372,
            0.51, 0.7,
            0.85, 0.3,
            155.96, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9408963222615, 30.55990053362132], [-113.93627510133864, 30.563267340360074], [-113.93731712733675, 30.5683649998208], [-113.94298077502839, 30.570095731320468], [-113.94760198684996, 30.566728759346365], [-113.94655956011218, 30.561631221122607], [-113.9408963222615, 30.55990053362132]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e90ddfffff', 8,
            30.57183, -113.94864,
            48.38, 'Bajo',
            0.0, 0.359,
            0.497, 0.7,
            0.85, 0.3,
            156.97, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94760198684996, 30.566728759346365], [-113.94298077502839, 30.570095731320468], [-113.9440231321324, 30.575193153415448], [-113.94968710180817, 30.576923482242236], [-113.95430830437815, 30.573556345063277], [-113.95326554655497, 30.568459044277063], [-113.94760198684996, 30.566728759346365]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e90d1fffff', 8,
            30.57865, -113.95535,
            47.93, 'Bajo',
            0.0, 0.346,
            0.484, 0.7,
            0.85, 0.3,
            157.98, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.95430830437815, 30.573556345063277], [-113.94968710180817, 30.576923482242236], [-113.95072979004904, 30.582020666750992], [-113.95639408158955, 30.58375059271494], [-113.96101527475759, 30.580383290361667], [-113.95997218581809, 30.57528622723343], [-113.95430830437815, 30.573556345063277]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e90d3fffff', 8,
            30.58548, -113.96206,
            47.53, 'Bajo',
            0.0, 0.335,
            0.472, 0.7,
            0.85, 0.3,
            159.0, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.96101527475759, 30.580383290361667], [-113.95639408158955, 30.58375059271494], [-113.95743710099828, 30.58884753941704], [-113.96310171428412, 30.590577062328265], [-113.96772289789982, 30.587209594831204], [-113.96667947781306, 30.582112769581368], [-113.96101527475759, 30.580383290361667]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e972dfffff', 8,
            30.58384, -113.97234,
            47.32, 'Bajo',
            0.0, 0.337,
            0.455, 0.7,
            0.85, 0.3,
            159.92, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97130018168264, 30.57874514198883], [-113.96667947781306, 30.582112769581368], [-113.96772289789982, 30.587209594831204], [-113.97338742245131, 30.588938670910636], [-113.97800811653988, 30.585570878158514], [-113.97696429588903, 30.5804741745012], [-113.97130018168264, 30.57874514198883]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9729fffff', 8,
            30.5822, -113.98263,
            47.15, 'Bajo',
            0.0, 0.34,
            0.44, 0.7,
            0.85, 0.3,
            160.84, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9815845102101, 30.577106221846655], [-113.97696429588903, 30.5804741745012], [-113.97800811653988, 30.585570878158514], [-113.983672551993, 30.587299507443156], [-113.98829275630445, 30.58393138961327], [-113.98724853520348, 30.578834807688725], [-113.9815845102101, 30.577106221846655]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9705fffff', 8,
            30.58056, -113.99291,
            47.01, 'Bajo',
            0.0, 0.343,
            0.427, 0.7,
            0.85, 0.3,
            161.77, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99186825972615, 30.575466530149477], [-113.98724853520348, 30.578834807688725], [-113.98829275630445, 30.58393138961327], [-113.9939571022952, 30.585659572140234], [-113.99857681657966, 30.582291129409956], [-113.99753219514265, 30.57719466935838], [-113.99186825972615, 30.575466530149477]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9701fffff', 8,
            30.57892, -114.0032,
            46.91, 'Bajo',
            0.0, 0.346,
            0.417, 0.7,
            0.85, 0.3,
            162.7, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00215142961714, 30.57382606711181], [-113.99753219514265, 30.57719466935838], [-113.99857681657966, 30.582291129409956], [-114.00424107274418, 30.58401886521644], [-114.00886029675192, 30.580650097763208], [-114.00781527509298, 30.575553759724777], [-114.00215142961714, 30.57382606711181]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e970bfffff', 8,
            30.57728, -114.01348,
            46.85, 'Bajo',
            0.0, 0.348,
            0.409, 0.7,
            0.85, 0.3,
            163.63, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01243401926969, 30.572184832948327], [-114.00781527509298, 30.575553759724777], [-114.00886029675192, 30.580650097763208], [-114.01452446272638, 30.58237738688653], [-114.01914319620784, 30.57900829488784], [-114.01809777444117, 30.573912079002685], [-114.01243401926969, 30.572184832948327]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9757fffff', 8,
            30.57564, -114.02376,
            46.83, 'Bajo',
            0.0, 0.351,
            0.403, 0.7,
            0.85, 0.3,
            164.57, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02271602807059, 30.570542827873886], [-114.01809777444117, 30.573912079002685], [-114.01914319620784, 30.57900829488784], [-114.02480727162855, 30.58073513736541], [-114.02942551433425, 30.57736572099881], [-114.02837969257408, 30.572269627407064], [-114.02271602807059, 30.570542827873886]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9753fffff', 8,
            30.574, -114.03404,
            46.85, 'Bajo',
            0.0, 0.354,
            0.4, 0.7,
            0.85, 0.3,
            165.5, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03299745540686, 30.568900052103466], [-114.02837969257408, 30.572269627407064], [-114.02942551433425, 30.57736572099881], [-114.03508949883754, 30.579092116868136], [-114.03970725051819, 30.57572237631129], [-114.03866102887882, 30.570626405152993], [-114.03299745540686, 30.568900052103466]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e962dfffff', 8,
            30.57235, -114.04432,
            46.91, 'Bajo',
            0.0, 0.358,
            0.4, 0.7,
            0.85, 0.3,
            166.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04327830066576, 30.56725650585228], [-114.03866102887882, 30.570626405152993], [-114.03970725051819, 30.57572237631129], [-114.04537114374048, 30.57744832560997], [-114.0499884041469, 30.57407826104055], [-114.0489417827427, 30.568982412455753], [-114.04327830066576, 30.56725650585228]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9629fffff', 8,
            30.57071, -114.05461,
            47.01, 'Bajo',
            0.0, 0.361,
            0.403, 0.7,
            0.85, 0.3,
            167.39, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05355856323474, 30.565612189335624], [-114.0489417827427, 30.568982412455753], [-114.0499884041469, 30.57407826104055], [-114.05565220572475, 30.57580376380631], [-114.06026897460792, 30.57243337540209], [-114.0592219535533, 30.567337649530803], [-114.05355856323474, 30.565612189335624]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9605fffff', 8,
            30.56906, -114.06489,
            47.15, 'Bajo',
            0.0, 0.364,
            0.408, 0.7,
            0.85, 0.3,
            168.33, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.0638382425015, 30.56396710276902], [-114.0592219535533, 30.567337649530803], [-114.06026897460792, 30.57243337540209], [-114.0659326841779, 30.57415843167271], [-114.07054896128895, 30.570787719611527], [-114.06950154069837, 30.565692116593723], [-114.0638382425015, 30.56396710276902]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e960dfffff', 8,
            30.5606, -114.06845,
            47.55, 'Bajo',
            0.0, 0.382,
            0.41, 0.7,
            0.85, 0.3,
            168.28, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06740696191929, 30.555500556277188], [-114.0627911528489, 30.55887126115706], [-114.0638382425015, 30.56396710276902], [-114.06950154069837, 30.565692116593723], [-114.07411733785393, 30.56232124636815], [-114.07306984875866, 30.557225527678177], [-114.06740696191929, 30.555500556277188]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9647fffff', 8,
            30.55213, -114.07202,
            47.99, 'Bajo',
            0.0, 0.402,
            0.413, 0.7,
            0.85, 0.3,
            168.24, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07097513296004, 30.54703373638325], [-114.06635980371028, 30.55040459914175], [-114.06740696191929, 30.555500556277188], [-114.07306984875866, 30.557225527678177], [-114.07768516601598, 30.553854499527688], [-114.07663760845756, 30.54875866538277], [-114.07097513296004, 30.54703373638325]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9641fffff', 8,
            30.54366, -114.07559,
            48.47, 'Bajo',
            0.0, 0.424,
            0.416, 0.7,
            0.85, 0.3,
            168.2, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07454275572246, 30.53856664354397], [-114.06992790623617, 30.541937663941614], [-114.07097513296004, 30.54703373638325], [-114.07663760845756, 30.54875866538277], [-114.08125244587382, 30.54538747954684], [-114.08020481989377, 30.540291530164243], [-114.07454275572246, 30.53856664354397]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9649fffff', 8,
            30.5352, -114.07916,
            48.98, 'Bajo',
            0.0, 0.447,
            0.419, 0.7,
            0.85, 0.3,
            168.16, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07810983030524, 30.530099278216145], [-114.07349546052528, 30.53347045601343], [-114.07454275572246, 30.53856664354397], [-114.08020481989377, 30.540291530164243], [-114.08481917752616, 30.53692018688235], [-114.083771483166, 30.531824122479364], [-114.07810983030524, 30.530099278216145]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ca3fffff', 8,
            30.52673, -114.08272,
            49.53, 'Bajo',
            0.0, 0.472,
            0.423, 0.7,
            0.85, 0.3,
            168.14, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.08167635680708, 30.521631640856633], [-114.07706246667628, 30.525002975814022], [-114.07810983030524, 30.530099278216145], [-114.083771483166, 30.531824122479364], [-114.08838536107176, 30.52845262199103], [-114.08733759837298, 30.523356442784983], [-114.08167635680708, 30.521631640856633]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512cabfffff', 8,
            30.51826, -114.08629,
            50.11, 'Moderado',
            0.0, 0.498,
            0.427, 0.7,
            0.85, 0.3,
            168.12, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.08524233532665, 30.513163731922347], [-114.08062892478782, 30.516535223800293], [-114.08167635680708, 30.521631640856633], [-114.08733759837298, 30.523356442784983], [-114.09195099660931, 30.51998478532973], [-114.09090316561343, 30.514888491537985], [-114.08524233532665, 30.513163731922347]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c85fffff', 8,
            30.50979, -114.08986,
            50.72, 'Moderado',
            0.0, 0.526,
            0.431, 0.7,
            0.85, 0.3,
            168.1, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.08880776596264, 30.504695551870217], [-114.08419483495861, 30.508067200429174], [-114.08524233532665, 30.513163731922347], [-114.09090316561343, 30.514888491537985], [-114.0955160842375, 30.51151667735536], [-114.09446818498597, 30.5064202691953], [-114.08880776596264, 30.504695551870217]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c8dfffff', 8,
            30.50132, -114.09342,
            51.35, 'Moderado',
            0.0, 0.554,
            0.435, 0.7,
            0.85, 0.3,
            168.1, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.09237264881368, 30.496227101157263], [-114.08776019728727, 30.499598906157654], [-114.08880776596264, 30.504695551870217], [-114.09446818498597, 30.5064202691953], [-114.09908062405502, 30.50304829852488], [-114.0980326565893, 30.497951776213938], [-114.09237264881368, 30.496227101157263]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512cc7fffff', 8,
            30.49286, -114.09698,
            52.0, 'Moderado',
            0.0, 0.583,
            0.44, 0.7,
            0.85, 0.3,
            168.09, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.09593698397839, 30.48775838024055], [-114.09132501187244, 30.49113034144277], [-114.09237264881368, 30.496227101157263], [-114.0980326565893, 30.497951776213938], [-114.10264461616055, 30.49457964929529], [-114.10159658052208, 30.489483013050926], [-114.09593698397839, 30.48775838024055]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512cc1fffff', 8,
            30.48439, -114.10055,
            52.66, 'Moderado',
            0.0, 0.612,
            0.445, 0.7,
            0.85, 0.3,
            168.1, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.09950077155544, 30.479289389577175], [-114.09488927881274, 30.482661506741614], [-114.09593698397839, 30.48775838024055], [-114.10159658052208, 30.489483013050926], [-114.10620806065273, 30.486110730123666], [-114.10515995688293, 30.48101398016337], [-114.09950077155544, 30.479289389577175]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512ccdfffff', 8,
            30.47756, -114.09384,
            53.0, 'Moderado',
            0.0, 0.636,
            0.436, 0.7,
            0.85, 0.3,
            167.12, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.09279413070979, 30.47246740912815], [-114.08818262550538, 30.475839360498576], [-114.08923000022853, 30.480936471031647], [-114.09488927881274, 30.482661506741614], [-114.09950077155544, 30.479289389577175], [-114.09845299820678, 30.474192402511324], [-114.09279413070979, 30.47246740912815]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c1bfffff', 8,
            30.47074, -114.08714,
            53.35, 'Moderado',
            0.0, 0.659,
            0.427, 0.7,
            0.85, 0.3,
            166.15, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.08608813820555, 30.465644789186346], [-114.08147662068976, 30.469016574731576], [-114.08252366500068, 30.474113922078303], [-114.08818262550538, 30.475839360498576], [-114.09279413070979, 30.47246740912815], [-114.091746687752, 30.4673701851772], [-114.08608813820555, 30.465644789186346]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c19fffff', 8,
            30.46392, -114.08043,
            53.72, 'Moderado',
            0.0, 0.683,
            0.42, 0.7,
            0.85, 0.3,
            165.17, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07938279413243, 30.458821530161657], [-114.0747712644555, 30.462193149850524], [-114.07581797838455, 30.467290733790378], [-114.08147662068976, 30.469016574731576], [-114.08608813820555, 30.465644789186346], [-114.08504102560838, 30.46054732857083], [-114.07938279413243, 30.458821530161657]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c57fffff', 8,
            30.4571, -114.07372,
            54.1, 'Moderado',
            0.0, 0.707,
            0.414, 0.7,
            0.85, 0.3,
            164.2, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.07267809858, 30.451997632464092], [-114.0680665568922, 30.455369086265463], [-114.06911294046971, 30.460466906577818], [-114.0747712644555, 30.462193149850524], [-114.07938279413243, 30.458821530161657], [-114.07833601186553, 30.453723833102124], [-114.07267809858, 30.451997632464092]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c55fffff', 8,
            30.45027, -114.06702,
            54.5, 'Moderado',
            0.0, 0.73,
            0.409, 0.7,
            0.85, 0.3,
            163.23, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.06597405163784, 30.44517309650378], [-114.06136249808928, 30.44854438438654], [-114.06240855134563, 30.45364244085075], [-114.0680665568922, 30.455369086265463], [-114.07267809858, 30.451997632464092], [-114.07163164661308, 30.446899699181174], [-114.06597405163784, 30.44517309650378]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c43fffff', 8,
            30.44345, -114.06032,
            54.9, 'Moderado',
            0.0, 0.753,
            0.405, 0.7,
            0.85, 0.3,
            162.26, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05927065339529, 30.438347922691005], [-114.05465908813616, 30.441719044624048], [-114.05570481110175, 30.44681733701943], [-114.06136249808928, 30.44854438438654], [-114.06597405163784, 30.44517309650378], [-114.0649279299405, 30.440074927218177], [-114.05927065339529, 30.438347922691005]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c41fffff', 8,
            30.43662, -114.05361,
            55.31, 'Moderado',
            0.0, 0.776,
            0.402, 0.7,
            0.85, 0.3,
            161.29, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.05256790394176, 30.43152211143618], [-114.04795632712214, 30.43489306738841], [-114.04900171982739, 30.439991595494178], [-114.05465908813616, 30.441719044624048], [-114.05927065339529, 30.438347922691005], [-114.05822486193719, 30.433249517623455], [-114.05256790394176, 30.43152211143618]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512c4dfffff', 8,
            30.42979, -114.04691,
            55.72, 'Moderado',
            0.0, 0.798,
            0.401, 0.7,
            0.85, 0.3,
            160.32, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.04586580336645, 30.42469566314983], [-114.04125421513639, 30.4280664530902], [-114.04229927761173, 30.43316521668552], [-114.04795632712214, 30.43489306738841], [-114.05256790394176, 30.43152211143618], [-114.05152244269249, 30.426423470807478], [-114.04586580336645, 30.42469566314983]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f1bfffff', 8,
            30.42297, -114.04021,
            56.14, 'Moderado',
            0.0, 0.819,
            0.4, 0.7,
            0.85, 0.3,
            159.35, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03916435175857, 30.417868578242622], [-114.03455275226806, 30.421239202140075], [-114.03559748454398, 30.42633820100407], [-114.04125421513639, 30.4280664530902], [-114.04586580336645, 30.42469566314983], [-114.04482067229559, 30.419596787180822], [-114.03916435175857, 30.417868578242622]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f19fffff', 8,
            30.41614, -114.03351,
            56.55, 'Moderado',
            0.0, 0.84,
            0.4, 0.7,
            0.85, 0.3,
            158.38, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.03246354920712, 30.411040857125354], [-114.02785193860618, 30.41441131494885], [-114.02889634071316, 30.41951054886061], [-114.03455275226806, 30.421239202140075], [-114.03916435175857, 30.417868578242622], [-114.03811955083565, 30.412769467154227], [-114.03246354920712, 30.411040857125354]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f57fffff', 8,
            30.40931, -114.02681,
            56.97, 'Moderado',
            0.0, 0.859,
            0.402, 0.7,
            0.85, 0.3,
            157.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.02576339580116, 30.40421250020895], [-114.02115177423966, 30.407582791927485], [-114.02219584620823, 30.41268226066601], [-114.02785193860618, 30.41441131494885], [-114.03246354920712, 30.411040857125354], [-114.0314190784017, 30.405941511138533], [-114.02576339580116, 30.40421250020895]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f0bfffff', 8,
            30.41095, -114.01654,
            56.95, 'Moderado',
            0.0, 0.855,
            0.407, 0.7,
            0.85, 0.3,
            156.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.01549600111808, 30.405853336831267], [-114.01088389031237, 30.409223307010336], [-114.01192756333032, 30.414322898360286], [-114.01758374613557, 30.416052396934322], [-114.02219584620823, 30.41268226066601], [-114.02115177423966, 30.407582791927485], [-114.01549600111808, 30.405853336831267]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f01fffff', 8,
            30.41259, -114.00627,
            56.96, 'Moderado',
            0.0, 0.85,
            0.414, 0.7,
            0.85, 0.3,
            155.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-114.00522802703182, 30.40749340771037], [-114.00061542723031, 30.41086305617259], [-114.00165870118393, 30.415962769993712], [-114.00731497403434, 30.41769271289602], [-114.01192756333032, 30.414322898360286], [-114.01088389031237, 30.409223307010336], [-114.00522802703182, 30.40749340771037]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f05fffff', 8,
            30.41423, -113.996,
            57.01, 'Moderado',
            0.0, 0.845,
            0.424, 0.7,
            0.85, 0.3,
            154.42, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.99495947415295, 30.409132712631838], [-113.99034638560418, 30.412502039199936], [-113.99138926037978, 30.417601875351917], [-113.99704562291312, 30.419332262619534], [-114.00165870118393, 30.415962769993712], [-114.00061542723031, 30.41086305617259], [-113.99495947415295, 30.409132712631838]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f29fffff', 8,
            30.41587, -113.98573,
            57.1, 'Moderado',
            0.0, 0.841,
            0.436, 0.7,
            0.85, 0.3,
            153.43, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.98469034309221, 30.410771251381487], [-113.98007676604486, 30.41414025587825], [-113.98111924152884, 30.419240214220746], [-113.98677569338275, 30.420971045890564], [-113.99138926037978, 30.417601875351917], [-113.99034638560418, 30.412502039199936], [-113.98469034309221, 30.410771251381487]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512f2dfffff', 8,
            30.41751, -113.97546,
            57.21, 'Moderado',
            0.0, 0.836,
            0.45, 0.7,
            0.85, 0.3,
            152.44, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.97442063446061, 30.412409023745266], [-113.96980656916347, 30.41577770599354], [-113.97084864524233, 30.42087778638617], [-113.9765051860544, 30.422609062495], [-113.98111924152884, 30.419240214220746], [-113.98007676604486, 30.41414025587825], [-113.97442063446061, 30.412409023745266]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128d3fffff', 8,
            30.41915, -113.96519,
            57.36, 'Moderado',
            0.0, 0.831,
            0.466, 0.7,
            0.85, 0.3,
            151.45, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.96415034886934, 30.414046029509294], [-113.95953579557136, 30.417414389332006], [-113.9605774721316, 30.422514591634354], [-113.96623410153934, 30.4242463122189], [-113.97084864524233, 30.42087778638617], [-113.96980656916347, 30.41577770599354], [-113.96415034886934, 30.414046029509294]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128d7fffff', 8,
            30.42078, -113.95492,
            57.54, 'Moderado',
            0.0, 0.826,
            0.485, 0.7,
            0.85, 0.3,
            150.46, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.9538794869298, 30.41568226845988], [-113.94926444588006, 30.41905030567998], [-113.95030572280827, 30.424150629751615], [-113.95596244044913, 30.425882794848494], [-113.9605774721316, 30.422514591634354], [-113.95953579557136, 30.417414389332006], [-113.9538794869298, 30.41568226845988]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '884851288bfffff', 8,
            30.42242, -113.94465,
            57.74, 'Moderado',
            0.0, 0.821,
            0.505, 0.7,
            0.85, 0.3,
            149.48, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.94360804925363, 30.417317740383435], [-113.93899252070138, 30.420685454823985], [-113.94003339788419, 30.42578590052443], [-113.94569020339551, 30.427518510170135], [-113.95030572280827, 30.424150629751615], [-113.94926444588006, 30.41905030567998], [-113.94360804925363, 30.417317740383435]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512881fffff', 8,
            30.42405, -113.93438,
            57.97, 'Moderado',
            0.0, 0.816,
            0.527, 0.7,
            0.85, 0.3,
            148.49, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.93333603645267, 30.41895244506658], [-113.92872002064728, 30.422319836550702], [-113.92976049797139, 30.427420403739436], [-113.93541739099045, 30.429153457970404], [-113.94003339788419, 30.42578590052443], [-113.93899252070138, 30.420685454823985], [-113.93333603645267, 30.41895244506658]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '8848512885fffff', 8,
            30.42569, -113.9241,
            58.21, 'Moderado',
            0.0, 0.811,
            0.55, 0.7,
            0.85, 0.3,
            147.51, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.92306344913901, 30.420586382296133], [-113.91844694632996, 30.42395345064697], [-113.91948702368214, 30.429054139183467], [-113.92514400384616, 30.430787638035998], [-113.92976049797139, 30.427420403739436], [-113.92872002064728, 30.422319836550702], [-113.92306344913901, 30.420586382296133]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128abfffff', 8,
            30.43415, -113.92053,
            57.8, 'Moderado',
            0.0, 0.784,
            0.558, 0.7,
            0.85, 0.3,
            147.52, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91948702368214, 30.429054139183467], [-113.914870042575, 30.432421050153792], [-113.91591005020668, 30.437521625860935], [-113.92156743904121, 30.43925516933324], [-113.92618441154269, 30.43588809246398], [-113.92514400384616, 30.430787638035998], [-113.91948702368214, 30.429054139183467]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485128a3fffff', 8,
            30.44262, -113.91695,
            57.37, 'Moderado',
            0.0, 0.756,
            0.566, 0.7,
            0.85, 0.3,
            147.53, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91591005020668, 30.437521625860935], [-113.91129259074508, 30.44088837921101], [-113.91233252861458, 30.445988841870918], [-113.91799032613434, 30.447722429984857], [-113.92260777706852, 30.444355510782593], [-113.92156743904121, 30.43925516933324], [-113.91591005020668, 30.437521625860935]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9249fffff', 8,
            30.45109, -113.91337,
            56.92, 'Moderado',
            0.0, 0.728,
            0.575, 0.7,
            0.85, 0.3,
            147.55, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.91233252861458, 30.445988841870918], [-113.90771459074213, 30.449355437361035], [-113.90875445880776, 30.45445578675587], [-113.91441266502746, 30.456189419533292], [-113.91903059445075, 30.45282265823772], [-113.91799032613434, 30.447722429984857], [-113.91233252861458, 30.445988841870918]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;
INSERT INTO public.grilla_h3_riesgo (
            h3_index, resolucion, latitud_centroide, longitud_centroide, ierc_score, nivel_riesgo,
            amenaza_score, exposicion_score, sensibilidad_score, dependencia_score, biocultural_score,
            capacidad_adaptativa_score, distancia_proyecto_mas_cercano_km, geometry
        ) VALUES (
            '88485e9241fffff', 8,
            30.45956, -113.90979,
            56.47, 'Moderado',
            0.0, 0.698,
            0.583, 0.7,
            0.85, 0.3,
            147.58, ST_SetSRID(ST_GeomFromGeoJSON('{"type": "Polygon", "coordinates": [[[-113.90875445880776, 30.45445578675587], [-113.90413604246804, 30.457822224146337], [-113.90517584068807, 30.462922460058287], [-113.9108344556224, 30.46465613752107], [-113.91545286359124, 30.461289534371872], [-113.91441266502746, 30.456189419533292], [-113.90875445880776, 30.45445578675587]]]}'), 4326)
        ) ON CONFLICT (h3_index) DO NOTHING;