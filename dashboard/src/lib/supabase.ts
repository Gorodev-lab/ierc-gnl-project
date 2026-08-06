import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://jhgdwhobefoyodrsmpnc.supabase.co'
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpoZ2R3aG9iZWZveW9kcnNtcG5jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU5NjI5NTgsImV4cCI6MjEwMTUzODk1OH0.Ii8gWRA1xDEFzZqZGkWsaTlulug0Tp1z4JAPGIrIMEY'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export type GrillaH3Riesgo = {
  id: number
  h3_index: string
  resolucion: number
  latitud_centroide: number
  longitud_centroide: number
  ierc_score: number
  nivel_riesgo: string
  amenaza_score: number
  exposicion_score: number
  sensibilidad_score: number
  dependencia_score: number
  biocultural_score: number
  capacidad_adaptativa_score: number
  distancia_proyecto_mas_cercano_km: number
  geometry: string
}

export type ProyectoGNL = {
  id: number
  nombre_proyecto: string
  estado: string
  municipio: string
  tipo_infraestructura: string
  empresa_promovente: string
  estatus_permiso: string
  fuente_oficial: string
  capacidad_mtpa: number
  latitud: number
  longitud: number
  geometry: string
}
