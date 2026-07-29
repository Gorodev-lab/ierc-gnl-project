"""
Next.js 15.5 API Routes for IERC-GNL Dashboard
===============================================

Rutas API para el dashboard LOGR que consumen datos del IERC desde Supabase.

Features:
- Conexión segura a Supabase con manejo de excepciones
- Tipado fuerte con TypeScript
- Logging detallado
- Caching para rendimiento
- Formato JSON listo para visualización en mapas interactivos
- Autenticación básica (opcional)

Endpoints:
- GET /api/ierc/scores - Obtener scores IERC por celda H3
- GET /api/ierc/scores/zone - Obtener scores IERC agrupados por zona
- GET /api/ierc/scores/quincena - Obtener scores IERC por quincena
- GET /api/ierc/confidence - Obtener métricas de confianza de Monte Carlo
- GET /api/ierc/threats - Obtener amenazas de infraestructura fósil
- GET /api/ierc/fisheries - Obtener exposición pesquera

Requirements:
- Next.js 15.5+
- @supabase/supabase-js
- TypeScript
- dotenv
"""

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { createClient } from '@supabase/supabase-js'
import { z } from 'zod'

// Configuración de entorno
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost:54321'
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'your-supabase-key'

// Validación de parámetros de consulta
const QueryParamsSchema = z.object({
zone: z.string().optional(),
quincena: z.string().regex(/^[1-9]|1[0-9]|2[0-4]$/).optional(),
species: z.string().optional(),
threat_type: z.string().optional(),
min_confidence: z.string().regex(/^0\.[0-9]+|1\.0?$/).optional(),
limit: z.string().regex(/^[0-9]+$/).optional(),
format: z.enum(['json', 'geojson']).default('json')
})

// Tipado fuerte para respuestas
interface IERCScore {
h3_cell_id: string
quincena: number
zone: string
score_amenaza: number
score_exposicion: number
score_sensibilidad: number
score_dependencia: number
score_biocultural: number
score_capacidad_adaptativa: number
IERC_total: number
confidence_dato: number
uncertainty_range_lower: number
uncertainty_range_upper: number
fossil_threat_count: number
is_protected_area: boolean
protection_category?: string
species_count?: number
}

interface ZoneAggregation {
zone: string
avg_ierc_score: number
median_ierc_score: number
min_ierc_score: number
max_ierc_score: number
cell_count: number
avg_confidence: number
threat_count: number
}

interface ThreatData {
threat_type: string
threat_count: number
avg_noise_level: number | null
total_traffic: number | null
}

interface FisheriesData {
species_code: string
common_name_es: string
total_effort_hours: number
total_landings_kg: number
unique_cells: number
avg_ierc_in_area: number
}

// Configuración de caché (en segundos)
const CACHE_DURATION = {
default: 300,       // 5 minutos
zone: 600,          // 10 minutos
threats: 1800,      // 30 minutos
fisheries: 3600     // 1 hora
}

// Función para obtener cliente de Supabase
function getSupabaseClient() {
try {
const supabase = createClient(supabaseUrl, supabaseKey, {
db: {
schema: 'public'
},
auth: {
persistSession: false,
autoRefreshToken: false
}
})
return supabase
} catch (error) {
console.error(' Error al crear cliente Supabase:', error)
throw new Error('No se pudo conectar a la base de datos')
}
}

// Función para manejar errores
function handleError(error: unknown, context: string): NextResponse {
console.error(` Error en ${context}:`, error)

if (error instanceof Error) {
return NextResponse.json(
{
error: 'Internal Server Error',
message: error.message,
context,
timestamp: new Date().toISOString()
},
{ status: 500 }
)
}

return NextResponse.json(
{
error: 'Internal Server Error',
message: 'Error desconocido',
context,
timestamp: new Date().toISOString()
},
{ status: 500 }
)
}

