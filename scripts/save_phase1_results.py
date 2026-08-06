#!/usr/bin/env python3
"""
Phase 1 Results - Compiled from web searches
"""

import json
import csv
from datetime import datetime
from pathlib import Path

# Results from web searches
results = [
    {
        "query": '"spatial risk index" "small-scale fisheries" LNG',
        "source": "scholar",
        "title": "2017 Mediterranean Quality Status Report",
        "url": "https://www.medqsr.org/sites/default/files/inline-files/2017MedQSR_Online_0.pdf",
        "snippet": "... small scale fisheries fleets are concentrated in the Aegean Sea, Gulf of ... spatial risk index, which combines variables (multiple data layers) ...",
        "year": 2017,
        "authors": None,
        "repo_url": None,
        "score": 3,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": True,
            "h3_hexagonal": False,
            "social_vulnerability": False,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": '"vulnerability assessment" "artisanal fisheries" "gas pipeline"',
        "source": "scholar",
        "title": "Review of the Embassy Development Assistance Portfolio: Mozambique",
        "url": "https://www.norad.no/contentassets/9ce6361daeed43efa13cc33c449edc96/mosambik-cc-env---final-031108.pdf",
        "snippet": "vulnerability assessment of climate change im- ... (Artisanal) Fisheries (IDPPE) ... ing is occurring from the central processing facility for the gas pipeline.",
        "year": None,
        "authors": None,
        "repo_url": None,
        "score": 3,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": True,
            "h3_hexagonal": False,
            "social_vulnerability": True,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": '"vulnerability assessment" "artisanal fisheries" "gas pipeline"',
        "source": "scholar",
        "title": "Environmental Impact Assessment - Gas to Energy Project",
        "url": "https://img.exim.gov/s3fs-public/external/GTE%20EIA%20Volume%202%20Appendices%20Nov%202022.pdf",
        "snippet": "... gas pipeline in Angola and for three separate ... artisanal fisheries in Guyana (Funded by WWF ... vulnerability assessment of the agriculture sector ...",
        "year": 2022,
        "authors": None,
        "repo_url": None,
        "score": 3,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": True,
            "h3_hexagonal": False,
            "social_vulnerability": True,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": '"spatial risk" fisheries "gas infrastructure"',
        "source": "scholar",
        "title": "Spatial Risk Assessment for the Proposed East African Crude Oil Pipeline",
        "url": "https://www.scirp.org/journal/paperinformation?paperid=137178",
        "snippet": "... spatial risk assessment model for enhancing the security and safety of ... gas infrastructure. This therefore, calls for a concerted effort between the ...",
        "year": None,
        "authors": None,
        "repo_url": None,
        "score": 2,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": False,
            "lng_gas_infra": True,
            "h3_hexagonal": False,
            "social_vulnerability": False,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": '"spatial risk" fisheries "gas infrastructure"',
        "source": "scholar",
        "title": "optimising environment and fishing interests (UKRI project NE/P016537/1)",
        "url": "https://gtr.ukri.org/projects?ref=NE%2FP016537%2F1",
        "snippet": "2. Developing spatial 'risk-layers' that can be ... gas infrastructure by fishing gear. In order to ... Commercial fisheries losses arising from ...",
        "year": None,
        "authors": None,
        "repo_url": None,
        "score": 3,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": True,
            "h3_hexagonal": False,
            "social_vulnerability": False,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": '"risk index" "small-scale fisheries" infrastructure',
        "source": "scholar",
        "title": "Fisheries@Risk - Vulnerability of Fisheries to Climate Change (TNC)",
        "url": "https://www.nature.org/content/dam/tnc/nature/en/documents/Fisheries-at-Risk-Technical-Report.pdf",
        "snippet": "The Fisheries@Risk Index identifies national risks to fish, fishers and fisheries by combining data on exposure to climate change and coastal hazards and ...",
        "year": 2020,
        "authors": "B.E. Hilft",
        "repo_url": None,
        "score": 3,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": False,
            "h3_hexagonal": False,
            "social_vulnerability": True,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": '"artisanal fisheries" "LNG" vulnerability spatial assessment',
        "source": "scholar",
        "title": "Addressing Project Impacts on Fishing-based Livelihoods (IFC)",
        "url": "https://ifcsia.org/wp-content/uploads/pdf/publications/P_IFC-SCI_FisheriesReport2015_R2-LoRes.pdf",
        "snippet": "a more thorough assessment of fisheries activities proximate to the proposed LNG site and recognized that ... of artisanal fisheries increases vulnerability to ...",
        "year": 2015,
        "authors": "IFC",
        "repo_url": None,
        "score": 4,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": True,
            "h3_hexagonal": False,
            "social_vulnerability": True,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": '"artisanal fisheries" "LNG" vulnerability spatial assessment',
        "source": "scholar",
        "title": "EXIM Mozambique LNG - Environmental Impact Assessment",
        "url": "https://www.fisheries.noaa.gov/s3//dam-migration/opr-2019-03473-508.pdf",
        "snippet": "Mozambique has commercial (industrial and semi-industrial) and artisanal fisheries with ... facilities to receive more LNG vessels and the addition of LNG trains ...",
        "year": 2019,
        "authors": "NOAA/EXIM",
        "repo_url": None,
        "score": 3,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": True,
            "h3_hexagonal": False,
            "social_vulnerability": False,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": '"artisanal fisheries" "LNG" vulnerability spatial assessment',
        "source": "scholar",
        "title": "Characterization of an artisanal fishery in Argentina using the social-ecological system approach",
        "url": "https://thecommonsjournal.org/articles/10.18352/ijc.534",
        "snippet": "... artisanal fisheries to determine their own operational access to the sea ... LNG plant project) and became extremely relevant for ...",
        "year": 2017,
        "authors": "S. London",
        "repo_url": None,
        "score": 3,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": True,
            "h3_hexagonal": False,
            "social_vulnerability": True,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": 'site:fao.org "spatial risk" fisheries',
        "source": "web",
        "title": "Spatial risk assessment of threats to Hector's/Māui dolphins (SEFRA approach)",
        "url": "https://www.fao.org/fishery/openasfa/a762df24-8e04-43b5-8c7e-84507134a1e4/ar",
        "snippet": "A Bayesian spatial risk model was developed using the spatially-explicit fisheries risk assessment (SEFRA) approach. Under this approach, encounters between ...",
        "year": None,
        "authors": "FAO",
        "repo_url": None,
        "score": 2,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": False,
            "lng_gas_infra": False,
            "h3_hexagonal": False,
            "social_vulnerability": False,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": 'site:worldbank.org "fishing communities" risk index',
        "source": "web",
        "title": "Climate Change and Marine Fisheries in Africa - Assessing Vulnerability",
        "url": "https://documents1.worldbank.org/curated/en/280891580715878729/pdf/Climate-Change-and-Marine-Fisheries-in-Africa-Assessing-Vulnerability-and-Strengthening-Adaptation-Capacity.pdf",
        "snippet": "All along the African coast, fishing communities report changes in fishing pattern and species caught. In 2013, the World Bank surveyed 463 fishermen in ...",
        "year": 2013,
        "authors": "World Bank",
        "repo_url": None,
        "score": 2,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": False,
            "h3_hexagonal": False,
            "social_vulnerability": True,
            "interactive_output": False,
            "open_access": True
        }
    },
    {
        "query": "ICES ASC \"fishing communities\" risk",
        "source": "web",
        "title": "Theme Session K – Small-Scale fisheries under global change threats and opportunities",
        "url": "https://ices-library.figshare.com/articles/conference_contribution/Theme_Session_K_Small-Scale_fisheries_under_global_change_threats_and_opportunities/24306016",
        "snippet": "... fishing communities; CM 393: Small-scale fishery mobilities across ... ICES Annual Science Conference 2023, Bilbao, Spain. Session. Theme ...",
        "year": 2023,
        "authors": "ICES",
        "repo_url": None,
        "score": 1,
        "match_criteria": {
            "multiplicative_index": False,
            "artisanal_fisheries": True,
            "lng_gas_infra": False,
            "h3_hexagonal": False,
            "social_vulnerability": False,
            "interactive_output": False,
            "open_access": True
        }
    }
]

