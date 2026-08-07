#!/usr/bin/env python3
"""
Catalog ECC_Climabase climate raster data.
Input: data/raw/ECC_Climabase/ECC_Climabase/
Output: lakehouse/processed/ecc_climabase/catalog.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir, ecc_raw_dir


def catalog_ecc() -> pd.DataFrame:
    base = ecc_raw_dir()  # Files are directly in ecc_climabase/
    
    records = []
    variables = {
        "PrecMxHijmans1950_2000": "precipitation_mm",
        "TmaxMxHijmans1950_2000": "tmax_celsius",
        "TmedMxHijmans1950_2000": "tmed_celsius",
        "TminMxHijmans1950_2000": "tmin_celsius",
    }
    
    for var_dir, var_name in variables.items():
        var_path = base / var_dir
        if not var_path.exists():
            print(f"Warning: {var_path} not found")
            continue
        
        tif_files = sorted(var_path.glob("*.tif"))
        for tif in tif_files:
            # Parse month from filename: prec_1950_2000_01.tif
            stem = tif.stem
            parts = stem.split("_")
            if len(parts) >= 3:
                month = parts[-1]
                period = "_".join(parts[:-1])
            else:
                month = "unknown"
                period = stem
            
            stat = tif.stat()
            records.append({
                "variable": var_name,
                "variable_dir": var_dir,
                "month": int(month) if month.isdigit() else None,
                "period": period,
                "file_name": tif.name,
                "file_path": str(tif.relative_to(Path(__file__).resolve().parents[2])),
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / 1024 / 1024, 2),
            })
    
    df = pd.DataFrame(records)
    df = df.sort_values(["variable", "month"]).reset_index(drop=True)
    return df


def main():
    df = catalog_ecc()
    
    out_dir = get_lakehouse_dir("silver") / "ecc_climabase"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    out_path = out_dir / "catalog.parquet"
    df.to_parquet(out_path, index=False)
    
    meta = {
        "source": "ecc_climabase",
        "dataset": "catalog",
        "build_date": datetime.now().isoformat() + "Z",
        "source_path": str(ecc_raw_dir() / "ECC_Climabase"),
        "rows": int(len(df)),
        "columns": list(df.columns),
        "schema_version": "1.0",
        "variables": sorted(df["variable"].unique().tolist()),
        "months_covered": sorted(df["month"].dropna().astype(int).unique().tolist()),
        "total_size_mb": round(df["size_mb"].sum(), 2),
        "notes": "ECC Climabase - Monthly climate normals 1950-2000 for Mexico (Hijmans et al.). Precipitation in mm, temperatures in °C. GeoTIFF format.",
    }
    meta_path = out_dir / "catalog.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    print(f"✅ Catalog: {len(df):,} files → {out_path}")
    print(f"   Variables: {df['variable'].nunique()}")
    print(f"   Months: {df['month'].nunique()}")
    print(f"   Total size: {df['size_mb'].sum():.1f} MB")


if __name__ == "__main__":
    main()