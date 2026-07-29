import { NextRequest, NextResponse } from 'next/server'
import path from 'path'
import Database from 'better-sqlite3'

const GPKG_PATH = path.join(
process.cwd(),
'..',
'deliverables',
'v1_geopackage',
'ierc_golfo_california.gpkg'
)

export async function GET(request: NextRequest) {
try {
const { searchParams } = new URL(request.url)
const layer = searchParams.get('layer') || 'proyectos_gnl'
const limitParam = searchParams.get('limit')
const limit = limitParam ? parseInt(limitParam, 10) : 1000

const db = new Database(GPKG_PATH, { readonly: true })

// Validar nombre de tabla para prevenir SQL Injection
const validLayers = ['proyectos_gnl', 'zonas_pesqueras_pangas', 'grilla_h3_riesgo', 'riqueza_relativa_pesquera']
if (!validLayers.includes(layer)) {
return NextResponse.json(
{ error: `Capa no válida. Capas permitidas: ${validLayers.join(', ')}` },
{ status: 400 }
)
}

// Consultar información de la capa
const countResult = db.prepare(`SELECT COUNT(*) as count FROM "${layer}"`).get() as { count: number }
const rows = db.prepare(`SELECT * FROM "${layer}" LIMIT ?`).all(limit) as Record<string, unknown>[]

db.close()

return NextResponse.json({
status: 'success',
layer,
total_features: countResult.count,
returned_features: rows.length,
crs: 'EPSG:4326',
data_source: 'ierc_golfo_california.gpkg (OGC GeoPackage v1.2)',
features: rows,
})
} catch (error: unknown) {
const message = error instanceof Error ? error.message : 'Error desconocido al consultar GeoPackage'
return NextResponse.json(
{ error: 'Falló la consulta al GeoPackage', details: message },
{ status: 500 }
)
}
}
