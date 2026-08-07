#!/usr/bin/env python3
"""
Harvest Extracciones SISTRANGAS from CENAGAS / datos.gob.mx.
Complementa inyecciones históricas (ya integrado).
Output: lakehouse/processed/cenegas/extracciones_sistrangas.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_raw_dir, get_lakehouse_dir


def download_raw() -> Path:
    """Download raw CSV from CENAGAS/datos.gob.mx to bronze."""
    import urllib.request

    bronze_dir = get_lakehouse_dir("bronze") / "cenegas"
    bronze_dir.mkdir(parents=True, exist_ok=True)

    # URL del recurso CSV en datos.gob.mx (extracciones)
    # Nota: la URL exacta puede cambiar; verificar en https://www.datos.gob.mx/dataset/extracciones_inyecciones_gas_natural_sistrangas
    url = "https://www.datos.gob.mx/dataset/extracciones_inyecciones_gas_natural_sistrangas"
    # Por ahora, asumimos que el usuario descarga manualmente o usamos la misma estructura que inyecciones
    # El archivo típico se llama similar a inyecciones pero con extracciones

    # Buscar archivo local en raw/cenegas/ que contenga "extraccion" (case-insensitive)
    raw_dir = get_raw_dir("cenegas")
    candidates = list(raw_dir.glob("*[Ee]xtraccion*.csv"))
    if candidates:
        print(f"Using existing file: {candidates[0]}")
        return candidates[0]

    # Fallback: intentar descargar (la URL real del recurso hay que obtenerla de la página)
    out_path = bronze_dir / "extracciones_sistrangas_raw.csv"
    if not out_path.exists():
        print(f"⚠️  No local extracciones file found. Download manually from:")
        print(f"   https://www.datos.gob.mx/dataset/extracciones_inyecciones_gas_natural_sistrangas")
        print(f"   Save to: {raw_dir / 'extracciones_sistrangas.csv'}")
        print(f"   Or to bronze: {out_path}")
    return out_path


def clean_transform(raw_path: Path) -> pd.DataFrame:
    """Transform raw CSV → silver-ready DataFrame."""
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw file not found: {raw_path}. Download first.")

    df = pd.read_csv(raw_path, encoding="utf-8", low_memory=False)

    # Extracciones schema differs from inyecciones:
    # punto, nombre_punto, centro_extraccion, cve_ent, nom_ent, cve_mun, nom_mun,
    # zona_tarifaria, cantidad_extraida, fecha, unidad, nom_ent_etq

    def fix_ent(val: str) -> str:
        v = val.strip()
        if "Nuevo Le" in v:
            return "Nuevo Leon"
        if "Quer" in v and ("taro" in v.lower() or "Taro" in v):
            return "Queretaro"
        return val

    df["nom_ent"] = df["nom_ent"].apply(fix_ent)
    # Fix encoding in nombre_punto if needed
    df["nombre_punto"] = df["nombre_punto"].str.replace("Tepeji delR?O Ocampo", "Tepeji del Rio Ocampo", regex=False)

    df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")

    # Rename columns to match inyecciones pattern
    df = df.rename(columns={
        "nombre_punto": "descripcion",
        "centro_extraccion": "origen",  # Use centro_extraccion as origen proxy
        "cantidad_extraida": "cantidad_extraida_gj",
        "unidad": "unidad_medida",
        "zona_tarifaria": "zona_tarifaria",  # Keep as extra column
    })

    # Drop redundant column
    df = df.drop(columns=["nom_ent_etq"])

    # Add tipo column for clarity
    df["tipo"] = "extraccion"

    df = df.sort_values(["punto", "fecha"]).reset_index(drop=True)

    return df


def main():
    raw_path = download_raw()

    if not raw_path.exists():
        print("❌ Raw file not found. Please download from CENAGAS/datos.gob.mx first.")
        print("   Expected at: data/raw/cenegas/extracciones_sistrangas.csv")
        sys.exit(1)

    df = clean_transform(raw_path)

    # Metadata
    meta = {
        "source": "cenagas",
        "dataset": "extracciones_sistrangas",
        "download_date": datetime.utcnow().isoformat() + "Z",
        "source_url": "https://www.datos.gob.mx/dataset/extracciones_inyecciones_gas_natural_sistrangas",
        "rows": int(len(df)),
        "columns": list(df.columns),
        "schema_version": "1.0",
        "date_range": {
            "min": df["fecha"].min().isoformat(),
            "max": df["fecha"].max().isoformat(),
        },
        "puntos": int(df["punto"].nunique()),
        "total_gj": float(df["cantidad_extraida_gj"].sum()),
    }

    # Write silver
    silver_dir = get_lakehouse_dir("silver") / "cenegas"
    silver_dir.mkdir(parents=True, exist_ok=True)
    out_path = silver_dir / "extracciones_sistrangas.parquet"
    df.to_parquet(out_path, index=False)

    # Write metadata
    meta_path = silver_dir / "extracciones_sistrangas.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    print(f"✅ {len(df):,} rows → {out_path}")
    print(f"   Puntos: {df['punto'].nunique()}")
    print(f"   Date range: {df['fecha'].min()} to {df['fecha'].max()}")
    print(f"   Total GJ: {df['cantidad_extraida_gj'].sum():,.0f}")


if __name__ == "__main__":
    main()