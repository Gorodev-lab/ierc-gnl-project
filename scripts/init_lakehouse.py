#!/usr/bin/env python3
"""
Initialize Lakehouse - IERC-GNL
================================
Script de inicialización del lakehouse: crea estructura, carga catálogo,
y ejecuta ingestas iniciales.
"""

import sys
import logging
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.catalog.catalog import DataCatalog, load_catalog_from_yaml
from src.data.lakehouse.storage import create_storage_from_config, LocalFileStorage, StorageConfig
from src.data.ingestion.nasa_oceancolor import create_nasa_ingester
from src.data.ingestion.gfw_fishing import create_gfw_ingester
from src.data.ingestion.tnc_vector import create_tnc_ingester
from src.data.ingestion.asea_mias import create_asea_ingester

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_lakehouse_structure(config_path: str = "/home/gorops/ierc-gnl-project/config/lakehouse.yaml"):
    """Inicializa estructura de directorios del lakehouse."""
    storage = create_storage_from_config(config_path)
    logger.info(f"Lakehouse inicializado en: {storage.root}")
    
    # Verificar capas
    for layer_name, layer_path in storage.config.layers.items():
        full_path = storage.root / layer_path
        logger.info(f"  Capa {layer_name}: {full_path} ({'existe' if full_path.exists() else 'creado'})")
    
    return storage


def init_catalog(config_path: str = "/home/gorops/ierc-gnl-project/config/lakehouse.yaml",
                 catalog_yaml: str = "/home/gorops/ierc-gnl-project/config/data_catalog.yaml"):
    """Inicializa catálogo DuckDB desde YAML."""
    storage = create_storage_from_config(config_path)
    catalog_path = storage.root / "metadata" / "catalog.duckdb"
    
    logger.info(f"Inicializando catálogo en: {catalog_path}")
    catalog = load_catalog_from_yaml(str(catalog_path), catalog_yaml)
    
    # Listar datasets registrados
    datasets = catalog.list_datasets()
    logger.info(f"Datasets registrados: {len(datasets)}")
    for ds in datasets:
        logger.info(f"  - {ds.name} [{ds.priority}] ({ds.format}) - {ds.source_type}")
    
    return catalog


def run_nasa_ingestion(catalog, storage, variable: str = "chlor_a"):
    """Ejecuta ingesta NASA OceanColor."""
    logger.info(f"=== Iniciando ingesta NASA {variable.upper()} ===")
    
    ingester = create_nasa_ingester(variable, catalog, storage)
    result = ingester.run()
    
    logger.info(f"Resultado NASA {variable}: {result}")
    return result


def run_gfw_ingestion(catalog, storage, dataset_type: str = "fishing_effort"):
    """Ejecuta ingesta GFW."""
    logger.info(f"=== Iniciando ingesta GFW {dataset_type} ===")
    
    ingester = create_gfw_ingester(dataset_type, catalog, storage)
    result = ingester.run()
    
    logger.info(f"Resultado GFW {dataset_type}: {result}")
    return result


def run_tnc_ingestion(catalog, storage):
    """Ejecuta ingesta TNC para ambas capas."""
    logger.info(f"=== Iniciando ingesta TNC ===")
    
    results = {}
    for layer_name in ["bajos_marinos", "arrecifes_coral_negro"]:
        logger.info(f"--- Procesando capa TNC: {layer_name} ---")
        ingester = create_tnc_ingester(catalog, storage, layer_name)
        result = ingester.run()
        results[layer_name] = result
        logger.info(f"Resultado TNC {layer_name}: {result}")
    
    return results


def run_asea_ingestion(catalog, storage):
    """Ejecuta ingesta ASEA."""
    logger.info(f"=== Iniciando ingesta ASEA ===")
    
    ingester = create_asea_ingester(catalog, storage)
    result = ingester.run()
    
    logger.info(f"Resultado ASEA: {result}")
    return result


def verify_lakehouse(storage):
    """Verifica estructura del lakehouse después de ingesta."""
    logger.info("=== Verificando Lakehouse ===")
    
    layers = ['bronze', 'silver', 'gold']
    for layer in layers:
        logger.info(f"\nCapa {layer}:")
        try:
            # Listar directorios principales
            layer_root = storage.root / storage.config.layers[layer]
            if layer_root.exists():
                for item in sorted(layer_root.iterdir()):
                    if item.is_dir():
                        size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                        logger.info(f"  {item.name}/ - {size / 1e6:.1f} MB")
        except Exception as e:
            logger.warning(f"  Error listando {layer}: {e}")


def main():
    """Función principal de inicialización."""
    logger.info("=" * 60)
    logger.info("INICIALIZACIÓN LAKEHOUSE IERC-GNL")
    logger.info("=" * 60)
    
    # 1. Inicializar estructura
    storage = init_lakehouse_structure()
    
    # 2. Inicializar catálogo
    catalog = init_catalog()
    
    # 3. Ejecutar ingestas (en orden de prioridad)
    results = {}
    
    try:
        # NASA Chlorofila-a (crítico para modelo de riesgo)
        results['nasa_chlor_a'] = run_nasa_ingestion(catalog, storage, "chlor_a")
    except Exception as e:
        logger.error(f"Fallo ingesta NASA chlor_a: {e}")
        results['nasa_chlor_a'] = {"status": "failed", "error": str(e)}
    
    try:
        # NASA SST
        results['nasa_sst'] = run_nasa_ingestion(catalog, storage, "sst")
    except Exception as e:
        logger.error(f"Fallo ingesta NASA sst: {e}")
        results['nasa_sst'] = {"status": "failed", "error": str(e)}
    
    try:
        # TNC (capas vectoriales estáticas)
        results['tnc'] = run_tnc_ingestion(catalog, storage)
    except Exception as e:
        logger.error(f"Fallo ingesta TNC: {e}")
        results['tnc'] = {"status": "failed", "error": str(e)}
    
    try:
        # ASEA (proyectos GNL)
        results['asea'] = run_asea_ingestion(catalog, storage)
    except Exception as e:
        logger.error(f"Fallo ingesta ASEA: {e}")
        results['asea'] = {"status": "failed", "error": str(e)}
    
    # GFW es grande, hacerlo opcional
    # try:
    #     results['gfw_vessels'] = run_gfw_ingestion(catalog, storage, "vessels")
    #     results['gfw_fishing'] = run_gfw_ingestion(catalog, storage, "fishing_effort")
    # except Exception as e:
    #     logger.error(f"Fallo ingesta GFW: {e}")
    
    # 4. Verificar lakehouse
    verify_lakehouse(storage)
    
    # 5. Resumen
    logger.info("\n" + "=" * 60)
    logger.info("RESUMEN DE INICIALIZACIÓN")
    logger.info("=" * 60)
    
    for name, result in results.items():
        status = result.get('status', 'unknown')
        if status == 'success':
            inserted = result.get('records_inserted', 0)
            logger.info(f"  ✅ {name}: {inserted:,} registros")
        else:
            error = result.get('error', 'unknown error')
            logger.info(f"  ❌ {name}: FALLÓ - {error}")
    
    # Cerrar catálogo
    catalog.close()
    
    logger.info("\n✅ Inicialización completada")
    logger.info(f"Lakehouse listo en: {storage.root}")
    logger.info(f"Catálogo: {storage.root / 'metadata' / 'catalog.duckdb'}")


if __name__ == "__main__":
    main()