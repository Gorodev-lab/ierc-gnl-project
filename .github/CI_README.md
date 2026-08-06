# CI Pipeline IERC-GNL — Documentación GitHub

Este workflow ejecuta las pruebas unitarias y verificaciones de calidad en cada push/PR.

## Jobs

| Job | Descripción | Tiempo estimado |
|-----|-------------|-----------------|
| `test` | Ejecuta pytest unitario (45 tests: storage, catalog, h3, ierc, spatial_validator, responsible_ai, monte_carlo) | ~2 min |
| `lint` | Verifica sintaxis Python (py_compile) en módulos core | ~30 seg |
| `verify-cdc` | Verificación CDC exact-once + schema contract | ~1 min |
| `dashboard-build` | Build Next.js 16 (compilación producción) | ~3 min |
| `summary` | Reporte consolidado de estado | ~10 seg |

## Triggers

- Push a `main`, `develop`
- Pull Request a `main`, `develop`

## Secrets Requeridos

| Secret | Descripción | Obligatorio |
|--------|-------------|-------------|
| `GFW_API_TOKEN` | Token API Global Fishing Watch (para ingesta real) | No (solo para ingesta manual) |

## Métricas de Calidad Actuales

- **Tests:** 45 passing (100%)
- **Coverage:** No configurado (añadir `pytest-cov` si requerido)
- **Type checking:** No configurado (añadir `mypy` si requerido)
- **Dashboard build:** Next.js 16 + React 19 + Tailwind CSS

## Ejecución Local

```bash
# Tests completos
PYTHONPATH=. ./.venv/bin/python3 -m pytest tests/ -v --tb=short

# Solo unitarios
PYTHONPATH=. ./.venv/bin/python3 -m pytest tests/unit/ -v

# Sintaxis
python3 -m py_compile \
  src/data/ingestion/base.py \
  src/data/ingestion/factory.py \
  src/data/catalog/catalog.py \
  src/data/ingestion/asea_mias.py \
  src/data/lakehouse/storage.py \
  src/utils/h3.py \
  src/utils/standardize.py \
  src/utils/logging.py \
  src/engine/spatial_validator.py \
  src/engine/responsible_ai.py \
  src/engine/ierc_calculator.py \
  src/engine/monte_carlo_engine.py

# Verificación CDC + Schema
python3 scripts/ci_verify_cdc.py

# Dashboard build
cd dashboard && npm run build
```

## Estructura de Archivos de Configuración

```
.github/
├── workflows/
│   └── ci.yml              # Pipeline principal
├── CI_README.md            # Este archivo
├── dependabot.yml          # (opcional) Actualizaciones de dependencias
└── CODEOWNERS              # (opcional) Dueños de código por directorio
```

## Reportes de Artefactos

El pipeline genera los siguientes artefactos descargables:

| Job | Artefacto | Retención |
|-----|-----------|-----------|
| `test` | `pytest-report.xml` (JUnit) | 7 días |
| `lint` | `syntax-check.log` | 7 días |
| `verify-cdc` | `cdc-verification.log` | 7 días |
| `dashboard-build` | `dashboard-build.log` | 7 días |

## Integración con Documentación del Proyecto

Este CI valida automáticamente:

1. **Inventario de datos** — Tests de `storage_catalog`, `h3`, `ierc` verifican integridad SILVER/GOLD
2. **Pipeline de ingesta** — `verify-cdc` confirma exact-once + schema contract
3. **Motor IERC** — Tests de `ierc_calculator`, `monte_carlo_engine`, `spatial_validator`
4. **Responsible AI** — Tests de `responsible_ai` (explainability, bias, smooth failing)
5. **Dashboard** — Build Next.js 16 sin errores de TypeScript/ESLint

## Referencias

- **Inventario completo:** `INVENTARIO_DATOS_IERC_GNL_v2.1.md`
- **GeoPackage Meta 1:** `REPORTE_INVENTARIO_GEOPACKAGE.md`
- **Metodología:** `docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md`
- **Matriz de vacíos:** `docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md`