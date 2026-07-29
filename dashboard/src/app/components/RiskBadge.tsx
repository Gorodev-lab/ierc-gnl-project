import React from 'react'

type RiskLevel = 'Alto' | 'Moderado' | 'Bajo' | 'Sin datos'

interface RiskBadgeProps {
level: RiskLevel | string
score?: number
showDot?: boolean
}

const levelConfig: Record<string, { cssClass: string; dotColor: string; label: string }> = {
'Alto':      { cssClass: 'badge--alto',      dotColor: 'var(--color-alert)', label: '● ALTO' },
'Moderado':  { cssClass: 'badge--moderado',  dotColor: 'var(--color-warn)',  label: '● MODERADO' },
'Bajo':      { cssClass: 'badge--bajo',      dotColor: 'var(--color-ok)',    label: '● BAJO' },
'Sin datos': { cssClass: 'badge--ocean',     dotColor: 'var(--color-ocean)', label: '○ SIN DATOS' },
}

export default function RiskBadge({ level, score, showDot = true }: RiskBadgeProps) {
const config = levelConfig[level] ?? levelConfig['Sin datos']

return (
<span className={`badge ${config.cssClass}`}>
{showDot && (
<span
className="blink"
style={{
width: 6, height: 6, borderRadius: '50%',
backgroundColor: config.dotColor,
display: 'inline-block',
}}
/>
)}
{score !== undefined ? `${score.toFixed(1)}/100` : level.toUpperCase()}
</span>
)
}
