"""
ASEA MIA Ingester with CDC - IERC-GNL
======================================
Ingesta incremental de proyectos GNL/Gas Natural desde ASEA/CENAGAS/SENER.
"""

import pandas as pd
import hashlib
from pathlib import Path
from typing import Iterator, Optional, List, Dict, Any
import logging

from .base import BaseIngester, IngestionConfig
from ..catalog.catalog import DataCatalog
from src.utils.h3 import add_h3_column_vectorized, filter_df_bbox
from src.utils.standardize import standardize_columns
from src.utils.logging import setup_logging
from config import get_causanatura_dir

logger = setup_logging(__name__)


class ASEAMIASIngester(BaseIngester):
    """
    Ingester para Manifestaciones de Impacto Ambiental (MIA) de ASEA
    y proyectos consolidados de CENAGAS/SENER.
    """
    
    def __init__(self, 
                 config: IngestionConfig,
                 catalog: DataCatalog,
                 storage,
                 source_dir: str = None,
                 files: List[str] = None):
        
        BaseIngester.__init__(self, config, catalog, storage)
        
        if source_dir is None:
            source_dir = str(get_causanatura_dir("output"))
        
        self.source_dir = Path(source_dir)
        self.files = files or [
            "gnl_proyectos_consolidados.csv",
            "asea_mias_alto_golfo.csv"
        ]
    
    def extract(self) -> Iterator[pd.DataFrame]:
        """Extrae y consolida datos de todos los archivos fuente."""
        
        all_dfs = []
        
        for file_name in self.files:
            file_path = self.source_dir / file_name
            if not file_path.exists():
                logger.warning(f"Archivo no encontrado: {file_path}")
                continue
            
            logger.info(f"Leyendo {file_path.name}")
            df = pd.read_csv(file_path)
            
            # Añadir metadatos de fuente
            df['source_file'] = file_name
            df['source_type'] = self._classify_source(file_name)
            
            all_dfs.append(df)
        
        if not all_dfs:
            logger.warning("No se encontraron datos en archivos fuente")
            return
        
        # Consolidar
        consolidated = pd.concat(all_dfs, ignore_index=True)
        
        # Deduplicar por proyecto_id manteniendo el más reciente
        if 'proyecto_id' in consolidated.columns:
            consolidated = consolidated.sort_values('source_file').drop_duplicates(
                subset=['proyecto_id'], keep='last'
            )
        
        logger.info(f"Consolidados {len(consolidated)} proyectos únicos")
        yield consolidated
    
    def _classify_source(self, file_name: str) -> str:
        """Clasifica tipo de fuente por nombre de archivo."""
        if 'gnl_proyectos_consolidados' in file_name:
            return 'consolidated'
        elif 'asea_mias' in file_name:
            return 'asea'
        elif 'cenagas' in file_name.lower():
            return 'cenagas'
        elif 'sener' in file_name.lower():
            return 'sener'
        return 'unknown'
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforma a formato estandarizado con H3 y CDC hash."""
        
        df = df.copy()
        
        # Estandarizar nombres de columnas
        df = self._standardize_columns(df)
        
        # Generar proyecto_id si no existe
        if 'proyecto_id' not in df.columns:
            df['proyecto_id'] = df.apply(self._generate_project_id, axis=1)
        
        # Añadir H3 cell (resolución 10 para infraestructura puntual)
        if 'lat' in df.columns and 'lon' in df.columns:
            df = add_h3_column_vectorized(df, 'lat', 'lon', 'h3_cell_10', 10)
        
        # Añadir timestamp de ingesta
        df['ingestion_timestamp'] = pd.Timestamp.utcnow()
        
        # Columnas temporales (proyectos son estáticos pero versionados)
        df['year'] = pd.Timestamp.utcnow().year
        df['month'] = pd.Timestamp.utcnow().month
        df['time_partition'] = pd.Timestamp.utcnow().strftime('%Y-%m')
        
        # Seleccionar columnas finales
        output_cols = [
            'proyecto_id', 'nombre', 'estado', 'tipo_proyecto', 'fuente',
            'lat', 'lon', 'estatus', 'capacidad_mtpa', 'longitud_km',
            'folio_asea', 'pdf_url', 'source_file', 'source_type',
            'h3_cell_10', 'ingestion_timestamp',
            'year', 'month', 'time_partition'
        ]
        
        output_cols = [c for c in output_cols if c in df.columns]
        
        return df[output_cols]
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Estandariza columnas entre diferentes fuentes."""
        
        df = df.copy()
        
        # Mapeo de columnas comunes
        column_map = {
            'proyecto_id': ['proyecto_id', 'id', 'folio', 'folio_asea'],
            'nombre': ['nombre', 'proyecto', 'nombre_proyecto', 'project_name'],
            'estado': ['estado', 'state', 'entidad'],
            'tipo_proyecto': ['tipo_proyecto', 'tipo', 'type', 'categoria'],
            'fuente': ['fuente', 'source', 'origen'],
            'lat': ['lat', 'latitud', 'latitude', 'y'],
            'lon': ['lon', 'longitud', 'longitude', 'x'],
            'estatus': ['estatus', 'status', 'estatus_proyecto', 'estado_proyecto'],
            'capacidad_mtpa': ['capacidad_mtpa', 'capacidad', 'capacity_mtpa'],
            'longitud_km': ['longitud_km', 'longitud', 'length_km'],
            'folio_asea': ['folio_asea', 'folio', 'numero_folio'],
            'pdf_url': ['pdf_url', 'url_pdf', 'pdf_link', 'url']
        }
        
        for std_name, possible_names in column_map.items():
            for col in possible_names:
                if col in df.columns:
                    df = df.rename(columns={col: std_name})
                    break
        
        # Normalizar tipo_proyecto
        if 'tipo_proyecto' in df.columns:
            type_map = {
                'terminal gnl': 'terminal_gnl',
                'terminal_gnl': 'terminal_gnl',
                'gnl terminal': 'terminal_gnl',
                'gasoducto transporte': 'gasoducto_transporte',
                'gasoducto_transporte': 'gasoducto_transporte',
                'pipeline': 'gasoducto_transporte',
                'gasoducto distribucion': 'gasoducto_distribucion',
                'gasoducto_distribucion': 'gasoducto_distribucion',
                'distribution': 'gasoducto_distribucion',
                'planta licuefaccion': 'planta_licuefaccion',
                'planta_licuefaccion': 'planta_licuefaccion',
                'liquefaction': 'planta_licuefaccion',
                'estacion compresion': 'estacion_compresion',
                'estacion_compresion': 'estacion_compresion',
                'compression station': 'estacion_compresion'
            }
            df['tipo_proyecto'] = df['tipo_proyecto'].str.lower().map(type_map).fillna(df['tipo_proyecto'])
        
        # Normalizar estatus
        if 'estatus' in df.columns:
            status_map = {
                'en operacion': 'En_operacion',
                'en_operacion': 'En_operacion',
                'operando': 'En_operacion',
                'operational': 'En_operacion',
                'en construccion': 'En_construccion',
                'en_construccion': 'En_construccion',
                'construccion': 'En_construccion',
                'under construction': 'En_construccion',
                'en planeacion': 'En_planeacion',
                'en_planeacion': 'En_planeacion',
                'planeacion': 'En_planeacion',
                'planned': 'En_planeacion',
                'autorizado': 'Autorizado',
                'authorized': 'Autorizado',
                'approved': 'Autorizado',
                'en evaluacion': 'En_evaluacion',
                'en_evaluacion': 'En_evaluacion',
                'evaluacion': 'En_evaluacion',
                'under review': 'En_evaluacion'
            }
            df['estatus'] = df['estatus'].str.lower().map(status_map).fillna(df['estatus'])
        
        # Asegurar tipos numéricos
        for col in ['lat', 'lon', 'capacidad_mtpa', 'longitud_km']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def _generate_project_id(self, row: pd.Series) -> str:
        """Genera ID único para proyecto."""
        # Usar folio_asea si existe, sino hash de nombre+estado+tipo
        if pd.notna(row.get('folio_asea')):
            return f"ASEA_{row['folio_asea']}"
        
        content = f"{row.get('nombre', '')}|{row.get('estado', '')}|{row.get('tipo_proyecto', '')}"
        return f"GEN_{hashlib.md5(content.encode()).hexdigest()[:12]}"
    
    def _get_partition_path(self, df: pd.DataFrame) -> str:
            return "asea/mias_enriched/"


def create_asea_ingester(catalog, storage, **kwargs):
    """Factory para crear ASEAMIASIngester."""
    from src.data.ingestion.factory import create_ingester
    return create_ingester(ASEAMIASIngester, "asea_mias", catalog, storage, **kwargs)


if __name__ == "__main__":
    from src.utils.logging import setup_logging
    setup_logging("ierc_gnl.asea_mias")
    print("ASEA MIA Ingester module loaded")