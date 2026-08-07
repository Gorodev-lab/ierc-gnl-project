#!/usr/bin/env python3
"""
Clean SENER bd_volumen_gas_natural_ta - almacenamiento gas natural por terminal.
Input: data/raw/bd_volumen_gas_natural_ta.csv
Output: lakehouse/processed/sener/volumen_almacenamiento_gas.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir


def clean_volumen_almacenamiento() -> pd.DataFrame:
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "bd_volumen_gas_natural_ta.csv"
    df = pd.read_csv(raw_path, encoding="utf-8-sig")  # BOM handling

    # Parse periodo_reporte as datetime (YYYY-MM)
    df["periodo_reporte"] = pd.to_datetime(df["periodo_reporte"], format="%Y-%m")

    # Numeric
    df["energia_gj"] = pd.to_numeric(df["energia_gj"], errors="coerce")

    # Clean strings
    df["permiso"] = df["permiso"].str.strip()
    df["permisionario"] = df["permisionario"].str.strip()
    df["actividad"] = df["actividad"].str.strip()

    df = df.sort_values(["permisionario", "periodo_reporte"]).reset_index(drop=True)

    return df


def main():
    df = clean_volumen_almacenamiento()

    out_dir = get_lakehouse_dir("silver") / "sener"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "volumen_almacenamiento_gas.parquet"
    df.to_parquet(out_path, index=False)

    meta = {
        "source": "sener",
        "dataset": "volumen_almacenamiento_gas",
        "download_date": datetime.now().isoformat() + "Z",
        "source_file": "bd_volumen_gas_natural_ta.csv",
        "rows": int(len(df)),
        "columns": list(df.columns),
        "schema_version": "1.0",
        "date_range": {
            "min": df["periodo_reporte"].min().isoformat(),
            "max": df["periodo_reporte"].max().isoformat(),
        },
        "permisionarios": int(df["permisionario"].nunique()),
        "total_gj": float(df["energia_gj"].sum()),
    }
    meta_path = out_dir / "volumen_almacenamiento_gas.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    print(f"✅ {len(df):,} rows → {out_path}")
    print(f"   Permisionarios: {df['permisionario'].nunique()}")
    print(f"   Periodo: {df['periodo_reporte'].min()} a {df['periodo_reporte'].max()}")
    print(f"   Total GJ: {df['energia_gj'].sum():,.0f}")


if __name__ == "__main__":
    main()