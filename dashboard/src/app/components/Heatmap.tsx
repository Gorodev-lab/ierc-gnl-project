'use client'

import React, { useEffect, useRef } from 'react'
import { useMap } from 'react-leaflet'

interface HeatmapProps {
  latLngs: [number, number, number][]
  options?: {
    radius?: number
    blur?: number
    maxZoom?: number
    gradient?: Record<number, string>
    minOpacity?: number
    max?: number
  }
}

export default function Heatmap({ latLngs, options }: HeatmapProps) {
  const map = useMap()
  const heatLayerRef = useRef<any>(null)
  const L = (typeof window !== 'undefined' ? (window as any).L : null)

  useEffect(() => {
    if (!L || !latLngs?.length) return

    // Create heat layer
    const layer = L.heatLayer(latLngs, {
      radius: options?.radius ?? 25,
      blur: options?.blur ?? 15,
      maxZoom: options?.maxZoom ?? 7,
      gradient: options?.gradient ?? { 0.2: '#4F46E5', 0.4: '#6366F1', 0.6: '#818CF8', 0.8: '#A5B4FC', 1: '#FFFFFF' },
      minOpacity: options?.minOpacity ?? 0.15,
      max: options?.max ?? 100,
      ...options,
    })

    heatLayerRef.current = layer
    layer.addTo(map)

    return () => {
      if (heatLayerRef.current) {
        map.removeLayer(heatLayerRef.current)
      }
    }
  }, [latLngs, options, map])

  // Update latLngs when they change
  useEffect(() => {
    if (heatLayerRef.current && latLngs) {
      heatLayerRef.current.setLatLngs(latLngs)
    }
  }, [latLngs])

  return null
}