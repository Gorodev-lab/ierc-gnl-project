#!/usr/bin/env python3
"""
Clean SENER Prontuario datos abiertos (volumen gas natural, producción, importación, etc).
Input: data/raw/prontuario_datos_abiertos.csv
Output: lakehouse/processed/sener/prontuario_datos_abiertos.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir


def clean_prontuario() -> pd.DataFrame:
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "prontuario_datos_abiertos.csv"
    df = pd.read_csv(raw_path, encoding="utf-8")

    # Parse periodo_reporte as datetime (YYYY-MM format)
    df["periodo_reporte"] = pd.to_datetime(df["periodo_reporte"], format="%Y-%m")

    # Numeric columns
    for col in ["producion", "importacion", "exportacion", "demanda"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Rename producion -> produccion (typo in source)
    df = df.rename(columns={"producion": "produccion"})

    df = df.sort_values(["periodo_reporte", "producto"]).reset_index(drop=True)

    return df


def main():
    df = clean_prontuario()

    out_dir = get_lakehouse_dir("silver") / "sener"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "prontuario_datos_abiertos.parquet"
    df.to_parquet(out_path, index=False)

    meta = {
        "source": "sener",
        "dataset": "prontuario_datos_abiertos",
        "download_date": datetime.now().isoformat() + "Z",
        "source_file": "prontuario_datos_abiertos.csv",
        "rows": int(len(df)),
        "columns": list(df.columns),
        "schema_version": "1.0",
        "date_range": {
            "min": df["periodo_reporte"].min().isoformat(),
            "max": df["periodo_reporte"].max().isoformat(),
        },
        "productos": int(df["producto"].nunique()),
        "total_produccion_mt": float(df["produccion"].sum()),
        "total_importacion_mt": float(df["importacion"].sum()),
    }
    meta_path = out_dir / "prontuario_datos_abiertos.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    print(f"✅ {len(df):,} rows → {out_path}")
    print(f"   Productos: {df['producto'].nunique()}")
    print(f"   Periodo: {df['periodo_reporte'].min()} a {df['periodo_reporte'].max()}")


if __name__ == "__main__":
    main()