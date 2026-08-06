#!/usr/bin/env python3
"""
Phase 1: Búsqueda Dirigida - Proyectos Similares a IERC-GNL
Busca proyectos globales con: spatial risk index + small-scale fisheries + LNG/gas + H3
"""

import json
import csv
from datetime import datetime
from pathlib import Path

# Queries de búsqueda priorizadas
QUERIES = [
    # Alta prioridad - combinaciones exactas
    ('"spatial risk index" "small-scale fisheries" LNG', 'scholar'),
    ('"spatial risk index" "artisanal fisheries" "gas infrastructure"', 'scholar'),
    ('"fishing communities" "risk index" "LNG terminal"', 'scholar'),
    ('"vulnerability assessment" "artisanal fisheries" "gas pipeline"', 'scholar'),
    ('H3 "fishing" "risk" "LNG"', 'github'),
    ('uber h3 fisheries vulnerability index', 'github'),
    ('"spatial risk" fisheries "gas infrastructure"', 'scholar'),
    ('"risk index" "small-scale fisheries" infrastructure', 'scholar'),
    
    # Gris literature
    ('site:fao.org "spatial risk" fisheries', 'web'),
    ('site:worldbank.org "fishing communities" risk index', 'web'),
    ('site:unep.org "fisheries vulnerability" spatial', 'web'),
    
    # Conferencias
    ('ICES ASC "fishing communities" risk', 'web'),
    ('MARE Conference "spatial risk" fisheries', 'web'),
]

# Estructura de resultados
class ProjectResult:
    def __init__(self, query, source, title, url, snippet, year=None, authors=None, repo_url=None):
        self.query = query
        self.source = source
        self.title = title
        self.url = url
        self.snippet = snippet
        self.year = year
        self.authors = authors
        self.repo_url = repo_url
        self.score = 0
        self.match_criteria = {
            'multiplicative_index': False,
            'artisanal_fisheries': False,
            'lng_gas_infra': False,
            'h3_hexagonal': False,
            'social_vulnerability': False,
            'interactive_output': False,
            'open_access': False
        }

def evaluate_match(result):
    """Evalúa criterios de match estricto (0-7)"""
    text = f"{result.title} {result.snippet}".lower()
    
    # Criterios
    if any(kw in text for kw in ['multiplicative', 'hazard × vulnerab', 'threat × vulnerab', 'risk = hazard', 'risk = threat']):
        result.match_criteria['multiplicative_index'] = True
    if any(kw in text for kw in ['artisanal', 'small-scale', 'small scale', 'traditional fisheries', 'small-scale fisheries']):
        result.match_criteria['artisanal_fisheries'] = True
    if any(kw in text for kw in ['lng', 'liquefied natural gas', 'gas terminal', 'gas pipeline', 'gas infrastructure', 'natural gas infrastructure']):
        result.match_criteria['lng_gas_infra'] = True
    if any(kw in text for kw in ['h3', 'uber h3', 'hexagonal grid', 'hex grid', 'h3 index']):
        result.match_criteria['h3_hexagonal'] = True
    if any(kw in text for kw in ['vulnerability', 'social vulnerability', 'dependence', 'governance', 'adaptive capacity', 'sensitivity']):
        result.match_criteria['social_vulnerability'] = True
    if any(kw in text for kw in ['dashboard', 'interactive map', 'web map', 'geopackage', 'webgis', 'viewer']):
        result.match_criteria['interactive_output'] = True
    if any(kw in text for kw in ['github', 'gitlab', 'zenodo', 'open access', 'open source', 'repository', 'doi.org']):
        result.match_criteria['open_access'] = True
    
    result.score = sum(result.match_criteria.values())
    return result

def save_results(results, output_dir):
    """Guarda resultados en CSV y JSON"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # CSV para análisis
    csv_path = output_dir / f'phase1_results_{timestamp}.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'query', 'source', 'title', 'url', 'snippet', 'year', 'authors', 'repo_url',
            'score', 'multiplicative_index', 'artisanal_fisheries', 'lng_gas_infra',
            'h3_hexagonal', 'social_vulnerability', 'interactive_output', 'open_access'
        ])
        for r in results:
            writer.writerow([
                r.query, r.source, r.title, r.url, r.snippet, r.year or '', r.authors or '', r.repo_url or '',
                r.score,
                r.match_criteria['multiplicative_index'],
                r.match_criteria['artisanal_fisheries'],
                r.match_criteria['lng_gas_infra'],
                r.match_criteria['h3_hexagonal'],
                r.match_criteria['social_vulnerability'],
                r.match_criteria['interactive_output'],
                r.match_criteria['open_access']
            ])
    
    # JSON para procesamiento posterior
    json_path = output_dir / f'phase1_results_{timestamp}.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump([{
            'query': r.query, 'source': r.source, 'title': r.title, 'url': r.url,
            'snippet': r.snippet, 'year': r.year, 'authors': r.authors, 'repo_url': r.repo_url,
            'score': r.score, 'match_criteria': r.match_criteria
        } for r in results], f, indent=2, ensure_ascii=False)
    
    return csv_path, json_path

if __name__ == '__main__':
    print("=== FASE 1: BÚSQUEDA DIRIGIDA ===")
    print(f"Queries a ejecutar: {len(QUERIES)}")
    print("Nota: Este script define la estructura. Ejecutar búsquedas con web_search tool.")
    print("\nQueries:")
    for i, (q, src) in enumerate(QUERIES, 1):
        print(f"  {i}. [{src}] {q}")