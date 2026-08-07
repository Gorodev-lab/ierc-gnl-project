#!/usr/bin/env python3
"""
Clean and merge gas pipeline (ductos) datasets from CNIH/SENER ArcGIS.
Input: Multiple GeoJSON files in data/raw/gasoductos/
Output: lakehouse/processed/gasoductos/ductos_cnih.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import geopandas as gpd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir, gasoductos_raw_dir


def load_and_standardize() -> gpd.GeoDataFrame:
    """Load all ductos GeoJSON files and standardize columns."""
    raw_dir = gasoductos_raw_dir()
    
    files = {
        'ductos_integrados_sistrangas.geojson': 'integrados_sistrangas',
        'ductos_no_integrados_sistrangas.geojson': 'no_integrados_sistrangas',
        'ducto_pacific_limited.geojson': 'pacific_limited',
        'poliductos_petroliferos.geojson': 'poliductos_petroliferos',
        'capas_contextuales.geojson': 'capas_contextuales',  # existing contextual layer
    }
    
    gdfs = []
    
    for fname, source in files.items():
        path = raw_dir / fname
        if not path.exists():
            print(f"Warning: {path} not found, skipping")
            continue
        
        gdf = gpd.read_file(path)
        gdf['source_dataset'] = source
        
        # Standardize common columns
        col_map = {}
        for col in gdf.columns:
            col_lower = col.lower()
            if col_lower in ['ducto', 'nombre', 'name']:
                col_map[col] = 'nombre'
            elif col_lower in ['proyecto', 'project']:
                col_map[col] = 'proyecto'
            elif col_lower in ['tipo', 'type']:
                col_map[col] = 'tipo'
            elif col_lower in ['longitud_k', 'longitud', 'length_km', 'longitud_km']:
                col_map[col] = 'longitud_km'
            elif col_lower in ['capacidad_', 'capacidad', 'capacity']:
                col_map[col] = 'capacidad'
            elif col_lower in ['zona_tarif', 'zona_tarifaria', 'tariff_zone']:
                col_map[col] = 'zona_tarifaria'
            elif col_lower in ['permiso_cr', 'permiso', 'permit']:
                col_map[col] = 'permiso'
            elif col_lower in ['estatus', 'status']:
                col_map[col] = 'estatus'
            elif col_lower in ['empresa', 'company', 'promotor', 'desarrolla']:
                col_map[col] = 'empresa'
            elif col_lower in ['tramo', 'segment']:
                col_map[col] = 'tramo'
            elif col_lower in ['integrado_', 'integrado']:
                col_map[col] = 'integrado_sistrangas'
        
        if col_map:
            gdf = gdf.rename(columns=col_map)
        
        # Ensure CRS
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)
        elif gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)
        
        # Remove duplicate columns (keep first)
        if gdf.columns.duplicated().any():
            gdf = gdf.loc[:, ~gdf.columns.duplicated()]
        
        gdfs.append(gdf)
        print(f"  Loaded {source}: {len(gdf)} features, cols={list(gdf.columns)}")
    
    if not gdfs:
        raise ValueError("No datasets loaded")
    
    # Combine all
    combined = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
    
    # Ensure geometry column
    combined = combined.set_geometry('geometry')
    combined.set_crs(epsg=4326, inplace=True)
    
    # Calculate length in km
    combined_proj = combined.to_crs(epsg=3857)
    combined['length_km_calc'] = combined_proj.geometry.length / 1000
    
    # Fill longitud_km from calculated if missing
    if 'longitud_km' in combined.columns:
        combined['longitud_km'] = pd.to_numeric(combined['longitud_km'], errors='coerce')
        combined['longitud_km'] = combined['longitud_km'].fillna(combined['length_km_calc'])
    else:
        combined['longitud_km'] = combined['length_km_calc']
    
    combined = combined.drop(columns=['length_km_calc'], errors='ignore')
    
    # Separate polygons (ANP/Ramsar) from line strings (ductos)
    ductos = combined[combined.geometry.geom_type == 'LineString'].copy()
    anp_polys = combined[combined.geometry.geom_type.isin(['Polygon', 'MultiPolygon'])].copy()
    
    # Sort
    sort_cols = [c for c in ['source_dataset', 'nombre', 'ducto'] if c in ductos.columns]
    if sort_cols:
        ductos = ductos.sort_values(sort_cols).reset_index(drop=True)
    
    return ductos, anp_polys


def main():
    ductos, anp_polys = load_and_standardize()
    
    out_dir = get_lakehouse_dir("silver") / "gasoductos"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Save ductos (LineStrings)
    ductos_path = out_dir / "ductos_cnih.parquet"
    ductos.to_parquet(ductos_path, index=False)
    
    # Save ANP polygons separately
    anp_path = out_dir / "anp_ramsar_cnih.parquet"
    anp_polys.to_parquet(anp_path, index=False)
    
    # Meta for ductos
    meta = {
        "source": "cnih_sener",
        "dataset": "ductos_cnih",
        "build_date": datetime.now().isoformat() + "Z",
        "source_files": [
            "ductos_integrados_sistrangas.geojson",
            "ductos_no_integrados_sistrangas.geojson",
            "ducto_pacific_limited.geojson",
            "poliductos_petroliferos.geojson",
            "capas_contextuales.geojson",
        ],
        "rows": int(len(ductos)),
        "columns": list(ductos.columns),
        "geometry_type": "LineString",
        "crs": "EPSG:4326",
        "schema_version": "1.0",
        "total_length_km": float(ductos['longitud_km'].sum()),
        "by_source": ductos['source_dataset'].value_counts().to_dict(),
    }
    meta_path = out_dir / "ductos_cnih.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    # Meta for ANP
    anp_meta = {
        "source": "cnih_sener",
        "dataset": "anp_ramsar_cnih",
        "build_date": datetime.now().isoformat() + "Z",
        "source_files": ["capas_contextuales.geojson"],
        "rows": int(len(anp_polys)),
        "columns": list(anp_polys.columns),
        "geometry_type": "Polygon",
        "crs": "EPSG:4326",
        "schema_version": "1.0",
        "by_source": anp_polys['source_dataset'].value_counts().to_dict() if len(anp_polys) > 0 else {},
    }
    anp_meta_path = out_dir / "anp_ramsar_cnih.meta.json"
    anp_meta_path.write_text(json.dumps(anp_meta, indent=2, ensure_ascii=False))
    
    print(f"✅ Ductos CNIH: {len(ductos):,} features → {out_dir / 'ductos_cnih.parquet'}")
    print(f"   Total length: {ductos['longitud_km'].sum():.1f} km")
    print(f"   By source: {ductos['source_dataset'].value_counts().to_dict()}")
    print(f"   Meta: {out_dir / 'ductos_cnih.meta.json'}")
    
    if len(anp_polys) > 0:
        print(f"✅ ANP/Ramsar CNIH: {len(anp_polys):,} features → {anp_path}")
        print(f"   Meta: {anp_meta_path}")


if __name__ == "__main__":
    main()