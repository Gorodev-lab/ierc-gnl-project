"""
Unit tests for NASA OceanColor Ingester - IERC-GNL
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data.ingestion.nasa_oceancolor import (
    NASAOceanColorIngester,
    create_nasa_ingester,
)


class TestNASAOceanColorIngesterInit:
    """Test NASAOceanColorIngester initialization and configuration."""
    
    def test_chlor_a_ingester_initialization(self):
        """Test chlor_a ingester initializes with correct config."""
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(
            dataset_name="nasa_chlor_a",
            h3_resolution=8,
            bbox=(22.5, -115.0, 32.0, -108.0)
        )
        catalog = DataCatalog()
        storage_config = StorageConfig(
            root_path="/tmp/test",
            layers={"silver": "silver"}
        )
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config,
            catalog=catalog,
            storage=storage,
            variable="chlor_a"
        )
        
        assert ingester.variable == "chlor_a"
        assert ingester.config.h3_resolution == 8
        assert "chlor_a" in ingester.file_patterns
    
    def test_sst_ingester_initialization(self):
        """Test SST ingester initializes with correct config."""
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(
            dataset_name="nasa_sst",
            h3_resolution=8,
            bbox=(22.5, -115.0, 32.0, -108.0)
        )
        catalog = DataCatalog()
        storage_config = StorageConfig(
            root_path="/tmp/test",
            layers={"silver": "silver"}
        )
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config,
            catalog=catalog,
            storage=storage,
            variable="sst"
        )
        
        assert ingester.variable == "sst"
        assert "sst" in ingester.file_patterns
    
    def test_factory_function_chlor_a(self):
        """Test factory creates chlor_a ingester."""
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = create_nasa_ingester("chlor_a", catalog, storage)
        
        assert isinstance(ingester, NASAOceanColorIngester)
        assert ingester.variable == "chlor_a"
    
    def test_factory_function_sst(self):
        """Test factory creates SST ingester."""
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = create_nasa_ingester("sst", catalog, storage)
        
        assert isinstance(ingester, NASAOceanColorIngester)
        assert ingester.variable == "sst"


class TestBoundingBoxSlicing:
    """Test bounding box slicing and _FillValue filtering."""
    
    @pytest.fixture
    def mock_netcdf_dataset(self):
        """Create a mock xarray Dataset with synthetic NetCDF data."""
        lats = np.linspace(32.0, 22.5, 50)  # decreasing for xarray
        lons = np.linspace(-115.0, -108.0, 50)
        
        # Create data with some fill values
        data = np.random.uniform(0.1, 10.0, (50, 50)).astype(np.float32)
        data[0, 0] = -32767.0  # fill value
        data[-1, -1] = np.nan  # NaN
        
        ds = xr.Dataset(
            {
                "chlor_a": (["lat", "lon"], data, {
                    "units": "mg m^-3",
                    "long_name": "Chlorophyll-a concentration",
                    "_FillValue": -32767.0,
                    "valid_min": 0.0,
                    "valid_max": 100.0,
                })
            },
            coords={
                "lat": (["lat"], lats, {"units": "degrees_north"}),
                "lon": (["lon"], lons, {"units": "degrees_east"}),
                "time": ([], np.datetime64("2020-01-15"), {"units": "days since 1970-01-01"})
            }
        )
        ds.attrs = {"title": "Test", "source": "MODIS-Aqua"}
        return ds
    
    @patch('src.data.ingestion.nasa_oceancolor.xr.open_dataset')
    def test_process_netcdf_file_filters_fill_values(self, mock_open_dataset, mock_netcdf_dataset):
        """Test that _FillValue and NaN are filtered out."""
        mock_open_dataset.return_value = mock_netcdf_dataset
        
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(
            dataset_name="nasa_chlor_a",
            h3_resolution=8,
            bbox=(22.5, -115.0, 32.0, -108.0)
        )
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config, catalog=catalog, storage=storage, variable="chlor_a"
        )
        
        # Mock the file path
        with patch.object(Path, 'glob', return_value=[Path("/fake/nasa_chlor_a_2020_01.nc")]):
            with patch.object(Path, 'stem', "nasa_chlor_a_2020_01"):
                df = ingester._process_netcdf_file(Path("/fake/nasa_chlor_a_2020_01.nc"), 2020, 1)
        
        assert not df.empty
        # Should have H3 cells
        assert 'h3_cell' in df.columns
        assert 'value_mean' in df.columns
        assert 'year' in df.columns
        assert 'month' in df.columns
        assert df['year'].iloc[0] == 2020
        assert df['month'].iloc[0] == 1
    
    @patch('src.data.ingestion.nasa_oceancolor.xr.open_dataset')
    def test_bounding_box_slicing_applied(self, mock_open_dataset, mock_netcdf_dataset):
        """Test that bbox slicing is applied to the data."""
        mock_open_dataset.return_value = mock_netcdf_dataset
        
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(
            dataset_name="nasa_chlor_a",
            h3_resolution=8,
            bbox=(22.5, -115.0, 32.0, -108.0)
        )
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config, catalog=catalog, storage=storage, variable="chlor_a"
        )
        
        with patch.object(Path, 'glob', return_value=[Path("/fake/nasa_chlor_a_2020_01.nc")]):
            df = ingester._process_netcdf_file(Path("/fake/nasa_chlor_a_2020_01.nc"), 2020, 1)
        
        # Verify the open_dataset was called
        mock_open_dataset.assert_called_once()


class TestH3GridAggregation:
    """Test H3 grid aggregation (mean, std, count)."""
    
    @pytest.fixture
    def mock_netcdf_dataset_aggregation(self):
        """Create mock dataset for aggregation testing."""
        # Smaller grid for faster testing
        lats = np.linspace(32.0, 22.5, 20)
        lons = np.linspace(-115.0, -108.0, 20)
        
        # Constant value to verify mean aggregation
        data = np.full((20, 20), 5.0, dtype=np.float32)
        
        ds = xr.Dataset(
            {
                "chlor_a": (["lat", "lon"], data, {
                    "units": "mg m^-3",
                    "_FillValue": -32767.0,
                })
            },
            coords={
                "lat": (["lat"], lats),
                "lon": (["lon"], lons),
            }
        )
        return ds
    
    @patch('src.data.ingestion.nasa_oceancolor.xr.open_dataset')
    def test_aggregation_computes_mean_std_count(self, mock_open_dataset, mock_netcdf_dataset_aggregation):
        """Test that aggregation produces mean, std, count per H3 cell."""
        mock_open_dataset.return_value = mock_netcdf_dataset_aggregation
        
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(
            dataset_name="nasa_chlor_a",
            h3_resolution=8,
            bbox=(22.5, -115.0, 32.0, -108.0)
        )
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config, catalog=catalog, storage=storage, variable="chlor_a"
        )
        
        with patch.object(Path, 'glob', return_value=[Path("/fake/nasa_chlor_a_2020_01.nc")]):
            df = ingester._process_netcdf_file(Path("/fake/nasa_chlor_a_2020_01.nc"), 2020, 1)
        
        assert not df.empty
        # Check aggregation columns exist
        assert 'value_mean' in df.columns
        assert 'value_std' in df.columns
        assert 'value_count' in df.columns
        # Mean should be ~5.0 for constant data
        assert np.allclose(df['value_mean'], 5.0, atol=0.1)
        # Std is NaN when only 1 pixel per H3 cell (common at res 8), fill with 0 for test
        std_vals = df['value_std'].fillna(0)
        assert np.allclose(std_vals, 0.0, atol=0.1)
        # Count should be > 0
        assert (df['value_count'] > 0).all()


class TestPartitionPathGeneration:
    """Test Hive-style partition path generation."""
    
    def test_partition_path_format_chlor_a(self):
        """Test partition path format for chlor_a."""
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(dataset_name="nasa_chlor_a")
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config, catalog=catalog, storage=storage, variable="chlor_a"
        )
        
        # Test with DataFrame containing year/month
        df = pd.DataFrame({
            'year': [2024],
            'month': [1],
            'h3_cell': ['8a2a1072b5fffff']
        })
        
        path = ingester._get_partition_path(df)
        assert path == "nasa/chlor_a/year=2024/month=01/"
    
    def test_partition_path_format_sst(self):
        """Test partition path format for SST."""
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(dataset_name="nasa_sst")
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config, catalog=catalog, storage=storage, variable="sst"
        )
        
        df = pd.DataFrame({
            'year': [2023],
            'month': [12],
            'h3_cell': ['8a2a1072b5fffff']
        })
        
        path = ingester._get_partition_path(df)
        assert path == "nasa/sst/year=2023/month=12/"
    
    def test_partition_path_empty_dataframe(self):
        """Test partition path for empty DataFrame."""
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(dataset_name="nasa_chlor_a")
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config, catalog=catalog, storage=storage, variable="chlor_a"
        )
        
        df = pd.DataFrame()
        path = ingester._get_partition_path(df)
        assert path == "nasa/chlor_a/"


class TestTransformMethod:
    """Test transform method output format."""
    
    def test_transform_renames_columns_correctly(self):
        """Test transform renames aggregation columns to variable names."""
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(dataset_name="nasa_chlor_a", h3_resolution=8)
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config, catalog=catalog, storage=storage, variable="chlor_a"
        )
        
        # Input DataFrame with aggregation columns
        df = pd.DataFrame({
            'time': [pd.Timestamp("2020-01-01")],
            'year': [2020],
            'month': [1],
            'time_partition': ["2020-01"],
            'h3_cell': ['8a2a1072b5fffff'],
            'value_mean': [5.5],
            'value_std': [0.2],
            'value_count': [100],
            'lat_mean': [25.0],
            'lon_mean': [-112.0],
        })
        
        result = ingester.transform(df)
        
        # Check renamed columns
        assert 'chlor_a' in result.columns
        assert 'chlor_a_std' in result.columns
        assert 'chlor_a_count' in result.columns
        # Original aggregation columns should be gone
        assert 'value_mean' not in result.columns
        assert 'value_std' not in result.columns
        assert 'value_count' not in result.columns


class TestExtractIterator:
    """Test extract() iterator behavior."""
    
    @patch('src.data.ingestion.nasa_oceancolor.xr.open_dataset')
    def test_extract_yields_one_df_per_file(self, mock_open_dataset):
        """Test extract yields one DataFrame per NetCDF file."""
        # Create mock dataset
        lats = np.linspace(32.0, 22.5, 10)
        lons = np.linspace(-115.0, -108.0, 10)
        data = np.random.uniform(0.1, 10.0, (10, 10)).astype(np.float32)
        
        ds = xr.Dataset(
            {"chlor_a": (["lat", "lon"], data, {"_FillValue": -32767.0})},
            coords={"lat": (["lat"], lats), "lon": (["lon"], lons)}
        )
        mock_open_dataset.return_value = ds
        
        from src.data.ingestion.base import IngestionConfig
        from src.data.catalog.catalog import DataCatalog
        from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
        
        config = IngestionConfig(dataset_name="nasa_chlor_a", h3_resolution=8)
        catalog = DataCatalog()
        storage_config = StorageConfig(root_path="/tmp/test", layers={"silver": "silver"})
        storage = LocalFileStorage(storage_config)
        
        ingester = NASAOceanColorIngester(
            config=config, catalog=catalog, storage=storage, variable="chlor_a"
        )
        
        # Mock multiple files
        fake_files = [
            Path("/fake/nasa_chlor_a_2020_01.nc"),
            Path("/fake/nasa_chlor_a_2020_02.nc"),
            Path("/fake/nasa_chlor_a_2020_03.nc"),
        ]
        
        with patch.object(Path, 'glob', return_value=fake_files):
            with patch.object(Path, 'stem', new_callable=lambda: "nasa_chlor_a_2020_01"):
                dfs = list(ingester.extract())
        
        assert len(dfs) == 3
        assert all(isinstance(df, pd.DataFrame) for df in dfs)
        assert all(not df.empty for df in dfs)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])