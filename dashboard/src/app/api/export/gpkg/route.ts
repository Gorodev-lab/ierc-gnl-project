import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  try {
    const filePath = path.join(
      process.cwd(),
      'public',
      'data',
      'ierc_golfo_california.gpkg'
    )

    if (!fs.existsSync(filePath)) {
      // Fallback check in deliverables
      const altPath = path.join(
        process.cwd(),
        '..',
        'deliverables',
        'v1_geopackage',
        'ierc_golfo_california.gpkg'
      )
      if (fs.existsSync(altPath)) {
        const fileBuffer = fs.readFileSync(altPath)
        return new NextResponse(fileBuffer, {
          headers: {
            'Content-Type': 'application/geopackage+sqlite3',
            'Content-Disposition':
              'attachment; filename="ierc_golfo_california_v1.1.gpkg"',
            'Cache-Control': 'public, max-age=3600',
          },
        })
      }

      return NextResponse.json(
        { error: 'Archivo GeoPackage v1.1 no encontrado en el servidor' },
        { status: 404 }
      )
    }

    const fileBuffer = fs.readFileSync(filePath)
    return new NextResponse(fileBuffer, {
      headers: {
        'Content-Type': 'application/geopackage+sqlite3',
        'Content-Disposition':
          'attachment; filename="ierc_golfo_california_v1.1.gpkg"',
        'Cache-Control': 'public, max-age=3600',
      },
    })
  } catch (error: unknown) {
    const message =
      error instanceof Error ? error.message : 'Error al procesar descarga GPKG'
    return NextResponse.json(
      { error: 'Falló la descarga del GeoPackage', details: message },
      { status: 500 }
    )
  }
}
