# ESTRATEGIA: MEJORAR PRESENTACIÓN GFW EN MAPA (SATURACIÓN)

## Problema actual
- 9,960 features GeoJSON → renderizados como circle markers individuales
- Todos a la vez, sin filtrado temporal/espacial
- Overplotting severo: puntos se superponen, ilegible
- Un solo color (#6366F1), radio solo por `fishing_hours`

---

## ESTRATEGIA PONYTAIL: MÍNIMO VIABLE → ITERAR

### NIVEL 1: Filtros cliente (1 día, alto impacto)
Añadir controles UI en el panel lateral:
- **Año**: 2016 / 2020 / Todos
- **Mes**: 1-12 / Todos
- **Arte de pesca**: 6 tipos / Todos
- **Bandera**: 6 flags / Todos

Resultado: Reduce features renderizadas de 9,960 → ~hundreds según filtro.

### NIVEL 2: Heatmap + Circle markers condicional (2 días)
- **Zoom ≤ 7**: Heatmap (Leaflet.heat) - densidad global
- **Zoom > 7**: Circle markers con clustering (leaflet.markercluster) - detalle
- Heatmap usa `hours` como peso, radius adaptativo

### NIVEL 3: Agregación servidor / H3 res 7 (1 semana)
- Pre-agregar en Silver: `lakehouse/processed/gfw/fishing_h3_agg/`
- Group by: h3_cell (res 7), year, month, geartype, flag
- Stats: sum(hours), count, mean(hours), max(hours)
- Sirve tiles vectoriales (PMTiles/MVT) o API paginada

---

## IMPLEMENTACIÓN INMEDIATA (NIVEL 1+2)

### Archivos a tocar:
1. `RiskMap.tsx` - Add filter state + conditional rendering
2. `RiskMap.tsx` - Add Leaflet.heat import + heatmap layer
3. (Opcional) `leaflet.markercluster` para clustering

### Cambios mínimos en RiskMap.tsx:

```typescript
// 1. Add filter state (lines ~176-194)
const [gfwFilters, setGfwFilters] = useState({
  year: 'all' as string,
  month: 'all' as string,
  geartype: 'all' as string,
  flag: 'all' as string,
})

// 2. Filter function (memoized)
const filteredGfwData = useMemo(() => {
  if (!layersData.gfw_fishing) return null
  return layersData.gfw_fishing.features.filter(f => {
    const p = f.properties
    return (gfwFilters.year === 'all' || p.year == gfwFilters.year) &&
           (gfwFilters.month === 'all' || p.month == gfwFilters.month) &&
           (gfwFilters.geartype === 'all' || p.geartype == gfwFilters.geartype) &&
           (gfwFilters.flag === 'all' || p.flag == gfwFilters.flag)
  })
}, [layersData.gfw_fishing, gfwFilters])

// 3. Conditional render: Heatmap at low zoom, circles at high zoom
// Use map zoom from mapRef.current.getZoom()

// 4. Filter UI in Layer Control Panel (after line ~479)
```

---

## SKIPPED (YAGNI)
- Custom WebGL layer (deck.gl) - overkill
- Server-side MVT tiles - requiere infra nueva
- Animación temporal - nice-to-have
- Leyenda dinámica - se añade después si hace falta

## CUÁNDO SUBIR DE NIVEL
- Nivel 1 listo → medir fps/render time
- Si >1000 features aún con filtros → Nivel 2 (heatmap)
- Si >5000 features en viewport → Nivel 3 (tiles vectoriales)

---

## PRÓXIMO PASO ACCIONABLE
Implementar Nivel 1 (filtros) en `RiskMap.tsx` - ~50 líneas de cambios.