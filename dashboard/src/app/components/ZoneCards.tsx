'use client'

import React, { useEffect, useState } from 'react'
import RiskBadge from './RiskBadge'

interface Project {
proyecto_id: string
proyecto_nombre: string
latitud: number
longitud: number
estado: string
estatus: string
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

const ZONE_META: Record<string, { zone: string; icon: string; desc: string }> = {
'NFE_Puerto_Libertad': {
zone: 'Puerto Libertad',
icon: '',
desc: 'Territorio costero Sonora. Comunidades pesqueras artesanales. Pesca de camarón, chano y almeja.',
},
'Bazan_San_Felipe': {
zone: 'San Felipe',
icon: '',
desc: 'Alta densidad de pangas. Zona crítica para camarón y peces de alto valor comercial.',
},
'Guaymas_Terminal': {
zone: 'Guaymas',
icon: '',
desc: 'Puerto pesquero industrial. Diversidad alta de artes de pesca. Incluye Riqueza_Relativa.',
},
}

function getRiskLevelClass(nivel: string) {
if (nivel === 'Alto')     return 'progress-fill--high'
if (nivel === 'Moderado') return 'progress-fill--medium'
if (nivel === 'Bajo')     return 'progress-fill--low'
return 'progress-fill--ocean'
}

function ComponentBar({ label, value }: { label: string; value: number }) {
return (
<div style={{ marginBottom: '0.625rem' }}>
<div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
<span style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>{label}</span>
<span style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--color-amber)', fontVariantNumeric: 'tabular-nums' }}>
{(value * 100).toFixed(0)}%
</span>
</div>
<div className="progress-bar">
<div
className="progress-fill progress-fill--high"
style={{ width: `${value * 100}%` }}
/>
</div>
</div>
)
}

function ProjectCard({ project }: { project: Project }) {
const meta = ZONE_META[project.proyecto_id]
const hasRisk = project.riesgo_pesquero > 0

return (
<div className="card card--amber" style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
{/* Header */}
<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem' }}>
<div>
<div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
<span style={{ fontSize: '1.125rem' }}>{meta?.icon ?? ''}</span>
<span style={{
fontSize: '0.9375rem',
fontWeight: 700,
color: 'var(--color-amber)',
fontFamily: 'var(--font-mono)',
}}>
{meta?.zone ?? project.estado}
</span>
</div>
<p style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)', lineHeight: 1.4 }}>
{project.proyecto_nombre}
</p>
</div>
<RiskBadge level={project.nivel_riesgo} />
</div>

{/* Score gauge */}
<div style={{ textAlign: 'center', padding: '0.25rem 0' }}>
<div className="score-number">
{hasRisk ? project.riesgo_pesquero.toFixed(1) : '—'}
</div>
<div className="score-label">Riesgo pesquero / 100</div>
<div className="progress-bar" style={{ marginTop: '0.5rem' }}>
<div
className={`progress-fill ${getRiskLevelClass(project.nivel_riesgo)}`}
style={{ width: `${project.riesgo_pesquero}%` }}
/>
</div>
</div>

{/* Zone description */}
{meta?.desc && (
<p style={{
fontSize: '0.75rem',
color: 'var(--color-text-secondary)',
lineHeight: 1.5,
padding: '0.625rem',
background: 'var(--color-surface-2)',
borderRadius: 'var(--radius-sm)',
border: '1px solid var(--color-border)',
}}>
{meta.desc}
</p>
)}

{/* Stats */}
{hasRisk && (
<div>
<ComponentBar label="Densidad de esfuerzo" value={project.densidad_esfuerzo_pesquero} />
<ComponentBar label="Proximidad normalizada" value={project.proximidad_normalizada} />
<ComponentBar label="Especies críticas" value={project.especies_criticas_score} />
</div>
)}

{/* Quick stats */}
<div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
<div style={{
background: 'var(--color-surface-2)',
border: '1px solid var(--color-border)',
borderRadius: 'var(--radius-sm)',
padding: '0.5rem',
}}>
<div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-ocean)', fontVariantNumeric: 'tabular-nums' }}>
{project.num_zonas_encontradas.toLocaleString()}
</div>
<div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)' }}>
zonas pesqueras
</div>
</div>
<div style={{
background: 'var(--color-surface-2)',
border: '1px solid var(--color-border)',
borderRadius: 'var(--radius-sm)',
padding: '0.5rem',
}}>
<div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-amber)', fontVariantNumeric: 'tabular-nums' }}>
{project.zona_mas_cercana_km !== null ? `${project.zona_mas_cercana_km} km` : 'N/A'}
</div>
<div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)' }}>
zona más cercana
</div>
</div>
</div>

{/* Artes */}
{project.artes_de_pesca?.length > 0 && (
<div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.25rem' }}>
{project.artes_de_pesca.map(art => (
<span key={art} style={{
padding: '0.15rem 0.5rem',
borderRadius: 3,
fontSize: '0.625rem',
background: 'var(--color-surface-3)',
border: '1px solid var(--color-border-hi)',
color: 'var(--color-text-secondary)',
}}>
{art}
</span>
))}
</div>
)}

{/* Location */}
<div style={{
display: 'flex',
justifyContent: 'space-between',
fontSize: '0.6875rem',
color: 'var(--color-text-muted)',
marginTop: 'auto',
paddingTop: '0.5rem',
borderTop: '1px solid var(--color-border)',
fontVariantNumeric: 'tabular-nums',
}}>
<span>{project.estado}</span>
<span>{project.latitud.toFixed(4)}°N · {Math.abs(project.longitud).toFixed(4)}°W</span>
</div>
</div>
)
}

export default function ZoneCards() {
const [projects, setProjects] = useState<Project[]>([])

useEffect(() => {
fetch('/data/riesgo_proyectos.json')
.then(r => r.json())
.then(data => {
const filtered = data.proyectos.filter(
(p: Project) => Object.keys(ZONE_META).includes(p.proyecto_id)
)
filtered.sort((a: Project, b: Project) => b.riesgo_pesquero - a.riesgo_pesquero)
setProjects(filtered)
})
.catch(console.error)
}, [])

return (
<div className="section">
<div className="section-title">Zonas de Mayor Riesgo (PANGAS & GNL)</div>
<div className="grid-3">
{projects.map(p => <ProjectCard key={p.proyecto_id} project={p} />)}
</div>
</div>
)
}
