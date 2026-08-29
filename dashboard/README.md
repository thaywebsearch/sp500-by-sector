# S&P 500 Dashboard

Dashboard estático interativo para visualizar os 503 componentes do S&P 500 por setor GICS, construído com Vite + Vanilla JS.

## Funcionalidades

- 📊 **Visualização tabular** de todas as empresas com paginação
- 🔍 **Filtros**: por setor, busca textual (símbolo, nome, subindústria, sede)
- 📈 **Ordenação**: Market Cap, símbolo, nome, dividend yield
- ✅ **Seleção múltipla**: checkbox por linha + "Selecionar tudo"
- 📥 **Exportação**: CSV e JSON das empresas selecionadas
- 📱 **Responsivo**: funciona em mobile e desktop
- ⚡ **Leve**: ~15 KB gzipped (JS + CSS)

## Desenvolvimento Local

```bash
cd dashboard
npm install
npm run dev
```

Acesse: http://localhost:3000/sp500-by-sector/dashboard/

## Build para Produção (GitHub Pages)

```bash
npm run build
```

Gera arquivos em `../docs/` (configurado no `vite.config.js`).

## Deploy no GitHub Pages

1. Commit a pasta `docs/` no repositório
2. Em **Settings > Pages**, selecione **Deploy from branch** → `main` → `/docs`
3. O site estará disponível em: `https://<usuario>.github.io/sp500-by-sector/dashboard/`

## Estrutura

```
dashboard/
├── index.html          # HTML principal
├── vite.config.js      # Config Vite (base path para GitHub Pages)
├── package.json
├── public/
│   └── data/           # JSONs dos 11 setores (copiados no build)
└── src/
    ├── main.js         # Lógica da aplicação
    └── style.css       # Estilos
```

## Dados

Os dados vêm dos arquivos JSON em `../<setor>/<setor>.json`, gerados pelo script `scripts/generate_marketcap_tables.py`.

Campos disponíveis por empresa:
- `symbol`, `name`, `sector`, `subIndustry`, `headquarters`
- `marketCap`, `marketCapClassification`
- `dividendYield`, `hasDividend`
- `dateAdded`, `cik`, `founded`

## Personalização

- **Cores/tema**: edite variáveis CSS em `src/style.css` (`:root`)
- **Tamanho da página**: altere `PAGE_SIZE` em `src/main.js`
- **Colunas da tabela**: modifique o HTML em `index.html` e o render em `main.js`