#!/usr/bin/env python3
"""
Atualiza automaticamente o dataset S&P 500 por setores GICS.
Fonte: https://github.com/datasets/s-and-p-500-companies
Execução: python scripts/update_sectors.py
"""

import json
import csv
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

SOURCE_URL = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
ROOT_DIR = Path(__file__).parent.parent
SECTORS_DIR = ROOT_DIR
GENERATED_AT = datetime.now().strftime("%Y-%m-%d")

SECTOR_ORDER = [
    "Communication Services",
    "Consumer Discretionary",
    "Consumer Staples",
    "Energy",
    "Financials",
    "Health Care",
    "Industrials",
    "Information Technology",
    "Materials",
    "Real Estate",
    "Utilities",
]

SECTOR_FOLDER_MAP = {
    "Communication Services": "communication-services",
    "Consumer Discretionary": "consumer-discretionary",
    "Consumer Staples": "consumer-staples",
    "Energy": "energy",
    "Financials": "financials",
    "Health Care": "health-care",
    "Industrials": "industrials",
    "Information Technology": "information-technology",
    "Materials": "materials",
    "Real Estate": "real-estate",
    "Utilities": "utilities",
}


def fetch_csv():
    print(f"[INFO] Baixando dados de {SOURCE_URL}...")
    with urlopen(SOURCE_URL) as response:
        content = response.read().decode("utf-8")
    return content


def parse_csv(content):
    reader = csv.DictReader(content.splitlines())
    companies = []
    for row in reader:
        companies.append({
            "symbol": row["Symbol"],
            "name": row["Security"],
            "sector": row["GICS Sector"],
            "subIndustry": row["GICS Sub-Industry"],
            "headquarters": row["Headquarters Location"],
            "dateAdded": row["Date added"],
            "cik": int(row["CIK"]) if row["CIK"] else None,
            "founded": row["Founded"] if row["Founded"] else None,
        })
    return companies


def group_by_sector(companies):
    sectors = {}
    for company in companies:
        sector = company["sector"]
        if sector not in sectors:
            sectors[sector] = []
        sectors[sector].append(company)
    return sectors


def write_json(sector_name, companies):
    folder = SECTOR_FOLDER_MAP[sector_name]
    folder_path = SECTORS_DIR / folder
    folder_path.mkdir(exist_ok=True)

    data = {
        "sector": sector_name,
        "count": len(companies),
        "generatedAt": GENERATED_AT,
        "source": SOURCE_URL,
        "companies": companies,
    }

    json_path = folder_path / f"{folder}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  [OK] {json_path} ({len(companies)} empresas)")


def write_readme(sector_name, companies):
    folder = SECTOR_FOLDER_MAP[sector_name]
    folder_path = SECTORS_DIR / folder

    lines = [
        f"# S&P 500 — Setor {sector_name}",
        "",
        f"> Fonte: `{folder}.json` · Gerado em: {GENERATED_AT} · Total: {len(companies)} empresas",
        "",
        "| # | Símbolo | Empresa | Subindústria | Sedes |",
        "|---|---------|---------|--------------|-------|",
    ]

    for idx, company in enumerate(companies, 1):
        lines.append(
            f"| {idx} | {company['symbol']} | {company['name']} | "
            f"{company['subIndustry']} | {company['headquarters']} |"
        )

    readme_path = folder_path / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [OK] {readme_path}")


