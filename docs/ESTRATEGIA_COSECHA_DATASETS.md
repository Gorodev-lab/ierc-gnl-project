# ESTRATEGIA Y PLAN DE IMPLEMENTACIÓN: COSECHA DE DATASETS RELEVANTES
## Proyecto IERC-GNL — Infraestructura Energética, Regulación y Cambio Climático (GNL)

---

## 1. MAPEO DE DATASETS PRIORITARIOS (datos.gob.mx)

### 1.1 Núcleo CENAGAS / SISTRANGAS (YA TENEMOS BASE)
| Dataset | Organización | Estado | Uso |
|---------|-------------|--------|-----|
| Capacidad histórica de inyecciones SISTRANGAS | CENAGAS | ✅ Integrado (parquet) | Baseline operacional |
| **Extracciones e Inyecciones de Gas Natural SISTRANGAS** | CENAGAS | 🎯 **Siguiente** | Complemento extracciones (par contrapartida) |
| **Tarifas de transporte gas natural** | CENAGAS | 🎯 **Siguiente** | Economía del transporte |
| **Boletín comercial - Capacidad disponible** | CENAGAS (web) | 🎯 **Siguiente** | Capacidad comercial por nodo |

### 1.2 Regulación y Concesiones (CRE / SENER / ASEA)
| Dataset | Organización | Fuente | Uso |
|---------|-------------|--------|-----|
| Permisos de transporte/distribución gas natural | CRE | datos.gob.mx / CRE | Mapa concesiones, titulares |
| Concesiones de ductos / gasoductos | CRE / ASEA | datos.gob.mx | Infraestructura física regulada |
| Prontuario Gas Natural (SENER) | SENER | base.energia.gob.mx | Contexto macro, reservas, balance |
| MIA sector hidrocarburos (post-2015) | ASEA | datos.gob.mx | Evaluaciones ambientales proyectos gas |

### 1.3 Infraestructura Física Geoespacial
| Dataset | Organización | Fuente | Formato |
|---------|-------------|--------|---------|
| **Gasoductos / ductos (polilíneas)** | CONAGUA / CRE / SENER | sigagis.conagua.gob.mx / SENER | Shapefile / GeoJSON |
| **Puntos de inyección/extracción (nodos)** | CENAGAS | boletin-gestor.cenagas.gob.mx | CSV / API |
| **Plantas de procesamiento / compresión** | PEMEX / CENAGAS | SENER | Puntos |
| **Áreas de influencia / servidumbre** | CRE / ASEA | datos.gob.mx | Polígonos |

### 1.4 Ambiental y Territorial (MIA, ANP, Agua, Biodiversidad)
| Dataset | Organización | Fuente | Uso |
|---------|-------------|--------|-----|
| **Manifestaciones Impacto Ambiental (MIA)** | SEMARNAT / ASEA | datos.gob.mx | Proyectos gas, evaluaciones |
| **Áreas Naturales Protegidas (ANP)** | CONANP | sig.conanp.gob.mx / CONABIO | Restricciones, buffers |
| **Acuíferos / disponibilidad agua** | CONAGUA | datos.gob.mx / SINAV | Riesgo hídrico |
| **Calidad del agua (cuencas receptoras)** | CONAGUA | SINAV | Impacto descargas |
| **Biodiversidad / especies (SNIB)** | CONABIO | snib.mx / GBIF | Especies sensibles en trazas |

### 1.5 Socioeconómico y Censal (INEGI)
| Dataset | Fuente | Uso |
|---------|--------|-----|
| DENUE (directorio económico) | INEGI | Actividad económica cerca de nodos |
| Censo poblacional 2020 / 2010 | INEGI | Población expuesta |
| Marco Geoestadístico (AGEB, manzanas) | INEGI | Análisis espacial fino |
| Índices de marginación / rezago | CONEVAL | Vulnerabilidad social |

---

## 2. ESTRATEGIA DE COSECHA (PONYTAIL: MÍNIMO VIABLE → ITERAR)

### Principios
1. **Reutilizar lo que ya existe** → `config.py` helpers, `data/raw/`, `data/processed/`, lakehouse bronze/silver/gold
2. **Un script por fuente** → `scripts/<fuente>/harvest_<dataset>.py`
3. **Salida estándar** → Parquet particionado por fecha/entidad + metadata JSON
4. **Idempotencia** → Re-ejecutable sin duplicados
5. **Provenance** → `source_url`, `download_date`, `schema_version` en metadata

