#!/usr/bin/env python3
"""
Build GOLD layer: Environmental risk by nodo/punto.
Joins gas infrastructure with: sitios_contaminados, ANP (when available), acuíferos, MIA.
Output: lakehouse/curated/env_risk_by_nodo.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir


def build_env_risk() -> pd.DataFrame:
    silver = get_lakehouse_dir("silver")
    gold = get_lakehouse_dir("gold") / "gas_infrastructure"
    
    # Load master puntos
    master = pd.read_parquet(gold / "gas_infrastructure_master.parquet")
    
    # Load sitios contaminados
    sitios = pd.read_parquet(silver / "semarnat" / "sitios_contaminados.parquet")
    
    # Load PROFEPA inspections
    profepa = pd.read_parquet(silver / "profepa" / "acciones_inspeccion_iao_zofemat.parquet")
    
    # For each punto, find sitios contaminados in same entidad
    # (municipio-level would need mapping - using entidad for now)
    sitio_by_ent = sitios.groupby("entidad_federativa").agg(
        total_sitios=("numero_sitios", "sum"),
        municipios_afectados=("municipio", "nunique"),
        anios_covered=("anio", lambda x: f"{x.min()}-{x.max()}"),
        tipos_contaminantes=("tipo_contaminante", lambda x: ", ".join(sorted(x.unique()))),
        contaminantes_detalle=("nombre_contaminante", lambda x: ", ".join(sorted(x.unique()))),
    ).reset_index()
    
    # PROFEPA by entidad
    profepa_by_ent = profepa.groupby("entidad").agg(
        total_inspecciones_iao_zofemat=("inspecciones", "sum"),
        materias=("materia", lambda x: ", ".join(sorted(x.unique()))),
    ).reset_index()
    
    # Merge into master
    # Need to map nom_ent to entidad_federativa (they should match)
    master_env = master.merge(
        sitio_by_ent, 
        left_on="nom_ent", 
        right_on="entidad_federativa", 
        how="left"
    ).merge(
        profepa_by_ent,
        left_on="nom_ent",
        right_on="entidad",
        how="left"
    )
    
    # Fill NaNs
    for col in ["total_sitios", "municipios_afectados", "total_inspecciones_iao_zofemat"]:
        if col in master_env.columns:
            master_env[col] = master_env[col].fillna(0).astype(int)
    
    # Risk score (simple heuristic)
    master_env["env_risk_score"] = (
        master_env.get("total_sitios", 0) * 1.0 +
        master_env.get("municipios_afectados", 0) * 2.0 +
        master_env.get("total_inspecciones_iao_zofemat", 0) * 0.1
    )
    
    # Sort by risk
    master_env = master_env.sort_values("env_risk_score", ascending=False).reset_index(drop=True)
    
    return master_env


def main():
    df = build_env_risk()
    
    out_dir = get_lakehouse_dir("gold") / "env_risk"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    out_path = out_dir / "env_risk_by_nodo.parquet"
    df.to_parquet(out_path, index=False)
    
    meta = {
        "source": "curated",
        "dataset": "env_risk_by_nodo",
        "build_date": datetime.now().isoformat() + "Z",
        "rows": int(len(df)),
        "cols": int(len(df.columns)),
        "schema_version": "1.0",
        "inputs": [
            "silver/cenegas/cenegas_injection_capacity.parquet",
            "silver/semarnat/sitios_contaminados.parquet",
            "silver/profepa/acciones_inspeccion_iao_zofemat.parquet",
        ],
        "notes": "Join at entidad level. Municipio-level join needs punto-municipio mapping. ANP/acuíferos not yet integrated.",
    }
    meta_path = out_dir / "env_risk_by_nodo.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    print(f"✅ Env risk by nodo: {len(df):,} → {out_path}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Top 5 risk:")
    print(df[["punto", "descripcion", "nom_ent", "total_sitios", "municipios_afectados", "total_inspecciones_iao_zofemat", "env_risk_score"]].head().to_string())


if __name__ == "__main__":
    main()