#!/usr/bin/env python3
"""
Clean and normalize Cenegas historical injection capacity data.
Input: data/raw/cenegas/cenegas_3_capacidad_historica_de_inyecciones_sistrangas.csv
Output: data/processed/cenegas_injection_capacity.parquet
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import cenegas_raw_dir, get_processed_dir


def clean_cenegas() -> pd.DataFrame:
    raw_path = cenegas_raw_dir() / "cenegas_3_capacidad_historica_de_inyecciones_sistrangas.csv"

    df = pd.read_csv(raw_path, encoding="utf-8")

    # Fix encoding issues in origen - handle all mojibake variants
    def fix_origen(val: str) -> str:
        v = val.lower().strip()
        if "importaci" in v and "lng" in v:
            return "importacion_lng"
        if "importaci" in v:
            return "importacion"
        if "nacional" in v:
            return "nacional"
        return val

    df["origen"] = df["origen"].apply(fix_origen)

    # Fix encoding in nom_ent
    def fix_ent(val: str) -> str:
        v = val.strip()
        if "Nuevo Le" in v or "Nuevo Le" in v:
            return "Nuevo Leon"
        if "Quer" in v and ("taro" in v.lower() or "Taro" in v):
            return "Queretaro"
        return val

    df["nom_ent"] = df["nom_ent"].apply(fix_ent)

    # Fix encoding in descripcion
    df["descripcion"] = df["descripcion"].str.replace("inyvirtjuand?az", "inyvirtjuandiaz", regex=False)

    # Parse fecha as datetime
    df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")

    # Rename columns to snake_case
    df.columns = [
        "punto", "descripcion", "cve_ent", "nom_ent", "cve_mun", "nom_mun",
        "origen", "cantidad_inyectada_gj", "fecha", "unidad_medida", "nom_ent_etq"
    ]

    # Drop redundant column
    df = df.drop(columns=["nom_ent_etq"])

    # Sort
    df = df.sort_values(["punto", "fecha"]).reset_index(drop=True)

    return df


def main():
    df = clean_cenegas()

    out_dir = get_processed_dir() / "cenegas"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "cenegas_injection_capacity.parquet"
    df.to_parquet(out_path, index=False)
    print(f"Written {len(df):,} rows to {out_path}")
    print(f"Date range: {df['fecha'].min()} to {df['fecha'].max()}")
    print(f"Puntos: {df['punto'].nunique()}")
    print(f"Total GJ: {df['cantidad_inyectada_gj'].sum():,.0f}")


if __name__ == "__main__":
    main()