### Capas (Lakehouse)
| Capa | Directorio | Contenido |
|------|------------|-----------|
| **Bronze** | `lakehouse/raw/<fuente>/` | Crudo tal cual (CSV, ZIP, SHP) |
| **Silver** | `lakehouse/processed/<fuente>/` | Limpio, tipado, dedup, enriquecido mínimo |
| **Gold** | `lakehouse/curated/<tema>/` | Listo para análisis: joins, agregaciones, features |

---

## 3. PLAN DE IMPLEMENTACIÓN POR FASES

### FASE 0 — FUNDAMENTOS (Semana 1) ✅ PARCIAL
- [x] `config.py` → `cenegas_raw_dir()`, `get_processed_dir()`
- [x] `scripts/cenegas/clean_cenegas.py` → inyecciones históricas (103K rows, parquet)
- [ ] `scripts/cenegas/harvest_extracciones.py` — **Extracciones SISTRANGAS** (pareja de inyecciones)
- [ ] `scripts/cenegas/harvest_tarifas.py` — Tarifas transporte
- [ ] `scripts/cenegas/harvest_capacidad_comercial.py` — Boletín comercial (nodos, MMPCD, GJ/día)

### FASE 1 — INFRAESTRUCTURA FÍSICA (Semana 2)
| Script | Fuente | Salida Silver | Notas |
|--------|--------|---------------|-------|
| `scripts/sener/harvest_gasoductos.py` | SENER mapa 2016 / base.energia.gob.mx | `lakehouse/processed/sener/gasoductos.parquet` | Polilíneas, atributos: diámetro, presión, operador |
| `scripts/cre/harvest_permisos_gas.py` | CRE / datos.gob.mx | `lakehouse/processed/cre/permisos_gas.parquet` | Permisos vigentes, titular, tramo |
| `scripts/cenagas/harvest_nodos.py` | boletin-gestor.cenagas.gob.mx/Capacidad | `lakehouse/processed/cenagas/nodos_comerciales.parquet` | Nodos con capacidad ofertada |

### FASE 2 — REGULACIÓN AMBIENTAL (Semana 3)
| Script | Fuente | Salida Silver | Notas |
|--------|--------|---------------|-------|
| `scripts/asea/harvest_mia_hidrocarburos.py` | ASEA / datos.gob.mx (MIA) | `lakehouse/processed/asea/mia_hidrocarburos.parquet` | Filtrar sector: gas natural, ductos, plantas |
| `scripts/conanp/harvest_anp.py` | CONANP SIG / CONABIO | `lakehouse/processed/conanp/anp_poligonos.parquet` | 182 ANP federales, categoría, decreto |
| `scripts/conagua/harvest_acuiferos.py` | CONAGUA / datos.gob.mx | `lakehouse/processed/conagua/acuiferos.parquet` | 653 acuíferos, disponibilidad, recarga |
| `scripts/conagua/harvest_calidad_agua.py` | SINAV CONAGUA | `lakehouse/processed/conagua/calidad_agua.parquet` | Estaciones, parámetros, tendencias |

### FASE 3 — BIODIVERSIDAD Y SOCIOECONÓMICO (Semana 4)
| Script | Fuente | Salida Silver | Notas |
|--------|--------|---------------|-------|
| `scripts/conabio/harvest_snib.py` | SNIB / GBIF / CONABIO | `lakehouse/processed/conabio/especies_cercanas_gas.parquet` | Buffer 10km alrededor de nodos/ductos |
| `scripts/inegi/harvest_denue.py` | INEGI DENUE API | `lakehouse/processed/inegi/denue_gas.parquet` | Actividades económicas cerca infraestructura |
| `scripts/inegi/harvest_marco_geo.py` | INEGI Marco Geoestadístico | `lakehouse/processed/inegi/marco_geoest.parquet` | AGEB, manzanas para joins espaciales |
| `scripts/coneval/harvest_marginacion.py` | CONEVAL | `lakehouse/processed/coneval/marginacion.parquet` | Índices municipal/estatal |

### FASE 4 — CURATED GOLD LAYER (Semana 5)
| Producto | Descripción | Scripts |
|----------|-------------|---------|
| `lakehouse/curated/gas_infrastructure_master.parquet` | Nodos + ductos + permisos + capacidad + tarifas (unificado) | `scripts/curated/build_master.py` |
| `lakehouse/curated/env_risk_by_nodo.parquet` | Riesgo ambiental por nodo: MIA, ANP overlap, acuífero, calidad agua, especies | `scripts/curated/build_env_risk.py` |
| `lakehouse/curated/socioeco_by_nodo.parquet` | Población, DENUE, marginación en buffers 5/10/25km | `scripts/curated/build_socioeco.py` |
| `lakehouse/curated/temporal_injection_extraction.parquet` | Serie temporal completa inyecciones + extracciones por nodo | `scripts/curated/build_temporal.py` |

