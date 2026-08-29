#!/usr/bin/env python3
"""
Gera tabelas Markdown ordenadas por Market Cap para cada setor.
"""

import json
import os
from pathlib import Path

SECTORS = [
    "communication-services",
    "consumer-discretionary",
    "consumer-staples",
    "energy",
    "financials",
    "health-care",
    "industrials",
    "information-technology",
    "materials",
    "real-estate",
    "utilities",
]

SECTOR_NAMES = {
    "communication-services": "Communication Services",
    "consumer-discretionary": "Consumer Discretionary",
    "consumer-staples": "Consumer Staples",
    "energy": "Energy",
    "financials": "Financials",
    "health-care": "Health Care",
    "industrials": "Industrials",
    "information-technology": "Information Technology",
    "materials": "Materials",
    "real-estate": "Real Estate",
    "utilities": "Utilities",
}


def format_market_cap(market_cap):
    """Formata market cap em formato legível (B = bilhões, M = milhões, T = trilhões)."""
    if market_cap is None:
        return "N/A"
    
    if market_cap >= 1_000_000_000_000:
        return f"${market_cap / 1_000_000_000_000:.2f}T"
    elif market_cap >= 1_000_000_000:
        return f"${market_cap / 1_000_000_000:.2f}B"
    elif market_cap >= 1_000_000:
        return f"${market_cap / 1_000_000:.2f}M"
    else:
        return f"${market_cap:,.0f}"


def generate_readme(sector_dir, sector_name, companies):
    """Gera o README.md com tabela ordenada por Market Cap."""
    
    # Ordena por marketCap descendente
    sorted_companies = sorted(
        companies, 
        key=lambda x: x.get("marketCap", 0) or 0, 
        reverse=True
    )
    
    lines = []
    lines.append(f"# S&P 500 — Setor {sector_name}")
    lines.append("")
    lines.append(f"> Fonte: `{sector_dir}.json` · Ordenado por Market Cap (maior para menor) · Total: {len(companies)} empresas")
    lines.append("")
    
    # Cabeçalho da tabela
    lines.append("| # | Símbolo | Empresa | Market Cap | Subindústria | Sedes | Dividend Yield |")
    lines.append("|---|---------|---------|------------|--------------|-------|----------------|")
    
    for i, company in enumerate(sorted_companies, 1):
        symbol = company.get("symbol", "")
        name = company.get("name", "")
        market_cap = format_market_cap(company.get("marketCap"))
        sub_industry = company.get("subIndustry", "")
        headquarters = company.get("headquarters", "")
        dividend_yield = company.get("dividendYield")
        div_str = f"{dividend_yield:.2f}%" if dividend_yield is not None else "—"
        
        lines.append(f"| {i} | {symbol} | {name} | {market_cap} | {sub_industry} | {headquarters} | {div_str} |")
    
    return "\n".join(lines)


def main():
    base_path = Path(__file__).parent.parent
    
    for sector_dir in SECTORS:
        json_path = base_path / sector_dir / f"{sector_dir}.json"
        readme_path = base_path / sector_dir / "README.md"
        
        if not json_path.exists():
            print(f"[AVISO] Arquivo não encontrado: {json_path}")
            continue
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        companies = data.get("companies", [])
        sector_name = SECTOR_NAMES.get(sector_dir, sector_dir)
        
        readme_content = generate_readme(sector_dir, sector_name, companies)
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print(f"[OK] {sector_name}: {len(companies)} empresas -> {readme_path}")
    
    # Também gera um arquivo consolidado com top 50 do S&P 500 por Market Cap
    all_companies = []
    for sector_dir in SECTORS:
        json_path = base_path / sector_dir / f"{sector_dir}.json"
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for company in data.get("companies", []):
                company["sector"] = sector_dir
                all_companies.append(company)
    
    # Top 50 geral
    top50 = sorted(all_companies, key=lambda x: x.get("marketCap", 0) or 0, reverse=True)[:50]
    
    lines = []
    lines.append("# S&P 500 — Top 50 por Market Cap (Consolidado)")
    lines.append("")
    lines.append(f"> Gerado em: 2026-08-29 · Total de empresas no S&P 500: {len(all_companies)}")
    lines.append("")
    lines.append("| # | Símbolo | Empresa | Setor | Market Cap | Subindústria | Dividend Yield |")
    lines.append("|---|---------|---------|-------|------------|--------------|----------------|")
    
    for i, company in enumerate(top50, 1):
        symbol = company.get("symbol", "")
        name = company.get("name", "")
        sector = SECTOR_NAMES.get(company.get("sector", ""), company.get("sector", ""))
        market_cap = format_market_cap(company.get("marketCap"))
        sub_industry = company.get("subIndustry", "")
        dividend_yield = company.get("dividendYield")
        div_str = f"{dividend_yield:.2f}%" if dividend_yield is not None else "—"
        
        lines.append(f"| {i} | {symbol} | {name} | {sector} | {market_cap} | {sub_industry} | {div_str} |")
    
    consolidated_path = base_path / "TOP50-MARKET-CAP.md"
    with open(consolidated_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"[OK] Consolidado: Top 50 -> {consolidated_path}")


if __name__ == "__main__":
    main()