#!/usr/bin/env python3
"""
Clean 42 Registros Públicos Oficiales - catálogo de registros públicos.
Input: data/raw/42_Registros_Publicos_Oficiales.csv
Output: lakehouse/processed/gobmx/registros_publicos_oficiales.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir


def clean_registros_publicos() -> pd.DataFrame:
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "42_Registros_Publicos_Oficiales.csv"
    df = pd.read_csv(raw_path, encoding="utf-8")

    # Clean strings
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()

    return df


def main():
    df = clean_registros_publicos()

    out_dir = get_lakehouse_dir("silver") / "gobmx"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "registros_publicos_oficiales.parquet"
    df.to_parquet(out_path, index=False)

    meta = {
        "source": "gobmx",
        "dataset": "registros_publicos_oficiales",
        "download_date": datetime.now().isoformat() + "Z",
        "source_file": "42_Registros_Publicos_Oficiales.csv",
        "rows": int(len(df)),
        "columns": list(df.columns),
        "schema_version": "1.0",
        "note": "Catálogo de 42 registros públicos oficiales del gobierno federal. Solo 1 registro de datos en el CSV original.",
    }
    meta_path = out_dir / "registros_publicos_oficiales.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    print(f"✅ {len(df):,} rows → {out_path}")
    print(f"   Columnas: {list(df.columns)}")


if __name__ == "__main__":
    main()