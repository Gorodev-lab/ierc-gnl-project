#!/usr/bin/env python3
"""
Clean PROFEPA acciones de inspección en zona federal marítimo terrestre (ZOFEMAT) e impacto ambiental.
Input: data/raw/accionesInspeccioniazofemat.csv
Output: lakehouse/processed/profepa/acciones_inspeccion_iao_zofemat.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir


def clean_acciones_inspeccion() -> pd.DataFrame:
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "accionesInspeccioniazofemat.csv"
    df = pd.read_csv(raw_path, encoding="utf-8")

    # Rename columns
    df.columns = ["entidad", "materia", "inspecciones"]

    # Numeric
    df["inspecciones"] = pd.to_numeric(df["inspecciones"], errors="coerce")

    df = df.sort_values(["entidad", "materia"]).reset_index(drop=True)

    return df


def main():
    df = clean_acciones_inspeccion()

    out_dir = get_lakehouse_dir("silver") / "profepa"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "acciones_inspeccion_iao_zofemat.parquet"
    df.to_parquet(out_path, index=False)

    meta = {
        "source": "profepa",
        "dataset": "acciones_inspeccion_iao_zofemat",
        "download_date": datetime.now().isoformat() + "Z",
        "source_file": "accionesInspeccioniazofemat.csv",
        "rows": int(len(df)),
        "columns": list(df.columns),
        "schema_version": "1.0",
        "entidades": int(df["entidad"].nunique()),
        "total_inspecciones": int(df["inspecciones"].sum()),
    }
    meta_path = out_dir / "acciones_inspeccion_iao_zofemat.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    print(f"✅ {len(df):,} rows → {out_path}")
    print(f"   Entidades: {df['entidad'].nunique()}")
    print(f"   Total inspecciones: {df['inspecciones'].sum():,.0f}")
    print(f"   Materias: {df['materia'].unique()}")


if __name__ == "__main__":
    main()