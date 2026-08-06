#!/usr/bin/env python3
"""
CI Verification Script: CDC exact-once + Schema contract + Derived versioning
Runs in GitHub Actions to verify the 3 v2.0 features work correctly.
"""
import pandas as pd
import shutil
from pathlib import Path

from src.data.ingestion.base import BaseIngester, IngestionConfig
from src.data.catalog.catalog import DataCatalog, load_catalog_from_yaml
from src.data.lakehouse.storage import LocalFileStorage, StorageConfig
from config import get_data_dir


def main():
    lakehouse_root = get_data_dir('lakehouse')
    catalog_dir = get_data_dir('catalog')
    test_dataset = 'ci_verify_cdc_schema'

    # Cleanup
    test_path = lakehouse_root / 'processed' / test_dataset
    if test_path.exists():
        shutil.rmtree(test_path)

    # Setup
    catalog = load_catalog_from_yaml(catalog_dir, 'config/data_catalog.yaml')
    storage = LocalFileStorage(StorageConfig(
        root_path=str(lakehouse_root),
        layers={'bronze': 'raw', 'silver': 'processed', 'gold': 'curated'}
    ))

    config = IngestionConfig(
        dataset_name=test_dataset,
        layer='silver',
        partition_cols=['h3_cell', 'year', 'month'],
        cdc_key_column='proyecto_id',
        cdc_hash_columns=['nombre', 'estado']
    )

    class TestIngester(BaseIngester):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._test_data = None

        def extract(self):
            if self._test_data is not None:
                yield self._test_data
                self._test_data = None

        def transform(self, df):
            return df

    # ── Feature 1: CDC exact-once ──────────────────────────────────────
    ing = TestIngester(config, catalog, storage)
    ing._test_data = pd.DataFrame({
        'proyecto_id': ['P1', 'P2'], 'nombre': ['A', 'B'], 'estado': ['Son', 'Sin'],
        'lat': [28.0, 25.0], 'lon': [-110.0, -109.0],
        'year': [2024, 2024], 'month': [1, 1], 'time_partition': ['2024-01', '2024-01'],
        'h3_cell': ['8a2a1072b5afff', '8a2a1072b5bfff']
    })
    assert ing.run()['records_inserted'] == 2, "CDC run1 failed"

    ing2 = TestIngester(config, catalog, storage)
    ing2._test_data = pd.DataFrame({
        'proyecto_id': ['P1', 'P2', 'P3'], 'nombre': ['A', 'B', 'C'], 'estado': ['Son', 'Sin', 'BCS'],
        'lat': [28.0, 25.0, 30.0], 'lon': [-110.0, -109.0, -114.0],
        'year': [2024]*3, 'month': [1]*3, 'time_partition': ['2024-01']*3,
        'h3_cell': ['8a2a1072b5afff', '8a2a1072b5bfff', '8a2a1072b5cfff']
    })
    assert ing2.run()['records_inserted'] == 1, "CDC run2 failed"

    ing3 = TestIngester(config, catalog, storage)
    ing3._test_data = pd.DataFrame({
        'proyecto_id': ['P1', 'P3'], 'nombre': ['A', 'C'], 'estado': ['Son', 'BCS'],
        'lat': [28.0, 30.0], 'lon': [-110.0, -114.0],
        'year': [2024]*2, 'month': [1]*2, 'time_partition': ['2024-01']*2,
        'h3_cell': ['8a2a1072b5afff', '8a2a1072b5cfff']
    })
    assert ing3.run()['records_inserted'] == 0, "CDC run3 failed"

    print("✅ Feature 1: CDC exact-once verified")

    # ── Feature 2: Schema contract ─────────────────────────────────────
    config2 = IngestionConfig(
        dataset_name='asea_mias_consolidated',
        layer='silver', partition_cols=['h3_cell_10', 'year', 'month'],
        cdc_key_column='proyecto_id', cdc_hash_columns=['nombre', 'estado']
    )
    ing4 = TestIngester(config2, catalog, storage)

    # Schema OK
    ing4._test_data = pd.DataFrame({'proyecto_id':['P1'],'nombre':['A'],'estado':['Son'],
        'tipo_proyecto':['terminal_gnl'],'fuente':['ASEA'],'lat':[28.0],'lon':[-110.0],
        'estatus':['En_operacion'],'capacidad_mtpa':[1.0],'longitud_km':[50.0],
        'folio_asea':['F1'],'pdf_url':['http://x'],'year':[2024],'month':[1],
        'time_partition':['2024-01'],'h3_cell_10':['8a2a1072b5afff']})
    assert ing4.validate_data(ing4._test_data)['passed'] == True, "Schema OK failed"

    # Missing columns
    ing4._test_data = pd.DataFrame({'proyecto_id':['P1'],'nombre':['A'],'estado':['Son'],
        'year':[2024],'month':[1],'time_partition':['2024-01'],'h3_cell_10':['8a2a1072b5afff']})
    assert ing4.validate_data(ing4._test_data)['passed'] == False, "Schema missing failed"

    print("✅ Feature 2: Schema contract validation verified")

    # ── Feature 3: Derived dataset versioning ──────────────────────────
    ds = catalog.register_derived_dataset('ci_test_derived', ['gfw','tnc'], 'v2.1', h3_resolution=8)
    assert ds.tags == ['derived'], "Derived tag failed"
    assert ds.schema['lineage']['transform_version'] == 'v2.1', "Lineage version failed"
    assert ds.schema['lineage']['sources'] == ['gfw','tnc'], "Lineage sources failed"

    print("✅ Feature 3: Derived dataset versioning verified")

    # Cleanup
    shutil.rmtree(test_path)
    print("\n🎉 ALL 3 FEATURES VERIFIED IN CI")


if __name__ == '__main__':
    main()