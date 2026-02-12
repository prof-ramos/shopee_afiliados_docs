# Exemplos de Uso - Shopee Affiliate API (Python)

Este diretorio contem exemplos praticos em Python para integracao com a API de Afiliados da Shopee Brasil.

## Estrutura

```text
examples/
├── python/
│   └── shopee_affiliate_client.py
├── test_api.py
└── README.md
```

## Configuracao de Credenciais

Crie um arquivo `.env` na raiz do projeto:

```bash
SHOPEE_APP_ID=seu_app_id_aqui
SHOPEE_APP_SECRET=seu_app_secret_aqui
```

## Configuracao do Ambiente

```bash
# Criar ambiente virtual com uv
uv venv
source .venv/bin/activate

# Instalar dependencias
uv pip install -r requirements.txt
```

## Teste Rapido

```bash
uv run --python .venv/bin/python python examples/test_api.py
```

## Operacoes Disponiveis (Python)

### 1. Buscar Ofertas da Shopee

```python
offers = client.get_shopee_offers(
    keyword="roupas",
    sort_type=2,
    page=1,
    limit=10
)
```

### 2. Buscar Ofertas de Lojas

```python
shops = client.get_shop_offers(
    shop_type=[1],
    sort_type=2,
    limit=10
)
```

### 3. Buscar Ofertas de Produtos

```python
products = client.get_product_offers(
    keyword="iphone",
    sort_type=5,
    limit=10
)
```

### 4. Gerar Link Curto

```python
short_link = client.generate_short_link(
    origin_url="https://shopee.com.br/produto-exemplo",
    sub_ids=["s1", "s2"]
)
```

### 5. Relatorio de Conversao

```python
report = client.get_conversion_report(
    purchase_time_start=week_ago,
    purchase_time_end=now,
    limit=500
)
```

## Links Uteis

- [Documentacao completa](../docs/docs_shopee_affiliate.md)
- [API Explorer](https://open-api.affiliate.shopee.com.br/explorer)
- [Solicitar acesso a API](https://help.shopee.com.br/portal/webform/bbce78695c364ba18c9cbceb74ec9091)