---

## 4. ARQUITECTURA DE SCRIPTS (TEMPLATE REUTILIZABLE)

```python
# scripts/<fuente>/harvest_<dataset>.py
#!/usr/bin/env python3
"""
Harvest <dataset> from <fuente>.
Output: lakehouse/raw/<fuente>/<dataset>_<YYYYMMDD>.<ext>
        lakehouse/processed/<fuente>/<dataset>.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_raw_dir, get_lakehouse_dir


def download_raw() -> Path:
    """Download to bronze. Return local path."""
    raw_dir = get_lakehouse_dir("bronze") / "<fuente>"
    raw_dir.mkdir(parents=True, exist_ok=True)
    # ... download logic ...
    return raw_path


def clean_transform(raw_path: Path) -> pd.DataFrame:
    """Transform raw → silver-ready DataFrame."""
    # ... cleaning logic ...
    return df


def main():
    raw_path = download_raw()
    df = clean_transform(raw_path)

    # Metadata
    meta = {
        "source": "<fuente>",
        "dataset": "<dataset>",
        "download_date": datetime.utcnow().isoformat() + "Z",
        "source_url": "...",
        "rows": len(df),
        "columns": list(df.columns),
        "schema_version": "1.0",
    }

    # Write silver
    silver_dir = get_lakehouse_dir("silver") / "<fuente>"
    silver_dir.mkdir(parents=True, exist_ok=True)
    out_path = silver_dir / "<dataset>.parquet"
    df.to_parquet(out_path, index=False)

    # Write metadata
    meta_path = silver_dir / "<dataset>.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    print(f"✅ {len(df):,} rows → {out_path}")


if __name__ == "__main__":
    main()
```

---

## 5. PRÓXIMOS PASOS INMEDIATOS (ACCIONABLES HOY)

1. **Extracciones SISTRANGAS** → `scripts/cenegas/harvest_extracciones.py`
   - URL: `https://www.datos.gob.mx/dataset/extracciones_inyecciones_gas_natural_sistrangas`
   - Mismo patrón que inyecciones, columna `tipo` = extraccion/inyeccion

2. **Tarifas transporte** → `scripts/cenegas/harvest_tarifas.py`
   - URL: `https://www.datos.gob.mx/dataset/tarifas_transporte_gas_natural_a_partir_1_octubre_2018`

3. **Capacidad comercial (nodos)** → `scripts/cenegas/harvest_capacidad_comercial.py`
   - Scrape: `https://boletin-gestor.cenagas.gob.mx/GestionComercial/Capacidad`
   - Tabla HTML → nodos con MMPCD y GJ/día ofertados

4. **Actualizar `config.py`** con helpers:
   ```python
   def get_lakehouse_bronze(source: str) -> Path: ...
   def get_lakehouse_silver(source: str) -> Path: ...
   def get_lakehouse_gold(tema: str) -> Path: ...
   ```

---

## 6. DATASETS "NICE TO HAVE" (BACKLOG)

| Dataset | Por qué | Dificultad |
|---------|---------|------------|
| Precios hub Henry / Waha / NBP (referencia internacional) | Benchmark precios importación | API pagadas / Banxico |
| Balanza energética (SENER) | Contexto macro oferta/demanda | PDF → parsing |
| Emisiones CO2e sector gas (INECC) | Huella de carbono | Datos.gob.mx |
| Sismicidad (SSN/UNAM) | Riesgo ductos | WFS / shapefile |
| Cambio uso de suelo (INEGI Serie VI) | Presión territorial | GeoTIFF grande |

---

## 7. MÉTRICAS DE ÉXITO

| Métrica | Target |
|---------|--------|
| Cobertura nodos SISTRANGAS | 100% (27+ puntos) con inyección + extracción + capacidad + tarifa |
| Frescura datos | < 30 días lag vs fuente oficial |
| Reproducibilidad | `make harvest` → todo silver regenerable |
| Documentación | Cada dataset: README.md + data_dictionary.csv |

---

*Generado: 2025-08-07 | Ponytail mode: full | Proyecto: IERC-GNL*