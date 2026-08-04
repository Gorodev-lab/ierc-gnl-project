/**
 * Shared Risk Utilities — IERC-GNL Dashboard
 * Single source of truth for risk color computation.
 * Used by RiskMap and ZoneCards to avoid duplication.
 */

export function getRiskColor(score: number): string {
  if (score >= 75.0) return '#EF4444'
  if (score >= 50.0) return '#F59E0B'
  return '#10B981'
}

export function getRiskLevel(score: number): string {
  if (score >= 70) return 'Alto'
  if (score >= 40) return 'Moderado'
  if (score > 0) return 'Bajo'
  return 'Sin datos'
}