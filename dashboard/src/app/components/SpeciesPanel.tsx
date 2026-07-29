'use client'

import React, { useEffect, useState } from 'react'

interface Species {
codigo: string
nombre_comun: string
nombre_cientifico: string
estado_iucn: string
importancia: string
}

interface ProjectSpecies {
especies_presentes: string[]
num_criticas: number
riesgo_pesquero: number
}

interface SpeciesData {
metadata: { fecha: string; fuente: string; total_zonas_analizadas: number }
especies_criticas: Species[]
por_proyecto: Record<string, ProjectSpecies>
}

const iucnColor: Record<string, { bg: string; color: string; border: string }> = {
'CR': { bg: 'rgba(231,76,60,0.2)',   color: '#E74C3C', border: '#E74C3C' },
'EN': { bg: 'rgba(243,156,18,0.2)',  color: '#F39C12', border: '#F39C12' },
'VU': { bg: 'rgba(255,176,0,0.18)',  color: '#FFB000', border: '#FFB000' },
'NT': { bg: 'rgba(14,165,233,0.15)',  color: '#0ea5e9', border: '#0ea5e9' },
'LC': { bg: 'rgba(46,204,113,0.15)',  color: '#2ECC71', border: '#2ECC71' },
}

const PROJECT_LABELS: Record<string, string> = {
'NFE_Puerto_Libertad': 'Puerto Libertad',
'Bazan_San_Felipe':    'San Felipe',
'Guaymas_Terminal':    'Guaymas',
}

function IUCNBadge({ status }: { status: string }) {
const cfg = iucnColor[status] ?? iucnColor['LC']
return (
<span style={{
display: 'inline-block',
padding: '0.1rem 0.45rem',
borderRadius: 3,
fontSize: '0.625rem',
fontWeight: 700,
letterSpacing: '0.08em',
background: cfg.bg,
color: cfg.color,
border: `1px solid ${cfg.border}`,
fontFamily: 'var(--font-mono)',
}}>
{status}
</span>
)
}

export default function SpeciesPanel() {
const [data, setData] = useState<SpeciesData | null>(null)
const [selected, setSelected] = useState<string | null>(null)

useEffect(() => {
fetch('/data/especies_criticas.json')
.then(r => r.json())
.then(setData)
.catch(console.error)
}, [])

if (!data) return null

const { especies_criticas, por_proyecto } = data
const filteredSpecies = selected
? especies_criticas.filter(s =>
por_proyecto[selected]?.especies_presentes.includes(s.codigo)
)
: especies_criticas

return (
<div className="section">
<div className="section-title">Especies Críticas en Riesgo Pesquero (IUCN)</div>

{/* Filter by project */}
<div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
<button
onClick={() => setSelected(null)}
style={{
padding: '0.35rem 0.875rem',
borderRadius: 4,
border: `1px solid ${!selected ? 'var(--color-amber)' : 'var(--color-border)'}`,
background: !selected ? 'var(--color-amber-glow)' : 'transparent',
color: !selected ? 'var(--color-amber)' : 'var(--color-text-muted)',
fontSize: '0.75rem',
fontWeight: 600,
cursor: 'pointer',
fontFamily: 'var(--font-mono)',
}}
>
TODOS LOS PROYECTOS
</button>
{Object.entries(PROJECT_LABELS).map(([id, label]) => (
<button
key={id}
onClick={() => setSelected(selected === id ? null : id)}
style={{
padding: '0.35rem 0.875rem',
borderRadius: 4,
border: `1px solid ${selected === id ? 'var(--color-amber)' : 'var(--color-border)'}`,
background: selected === id ? 'var(--color-amber-glow)' : 'transparent',
color: selected === id ? 'var(--color-amber)' : 'var(--color-text-muted)',
fontSize: '0.75rem',
fontWeight: 600,
cursor: 'pointer',
fontFamily: 'var(--font-mono)',
}}
>
{label.toUpperCase()}
{por_proyecto[id] && (
<span style={{
marginLeft: '0.375rem',
padding: '0.1rem 0.35rem',
borderRadius: 3,
background: 'rgba(231,76,60,0.2)',
color: 'var(--color-alert)',
fontSize: '0.625rem',
fontWeight: 700,
}}>
{por_proyecto[id].riesgo_pesquero}/100
</span>
)}
</button>
))}
</div>

{/* Species grid */}
<div className="grid-2">
{filteredSpecies.map(sp => {
const projectsWith = Object.entries(por_proyecto)
.filter(([, pd]) => pd.especies_presentes.includes(sp.codigo))
.map(([id]) => PROJECT_LABELS[id] ?? id)

const isCritical = ['CR', 'EN'].includes(sp.estado_iucn)

return (
<div
key={sp.codigo}
className={`card ${isCritical ? 'card--amber' : 'card--ocean'}`}
style={{
display: 'flex',
gap: '1rem',
alignItems: 'flex-start',
}}
>
{/* Icon */}
<div style={{
width: 40, height: 40,
borderRadius: 6,
background: 'var(--color-surface-2)',
border: `1px solid ${isCritical ? 'var(--color-alert)' : 'var(--color-ocean-dim)'}`,
display: 'flex', alignItems: 'center', justifyContent: 'center',
fontSize: '1.25rem',
flexShrink: 0,
}}>
{sp.codigo.startsWith('sph') ? ''
: sp.codigo.startsWith('rhi') || sp.codigo.startsWith('das') ? ''
: sp.codigo.startsWith('gym') ? ''
: sp.codigo.startsWith('car') ? ''
: sp.codigo.startsWith('lut') || sp.codigo.startsWith('par') ? ''
: ''}
</div>

<div style={{ flex: 1, minWidth: 0 }}>
{/* Name + IUCN */}
<div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '0.25rem' }}>
<span style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-amber)', fontFamily: 'var(--font-mono)' }}>
{sp.nombre_comun}
</span>
<IUCNBadge status={sp.estado_iucn} />
</div>

{/* Scientific name */}
<p style={{
fontSize: '0.6875rem',
color: 'var(--color-text-muted)',
fontStyle: 'italic',
marginBottom: '0.5rem',
}}>
{sp.nombre_cientifico}
</p>

{/* Importancia */}
<div style={{
display: 'flex',
justifyContent: 'space-between',
fontSize: '0.6875rem',
marginBottom: '0.5rem',
}}>
<span style={{ color: 'var(--color-text-muted)' }}>IMPORTANCIA:</span>
<span style={{ color: 'var(--color-text-secondary)', fontWeight: 600 }}>{sp.importancia.toUpperCase()}</span>
</div>

{/* Projects present */}
<div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
{projectsWith.map(proj => (
<span key={proj} style={{
padding: '0.1rem 0.45rem',
borderRadius: 3,
fontSize: '0.625rem',
fontWeight: 600,
background: 'rgba(255,176,0,0.1)',
border: '1px solid var(--color-amber-muted)',
color: 'var(--color-amber)',
}}>
{proj}
</span>
))}
</div>
</div>
</div>
)
})}
</div>

{/* Source note */}
<p style={{
marginTop: '1rem',
fontSize: '0.6875rem',
color: 'var(--color-text-muted)',
fontFamily: 'var(--font-mono)',
}}>
FUENTE: {data.metadata.fuente} · {data.metadata.total_zonas_analizadas.toLocaleString()} ZONAS ANALIZADAS
</p>
</div>
)
}
