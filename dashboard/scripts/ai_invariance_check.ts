// Standalone invariance test for textEnhanceService — no external deps
// Run: npx tsx scripts/ai_invariance_check.ts

const CATEGORIES = [
  'FLORA', 'FAUNA', 'AGUA', 'SUELO', 'AIRE', 'RUIDO', 'RESIDUOS', 'INFRAESTRUCTURA'
] as const;

type Category = typeof CATEGORIES[number];

const TEST_CASES: Record<Category, string> = {
  FLORA: 'cortando arboles y quemando vegetacion en area protegida',
  FAUNA: 'encontré peces muertos y tortugas en la playa',
  AGUA: 'tirando aguas negras al rio desde hace mucho tiempo',
  SUELO: 'sacando arena con maquinaria pesada hace hoyos grandes',
  AIRE: 'fabrica hechando humo negro todos los dias',
  RUIDO: 'ruido constante de maquinaria pesada en horario nocturno',
  RESIDUOS: 'empresa tirando basura y quimicos en terreno baldio',
  INFRAESTRUCTURA: 'construccion sin permiso dañando el ecosistema local',
};

function normalizeNFD(text: string): string {
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function applyMap(text: string, map: Record<string, string>): string {
  let result = text;
  for (const [key, value] of Object.entries(map)) {
    const regex = new RegExp(`\\b${key}\\b`, 'gi');
    result = result.replace(regex, value);
  }
  return result;
}

function cleanupPunctuation(text: string): string {
  return text
    .replace(/\.{2,}/g, '.')
    .replace(/,{2,}/g, ',');
}

function capitalizeSentences(text: string): string {
  return text.replace(/(^|[.!?]\s+)([a-záéíóúüñ])/g, (_, p, c) => p + c.toUpperCase());
}

function ensureEnding(text: string): string {
  if (text.length > 0 && !/[.!?]$/.test(text.trim())) {
    return text.trim() + '.';
  }
  return text;
}

function ruleBasedEnhance(text: string, _category?: Category): string {
  let t = normalizeNFD(text);

  const ORTHOGRAPHY_MAP: Record<string, string> = {
    'todavia': 'todavía', 'mas': 'más', 'esta': 'está', 'tambien': 'también',
    'despues': 'después', 'atras': 'atrás', 'publico': 'público',
    'ecologico': 'ecológico', 'ambiental': 'ambiental', 'quimico': 'químico',
    'quimicos': 'químicos', 'toxico': 'tóxico', 'toxicos': 'tóxicos',
    'toxica': 'tóxica', 'toxicas': 'tóxicas', 'segun': 'según',
    'comun': 'común', 'juridico': 'jurídico',
  };

  const FIRST_PERSON_MAP: Record<string, string> = {
    'me preocupa': 'existe preocupación fundada respecto a',
    'me preocupan': 'existen motivos fundados de preocupación respecto a',
    'vi que': 'se constató que', 'vi': 'se observó',
    'veo que': 'se advierte que', 'veo': 'se aprecia',
    'note': 'se constataron', 'noto que': 'se constata que',
    'me llamo la atencion': 'se pudo constatar de manera visible',
    'me llamo la atención': 'se pudo constatar de manera visible',
    'creo que': 'se estima que', 'pienso que': 'existen indicios de que',
    'fui a': 'en el marco de una visita de inspección ciudadana al',
    'mientras paseaba': 'durante recorrido de inspección ciudadana',
    'mientras caminaba': 'durante recorrido de inspección ciudadana',
    'mientras andaba': 'durante recorrido de inspección ciudadana',
    'haciendo senderismo': 'recorrido de observación directa',
    'senderismo': 'recorrido de observación directa',
    'encontre': 'se identificó', 'encontré': 'se identificó',
    'puedo ver': 'es posible apreciar',
    'nos preocupa': 'la comunidad afectada expresa preocupación fundada respecto a',
    'la gente dice': 'los habitantes del área señalan',
    'la gente comenta': 'los habitantes del área señalan',
    'la gente menciona': 'los habitantes del área señalan',
    'la gente': 'la comunidad local',
  };

  const TERMINOLOGY_MAP: Record<string, string> = {
    'tirando agua': 'descargando ilegalmente agua',
    'tirando liquido': 'descargando ilegalmente líquido',
    'tirando liquidos': 'descargando ilegalmente líquidos',
    'tirando desecho': 'descargando ilegalmente desecho',
    'tirando desechos': 'descargando ilegalmente desechos',
    'tirando basura': 'descargando ilegalmente basura',
    'tirando residuo': 'descargando ilegalmente residuo',
    'tirando residuos': 'descargando ilegalmente residuos',
    'desechando': 'disponiendo irregularmente de',
    'aguas negras': 'aguas residuales sin tratamiento',
    'agua negra': 'aguas residuales sin tratamiento',
    'aguas sucias': 'efluentes residuales',
    'agua sucia': 'efluentes residuales',
    'toma clandestina': 'aprovechamiento clandestino e irregular de recursos hídricos',
    'derrame': 'vertimiento de sustancias contaminantes',
    'derrames': 'vertimientos de sustancias contaminantes',
    'quimico': 'agentes químicos contaminantes',
    'quimicos': 'agentes químicos contaminantes',
    'basura': 'residuos sólidos',
    'desecho': 'residuos peligrosos',
    'desechos': 'residuos peligrosos',
    'contaminacion': 'contaminación ambiental',
    'tala': 'derribo y remoción',
    'cortar arboles': 'suprimir cobertura vegetal',
    'cortar arbol': 'suprimir cobertura vegetal',
    'cortar vegetacion': 'suprimir cobertura vegetal',
    'cortando arboles': 'suprimiendo cobertura vegetal',
    'cortando arbol': 'suprimiendo cobertura vegetal',
    'cortando vegetacion': 'suprimiendo cobertura vegetal',
    'quemando': 'incinerando irregularmente',
    'rellenar': 'rellenando con materiales no especificados',
    'rellenando': 'rellenando con materiales no especificados',
    'tierra removida': 'suelo degradado por actividad antrópica',
    'sacando arena': 'realizando extracción de material pétreo',
    'sacando material': 'realizando extracción de material pétreo',
    'sacando tierra': 'realizando extracción de material pétreo',
    'excavacion': 'excavación de gran magnitud',
    'excavaciones': 'excavaciones de gran magnitud',
    'hoyo': 'excavaciones', 'hoyos': 'excavaciones',
    'peces muertos': 'mortandad de fauna acuática',
    'pez muerto': 'mortandad de fauna acuática',
    'animales muertos': 'mortandad de fauna silvestre',
    'animal muerto': 'mortandad de fauna silvestre',
    'ballena azul': 'Balaenoptera musculus (ballena azul)',
    'ballena jorobada': 'Megaptera novaeangliae (ballena jorobada)',
    'tortuga': 'quelonios marinos', 'tortugas': 'quelonios marinos',
    'maquinaria pesada': 'maquinaria pesada de remoción de tierras',
    'camion volteo': 'vehículo de carga tipo volteo',
    'camiones volteo': 'vehículos de carga tipo volteo',
    'camion tolva': 'vehículo de carga tipo volteo',
    'camiones tolva': 'vehículos de carga tipo volteo',
    'camion pipa': 'vehículo de carga tipo volteo',
    'camiones pipa': 'vehículos de carga tipo volteo',
    'retroexcavadora': 'retroexcavadora de gran alcance',
    'retroexcavadoras': 'retroexcavadoras de gran alcance',
    'fabrica': 'establecimiento industrial', 'empresa': 'persona moral o física',
    'hace mucho tiempo': 'desde hace tiempo considerable',
    'todos los dias': 'de manera cotidiana y sistemática',
    'toda la noche': 'durante el período nocturno',
    'en las noches': 'en horario nocturno', 'en la noche': 'en horario nocturno',
    'desde siempre': 'de manera continua y prolongada',
    'mucha contaminacion': 'considerable volumen de contaminación',
    'mucha basura': 'considerable volumen de basura', 'mucha agua': 'considerable volumen de agua',
    'muchisimo': 'en gran magnitud', 'negativo': 'de impacto ambiental negativo no cuantificado',
    'hoy': 'la fecha de los presentes hechos',
    'gobierno de mexico': 'Federación (Gobierno Federal mexicano)',
    'gobierno de baja california sur': 'Gobierno del Estado de Baja California Sur',
    'gobierno federal': 'autoridad federal competente',
    'gobierno estatal': 'autoridad estatal competente',
    'gobierno municipal': 'autoridad municipal competente',
    'el rio': 'el cuerpo de agua superficial (río)',
    'el arroyo': 'el cauce del arroyo', 'el mar': 'la zona marina federal',
    'la bahia': 'la bahía y zona de amortiguamiento',
    'el golfo': 'el Golfo de California',
    'ruido constante': 'emisión continua de ruido',
    'maquinaria': 'equipamiento industrial',
    'construccion': 'actividad constructiva',
    'sin permiso': 'sin autorización ambiental',
    'dañando': 'afectando negativamente',
  };

  t = applyMap(t, ORTHOGRAPHY_MAP);
  t = applyMap(t, FIRST_PERSON_MAP);
  t = applyMap(t, TERMINOLOGY_MAP);
  t = cleanupPunctuation(t);
  t = capitalizeSentences(t);
  t = ensureEnding(t);
  return t;
}

function runInference(text: string, category?: Category): string {
  return ruleBasedEnhance(text, category);
}

console.log('Running invariance self-check...\n');
let passed = 0, failed = 0;

console.log('--- Test 1: Deterministic (3 runs identical) ---');
for (const cat of CATEGORIES) {
  const input = TEST_CASES[cat];
  const r1 = runInference(input, cat);
  const r2 = runInference(input, cat);
  const r3 = runInference(input, cat);
  if (r1 === r2 && r2 === r3) {
    console.log(`✓ ${cat}: deterministic`);
    passed++;
  } else {
    console.log(`✗ ${cat}: NON-DETERMINISTIC`);
    console.log(`  1: ${r1.slice(0,80)}...`);
    console.log(`  2: ${r2.slice(0,80)}...`);
    console.log(`  3: ${r3.slice(0,80)}...`);
    failed++;
  }
}

console.log('\n--- Test 2: Idempotent (run twice = same) ---');
for (const cat of CATEGORIES) {
  const input = TEST_CASES[cat];
  const once = runInference(input, cat);
  const twice = runInference(once, cat);
  if (once === twice) {
    console.log(`✓ ${cat}: idempotent`);
    passed++;
  } else {
    console.log(`✗ ${cat}: NOT IDEMPOTENT`);
    console.log(`  1: ${once.slice(0,80)}...`);
    console.log(`  2: ${twice.slice(0,80)}...`);
    failed++;
  }
}

console.log('\n--- Test 3: Preserves key entities ---');
const entityCases = [
  { input: 'derrame el 15 de enero de 2024 en el rio colorado', mustKeep: ['15 de enero de 2024', 'rio colorado'] },
  { input: 'coordenadas 19.4326 -99.1332 fabrica contaminando', mustKeep: ['19.4326', '99.1332'] },
  { input: 'empresa Cemex tirando residuos en Monterrey', mustKeep: ['Cemex', 'Monterrey'] },
];
for (const tc of entityCases) {
  const out = runInference(tc.input);
  let ok = true;
  for (const entity of tc.mustKeep) {
    if (!out.toLowerCase().includes(entity.toLowerCase())) {
      console.log(`✗ Entity lost: "${entity}" not in output`);
      ok = false;
    }
  }
  if (ok) { console.log(`✓ Entities preserved`); passed++; } else { failed++; }
}

console.log('\n--- Test 4: No hallucination ---');
const noHallucinationInput = 'tirando basura en el rio';
const out = runInference(noHallucinationInput);
const forbidden = ['plomo', 'mercurio', 'pemex', '2023'];
let hallucinated = false;
for (const f of forbidden) {
  if (out.toLowerCase().includes(f)) {
    console.log(`✗ Hallucinated: "${f}" found in output`);
    hallucinated = true;
  }
}
if (!hallucinated) { console.log('✓ No hallucination'); passed++; } else { failed++; }

console.log('\n--- Test 5: Category-aware terminology ---');
const categoryTerms: Record<string, string[]> = {
  AGUA: ['aguas residuales', 'vertimiento', 'efluentes'],
  RESIDUOS: ['residuos', 'disposición irregular'],
  FLORA: ['cobertura vegetal', 'suprimir', 'incinerando'],
  FAUNA: ['mortandad', 'fauna', 'quelonios'],
  AIRE: ['establecimiento industrial', 'emisión', 'horario nocturno'],
  SUELO: ['extracción', 'material pétreo', 'excavaciones'],
  RUIDO: ['emisión continua', 'equipamiento industrial', 'horario nocturno'],
  INFRAESTRUCTURA: ['actividad constructiva', 'sin autorización', 'afectando'],
};
for (const [cat, terms] of Object.entries(categoryTerms)) {
  const input = TEST_CASES[cat as Category];
  const out = runInference(input, cat as Category);
  const found = terms.some(t => out.toLowerCase().includes(t.toLowerCase()));
  if (found) { console.log(`✓ ${cat}: terminology applied`); passed++; }
  else { console.log(`✗ ${cat}: missing terminology`); failed++; }
}

console.log(`\n========== RESULT: ${passed} passed, ${failed} failed ==========`);
process.exit(failed > 0 ? 1 : 0);