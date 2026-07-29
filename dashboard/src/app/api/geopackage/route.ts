import { NextRequest, NextResponse } from 'next/server'
import path from 'path'
import fs from 'fs'
import Database from 'better-sqlite3'

const GPKG_V2_PATH = path.join(
  process.cwd(),
  '..',
  'deliverables',
  'v2_geopackage',
  'ierc_golfo_california_v2.gpkg'
)

const GPKG_V1_PATH = path.join(
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

    const targetPath = fs.existsSync(GPKG_V2_PATH) ? GPKG_V2_PATH : GPKG_V1_PATH
    const db = new Database(targetPath, { readonly: true })

    const validLayers = [
      'proyectos_gnl',
      'gasoductos_infraestructura_gnl',
      'localidades_estudio_ierc',
      'anp_habitats_criticos',
      'zonas_pesqueras_pangas',
      'riqueza_relativa_pesquera',
      'grilla_h3_riesgo',
      'campo_rutas_pesqueras',
      'campo_zonas_pesca_quincenales',
      'campo_sitios_bioculturales_comcaac',
      'campo_puntos_desembarque_costo',
      'campo_interaccion_fondeaderos_gnl',
    ]

    if (!validLayers.includes(layer)) {
      db.close()
      return NextResponse.json(
        { error: `Capa no válida. Capas permitidas: ${validLayers.join(', ')}` },
        { status: 400 }
      )
    }

    const countResult = db.prepare(`SELECT COUNT(*) as count FROM "${layer}"`).get() as { count: number }
    const rows = db.prepare(`SELECT * FROM "${layer}" LIMIT ?`).all(limit) as Record<string, unknown>[]

    db.close()

    return NextResponse.json({
      status: 'success',
      layer,
      total_features: countResult.count,
      returned_features: rows.length,
      crs: 'EPSG:4326',
      data_source: path.basename(targetPath),
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
