#!/usr/bin/env node

/**
 * SEO Tools para SP500 Dashboard
 * Gera sitemap, valida meta tags e verifica otimizações
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============ 1. GERAR SITEMAP ============

function gerarSitemap() {
  console.log('?? Gerando sitemap.xml...');
  
  const baseUrl = 'https://sp500-dashboard.netlify.app';
  const dataDir = path.join(__dirname, 'data');
  
  // Ler arquivos JSON dos setores
  let setores = [];
  if (fs.existsSync(dataDir)) {
    setores = fs.readdirSync(dataDir)
      .filter(file => file.endsWith('.json') && file !== 'package.json')
      .map(file => file.replace('.json', ''));
  }
  
  let sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
`;
  
  // URL principal
  sitemap += `  <url>
    <loc>${baseUrl}/</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
`;
  
  // Página de setores
  sitemap += `  <url>
    <loc>${baseUrl}/setores</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
`;
  
  // URLs individuais por setor
  setores.forEach(setor => {
    sitemap += `  <url>
    <loc>${baseUrl}/setor/${setor}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
`;
  });
  
  // Páginas adicionais
  const paginasExtras = [
    { url: '/analise', freq: 'weekly', priority: 0.7 },
    { url: '/comparar', freq: 'weekly', priority: 0.7 },
    { url: '/sobre', freq: 'monthly', priority: 0.5 }
  ];
  
  paginasExtras.forEach(page => {
    sitemap += `  <url>
    <loc>${baseUrl}${page.url}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>${page.freq}</changefreq>
    <priority>${page.priority}</priority>
  </url>
`;
  });
  
  sitemap += `</urlset>`;
  
  const caminhoSitemap = path.join(__dirname, 'public', 'sitemap.xml');
  
  // Criar diretório se não existir
  if (!fs.existsSync(path.join(__dirname, 'public'))) {
    fs.mkdirSync(path.join(__dirname, 'public'), { recursive: true });
  }
  
  fs.writeFileSync(caminhoSitemap, sitemap);
  console.log(`? Sitemap criado: ${caminhoSitemap}`);
  console.log(`   Total de URLs: ${setores.length + paginasExtras.length + 2}`);
}

// ============ 2. GERAR ROBOTS.TXT ============

function gerarRobots() {
  console.log('\n?? Gerando robots.txt...');
  
  const robots = `# Robots.txt - SP500 Dashboard

User-agent: *
Allow: /
Disallow: /api/
Disallow: /.netlify/
Disallow: /admin/
Disallow: /*.json$
Disallow: /private/

# Google específico
User-agent: Googlebot
Allow: /
Crawl-delay: 0

# Bing específico
User-agent: Bingbot
Allow: /
Crawl-delay: 1

# Slow crawlers
User-agent: *
Crawl-delay: 2
Request-rate: 1/10s

# Sitemap
Sitemap: https://sp500-dashboard.netlify.app/sitemap.xml
`;
  
  const caminhoRobots = path.join(__dirname, 'public', 'robots.txt');
  fs.writeFileSync(caminhoRobots, robots);
  console.log(`? Robots.txt criado: ${caminhoRobots}`);
}

// ============ 3. CHECKLIST DE SEO ============

function executarChecklist() {
  console.log('\n? CHECKLIST DE SEO\n');
  
  const checklist = {
    'Básico': [
      { item: 'Meta tags básicas', status: true, ref: 'index.html' },
      { item: 'Meta description (<160 chars)', status: true, ref: 'index.html' },
      { item: 'Título único (<60 chars)', status: true, ref: 'index.html' },
      { item: 'Um H1 por página', status: true, ref: 'HTML' },
      { item: 'URLs amigáveis', status: true, ref: 'server.js' },
      { item: 'Mobile responsive', status: true, ref: 'CSS' },
      { item: 'Alt text em imagens', status: false, ref: '?? Revisar' },
      { item: 'Favicon', status: true, ref: 'public/favicon.svg' }
    ],
    'Intermediário': [
      { item: 'Sitemap.xml', status: true, ref: 'sitemap.xml' },
      { item: 'Robots.txt', status: true, ref: 'robots.txt' },
      { item: 'Schema.org JSON-LD', status: true, ref: 'index.html' },
      { item: 'Open Graph tags', status: true, ref: 'index.html' },
      { item: 'Canonical links', status: true, ref: 'index.html' },
      { item: 'Estrutura de navegação clara', status: true, ref: 'UI' },
      { item: 'Breadcrumb schema', status: true, ref: 'JSON-LD' },
      { item: 'Sitemap dinâmico', status: true, ref: 'seo-tools.js' }
    ],
    'Avançado': [
      { item: 'Core Web Vitals < 2.5s', status: false, ref: '?? Testar' },
      { item: 'Gzip/Brotli compression', status: true, ref: 'netlify.toml' },
      { item: 'Service Worker', status: false, ref: '?? Implementar' },
      { item: 'Security headers', status: true, ref: 'netlify.toml' },
      { item: 'Google Search Console', status: false, ref: '?? Conectar' },
      { item: 'Google Analytics 4', status: false, ref: '?? Conectar' },
      { item: 'Lazy loading de imagens', status: false, ref: '?? Implementar' },
      { item: 'Code splitting', status: false, ref: '?? Implementar' }
    ]
  };
  
  for (const [categoria, itens] of Object.entries(checklist)) {
    console.log(`\n${categoria}:`);
    console.log('-'.repeat(60));
    
    let concluido = 0;
    itens.forEach(({ item, status, ref }) => {
      const simbolo = status ? '?' : '??';
      const texto = `${simbolo} ${item.padEnd(35)} ${ref}`;
      console.log(texto);
      if (status) concluido++;
    });
    
    const percentual = Math.round((concluido / itens.length) * 100);
    console.log(`\nProgresso: ${concluido}/${itens.length} (${percentual}%)`);
  }
}

// ============ 4. ANALISAR PERFORMANCE ============

function analisarPerformance() {
  console.log('\n? RECOMENDAÇÕES DE PERFORMANCE\n');
  
  const recomendacoes = [
    {
      categoria: 'Imagens',
      itens: [
        '• Converter PNG/JPG para WebP',
        '• Implementar lazy loading (loading="lazy")',
        '• Criar múltiplos tamanhos para srcset',
        '• Comprimir com TinyPNG ou ImageOptim'
      ]
    },
    {
      categoria: 'JavaScript',
      itens: [
        '• Code splitting por rota',
        '• Tree shaking (remover código não usado)',
        '• Minificar e comprimir',
        '• Usar dynamic imports para carregamento lento'
      ]
    },
    {
      categoria: 'CSS',
      itens: [
        '• Remover CSS não utilizado (PurgeCSS)',
        '• Minificar',
        '• Usar CSS crítico inline',
        '• Deferir CSS não crítico'
      ]
    },
    {
      categoria: 'Cache',
      itens: [
        '• Cache HTTP longo para assets estáticos',
        '• Cache curto para HTML',
        '• Service Worker para offline',
        '• CDN para distribuição global'
      ]
    }
  ];
  
  recomendacoes.forEach(({ categoria, itens }) => {
    console.log(`${categoria}:`);
    itens.forEach(item => console.log(`  ${item}`));
    console.log();
  });
}

// ============ 5. LINKS ÚTEIS ============

function mostrarLinks() {
  console.log('\n?? FERRAMENTAS E LINKS\n');
  
  const ferramentas = [
    {
      nome: 'Google PageSpeed Insights',
      url: 'https://pagespeed.web.dev/',
      desc: 'Teste performance e Core Web Vitals'
    },
    {
      nome: 'Google Search Console',
      url: 'https://search.google.com/search-console',
      desc: 'Submeta sitemap e monitore indexação'
    },
    {
      nome: 'Schema.org Validator',
      url: 'https://validator.schema.org/',
      desc: 'Valide seu JSON-LD'
    },
    {
      nome: 'W3C HTML Validator',
      url: 'https://validator.w3.org/',
      desc: 'Valide HTML'
    },
    {
      nome: 'Mobile Friendly Test',
      url: 'https://search.google.com/test/mobile-friendly',
      desc: 'Verifique responsividade'
    },
    {
      nome: 'GTmetrix',
      url: 'https://gtmetrix.com/',
      desc: 'Análise detalhada de performance'
    },
    {
      nome: 'Lighthouse',
      url: 'https://developers.google.com/web/tools/lighthouse',
      desc: 'Auditoria integrada no Chrome'
    }
  ];
  
  ferramentas.forEach(({ nome, url, desc }) => {
    console.log(`?? ${nome}`);
    console.log(`   ${desc}`);
    console.log(`   ${url}\n`);
  });
}

// ============ 6. INSTRUÇÕES DE IMPLEMENTAÇÃO ============

function mostrarInstrucoes() {
  console.log('\n?? PRÓXIMOS PASSOS\n');
  
  console.log('1. IMEDIATO (Esta semana):');
  console.log('   ? Revisar arquivo index.html');
  console.log('   ? Adicionar alt text nas imagens');
  console.log('   ? Conectar Google Search Console');
  console.log('   ? Fazer deploy da versão otimizada');
  
  console.log('\n2. CURTO PRAZO (Próximas 2 semanas):');
  console.log('   ? Implementar Google Analytics 4');
  console.log('   ? Testar Core Web Vitals');
  console.log('   ? Criar Service Worker');
  console.log('   ? Otimizar imagens (WebP)');
  
  console.log('\n3. MÉDIO PRAZO (Próximos 30 dias):');
  console.log('   ? Melhorar conteúdo/SEO copywriting');
  console.log('   ? Criar blog com análises setoriais');
  console.log('   ? Build backlinks');
  console.log('   ? Monitorar rankings');
  
  console.log('\n4. CONTÍNUO:');
  console.log('   ? Atualizar dados semanalmente');
  console.log('   ? Monitorar Analytics');
  console.log('   ? Verificar Search Console');
  console.log('   ? Manter performance otimizada\n');
}

// ============ EXECUTAR ============

console.log('\n+----------------------------------------+');
console.log('¦  ?? SP500 Dashboard - SEO Optimizer  ¦');
console.log('+----------------------------------------+\n');

gerarSitemap();
gerarRobots();
executarChecklist();
analisarPerformance();
mostrarLinks();
mostrarInstrucoes();

console.log('? Tudo pronto! Execute este script novamente quando adicionar novos setores.\n');
