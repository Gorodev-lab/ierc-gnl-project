import { NextRequest, NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'


// Datos estáticos representativos de fallback v2.3
const FALLBACK_DATA = {
  inyecciones: [
    { punto: 'inj-01', descripcion: 'El Oro (Nodo 1)',           total_gj_inyectado_all: 8241500, avg_daily_gj_inyectado: 22578, days_with_data_iny: 3652, origen_principal_iny: 'nacional' },
    { punto: 'inj-02', descripcion: 'Guaymas (Nodo 7)',          total_gj_inyectado_all: 6890200, avg_daily_gj_inyectado: 18877, days_with_data_iny: 3650, origen_principal_iny: 'importación' },
    { punto: 'inj-03', descripcion: 'San Isidro (Nodo 14)',      total_gj_inyectado_all: 5102300, avg_daily_gj_inyectado: 13978, days_with_data_iny: 3651, origen_principal_iny: 'importación' },
    { punto: 'inj-04', descripcion: 'Puerto Libertad (Nodo 22)', total_gj_inyectado_all: 4783900, avg_daily_gj_inyectado: 13106, days_with_data_iny: 3652, origen_principal_iny: 'importación' },
    { punto: 'inj-05', descripcion: 'Topolobampo (Nodo 29)',     total_gj_inyectado_all: 3421100, avg_daily_gj_inyectado: 9373,  days_with_data_iny: 3648, origen_principal_iny: 'importación' },
  ],
  ductos: [
    { nombre: 'SISTRANGAS Norte-Sonora',   longitud_km: 892.3, empresa: 'CFE / CENAGAS',   tipo: 'Gas Natural',     integrado_sistrangas: true,  fuente_capa: 'integrados' },
    { nombre: 'Sierra Madre Occidental',   longitud_km: 804.1, empresa: 'TAG Pipelines',   tipo: 'Gas Natural',     integrado_sistrangas: true,  fuente_capa: 'integrados' },
    { nombre: 'Guaymas-El Oro',            longitud_km: 311.0, empresa: 'CENAGAS',         tipo: 'Gas Natural',     integrado_sistrangas: true,  fuente_capa: 'integrados' },
    { nombre: 'Puerto Libertad-Hermosillo',longitud_km: 241.5, empresa: 'IEnova / Sempra',  tipo: 'Gas Natural',     integrado_sistrangas: false, fuente_capa: 'no_integrados' },
    { nombre: 'Pacific Limited (FLNG)',    longitud_km: 188.7, empresa: 'Pacific Ltd.',     tipo: 'GNL (suspendido)',integrado_sistrangas: false, fuente_capa: 'pacific' },
    { nombre: 'Poliducto Mazatlán',        longitud_km: 156.4, empresa: 'PEMEX Logística', tipo: 'Petrolíferos',    integrado_sistrangas: false, fuente_capa: 'poliductos' },
  ],
  env_risk: [
    { punto: 'V022', descripcion: 'Puerto Libertad (Nodo 22)', total_sitios: 3, env_risk_score: 78.0, total_gj_all_years: 4783900 },
    { punto: 'V007', descripcion: 'Guaymas (Nodo 7)',          total_sitios: 5, env_risk_score: 71.0, total_gj_all_years: 6890200 },
    { punto: 'V029', descripcion: 'Topolobampo (Nodo 29)',     total_sitios: 2, env_risk_score: 64.0, total_gj_all_years: 3421100 },
    { punto: 'V001', descripcion: 'El Oro (Nodo 1)',           total_sitios: 1, env_risk_score: 48.0, total_gj_all_years: 8241500 },
  ],
}

export async function GET(request: NextRequest) {
  try {
    // Intentar conectar con el backend de Python FastAPI (puerto 8000)
    const response = await fetch('http://localhost:8000/gas-infra', {
      next: { revalidate: 60 }, // Cache por 60 segundos
      signal: AbortSignal.timeout(1500), // Timeout corto de 1.5s
    })

    if (!response.ok) {
      throw new Error(`FastAPI respondió con estatus: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json({
      status: 'success',
      data_source: 'DuckDB/Parquet (FastAPI Backend)',
      inyecciones: data.inyecciones || FALLBACK_DATA.inyecciones,
      ductos: data.ductos || FALLBACK_DATA.ductos,
      env_risk: data.env_risk || FALLBACK_DATA.env_risk,
    })

  } catch (err: any) {
    // Si falla el backend de FastAPI, aplicar degradación elegante con los datos estáticos de fallback
    return NextResponse.json({
      status: 'fallback',
      data_source: 'Static fallback (v2.3 curated)',
      inyecciones: FALLBACK_DATA.inyecciones,
      ductos: FALLBACK_DATA.ductos,
      env_risk: FALLBACK_DATA.env_risk,
      error_info: err.message,
    })
  }
}
