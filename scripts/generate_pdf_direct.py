#!/usr/bin/env python3
"""
generate_pdf_direct.py
----------------------
Convierte directamente el archivo HTML con estilo Causa Natura Data (output/DOCUMENTO_EJECUTIVO_ENTREGABLE1_PDF.html)
a un archivo PDF nativo (output/DOCUMENTO_EJECUTIVO_ENTREGABLE1.pdf) utilizando WeasyPrint.
"""

from pathlib import Path
import weasyprint

BASE_DIR = Path(__file__).resolve().parent.parent
HTML_PATH = BASE_DIR / 'output' / 'DOCUMENTO_EJECUTIVO_ENTREGABLE1_PDF.html'
PDF_OUTPUT_PATH = BASE_DIR / 'output' / 'DOCUMENTO_EJECUTIVO_ENTREGABLE1.pdf'

print("Iniciando conversión directa de HTML a PDF con WeasyPrint...")
html_obj = weasyprint.HTML(filename=str(HTML_PATH), base_url=str(HTML_PATH.parent))
html_obj.write_pdf(target=str(PDF_OUTPUT_PATH))

print(f"Archivo PDF directo generado exitosamente en: {PDF_OUTPUT_PATH}")