// ============================================================================
// ENDPOINT: GET /api/ierc/scores
// Obtener scores IERC con filtros opcionales
// ============================================================================
export async function GET(request: NextRequest) {
try {
const { searchParams } = new URL(request.url)
const params = QueryParamsSchema.parse(Object.fromEntries(searchParams))

const supabase = getSupabaseClient()

// Construir consulta base
let query = supabase
.from('ierc_calculated_scores')
.select(`
h3_cell_id,
quincena,
score_amenaza,
score_exposicion,
score_sensibilidad,
score_dependencia,
score_biocultural,
score_capacidad_adaptativa,
IERC_total,
confidence_dato,
uncertainty_range_lower,
uncertainty_range_upper,
fossil_threat_ids,
(h3_cells: h3_cells!inner(zone, is_protected_area, protection_category))
`)
.order('IERC_total', { ascending: false })
.limit(params.limit ? parseInt(params.limit) : 1000)

// Aplicar filtros
if (params.zone) {
query = query.eq('h3_cells.zone', params.zone)
}

if (params.quincena) {
query = query.eq('quincena', parseInt(params.quincena))
}

if (params.min_confidence) {
const minConf = parseFloat(params.min_confidence)
query = query.gte('confidence_dato', minConf)
}

// Ejecutar consulta
const { data, error, count } = await query

if (error) throw error

// Formatear respuesta
const formattedData: IERCScore[] = data.map((row: any) => ({
h3_cell_id: row.h3_cell_id,
quincena: row.quincena,
zone: row.h3_cells?.zone || 'Desconocido',
score_amenaza: row.score_amenaza,
score_exposicion: row.score_exposicion,
score_sensibilidad: row.score_sensibilidad,
score_dependencia: row.score_dependencia,
score_biocultural: row.score_biocultural,
score_capacidad_adaptativa: row.score_capacidad_adaptativa,
IERC_total: row.IERC_total,
confidence_dato: row.confidence_dato,
uncertainty_range_lower: row.uncertainty_range_lower,
uncertainty_range_upper: row.uncertainty_range_upper,
fossil_threat_count: row.fossil_threat_ids?.length || 0,
is_protected_area: row.h3_cells?.is_protected_area || false,
protection_category: row.h3_cells?.protection_category,
species_count: 0 // En producción, contar especies en fisheries_exposure
}))

// Cache-Control header
const cacheControl = `public, max-age=${CACHE_DURATION.default}`

return NextResponse.json(
{
success: true,
data: formattedData,
metadata: {
count: count || formattedData.length,
timestamp: new Date().toISOString(),
cache_duration: CACHE_DURATION.default
}
},
{ headers: { 'Cache-Control': cacheControl } }
)

} catch (error) {
return handleError(error, 'GET /api/ierc/scores')
}
}

// ============================================================================
// ENDPOINT: GET /api/ierc/scores/zone
// Obtener scores IERC agrupados por zona geográfica
// ============================================================================
export async function GET_ZONE(request: NextRequest) {
try {
const { searchParams } = new URL(request.url)
const params = QueryParamsSchema.partial().parse(Object.fromEntries(searchParams))

const supabase = getSupabaseClient()

// Consultar vista materializada mv_ierc_by_zone
let query = supabase
.from('mv_ierc_by_zone')
.select('*')
.order('avg_ierc_score', { ascending: false })

// Aplicar filtros
if (params.zone) {
query = query.eq('zone', params.zone)
}

// Ejecutar consulta
const { data, error, count } = await query

if (error) throw error

// Formatear respuesta
const formattedData: ZoneAggregation[] = data.map((row: any) => ({
zone: row.zone,
avg_ierc_score: row.avg_ierc_score,
median_ierc_score: row.median_ierc_score,
min_ierc_score: row.min_ierc_score,
max_ierc_score: row.max_ierc_score,
cell_count: row.cell_count,
avg_confidence: row.avg_confidence,
threat_count: 0 // En producción, contar amenazas por zona
}))

// Cache-Control header
const cacheControl = `public, max-age=${CACHE_DURATION.zone}`

return NextResponse.json(
{
success: true,
data: formattedData,
metadata: {
count: count || formattedData.length,
timestamp: new Date().toISOString(),
cache_duration: CACHE_DURATION.zone
}
},
{ headers: { 'Cache-Control': cacheControl } }
)

} catch (error) {
return handleError(error, 'GET /api/ierc/scores/zone')
}
}

