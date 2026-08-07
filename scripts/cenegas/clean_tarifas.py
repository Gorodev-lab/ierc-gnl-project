#!/usr/bin/env python3
"""
Clean CENEGAS Tarifas por puntos de inyección/extracción.
Input: data/raw/cenegas/CENEGAS_1_Tarifas_por_puntos.csv
Output: lakehouse/processed/cenegas/tarifas_por_puntos.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir


def clean_tarifas() -> pd.DataFrame:
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "CENEGAS_1_Tarifas_por_puntos.csv"
    df = pd.read_csv(raw_path, encoding="utf-8")

    # Parse dates
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], format="%d/%m/%Y")
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"], format="%d/%m/%Y")

    # Numeric columns (stored as strings with comma decimals?)
    for col in ["capacidad_base_firme", "uso_base_firme", "servicio_base_interrumpible"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort
    df = df.sort_values(["zona_inyeccion", "zona_extraccion", "fecha_inicio"]).reset_index(drop=True)

    return df


def main():
    df = clean_tarifas()

    out_dir = get_lakehouse_dir("silver") / "cenegas"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "tarifas_por_puntos.parquet"
    df.to_parquet(out_path, index=False)

    meta = {
        "source": "cenegas",
        "dataset": "tarifas_por_puntos",
        "download_date": datetime.utcnow().isoformat() + "Z",
        "source_file": "CENEGAS_1_Tarifas_por_puntos.csv",
        "rows": int(len(df)),
        "columns": list(df.columns),
        "schema_version": "1.0",
        "date_range": {
            "min": df["fecha_inicio"].min().isoformat(),
            "max": df["fecha_fin"].max().isoformat(),
        },
        "zonas_inyeccion": int(df["zona_inyeccion"].nunique()),
        "zonas_extraccion": int(df["zona_extraccion"].nunique()),
    }
    meta_path = out_dir / "tarifas_por_puntos.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    print(f"✅ {len(df):,} rows → {out_path}")
    print(f"   Zonas inyección: {df['zona_inyeccion'].nunique()}, extracción: {df['zona_extraccion'].nunique()}")
    print(f"   Periodo: {df['fecha_inicio'].min()} a {df['fecha_fin'].max()}")


if __name__ == "__main__":
    main()