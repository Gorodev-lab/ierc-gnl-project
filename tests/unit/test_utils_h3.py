"""
Unit Tests — H3 Utilities (src/utils/h3.py)
==============================================
"""

import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from src.utils.h3 import (
    get_gulf_h3_cells,
    add_h3_column_vectorized,
    vector_to_h3_grid,
    create_temporal_partition_columns
)


def test_get_gulf_h3_cells():
    """Prueba la generación de celdas H3 en el Golfo de California."""
    cells_res8 = get_gulf_h3_cells(resolution=8)
    assert isinstance(cells_res8, list)
    assert len(cells_res8) > 0
    assert isinstance(cells_res8[0], str)


def test_add_h3_column_vectorized(sample_fishing_df):
    """Prueba la adición vectorizada de índices H3 a un DataFrame."""
    res_df = add_h3_column_vectorized(sample_fishing_df, lat_col="lat", lon_col="lon", h3_col="h3_cell", resolution=8)
    assert "h3_cell" in res_df.columns
    assert res_df["h3_cell"].notna().all()
    assert len(res_df["h3_cell"].iloc[0]) == 15  # H3 cell index string length


def test_vector_to_h3_grid(sample_gdf):
    """Prueba la conversión de polígonos a rejilla H3 con fracciones de área."""
    grid_gdf = vector_to_h3_grid(sample_gdf, resolution=8, area_weight=True)
    assert isinstance(grid_gdf, gpd.GeoDataFrame)
    assert "h3_cell" in grid_gdf.columns
    assert "area_fraction" in grid_gdf.columns
    assert len(grid_gdf) > 0
    assert grid_gdf["area_fraction"].between(0.0, 1.0, inclusive="both").all()


def test_create_temporal_partition_columns():
    """Prueba la creación de columnas de partición temporal."""
    df = pd.DataFrame({"timestamp": ["2023-05-15 12:00:00", "2023-11-20 18:30:00"]})
    res_df = create_temporal_partition_columns(df, time_col="timestamp", freq="monthly")
    assert "year" in res_df.columns
    assert "month" in res_df.columns
    assert "time_partition" in res_df.columns
    assert res_df["time_partition"].iloc[0] == "2023-05"
    assert res_df["time_partition"].iloc[1] == "2023-11"