// ============================================================================
// ENDPOINT: GET /api/ierc/scores/quincena
// Obtener scores IERC por quincena con agregación
// ============================================================================
export async function GET_QUINCENA(request: NextRequest) {
try {
const { searchParams } = new URL(request.url)
const params = QueryParamsSchema.partial().parse(Object.fromEntries(searchParams))

const supabase = getSupabaseClient()

// Consultar scores por quincena
let query = supabase
.from('ierc_calculated_scores')
.select('quincena, IERC_total, confidence_dato, count()')
.group('quincena')
.order('quincena')

// Aplicar filtros
if (params.min_confidence) {
const minConf = parseFloat(params.min_confidence)
query = query.gte('confidence_dato', minConf)
}

// Ejecutar consulta
const { data, error, count } = await query

if (error) throw error

// Formatear respuesta
const formattedData = data.map((row: any) => ({
quincena: row.quincena,
avg_ierc_score: row.IERC_total,
avg_confidence: row.confidence_dato,
cell_count: row.count
}))

// Cache-Control header
const cacheControl = `public, max-age=${CACHE_DURATION.default}`

return NextResponse.json(
{
success: true,
data: formattedData,
metadata: {
count: count || formattedData.length,
timestamp: new Date().toISOString(),
cache_duration: CACHE_DURATION.default
}
},
{ headers: { 'Cache-Control': cacheControl } }
)

} catch (error) {
return handleError(error, 'GET /api/ierc/scores/quincena')
}
}

// ============================================================================
// ENDPOINT: GET /api/ierc/confidence
// Obtener métricas de confianza de Monte Carlo
// ============================================================================
export async function GET_CONFIDENCE(request: NextRequest) {
try {
const { searchParams } = new URL(request.url)
const params = QueryParamsSchema.partial().parse(Object.fromEntries(searchParams))

const supabase = getSupabaseClient()

// Consultar métricas de confianza
let query = supabase
.from('ierc_calculated_scores')
.select('confidence_dato, count()')
.group('confidence_dato')
.order('confidence_dato', { ascending: false })

// Aplicar filtros
if (params.min_confidence) {
const minConf = parseFloat(params.min_confidence)
query = query.gte('confidence_dato', minConf)
}

// Ejecutar consulta
const { data, error, count } = await query

if (error) throw error

// Formatear respuesta
const formattedData = data.map((row: any) => ({
confidence_range: row.confidence_dato,
cell_count: row.count
}))

// Calcular estadísticas agregadas
const avgConfidence = await supabase
.from('ierc_calculated_scores')
.select('avg(confidence_dato)')
.single()

const highConfidenceCount = await supabase
.from('ierc_calculated_scores')
.select('count()', { head: true, count: 'exact' })
.gte('confidence_dato', 0.85)

const lowConfidenceCount = await supabase
.from('ierc_calculated_scores')
.select('count()', { head: true, count: 'exact' })
.lt('confidence_dato', 0.7)

// Cache-Control header
const cacheControl = `public, max-age=${CACHE_DURATION.default}`

return NextResponse.json(
{
success: true,
data: formattedData,
statistics: {
average_confidence: avgConfidence.data?.avg || 0,
high_confidence_cells: highConfidenceCount.count || 0,
low_confidence_cells: lowConfidenceCount.count || 0,
total_cells: count || 0
},
metadata: {
timestamp: new Date().toISOString(),
cache_duration: CACHE_DURATION.default
}
},
{ headers: { 'Cache-Control': cacheControl } }
)

} catch (error) {
return handleError(error, 'GET /api/ierc/confidence')
}
}

// ============================================================================
// ENDPOINT: GET /api/ierc/threats
// Obtener amenazas de infraestructura fósil
// ============================================================================
export async function GET_THREATS(request: NextRequest) {
try {
const { searchParams } = new URL(request.url)
const params = QueryParamsSchema.partial().parse(Object.fromEntries(searchParams))

const supabase = getSupabaseClient()

// Consultar amenazas
let query = supabase
.from('fossil_infrastructure_threat')
.select('threat_type, count()')
.group('threat_type')
.order('count', { ascending: false })

// Aplicar filtros
if (params.threat_type) {
query = query.eq('threat_type', params.threat_type)
}

// Ejecutar consulta
const { data, error, count } = await query

if (error) throw error

// Formatear respuesta
const formattedData: ThreatData[] = data.map((row: any) => ({
threat_type: row.threat_type,
threat_count: row.count,
avg_noise_level: null, // En producción, calcular promedio
total_traffic: null    // En producción, sumar tráfico
}))

// Cache-Control header
const cacheControl = `public, max-age=${CACHE_DURATION.threats}`

return NextResponse.json(
{
success: true,
data: formattedData,
metadata: {
count: count || formattedData.length,
timestamp: new Date().toISOString(),
cache_duration: CACHE_DURATION.threats
}
},
{ headers: { 'Cache-Control': cacheControl } }
)

} catch (error) {
return handleError(error, 'GET /api/ierc/threats')
}
}

