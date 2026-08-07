import { NextRequest, NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const layer = searchParams.get('layer') || 'proyectos_gnl'
    const limitParam = searchParams.get('limit')
    const limit = limitParam ? parseInt(limitParam, 10) : 1000

    const validLayers = [
        'proyectos_gnl',
        'gasoductos_infraestructura_gnl',
        'localidades_estudio_ierc',
        'anp_habitats_criticos',
        'zonas_pesqueras_pangas',
        'riqueza_relativa_pesquera',
        'grilla_h3_riesgo',
        'ierc_features_summary',
        'ductos_cnih',
      ]

    if (!validLayers.includes(layer)) {
      return NextResponse.json(
        { error: `Capa no válida. Capas permitidas: ${validLayers.join(', ')}` },
        { status: 400 }
      )
    }

    // Query count and features from Supabase
    const { data, count, error } = await supabase
      .from(layer)
      .select('*', { count: 'exact' })
      .limit(limit)

    if (error) {
      throw error
    }

    return NextResponse.json({
      status: 'success',
      layer,
      total_features: count || (data ? data.length : 0),
      returned_features: data ? data.length : 0,
      crs: 'EPSG:4326',
      data_source: 'Supabase PostgreSQL + PostGIS (ierc-gnl)',
      features: data || [],
    })
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Error desconocido al consultar Supabase'
    return NextResponse.json(
      { error: 'Falló la consulta a Supabase', details: message },
      { status: 500 }
    )
  }
}
