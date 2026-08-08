'use client'

import React, { useState, useEffect } from 'react'
import { useFetch } from '@/lib/useFetch'
import ProjectCard from './ProjectCard'

interface Project {
  proyecto_id: string
  proyecto_nombre: string
  latitud: number
  longitud: number
  estado: string
  estatus: string
  capacidad_mtpa: number | null
  riesgo_pesquero: number
  nivel_riesgo: string
  num_zonas_encontradas: number
  zona_mas_cercana_km: number | null
  densidad_esfuerzo_pesquero: number
  proximidad_normalizada: number
  especies_criticas_score: number
  artes_de_pesca: string[]
  nota: string
}

export default function ZoneCards() {
  const { data, loading, error, refetch } = useFetch<{ proyectos: Project[] }>('/data/riesgo_proyectos.json')
  const [zoneMeta, setZoneMeta] = useState<Record<string, { zone: string; code: string; desc: string }>>({})

  useEffect(() => {
    fetch('/data/zone_meta.json')
      .then(r => r.json())
      .then(setZoneMeta)
      .catch(console.error)
  }, [])

  return (
    <div className="section">
      <div className="section-title">Terminales GNL & Evaluación de Riesgo Pesquero PANGAS</div>

      {loading && (
        <div style={{ padding: '2rem', textAlign: 'center', fontFamily: 'var(--font-mono)', color: 'var(--color-text-muted)' }}>
          [ CARGANDO TERMINALES GNL... ]
        </div>
      )}

      {error && (
        <div style={{ padding: '1rem', background: 'rgba(192,57,43,0.15)', border: '1px solid #C0392B', color: '#E74C3C', fontFamily: 'var(--font-mono)', fontSize: '0.75rem' }}>
          Error cargando datos: {error.message}
          <button onClick={refetch} style={{ marginLeft: '1rem', background: 'transparent', border: '1px solid #C0392B', color: '#E74C3C', padding: '0.2rem 0.5rem', cursor: 'pointer', fontFamily: 'var(--font-mono)', fontSize: '0.6875rem' }}>
            REINTENTAR
          </button>
        </div>
      )}

      {!loading && !error && (
        <div className="grid-2" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.25rem' }}>
          {data?.proyectos?.map(p => (
            <ProjectCard key={p.proyecto_id} project={p} zoneMeta={zoneMeta[p.proyecto_id] || null} />
          )) || []}
        </div>
      )}
    </div>
  )
}