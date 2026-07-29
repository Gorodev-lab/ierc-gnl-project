#!/usr/bin/env python3
"""
build_drive_package.py
----------------------
Empaqueta todos los insumos del Entregable 1 (Meta 1) en una estructura organizada:
output/ENTREGABLE_1_CAUSA_NATURA_DRIVE/
  ├── 01_Documento_Ejecutivo/
  │   ├── DOCUMENTO_EJECUTIVO_ENTREGABLE1_PDF.html
  │   └── DOCUMENTO_EJECUTIVO_ENTREGABLE1.md
  ├── 02_Base_de_Datos_GeoPackage/
  │   ├── ierc_golfo_california.gpkg
  │   └── GEOPACKAGE_METADATOS.md
  ├── 03_Atlas_y_Paquetes_Cartograficos_PANGAS/
  │   ├── ATLAS_PAQUETES_COMPLETO.html
  │   └── paquetes_capas_pangas/ (7 carpetas con 14 mapas JPG y metadatos)
  └── 04_Auditoria_y_Dictamen_Tecnico/
      ├── AUDITORIA_META1_ENTREGABLE1.md
      └── PLAN_DE_AUDITORIA_Y_SUPERVISION_IERC.md

Y genera la versión comprimida `output/ENTREGABLE_1_IERC_GNL.zip` lista para subir a Google Drive.
"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / 'output'
DRIVE_PACKAGE_DIR = OUTPUT_DIR / 'ENTREGABLE_1_CAUSA_NATURA_DRIVE'
ZIP_PATH = OUTPUT_DIR / 'ENTREGABLE_1_IERC_GNL'

# Limpiar directorio previo si existe
if DRIVE_PACKAGE_DIR.exists():
    shutil.rmtree(DRIVE_PACKAGE_DIR)

DRIVE_PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

# 1. Crear subcarpetas organizadas
dir_doc = DRIVE_PACKAGE_DIR / '01_Documento_Ejecutivo'
dir_gpkg = DRIVE_PACKAGE_DIR / '02_Base_de_Datos_GeoPackage'
dir_atlas = DRIVE_PACKAGE_DIR / '03_Atlas_y_Paquetes_Cartograficos_PANGAS'
dir_audit = DRIVE_PACKAGE_DIR / '04_Auditoria_y_Dictamen_Tecnico'

dir_doc.mkdir(parents=True, exist_ok=True)
dir_gpkg.mkdir(parents=True, exist_ok=True)
dir_atlas.mkdir(parents=True, exist_ok=True)
dir_audit.mkdir(parents=True, exist_ok=True)

# 2. Copiar Documentos Ejecutivos
shutil.copy2(OUTPUT_DIR / 'DOCUMENTO_EJECUTIVO_ENTREGABLE1_PDF.html', dir_doc / 'DOCUMENTO_EJECUTIVO_ENTREGABLE1_PDF.html')
shutil.copy2(BASE_DIR / 'docs' / 'metodologia' / 'DOCUMENTO_EJECUTIVO_ENTREGABLE1.md', dir_doc / 'DOCUMENTO_EJECUTIVO_ENTREGABLE1.md')
shutil.copy2(BASE_DIR / 'docs' / 'metodologia' / 'PRESENTACION_EJECUTIVA_ENTREGABLE1.md', dir_doc / 'PRESENTACION_EJECUTIVA_ENTREGABLE1.md')

# 3. Copiar Base de Datos GeoPackage
shutil.copy2(BASE_DIR / 'deliverables' / 'v1_geopackage' / 'ierc_golfo_california.gpkg', dir_gpkg / 'ierc_golfo_california.gpkg')
shutil.copy2(BASE_DIR / 'deliverables' / 'v1_geopackage' / 'GEOPACKAGE_METADATA.md', dir_gpkg / 'GEOPACKAGE_METADATOS.md')

# 4. Copiar Atlas y Paquetes Cartográficos
shutil.copytree(OUTPUT_DIR / 'paquetes_capas_pangas', dir_atlas / 'paquetes_capas_pangas')

# 5. Copiar Expediente de Auditoría
shutil.copy2(BASE_DIR / 'docs' / 'auditoria' / 'AUDITORIA_META1_ENTREGABLE1.md', dir_audit / 'AUDITORIA_META1_ENTREGABLE1.md')
shutil.copy2(BASE_DIR / 'docs' / 'auditoria' / 'PLAN_DE_AUDITORIA_Y_SUPERVISION_IERC.md', dir_audit / 'PLAN_DE_AUDITORIA_Y_SUPERVISION_IERC.md')

# 6. Comprimir en archivo ZIP
shutil.make_archive(str(ZIP_PATH), 'zip', DRIVE_PACKAGE_DIR)

print(f"Directorio de Google Drive empaquetado exitosamente en: {DRIVE_PACKAGE_DIR}")
print(f"Archivo ZIP comprimido listo para subir generado en: {ZIP_PATH}.zip")
