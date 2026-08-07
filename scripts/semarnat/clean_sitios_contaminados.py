#!/usr/bin/env python3
"""
Clean SEMARNAT sitios contaminados por tipo de contaminante.
Input: data/raw/sitios_contaminados_tipo_contaminante.csv
Output: lakehouse/processed/semarnat/sitios_contaminados.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir


def clean_sitios_contaminados() -> pd.DataFrame:
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "sitios_contaminados_tipo_contaminante.csv"
    df = pd.read_csv(raw_path, encoding="utf-8")

    # Rename columns (strip quotes from header)
    df.columns = [c.strip('"') for c in df.columns]
    df.columns = ["entidad_federativa", "municipio", "anio", "tipo_contaminante", "nombre_contaminante", "numero_sitios"]

    # Numeric
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce").astype("Int64")
    df["numero_sitios"] = pd.to_numeric(df["numero_sitios"], errors="coerce").astype("Int64")

    # Clean strings
    for col in ["entidad_federativa", "municipio", "tipo_contaminante", "nombre_contaminante"]:
        df[col] = df[col].str.strip()

    df = df.sort_values(["entidad_federativa", "municipio", "anio"]).reset_index(drop=True)

    return df


def main():
    df = clean_sitios_contaminados()

    out_dir = get_lakehouse_dir("silver") / "semarnat"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "sitios_contaminados.parquet"
    df.to_parquet(out_path, index=False)

    meta = {
        "source": "semarnat",
        "dataset": "sitios_contaminados",
        "download_date": datetime.now().isoformat() + "Z",
        "source_file": "sitios_contaminados_tipo_contaminante.csv",
        "rows": int(len(df)),
        "columns": list(df.columns),
        "schema_version": "1.0",
        "date_range": {
            "min": int(df["anio"].min()),
            "max": int(df["anio"].max()),
        },
        "entidades": int(df["entidad_federativa"].nunique()),
        "municipios": int(df["municipio"].nunique()),
        "total_sitios": int(df["numero_sitios"].sum()),
        "tipos_contaminante": sorted(df["tipo_contaminante"].unique().tolist()),
    }
    meta_path = out_dir / "sitios_contaminados.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    print(f"✅ {len(df):,} rows → {out_path}")
    print(f"   Entidades: {df['entidad_federativa'].nunique()}")
    print(f"   Municipios: {df['municipio'].nunique()}")
    print(f"   Años: {df['anio'].min()} - {df['anio'].max()}")
    print(f"   Total sitios: {df['numero_sitios'].sum():,}")
    print(f"   Tipos contaminante: {df['tipo_contaminante'].nunique()}")


if __name__ == "__main__":
    main()