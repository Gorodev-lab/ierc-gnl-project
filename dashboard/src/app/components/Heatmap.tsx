'use client'

import React, { useEffect, useRef, useState } from 'react'
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

let HeatLayerClass: any = null

export default function Heatmap({ latLngs, options }: HeatmapProps) {
  const map = useMap()
  const heatLayerRef = useRef<any>(null)
  const [ready, setReady] = useState(false)

  // Initialize leaflet.heat once
  useEffect(() => {
    let mounted = true
    const initHeat = async () => {
      if (typeof window === 'undefined') return
      const L = (window as any).L
      if (!L) {
        return
      }
      if (!HeatLayerClass) {
        try {
          await import('leaflet.heat')
          HeatLayerClass = (L as any).heatLayer
        } catch (e) {
          return
        }
      }
      if (mounted) setReady(true)
    }
    initHeat()
    return () => { mounted = false }
  }, [])

  // Create/update heat layer when ready and data changes
  useEffect(() => {
    if (!ready || !latLngs?.length || !HeatLayerClass) return
    const L = (window as any).L
    if (!L) return

    // Compute max from data - use passed max only if it's >= data max (user explicitly wants clamp)
    const dataMax = latLngs.length ? Math.max(...latLngs.map(d => d[2])) : 100
    const passedMax = options?.max
    // If passed max is unreasonably low (< data max / 10), ignore it and use data max
    const effectiveMax = (passedMax !== undefined && passedMax >= dataMax / 10) ? passedMax : Math.max(dataMax, 1)

    // Gradient visible on dark basemap: start bright, not dark indigo
    const defaultGradient = { 0.1: '#FFFF00', 0.3: '#FF8C00', 0.5: '#FF4444', 0.7: '#FF00FF', 1: '#FFFFFF' }

    try {
      const layer = HeatLayerClass(latLngs, {
        radius: options?.radius ?? 25,
        blur: options?.blur ?? 15,
        maxZoom: options?.maxZoom ?? 7,
        gradient: options?.gradient ?? defaultGradient,
        minOpacity: options?.minOpacity ?? 0.15,
        max: effectiveMax,
      })

      heatLayerRef.current = layer
      layer.addTo(map)
    } catch (err) {
    }

    return () => {
      if (heatLayerRef.current) {
        try { map.removeLayer(heatLayerRef.current) } catch {}
      }
    }
  }, [ready, latLngs, options, map])

  // Update latLngs on data change (without recreating layer)
  useEffect(() => {
    if (heatLayerRef.current && latLngs?.length) {
      try { heatLayerRef.current.setLatLngs(latLngs) } catch {}
    }
  }, [latLngs])

  return null
}