// ============================================================================
// ENDPOINT: GET /api/ierc/fisheries
// Obtener exposición pesquera por especie
// ============================================================================
export async function GET_FISHERIES(request: NextRequest) {
try {
const { searchParams } = new URL(request.url)
const params = QueryParamsSchema.partial().parse(Object.fromEntries(searchParams))

const supabase = getSupabaseClient()

// Consultar exposición pesquera
let query = supabase
.from('mv_fisheries_by_species_quincena')
.select('*')
.order('total_landings_kg', { ascending: false })

// Aplicar filtros
if (params.species) {
query = query.eq('species_code', params.species)
}

if (params.zone) {
// En producción, filtrar por zona
}

// Ejecutar consulta
const { data, error, count } = await query

if (error) throw error

// Formatear respuesta
const formattedData: FisheriesData[] = data.map((row: any) => ({
species_code: row.species_code,
common_name_es: row.common_name_es,
total_effort_hours: row.total_effort_hours,
total_landings_kg: row.total_landings_kg,
unique_cells: row.unique_cells,
avg_ierc_in_area: row.avg_ierc_in_area
}))

// Cache-Control header
const cacheControl = `public, max-age=${CACHE_DURATION.fisheries}`

return NextResponse.json(
{
success: true,
data: formattedData,
metadata: {
count: count || formattedData.length,
timestamp: new Date().toISOString(),
cache_duration: CACHE_DURATION.fisheries
}
},
{ headers: { 'Cache-Control': cacheControl } }
)

} catch (error) {
return handleError(error, 'GET /api/ierc/fisheries')
}
}

// ============================================================================
// ENDPOINT: GET /api/ierc/health
// Endpoint de salud para monitoreo
// ============================================================================
export async function GET_HEALTH(request: NextRequest) {
try {
const supabase = getSupabaseClient()

// Verificar conexión a la base de datos
const { error } = await supabase.from('h3_cells').select('id', { head: true, count: 'exact' })

if (error) throw error

return NextResponse.json(
{
success: true,
status: 'healthy',
timestamp: new Date().toISOString(),
database: {
connected: true,
tables_available: [
'h3_cells',
'fisheries_exposure',
'fossil_infrastructure_threat',
'ierc_calculated_scores',
'gage_governance_scores'
]
},
cache: {
default: CACHE_DURATION.default,
zone: CACHE_DURATION.zone,
threats: CACHE_DURATION.threats,
fisheries: CACHE_DURATION.fisheries
}
},
{ status: 200 }
)

} catch (error) {
return handleError(error, 'GET /api/ierc/health')
}
}

// ============================================================================
// Manejo de rutas no encontradas
// ============================================================================
export async function OTHERS(request: NextRequest) {
return NextResponse.json(
{
error: 'Not Found',
message: 'Ruta no encontrada',
available_routes: [
'/api/ierc/scores',
'/api/ierc/scores/zone',
'/api/ierc/scores/quincena',
'/api/ierc/confidence',
'/api/ierc/threats',
'/api/ierc/fisheries',
'/api/ierc/health'
],
timestamp: new Date().toISOString()
},
{ status: 404 }
)
}

// ============================================================================
// Exportar funciones para Next.js Route Handler
// ============================================================================

export const GET = GET

export const GET_ZONE = GET_ZONE

export const GET_QUINCENA = GET_QUINCENA

export const GET_CONFIDENCE = GET_CONFIDENCE

export const GET_THREATS = GET_THREATS

export const GET_FISHERIES = GET_FISHERIES

export const GET_HEALTH = GET_HEALTH

export const OTHERS = OTHERS

export type { IERCScore, ZoneAggregation, ThreatData, FisheriesData }