# Save results
output_dir = Path("/home/gorops/ierc-gnl-project/docs/research/phase1")
output_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# CSV
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
            r['query'], r['source'], r['title'], r['url'], r['snippet'],
            r['year'] or '', r['authors'] or '', r['repo_url'] or '',
            r['score'],
            r['match_criteria']['multiplicative_index'],
            r['match_criteria']['artisanal_fisheries'],
            r['match_criteria']['lng_gas_infra'],
            r['match_criteria']['h3_hexagonal'],
            r['match_criteria']['social_vulnerability'],
            r['match_criteria']['interactive_output'],
            r['match_criteria']['open_access']
        ])

# JSON
json_path = output_dir / f'phase1_results_{timestamp}.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Saved {len(results)} results to:")
print(f"  {csv_path}")
print(f"  {json_path}")

# Summary stats
print(f"\n=== SUMMARY ===")
print(f"Total results: {len(results)}")
print(f"Score distribution:")
for score in range(5):
    count = sum(1 for r in results if r['score'] == score)
    print(f"  Score {score}: {count}")

# Top results
print("\n=== TOP RESULTS (score >= 3) ===")
for r in sorted(results, key=lambda x: x['score'], reverse=True):
    if r['score'] >= 3:
        print(f"  [{r['score']}] {r['title'][:80]}... ({r['source']})")