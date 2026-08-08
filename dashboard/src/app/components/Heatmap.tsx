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

// Variable a nivel de módulo para evitar re-definir la clase en cada render
let HeatLayerClass: any = null

export default function Heatmap({ latLngs, options }: HeatmapProps) {
  const map = useMap()
  const heatLayerRef = useRef<any>(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    const initHeat = async () => {
      if (typeof window === 'undefined') return
      // Leaflet se carga asíncronamente en RiskMap, esperar a que esté disponible
      let L = (window as any).L
      while (!L) {
        await new Promise(r => setTimeout(r, 100))
        L = (window as any).L
      }
      
      // Cargar leaflet.heat dinámicamente
      if (!HeatLayerClass) {
        try {
          await import('leaflet.heat')
          HeatLayerClass = (L as any).heatLayer
          setReady(true)
        } catch (e) {
          console.error('Failed to load leaflet.heat:', e)
        }
      }
    }
    initHeat()
  }, [])

  useEffect(() => {
    if (!ready || !latLngs?.length || !HeatLayerClass) return
    const L = (window as any).L
    if (!L) return

    try {
      const layer = HeatLayerClass(latLngs, {
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
    } catch (err) {
      console.error('Error creating heatLayer:', err)
    }

    return () => {
      if (heatLayerRef.current) {
        try {
          map.removeLayer(heatLayerRef.current)
        } catch (e) {
          // ignore removal errors during unmount
        }
      }
    }
  }, [ready, latLngs, options, map])

  // Update latLngs when they change
  useEffect(() => {
    if (heatLayerRef.current && latLngs) {
      try {
        heatLayerRef.current.setLatLngs(latLngs)
      } catch (e) {}
    }
  }, [latLngs])

  return null
}