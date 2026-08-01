"""
PANGAS Vector Ingester - IERC-GNL
=================================
Ingesta de polígonos pesqueros artesanales PANGAS (GeoJSON) → H3 grid.
Aplica el estándar oficial `uid_espaciotemporal`.
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from typing import Iterator, Optional, List, Dict, Any
import logging

from .base import BaseIngester, IngestionConfig
from ..lakehouse.partitioning import vector_to_h3_grid

logger = logging.getLogger(__name__)

CRITICAL_SPECIES_CODES = {
    'CARSPP', 'GYMMAR', 'RHILON', 'RHIPRO', 'RHISPP',
    'SPHSPP', 'LUTARG', 'PARSPP', 'DASSPP', 'DASDIP', 'MYCROS'
}


class PangasVectorIngester(BaseIngester):
    """
    Ingester para datos pesqueros artesanales PANGAS.
    Capas soportadas:
    - ZPesca_PANGAS_wgs84.geojson
    - Riqueza_Relativa_wgs84.geojson
    - ZPesca_Buceo_wgs84.geojson / Chinchorro / Redes / Trampa
    """

    def __init__(self,
                 config: IngestionConfig,
                 catalog,
                 storage,
                 source_dir: str = "/home/gorops/ierc-gnl-project/data/raw/pangas_wgs84",
                 h3_resolution: int = 8):
        super().__init__(config, catalog, storage)
        self.source_dir = Path(source_dir)
        self.h3_resolution = h3_resolution

    def extract(self) -> Iterator[pd.DataFrame]:
        """Extrae y convierte polígonos PANGAS a grid H3 con uid_espaciotemporal."""
        pangas_path = self.source_dir / "ZPesca_PANGAS_wgs84.geojson"
        riqueza_path = self.source_dir / "Riqueza_Relativa_wgs84.geojson"

        if not pangas_path.exists():
            logger.error(f"Archivo PANGAS no encontrado en: {pangas_path}")
            return

        logger.info(f"Procesando zonas pesqueras PANGAS desde: {pangas_path.name}")
        gdf = gpd.read_file(pangas_path)

        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)
        elif gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")

        # Construir uid_espaciotemporal si no existe
        uids = []
        for _, row in gdf.iterrows():
            comunidad = str(row.get('sitio_nomb') or row.get('sitio_code') or 'DESCONOCIDO').upper().replace(' ', '_')
            sitio_code = str(row.get('sitio_code') or 'ZONA_PESCA')
            arte = str(row.get('ARTE') or 'PANGAS').upper().replace(' ', '_')
            spp = str(row.get('spp_code') or row.get('spp_nomb') or 'MULTIESPECIE').upper().replace(' ', '_')
            
            uid = f"{comunidad}-ARTESANAL-{spp}-{arte}-{sitio_code}-ANUAL-RUTA_PRINCIPAL"
            uids.append(uid)

        gdf['uid_espaciotemporal'] = uids

        # H3 grid conversion
        h3_grid = vector_to_h3_grid(gdf, resolution=self.h3_resolution, area_weight=True)

        if h3_grid.empty:
            logger.warning("No se generaron celdas H3 para PANGAS")
            return

        # Si se cuenta con riqueza relativa, realizar join por H3
        if riqueza_path.exists():
            logger.info("Incorporando capa Riqueza Relativa Pesquera...")
            gdf_riq = gpd.read_file(riqueza_path)
            if gdf_riq.crs != "EPSG:4326":
                gdf_riq = gdf_riq.to_crs("EPSG:4326")
            h3_riq = vector_to_h3_grid(gdf_riq, resolution=self.h3_resolution, area_weight=True)
            if not h3_riq.empty and 'all' in h3_riq.columns:
                h3_riq_grouped = h3_riq.groupby('h3_cell')['all'].mean().reset_index().rename(columns={'all': 'riqueza_relativa_mean'})
                h3_grid = h3_grid.merge(h3_riq_grouped, on='h3_cell', how='left')

        h3_grid['year'] = 2024
        h3_grid['month'] = 1
        h3_grid['time_partition'] = '2024-01'

        if 'geometry' in h3_grid.columns:
            h3_grid['h3_geometry_wkt'] = h3_grid['geometry'].apply(lambda g: g.wkt if g else None)
            h3_grid = h3_grid.drop(columns=['geometry'])

        yield h3_grid

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        if 'h3_cell' not in df.columns and 'h3' in df.columns:
            df = df.rename(columns={'h3': 'h3_cell'})
        return df


def create_pangas_ingester(catalog, storage, config_overrides: Dict = None) -> PangasVectorIngester:
    """Factory para crear el ingester PANGAS."""
    base_config = IngestionConfig(
        dataset_name="pangas_fishing_zones",
        layer="silver",
        partition_cols=[],
        h3_resolution=8,
        bbox=(22.5, -115.0, 32.0, -108.0),
        compression="zstd",
        batch_size=50000,
        validate=True
    )
    if config_overrides:
        for k, v in config_overrides.items():
            setattr(base_config, k, v)

    return PangasVectorIngester(
        config=base_config,
        catalog=catalog,
        storage=storage
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("PANGAS Vector Ingester module loaded")
