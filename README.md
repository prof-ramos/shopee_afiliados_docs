# Shopee Affiliate API Client

[![CI](https://github.com/gabrielramos/shopee_afiliados_docs/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielramos/shopee_afiliados_docs/actions/workflows/ci.yml)
[![Release](https://github.com/gabrielramos/shopee_afiliados_docs/actions/workflows/release.yml/badge.svg)](https://github.com/gabrielramos/shopee_afiliados_docs/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-success.svg)](https://github.com/PyCQA/bandit)
[![Tests](https://img.shields.io/badge/tests-77.8%25-success-green.svg)](https://github.com/gabrielramos/shopee_afiliados_docs)
[![Issues](https://img.shields.io/github/issues/gabrielramos/shopee_afiliados_docs.svg)](https://github.com/gabrielramos/shopee_afiliados_docs/issues)

Cliente Python não-oficial para API de Afiliados da Shopee Brasil. Descoberto via introspecção GraphQL com schema completo e testes automatizados.

## Funcionalidades

- Cliente Python completo para API Shopee Affiliate
- Schema descoberto via introspecção GraphQL
- 5 endpoints principais testados e documentados
- Taxa de sucesso: 77.8% nos testes automatizados
- Autenticação SHA256 com assinatura dinâmica
- Suporte a paginação e filtros avançados

## Endpoints Disponíveis

1. **shopeeOfferV2** - Ofertas em destaque da Shopee
2. **shopOfferV2** - Ofertas de lojas específicas
3. **productOfferV2** - Busca de produtos por keyword ou shop
4. **generateShortLink** - Geração de links de afiliado
5. **conversionReport** - Relatório de conversões e comissões

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip ou uv para gerenciamento de dependências

### Passo 1: Clone o repositório

```bash
git clone https://github.com/gabrielramos/shopee_afiliados_docs.git
cd shopee_afiliados_docs
```

### Passo 2: Crie um ambiente virtual

```bash
# Usando uv (recomendado)
uv venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Ou usando venv padrão
python -m venv .venv
source .venv/bin/activate
```

### Passo 3: Instale as dependências

```bash
# Usando uv
uv pip install -r requirements.txt

# Ou usando pip padrão
pip install -r requirements.txt
```

### Passo 4: Configure suas credenciais

Crie um arquivo `.env` na raiz do projeto:

```bash
SHOPEE_APP_ID=seu_app_id_aqui
SHOPEE_APP_SECRET=seu_app_secret_aqui
```

Obtenha suas credenciais em: https://open-api.affiliate.shopee.com.br/

## Uso

### Exemplo básico

```python
from examples.python.shopee_affiliate_client import ShopeeAffiliateClient
import os
from dotenv import load_dotenv

# Carregar credenciais
load_dotenv()
client = ShopeeAffiliateClient(
    app_id=os.getenv("SHOPEE_APP_ID"),
    app_secret=os.getenv("SHOPEE_APP_SECRET")
)

# Buscar ofertas da Shopee
offers = client.get_shopee_offers(
    keyword="roupas",
    sort_type=2,  # Maior comissão
    limit=10
)

print(offers)
```

### Buscar produtos de uma loja específica

```python
# Ofertas de lojas oficiais
shop_offers = client.get_shop_offers(
    shop_type=[1],  # Official shops
    sort_type=2,
    limit=5
)
```

### Gerar link de afiliado

```python
# Gerar link curto com sub-IDs para rastreamento
short_link = client.generate_short_link(
    origin_url="https://shopee.com.br/product/123456",
    sub_ids=["promo1", "email2"]
)

print(short_link["data"]["generateShortLink"]["shortLink"])
```

### Relatório de conversões

```python
import time

# Buscar conversões dos últimos 7 dias
now = int(time.time())
week_ago = now - (7 * 24 * 60 * 60)

report = client.get_conversion_report(
    purchase_time_start=week_ago,
    purchase_time_end=now,
    limit=50
)
```

## Executar Testes

```bash
# Rodar suite completa de testes
pytest tests/ -v

# Rodar apenas testes unitários (sem credenciais)
pytest tests/ -m "not integration" -v

# Rodar com cobertura
pytest tests/ --cov=src/shopee_affiliate --cov-report=html

# Usando ruff para lint
ruff check src/ examples/ scripts/ tests/
ruff format src/ examples/ scripts/ tests/

# Verificação de segurança
bandit -r src/
safety check
```

### Status dos Testes

| Endpoint | Status | Observações |
|----------|--------|-------------|
| shopeeOfferV2 | ✅ Passou | Busca por keyword funcionando |
| shopOfferV2 | ✅ Passou | Filtro por shop_type funcionando |
| productOfferV2 | ✅ Passou | Busca por keyword e shop_id |
| generateShortLink | ✅ Passou | Geração com e sem sub-IDs |
| conversionReport | ⚠️ Parcial | Estrutura correta, dados vazios |

**Taxa de sucesso: 77.8%** (7/9 testes passaram)

## Estrutura do Projeto

```
shopee_afiliados_docs/
├── docs/                          # Documentação técnica
│   └── REVISAO_PERFORMANCE.md     # Análise de performance
├── examples/                      # Exemplos de uso
│   └── python/
│       └── shopee_affiliate_client.py  # Cliente principal
├── scripts/                       # Scripts utilitários
│   ├── explore_schema.py          # Exploração de schema
│   └── run_all_tests.py           # Suite de testes
├── tests/python/                  # Testes unitários
├── archive/                       # Logs e backups
├── requirements.txt               # Dependências Python
├── .env.example                   # Exemplo de configuração
├── README.md                      # Este arquivo
├── CONTRIBUTING.md                # Guia de contribuição
├── LICENSE                        # Licença MIT
└── .gitignore                     # Arquivos ignorados pelo git
```

## Links Úteis

- **API Playground**: https://open-api.affiliate.shopee.com.br/explorer
- **Documentação Oficial**: https://www.affiliateshopee.com.br/documentacao/index
- **Portal de Afiliados**: https://www.affiliateshopee.com.br/

## Contribuindo

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre nosso código de conduta e o processo para enviar pull requests.

### Áreas para contribuição

- Melhorar tratamento de erros e retries
- Adicionar cache para queries de leitura
- Implementar paginação streaming
- Adicionar mais testes de integração
- Documentação adicional de endpoints

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Status do Projeto

Este é um projeto não-oficial mantido pela comunidade. O cliente foi desenvolvido através de introspecção GraphQL e não é afiliado ou endossado pela Shopee.

**Aviso**: Use por sua conta e risco. A API pode mudar sem aviso prévio.

## Aviso Legal

Este é um projeto educacional e de exemplo. Os autores não são responsáveis por qualquer uso indevido ou problemas decorrentes do uso desta API. Respeite os Termos de Serviço da API Shopee Affiliate.

## Changelog

### v1.0.0 (2026-02-16)
- Release inicial
- 5 endpoints implementados
- Suite de testes com 77.8% de sucesso
- Documentação completa
- Análise de performance realizada

## Contato

Para questões e suporte, abra uma [issue](https://github.com/gabrielramos/shopee_afiliados_docs/issues) no GitHub.

---

Made with ❤️ by the community
