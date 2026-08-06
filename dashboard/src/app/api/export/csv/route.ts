import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

const LAYER_FILES: Record<string, string> = {
  proyectos_gnl: 'terminales_gnl_v3.geojson',
  poligonos_saguaro: 'saguaro_polygons_181v.geojson',
  capas_contexto: 'capas_contextuales.geojson',
  batimetria: 'batimetria_golfo.geojson',
  h3_riesgo: 'grilla_h3_riesgo.geojson',
  gfw_fishing: 'gfw_fishing_h3.geojson',
  pangas: 'zpesca_pangas_sample.geojson',
  buceo: 'zpesca_buceo_sample.geojson',
  chinchorro: 'zpesca_chinchorro_sample.geojson',
  redes: 'zpesca_redes_sample.geojson',
  manta: 'zpesca_redes_manta_camaron_sample.geojson',
  trampa: 'zpesca_trampa_sample.geojson',
  riqueza: 'riqueza_relativa_sample.geojson',
}

function escapeCsvCell(val: any): string {
  if (val === null || val === undefined) return ''
  let str = typeof val === 'object' ? JSON.stringify(val) : String(val)
  if (str.includes('"') || str.includes(',') || str.includes('\n') || str.includes('\r')) {
    str = str.replace(/"/g, '""')
    return `"${str}"`
  }
  return str
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const layer = searchParams.get('layer') || 'proyectos_gnl'

    const fileName = LAYER_FILES[layer]
    if (!fileName) {
      return NextResponse.json(
        {
          error: `Capa no válida. Capas permitidas: ${Object.keys(LAYER_FILES).join(', ')}`,
        },
        { status: 400 }
      )
    }

    const filePath = path.join(process.cwd(), 'public', 'data', fileName)
    if (!fs.existsSync(filePath)) {
      return NextResponse.json(
        { error: `Archivo de datos no encontrado para la capa: ${layer}` },
        { status: 404 }
      )
    }

    const rawData = fs.readFileSync(filePath, 'utf-8')
    const geojson = JSON.parse(rawData)

    const features: any[] = geojson.features || []
    if (features.length === 0) {
      return new NextResponse('\uFEFFno_data\n', {
        headers: {
          'Content-Type': 'text/csv; charset=utf-8',
          'Content-Disposition': `attachment; filename="${layer}_export.csv"`,
        },
      })
    }

    // Collect all unique property keys
    const propKeysSet = new Set<string>()
    features.forEach((f) => {
      if (f.properties) {
        Object.keys(f.properties).forEach((k) => propKeysSet.add(k))
      }
    })

    const propKeys = Array.from(propKeysSet)
    const headers = [...propKeys, 'longitude', 'latitude']

    const rows: string[] = []
    rows.push(headers.map(escapeCsvCell).join(','))

    features.forEach((f) => {
      const props = f.properties || {}
      const rowValues = propKeys.map((k) => props[k])

      // Extract geometry centroids if available
      let lon = ''
      let lat = ''
      if (f.geometry) {
        if (f.geometry.type === 'Point' && Array.isArray(f.geometry.coordinates)) {
          lon = f.geometry.coordinates[0]
          lat = f.geometry.coordinates[1]
        } else if (f.geometry.type === 'Polygon' && Array.isArray(f.geometry.coordinates[0]?.[0])) {
          // BBox center approximation
          const coords = f.geometry.coordinates[0]
          let sumLon = 0, sumLat = 0
          coords.forEach((c: number[]) => {
            sumLon += c[0]
            sumLat += c[1]
          })
          lon = (sumLon / coords.length).toFixed(6)
          lat = (sumLat / coords.length).toFixed(6)
        }
      }

      rowValues.push(lon, lat)
      rows.push(rowValues.map(escapeCsvCell).join(','))
    })

    // Prepend UTF-8 BOM for Excel / GIS compatibility
    const csvContent = '\uFEFF' + rows.join('\n')

    return new NextResponse(csvContent, {
      headers: {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': `attachment; filename="ierc_${layer}_export.csv"`,
        'Cache-Control': 'no-cache',
      },
    })
  } catch (error: unknown) {
    const message =
      error instanceof Error ? error.message : 'Error al exportar capa a CSV'
    return NextResponse.json(
      { error: 'Falló la generación del reporte CSV', details: message },
      { status: 500 }
    )
  }
}
