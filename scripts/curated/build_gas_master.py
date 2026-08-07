#!/usr/bin/env python3
"""
Build GOLD layer: Master gas infrastructure table.
Joins: inyecciones + tarifas + (extracciones when available) + nodos info.
Output: lakehouse/curated/gas_infrastructure_master.parquet
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config import get_lakehouse_dir


def build_master() -> pd.DataFrame:
    silver = get_lakehouse_dir("silver")
    
    # Load inyecciones (main fact table)
    iny = pd.read_parquet(silver / "cenegas" / "cenegas_injection_capacity.parquet")
    
    # Load extracciones (now available)
    ext = pd.read_parquet(silver / "cenegas" / "extracciones_sistrangas.parquet")
    
    # Load tarifas (dimension: zona_inyeccion x zona_extraccion x year)
    tar = pd.read_parquet(silver / "cenegas" / "tarifas_por_puntos.parquet")
    
    # NOTE: Inyecciones (Vxxx) and Extracciones (Exxx) use DIFFERENT punto codes.
    # They are separate networks (injection points vs extraction points).
    # Cannot merge directly on "punto". They link via tariff zones.
    # Extracciones has "zona_tarifaria"; Inyecciones does not.
    # Tarifas uses "zona_inyeccion" x "zona_extraccion".
    
    # Aggregate inyecciones to yearly per punto
    iny_yearly = iny.copy()
    iny_yearly["year"] = iny_yearly["fecha"].dt.year
    iny_agg = iny_yearly.groupby(["punto", "descripcion", "nom_ent", "year", "origen"]).agg(
        total_gj_inyectado=("cantidad_inyectada_gj", "sum"),
        avg_daily_gj_inyectado=("cantidad_inyectada_gj", "mean"),
        days_with_data_iny=("fecha", "count"),
    ).reset_index()
    
    # Aggregate extracciones to yearly per punto
    ext_yearly = ext.copy()
    ext_yearly["year"] = ext_yearly["fecha"].dt.year
    ext_agg = ext_yearly.groupby(["punto", "descripcion", "nom_ent", "year", "origen", "zona_tarifaria"]).agg(
        total_gj_extraido=("cantidad_extraida_gj", "sum"),
        avg_daily_gj_extraido=("cantidad_extraida_gj", "mean"),
        days_with_data_ext=("fecha", "count"),
    ).reset_index()
    
    # Punto metadata (inyecciones points)
    punto_meta_iny = iny[["punto", "descripcion", "cve_ent", "nom_ent", "cve_mun", "nom_mun"]].drop_duplicates()
    
    # Punto metadata (extracciones points)
    punto_meta_ext = ext[["punto", "descripcion", "cve_ent", "nom_ent", "cve_mun", "nom_mun"]].drop_duplicates()
    
    # Yearly tables (separate - different punto spaces)
    yearly_iny = iny_agg.sort_values(["punto", "year"]).reset_index(drop=True)
    yearly_ext = ext_agg.sort_values(["punto", "year"]).reset_index(drop=True)
    
    # Overall summary per punto (inyecciones)
    overall_iny = iny.groupby(["punto", "descripcion", "nom_ent"]).agg(
        total_gj_inyectado_all=("cantidad_inyectada_gj", "sum"),
        avg_daily_gj_inyectado=("cantidad_inyectada_gj", "mean"),
        max_daily_gj_inyectado=("cantidad_inyectada_gj", "max"),
        min_daily_gj_inyectado=("cantidad_inyectada_gj", "min"),
        days_with_data_iny=("fecha", "count"),
        first_date_iny=("fecha", "min"),
        last_date_iny=("fecha", "max"),
        origen_principal_iny=("origen", lambda x: x.mode().iloc[0] if not x.mode().empty else None),
    ).reset_index()
    
    # Overall summary per punto (extracciones)
    overall_ext = ext.groupby(["punto", "descripcion", "nom_ent"]).agg(
        total_gj_extraido_all=("cantidad_extraida_gj", "sum"),
        avg_daily_gj_extraido=("cantidad_extraida_gj", "mean"),
        max_daily_gj_extraido=("cantidad_extraida_gj", "max"),
        min_daily_gj_extraido=("cantidad_extraida_gj", "min"),
        days_with_data_ext=("fecha", "count"),
        first_date_ext=("fecha", "min"),
        last_date_ext=("fecha", "max"),
        origen_principal_ext=("origen", lambda x: x.mode().iloc[0] if not x.mode().empty else None),
        zona_tarifaria_principal=("zona_tarifaria", lambda x: x.mode().iloc[0] if not x.mode().empty else None),
    ).reset_index()
    
    # Master tables (separate for inyecciones vs extracciones)
    master_iny = punto_meta_iny.merge(overall_iny, on=["punto", "descripcion", "nom_ent"], how="left")
    master_ext = punto_meta_ext.merge(overall_ext, on=["punto", "descripcion", "nom_ent"], how="left")
    
    # Add tarifas info (zone-level)
    zone_info = tar.groupby(["zona_inyeccion", "zona_extraccion"]).agg(
        cap_base_firme_avg=("capacidad_base_firme", "mean"),
        cap_interrumpible_avg=("servicio_base_interrumpible", "mean"),
        years_covered=("fecha_inicio", lambda x: f"{x.dt.year.min()}-{x.dt.year.max()}"),
    ).reset_index()
    
    return master_iny, master_ext, yearly_iny, yearly_ext, zone_info


def main():
    master_iny, master_ext, yearly_iny, yearly_ext, zone_info = build_master()
    
    out_dir = get_lakehouse_dir("gold") / "gas_infrastructure"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Master inyecciones
    master_iny_path = out_dir / "gas_infrastructure_master_inyecciones.parquet"
    master_iny.to_parquet(master_iny_path, index=False)
    
    # Master extracciones
    master_ext_path = out_dir / "gas_infrastructure_master_extracciones.parquet"
    master_ext.to_parquet(master_ext_path, index=False)
    
    # Yearly inyecciones
    yearly_iny_path = out_dir / "gas_injection_yearly.parquet"
    yearly_iny.to_parquet(yearly_iny_path, index=False)
    
    # Yearly extracciones
    yearly_ext_path = out_dir / "gas_extraction_yearly.parquet"
    yearly_ext.to_parquet(yearly_ext_path, index=False)
    
    # Zone tarifas
    zone_path = out_dir / "tarifas_zone_summary.parquet"
    zone_info.to_parquet(zone_path, index=False)
    
    # Meta
    meta = {
        "source": "curated",
        "dataset": "gas_infrastructure_master",
        "build_date": datetime.now().isoformat() + "Z",
        "tables": {
            "master_inyecciones": {"rows": int(len(master_iny)), "cols": int(len(master_iny.columns))},
            "master_extracciones": {"rows": int(len(master_ext)), "cols": int(len(master_ext.columns))},
            "yearly_injection": {"rows": int(len(yearly_iny)), "cols": int(len(yearly_iny.columns))},
            "yearly_extraction": {"rows": int(len(yearly_ext)), "cols": int(len(yearly_ext.columns))},
            "zone_tarifas": {"rows": int(len(zone_info)), "cols": int(len(zone_info.columns))},
        },
        "schema_version": "1.0",
        "notes": "Inyecciones (Vxxx) and Extracciones (Exxx) are separate punto networks. Link via tariff zones. Ductos/infrastructure geospatial not yet integrated.",
    }
    meta_path = out_dir / "gas_infrastructure_master.meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    print(f"✅ Master inyecciones: {len(master_iny):,} → {master_iny_path}")
    print(f"✅ Master extracciones: {len(master_ext):,} → {master_ext_path}")
    print(f"✅ Yearly injection: {len(yearly_iny):,} → {yearly_iny_path}")
    print(f"✅ Yearly extraction: {len(yearly_ext):,} → {yearly_ext_path}")
    print(f"✅ Zone tarifas: {len(zone_info):,} → {zone_path}")
    print(f"✅ Meta: {meta_path}")


if __name__ == "__main__":
    main()