def write_root_readme(sectors):
    lines = [
        "# S&P 500 por Setores GICS",
        "",
        "Repositório de dados limpos e organizados do S&P 500 divididos nos **11 setores GICS** "
        "(Global Industry Classification Standard).",
        "",
        "## Estrutura do Projeto",
        "",
        "```",
        "sp500-by-sector/",
    ]

    for sector in SECTOR_ORDER:
        folder = SECTOR_FOLDER_MAP[sector]
        count = len(sectors.get(sector, []))
        lines.append(f"├── {folder}/     # {sector} ({count} empresas)")

    lines.extend([
        "└── README.md                   # Este arquivo",
        "```",
        "",
        "Cada pasta de setor contém:",
        "- **`dados.json`** — Dados estruturados completos (símbolo, nome, subindústria, sede, CIK, data de adição, ano de fundação)",
        "- **`README.md`** — Tabela formatada renderizável no GitHub",
        "",
        "## Setores GICS",
        "",
        "| Setor | Pasta | Empresas | Descrição |",
        "|-------|-------|----------|-----------|",
    ])

    sector_descriptions = {
        "Communication Services": "Mídia, telecom, entretenimento interativo",
        "Consumer Discretionary": "Varejo, automóveis, lazer, bens duráveis",
        "Consumer Staples": "Alimentos, bebidas, produtos de higiene",
        "Energy": "Petróleo, gás, equipamentos energéticos",
        "Financials": "Bancos, seguros, gestão de ativos",
        "Health Care": "Farmacêuticas, biotecnologia, equipamentos médicos",
        "Industrials": "Aeroespacial, construção, maquinaria, transporte",
        "Information Technology": "Software, hardware, semicondutores, serviços de TI",
        "Materials": "Químicos, construção, embalagens, metais",
        "Real Estate": "REITs, gestão imobiliária, desenvolvimento",
        "Utilities": "Elétricas, gás, água, energias renováveis",
    }

    for sector in SECTOR_ORDER:
        folder = SECTOR_FOLDER_MAP[sector]
        count = len(sectors.get(sector, []))
        desc = sector_descriptions.get(sector, "")
        lines.append(f"| **{sector}** | [`{folder}/`]({folder}/) | {count} | {desc} |")

    lines.extend([
        "",
        "## Fonte dos Dados",
        "",
        f"- **Origem**: [datasets/s-and-p-500-companies]({SOURCE_URL}) no GitHub",
        "- **Classificação**: GICS (Global Industry Classification Standard)",
        f"- **Atualização**: {GENERATED_AT}",
        "",
        "## Uso",
        "",
        "### Carregar dados em Python",
        "",
        "```python",
        "import json",
        "",
        "with open('communication-services/communication-services.json', 'r', encoding='utf-8') as f:",
        "    data = json.load(f)",
        "",
        "print(f\"Setor: {data['sector']}\")",
        "print(f\"Total de empresas: {data['count']}\")",
        "",
        "for company in data['companies']:",
        "    print(f\"{company['symbol']} - {company['name']} ({company['subIndustry']})\")",
        "```",
        "",
        "### Carregar dados em JavaScript/Node.js",
        "",
        "```javascript",
        "const fs = require('fs');",
        "",
        "const data = JSON.parse(fs.readFileSync('communication-services/communication-services.json', 'utf8'));",
        "console.log(`Setor: ${data.sector}`);",
        "console.log(`Total: ${data.count} empresas`);",
        "```",
        "",
        "## Licença",
        "",
        "Dados públicos do S&P 500. Consulte a [fonte original]("
        "https://github.com/datasets/s-and-p-500-companies) para detalhes de licenciamento.",
        "",
        "---",
        "",
        f"*Gerado automaticamente — Última atualização: {GENERATED_AT}*",
    ])

    readme_path = ROOT_DIR / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] {readme_path}")


def main():
    print(f"[INFO] Atualizando dataset S&P 500 por setores -- {GENERATED_AT}")
    print("=" * 60)

    try:
        content = fetch_csv()
        companies = parse_csv(content)
        print(f"[INFO] Total de empresas: {len(companies)}")

        sectors = group_by_sector(companies)
        print(f"[INFO] Setores encontrados: {len(sectors)}")

        for sector in SECTOR_ORDER:
            if sector in sectors:
                sector_companies = sectors[sector]
                print(f"\n[INFO] Processando: {sector} ({len(sector_companies)} empresas)")
                write_json(sector, sector_companies)
                write_readme(sector, sector_companies)
            else:
                print(f"\n[WARN] Setor não encontrado nos dados: {sector}")

        write_root_readme(sectors)

        print("\n" + "=" * 60)
        print("[INFO] Atualizacao concluida com sucesso!")
        return 0

    except Exception as e:
        print(f"\n[ERROR] Erro: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())