# Shopee Affiliate API Client

[![CI](https://github.com/gabrielramos/shopee_afiliados_docs/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielramos/shopee_afiliados_docs/actions/workflows/ci.yml)
[![uv](https://img.shields.io/badge/uv-0.10.2-blue.svg)](https://docs.astral.sh/uv/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)

Cliente Python não-oficial para API de Afiliados da Shopee Brasil. Gerenciado com **uv** - o gerenciador de pacotes Python ultra-rápido.

## Funcionalidades

- Cliente Python completo para API Shopee Affiliate
- Schema descoberto via introspecção GraphQL
- 5 endpoints principais testados e documentados
- Autenticação SHA256 com assinatura dinâmica
- Suporte a paginação e filtros avançados
- **100% compatível com uv** (10-100x mais rápido que pip)

## Endpoints Disponíveis

1. **shopeeOfferV2** - Ofertas em destaque da Shopee
2. **shopOfferV2** - Ofertas de lojas específicas
3. **productOfferV2** - Busca de produtos por keyword ou shop
4. **generateShortLink** - Geração de links de afiliado
5. **conversionReport** - Relatório de conversões (estimado)

## Instalação Rápida com uv

### Pré-requisitos

- Python 3.10 ou superior
- uv (gerenciador de pacotes Python)

### Instalar uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Homebrew
brew install uv
```

### Setup do Projeto

```bash
# 1. Clone o repositório
git clone https://github.com/prof-ramos/shopee_afiliados_docs.git
cd shopee_afiliados_docs

# 2. Crie ambiente virtual com uv
uv venv

# 3. Ative o ambiente
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 4. Instale as dependências
uv pip install -e .
```

### Configurar Credenciais

Crie um arquivo `.env` na raiz:

```bash
SHOPEE_APP_ID=seu_app_id_aqui
SHOPEE_APP_SECRET=seu_app_secret_aqui
```

Obtenha suas credenciais em: https://open-api.affiliate.shopee.com.br/

## Uso

### Exemplo Básico

```python
from shopee_affiliate_client import ShopeeAffiliateClient
import os
from dotenv import load_dotenv

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
```

### Gerar Link de Afiliado com Sub-IDs

```python
# Rastreamento granular (até 5 sub-IDs)
short_link = client.generate_short_link(
    origin_url="https://shopee.com.br/product/123456",
    sub_ids=["telegram", "grupo_vip", "promo_verao"]
)

print(short_link["data"]["generateShortLink"]["shortLink"])
```

### Relatório de Conversões

```python
import time

now = int(time.time())
week_ago = now - (7 * 24 * 60 * 60)

# Relatório de conversões
report = client.get_conversion_report(
    purchase_time_start=week_ago,
    purchase_time_end=now,
    limit=50
)

# Iterar sobre páginas
for page in client.iter_conversion_report_pages(
    purchase_time_start=week_ago,
    purchase_time_end=now,
    limit=100
):
    for order in page['data']['conversionReport']['nodes']:
        print(f"Order: {order.get('orderId')}")
```

## Comandos uv

```bash
# Criar ambiente virtual
uv venv

# Instalar pacote
uv pip install requests

# Instalar projeto em modo editável
uv pip install -e .

# Listar pacotes
uv pip list

# Atualizar pacote
uv pip install --upgrade requests

# Verificar vulnerabilidades
uv pip check
```

## Executar Testes

```bash
# Com uv (instalação mais rápida)
uv pip install pytest python-dotenv
pytest tests/ -v

# Lint com ruff
uv pip install ruff
ruff check src/ tests/
ruff format src/ tests/

# Verificação de segurança
uv pip install bandit
bandit -r src/
```

## Estrutura do Projeto

```
shopee_afiliados_docs/
├── docs/                      # Documentação técnica
│   ├── GUIA_UV.md             # Guia completo do uv
│   ├── RASTREAMENTO_COMISSOES.md
│   └── OTIMIZACAO_DESEMPENHO.md
├── src/shopee_affiliate/      # Pacote Python
│   ├── __init__.py
│   ├── client.py              # Cliente principal
│   ├── auth.py                # Autenticação SHA256
│   ├── transport.py           # Camada HTTP
│   ├── queries.py             # Queries GraphQL
│   ├── validators.py          # Validações
│   └── graphql/               # Templates GraphQL
├── tests/python/              # Testes automatizados
├── benchmarks/                # Benchmarks de performance
├── .github/workflows/         # CI/CD com uv
├── pyproject.toml             # Configuração do projeto
└── README.md
```

## Links Úteis

- **uv Docs**: https://docs.astral.sh/uv/
- **API Playground**: https://open-api.affiliate.shopee.com.br/explorer
- **Documentação Shopee**: https://www.affiliateshopee.com.br/documentacao
- **Portal de Afiliados**: https://affiliate.shopee.com.br/

## Contribuindo

Contribuições são bem-vindas! Leia [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

MIT - veja [LICENSE](LICENSE)

---

Made with ❤️ using [uv](https://docs.astral.sh/uv/)
