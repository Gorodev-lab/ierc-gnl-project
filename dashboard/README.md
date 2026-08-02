# IERC-GNL Interactive Dashboard (Next.js 16)

Dashboard de Inteligencia Geoespacial y Evaluación del Índice Espacial de Riesgo Socioeconómico (IERC) para Causa Natura Center.

---

## 🎨 Estándar de Diseño & Skill Hallmark Anti-AI-Slop

Este proyecto sigue estrictamente el **Esoteria Design System v1.1** (`STYLE_GUIDE.md`) y el protocolo anti-AI-slop de **Nutlope/Hallmark**:

- **Skill de Agente**: Todos los agentes de IA (Claude Code, Cursor, Codex, Gemini) deben acatar las reglas descritas en `.gemini/skills/hallmark/SKILL.md` y `dashboard/AGENTS.md`.
- **Política Cero-Emoticones**: Se prohíbe el uso de emojis decorativos en la interfaz (ej. 🦐, 🦈, 🐟). En su lugar se utilizan **Badges Monospace Taxonómicos** (`[CAM]`, `[TIB]`, `[RAY]`, `[PAR]`).
- **Restricciones Visuales**:
  - `IBM Plex Mono` como tipografía principal.
  - `border-radius: 0px` en todos los componentes.
  - `box-shadow: none` (sin sombras flotantes ni efectos glow).
  - Fondo oscuro permanente (`#0A0A0A`, superficie `#111111`, bordes `#222222`).

---

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo (puerto 3001)
npm run dev

# Compilar paquete de producción
npm run build
```

Navegar a [http://localhost:3001](http://localhost:3001) para ver el dashboard.

---

## 📁 Estructura de Componentes

- `src/app/components/Header.tsx`: Consola superior con ticker de estado del sistema e indicadores OGC GeoPackage.
- `src/app/components/RiskMap.tsx`: Visor mapa Leaflet con navegación rápida de terminales GNL, mallas Uber H3 y contornos GEBCO.
- `src/app/components/ZoneCards.tsx`: Tarjetas de riesgo pesquero PANGAS con barras ASCII `[██████░░░░]`.
- `src/app/components/SpeciesPanel.tsx`: Panel de especies en riesgo IUCN con badges taxonómicos monospace.
- `src/app/components/MethodologyPanel.tsx`: Desglose de fórmulas y motor de cálculo Monte Carlo.
- `src/app/components/CoverageModal.tsx`: Matriz de vacíos de información e ingestas institucionales.
