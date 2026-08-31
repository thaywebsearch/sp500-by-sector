# S&P 500 por Setores GICS

Repositório de dados limpos e organizados do S&P 500 divididos nos **11 setores GICS** (Global Industry Classification Standard).

## Estrutura do Projeto

```
sp500-by-sector/
├── communication-services/     # Communication Services (24 empresas)
├── consumer-discretionary/     # Consumer Discretionary (47 empresas)
├── consumer-staples/     # Consumer Staples (34 empresas)
├── energy/     # Energy (21 empresas)
├── financials/     # Financials (76 empresas)
├── health-care/     # Health Care (59 empresas)
├── industrials/     # Industrials (83 empresas)
├── information-technology/     # Information Technology (73 empresas)
├── materials/     # Materials (25 empresas)
├── real-estate/     # Real Estate (30 empresas)
├── utilities/     # Utilities (31 empresas)
└── README.md                   # Este arquivo
```

Cada pasta de setor contém:
- **`dados.json`** — Dados estruturados completos (símbolo, nome, subindústria, sede, CIK, data de adição, ano de fundação)
- **`README.md`** — Tabela formatada renderizável no GitHub

## Setores GICS

| Setor | Pasta | Empresas | Descrição |
|-------|-------|----------|-----------|
| **Communication Services** | [`communication-services/`](communication-services/) | 24 | Mídia, telecom, entretenimento interativo |
| **Consumer Discretionary** | [`consumer-discretionary/`](consumer-discretionary/) | 47 | Varejo, automóveis, lazer, bens duráveis |
| **Consumer Staples** | [`consumer-staples/`](consumer-staples/) | 34 | Alimentos, bebidas, produtos de higiene |
| **Energy** | [`energy/`](energy/) | 21 | Petróleo, gás, equipamentos energéticos |
| **Financials** | [`financials/`](financials/) | 76 | Bancos, seguros, gestão de ativos |
| **Health Care** | [`health-care/`](health-care/) | 59 | Farmacêuticas, biotecnologia, equipamentos médicos |
| **Industrials** | [`industrials/`](industrials/) | 83 | Aeroespacial, construção, maquinaria, transporte |
| **Information Technology** | [`information-technology/`](information-technology/) | 73 | Software, hardware, semicondutores, serviços de TI |
| **Materials** | [`materials/`](materials/) | 25 | Químicos, construção, embalagens, metais |
| **Real Estate** | [`real-estate/`](real-estate/) | 30 | REITs, gestão imobiliária, desenvolvimento |
| **Utilities** | [`utilities/`](utilities/) | 31 | Elétricas, gás, água, energias renováveis |

## Fonte dos Dados

- **Origem**: [datasets/s-and-p-500-companies](https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv) no GitHub
- **Classificação**: GICS (Global Industry Classification Standard)
- **Atualização**: 2026-08-31

## Uso

### Carregar dados em Python

```python
import json

with open('communication-services/communication-services.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Setor: {data['sector']}")
print(f"Total de empresas: {data['count']}")

for company in data['companies']:
    print(f"{company['symbol']} - {company['name']} ({company['subIndustry']})")
```

### Carregar dados em JavaScript/Node.js

```javascript
const fs = require('fs');

const data = JSON.parse(fs.readFileSync('communication-services/communication-services.json', 'utf8'));
console.log(`Setor: ${data.sector}`);
console.log(`Total: ${data.count} empresas`);
```

## Licença

Dados públicos do S&P 500. Consulte a [fonte original](https://github.com/datasets/s-and-p-500-companies) para detalhes de licenciamento.

---

*Gerado automaticamente — Última atualização: 2026-08-31*