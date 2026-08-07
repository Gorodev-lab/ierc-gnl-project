#!/usr/bin/env python3
"""
Clean/Catalog gasoductos from contextual layers.
Input: data/raw/gasoductos/capas_contextuales.geojson
Output: lakehouse/processed/gasoductos/capas_contextuales.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import geopandas as gpd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir, gasoductos_raw_dir


def clean_gasoductos() -> gpd.GeoDataFrame:
    raw_path = gasoductos_raw_dir() / "capas_contextuales.geojson"
    gdf = gpd.read_file(raw_path)
    
    # Filter to gasoductos only
    gasoductos = gdf[gdf["tipo_capa"] == "Gasoducto"].copy()
    
    # Ensure standard columns
    if "nombre" in gasoductos.columns:
        gasoductos = gasoductos.drop(columns=["descripcion"]).rename(columns={"nombre": "descripcion"})
    
    # Add metadata columns
    gasoductos["source"] = "capas_contextuales"
    gasoductos["catalog_date"] = datetime.now().isoformat()
    
    # Ensure CRS
    if gasoductos.crs is None:
        gasoductos.set_crs(epsg=4326, inplace=True)
    elif gasoductos.crs.to_epsg() != 4326:
        gasoductos = gasoductos.to_crs(epsg=4326)
    
    # Calculate length in km (project to metric CRS first)
    gasoductos_proj = gasoductos.to_crs(epsg=3857)
    gasoductos["length_km"] = gasoductos_proj.geometry.length / 1000
    
    return gasoductos


def main():
    gdf = clean_gasoductos()
    
    out_dir = get_lakehouse_dir("silver") / "gasoductos"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Write GeoParquet
    out_path = out_dir / "capas_contextuales.parquet"
    gdf.to_parquet(out_path, index=False)
    
    meta = {
        "source": "gasoductos",
        "dataset": "capas_contextuales",
        "build_date": datetime.now().isoformat() + "Z",
        "source_file": "capas_contextuales.geojson",
        "rows": int(len(gdf)),
        "columns": list(gdf.columns),
        "geometry_type": "LineString",
        "crs": "EPSG:4326",
        "schema_version": "1.0",
        "total_length_km": float(gdf["length_km"].sum()),
        "features": gdf[["descripcion", "empresa", "estatus", "length_km"]].to_dict(orient="records"),
    }
    meta_path = out_dir / "capas_contextuales.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    print(f"✅ Gasoductos: {len(gdf):,} features → {out_path}")
    print(f"   Total length: {gdf['length_km'].sum():.1f} km")
    for _, row in gdf.iterrows():
        print(f"   - {row['descripcion']}: {row['length_km']:.1f} km ({row['estatus']})")


if __name__ == "__main__":
    main()