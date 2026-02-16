# Documentação Completa - API Shopee Affiliate

**Versão:** 0.1.0
**Data:** 2026-02-16
**Status:** Produção

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Autenticação](#autenticação)
3. [Endpoints](#endpoints)
   - [Queries](#queries)
   - [Mutations](#mutations)
4. [Tipos e Enums](#tipos-e-enums)
5. [Limitações e Restrições](#limitações-e-restrições)
6. [Boas Práticas](#boas-práticas)

---

## Visão Geral

A API Shopee Affiliate é uma interface GraphQL para afiliados da Shopee Brasil. Permite buscar produtos, gerar links de rastreamento e consultar relatórios de conversões.

**URL Base:** `https://open-api.affiliate.shopee.com.br/graphql`

**Método:** HTTP POST com corpo JSON contendo query GraphQL

**Versão:** GraphQL via HTTP/1.1

---

## Autenticação

### SHA256 Signature

Todas as requisições requerem assinatura HMAC-SHA256:

```python
import hmac
import hashlib
import time

def generate_signature(app_id: str, app_secret: str, timestamp: int) -> str:
    """Gera assinatura SHA256 para API Shopee."""
    message = f"{app_id}{timestamp}"
    return hmac.new(
        app_secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
```

### Headers Requeridos

```http
POST /graphql HTTP/1.1
Host: open-api.affiliate.shopee.com.br
Content-Type: application/json

{
  "query": "...",
  "variables": {}
}
```

### Parâmetros de Autenticação

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `app_id` | String | Identificador da aplicação |
| `timestamp` | Int64 | Timestamp Unix atual em segundos |
| `signature` | String | HMAC-SHA256 de `{app_id}{timestamp}` |

---

## Endpoints

### Queries

#### 1. shopeeOfferV2

Ofertas em destaque da Shopee (campanhas oficiais).

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `keyword` | String | Não | Palavra-chave para busca |
| `sortType` | Int | Não | Tipo de ordenação (default: 1) |
| `page` | Int | Não | Número da página (default: 1) |
| `limit` | Int | Não | Itens por página (default: 10, max: 100) |

**SortType:**
- `1` - Recomendados
- `2` - Maior comissão
- `3` - Mais vendidos
- `4` - Mais recentes

**Exemplo:**

```python
from shopee_affiliate_client import ShopeeAffiliateClient

client = ShopeeAffiliateClient(APP_ID, APP_SECRET)

offers = client.get_shopee_offers(
    keyword="tenis",
    sort_type=2,  # Maior comissão
    page=1,
    limit=10
)

# Resposta
{
  "data": {
    "shopeeOfferV2": {
      "nodes": [
        {
          "itemName": "Tênis Esportivo",
          "itemPrice": 199.90,
          "itemCommission": 20.00,
          "itemCommissionRate": "10.0",
          "shopId": 123456,
          "shopName": "Loja Oficial",
          "itemId": 789012,
          "imageUrl": "https://...",
          "itemLink": "https://shopee.com.br/..."
        }
      ]
    }
  }
}
```

---

#### 2. shopOfferV2

Ofertas de lojas específicas ou por tipo.

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `keyword` | String | Não | Palavra-chave para busca |
| `shopId` | Int64 | Não | ID da loja específica |
| `shopType` | [Int!] | Não | Tipo de loja (lista) |
| `isKeySeller` | Boolean | Não | Vendedores chave (default: false) |
| `sortType` | Int | Não | Tipo de ordenação |
| `page` | Int | Não | Número da página |
| `limit` | Int | Não | Itens por página |

**ShopType:**
- `1` - Shopee Mall CB
- `2` - Shopee Mall Non-CB
- `3` - C2C CB
- `4` - C2C Non-CB
- `5` - Preferred CB
- `6` - Preferred Non-CB

**Exemplo:**

```python
# Ofertas de Shopee Mall
offers = client.get_shop_offers(
    keyword="iphone",
    shop_type=[1, 2],  # Shopee Mall
    is_key_seller=True,
    sort_type=2,
    limit=20
)
```

---

#### 3. productOfferV2

Busca de produtos por palavra-chave ou loja.

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `keyword` | String | Não | Palavra-chave para busca |
| `shopId` | Int64 | Não | ID da loja |
| `itemId` | Int64 | Não | ID do produto específico |
| `productCatId` | Int | Não | ID da categoria |
| `listType` | Int | Não | Tipo de lista (default: 0) |
| `matchId` | Int64 | Não | ID de correspondência |
| `sortType` | Int | Não | Tipo de ordenação |
| `page` | Int | Não | Número da página |
| `limit` | Int | Não | Itens por página |

**ListType:**
- `0` - Todos
- `1` - Shopee Mall
- `2` - Shopee Preferred

**Exemplo:**

```python
# Buscar produto específico
products = client.get_product_offers(
    keyword="smartwatch",
    list_type=0,
    sort_type=2,
    page=1,
    limit=10
)
```

---

#### 4. generateShortLink

**Mutation** - Gera link de afiliado para rastreamento.

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `input` | GenerateShortLinkInput | Sim | Configuração do link |
| `input.originUrl` | String | Sim | URL original do produto |
| `input.subIds` | [String!] | Não | Sub-IDs para rastreamento (max 5) |

**Sub-IDs:**
- Máximo 5 itens
- Apenas caracteres alfanuméricos (sem underscore, hífen)
- Usados para rastreamento granular

**Exemplo:**

```python
# Link básico
link = client.generate_short_link(
    origin_url="https://shopee.com.br/product-i.123.456"
)
# Retorna: "https://s.shopee.com.br/abc123"

# Link com sub-IDs para rastreamento
link = client.generate_short_link(
    origin_url="https://shopee.com.br/product-i.123.456",
    sub_ids=["telegram", "grupo_vip", "promo_verao"]
)
# No relatório: utm_content = "telegram.grupo_vip.promo_verao"
```

---

#### 5. conversionReport

Relatório de conversões (comissões estimadas).

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `purchaseTimeStart` | Int64 | Não | Timestamp inicial (compra) |
| `purchaseTimeEnd` | Int64 | Não | Timestamp final (compra) |
| `completeTimeStart` | Int64 | Não | Timestamp inicial (conclusão) |
| `completeTimeEnd` | Int64 | Não | Timestamp final (conclusão) |
| `shopName` | String | Não | Nome da loja |
| `shopId` | Int64 | Não | ID da loja |
| `shopType` | [ShopType!] | Não | Tipo de loja |
| `conversionId` | Int64 | Não | ID da conversão |
| `conversionStatus` | ConversionStatus | Não | Status da conversão |
| `checkoutId` | Int64 | Não | ID do checkout |
| `orderId` | String | Não | ID do pedido |
| `productName` | String | Não | Nome do produto |
| `productId` | Int64 | Não | ID do produto |
| `categoryLv1Id/2/3Id` | Int64 | Não | ID da categoria |
| `categoryType` | CategoryType | Não | Tipo de categoria |
| `orderStatus` | DisplayOrderStatus | Não | Status do pedido |
| `buyerType` | BuyerType | Não | Tipo de comprador |
| `productType` | ProductType | Não | Tipo de produto |
| `fraudStatus` | FraudStatus | Não | Status de fraude |
| `device` | DeviceType | Não | Dispositivo |
| `attributionType` | AttributionType | Não | Tipo de atribuição |
| `campaignPartnerName` | String | Não | Nome da campanha |
| `campaignType` | CampaignType | Não | Tipo de campanha |
| `limit` | Int | Não | Itens por página |
| `scrollId` | String | Não | Token de paginação |

**Exemplo:**

```python
import time

now = int(time.time())
week_ago = now - (7 * 24 * 60 * 60)

# Relatório de conversões da última semana
report = client.get_conversion_report(
    purchase_time_start=week_ago,
    purchase_time_end=now,
    limit=50
)

# Paginação
for page in client.iter_conversion_report_pages(
    purchase_time_start=week_ago,
    purchase_time_end=now,
    limit=100
):
    orders = page['data']['conversionReport']['nodes']
    for order in orders:
        print(f"Order: {order['orderId']}")
        print(f"Commission: {order.get('estimatedCommission')}")
```

---

#### 6. validatedReport

**STATUS: NÃO DISPONÍVEL** - Requer `validationId` específico.

Este endpoint existe mas **não foi implementado** pois requer um `validationId` que não sabemos como obter.

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `validationId` | Int64 | **Sim** | ID de validação (desconhecido) |
| `limit` | Int | Não | Itens por página |
| `scrollId` | String | Não | Token de paginação |

**Nota:** Use `conversionReport` como alternativa.

---

#### 7. partnerOrderReport

**STATUS: NÃO DISPONÍVEL** - Erro 10031 (access deny).

Este endpoint pode ser uma alternativa ao `validatedReport` quando disponível.

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `purchaseTimeStart` | Int64 | Não | Timestamp inicial |
| `purchaseTimeEnd` | Int64 | Não | Timestamp final |
| `completeTimeStart` | Int64 | Não | Timestamp conclusão inicial |
| `completeTimeEnd` | Int64 | Não | Timestamp conclusão final |
| `limit` | Int | Não | Itens por página |
| `searchNextToken` | String | Não | Token de paginação |

---

#### 8. brandOffer

Ofertas de marcas específicas.

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `name` | String | Não | Nome da marca |
| `commissionRateLower` | String | Não | Comissão mínima |
| `commissionRateUpper` | String | Não | Comissão máxima |
| `periodStartTime` | Int | Não | Início do período |
| `periodEndTime` | Int | Não | Fim do período |
| `offerStatus` | [OfferStatus!] | Não | Status da oferta |
| `orderBy` | BrandOfferOrder | Não | Ordenação |
| `page` | Int | Não | Página |
| `limit` | Int | Não | Limite |

---

#### 9. checkAffiliateId

Verifica se um ID de afiliado é válido.

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `affiliateId` | Int64! | **Sim** | ID do afiliado |
| `source` | String! | **Sim** | Origem da solicitação |

---

#### 10. getItemFeedData / listItemFeeds

Endpoints para feeds de dados de produtos.

**Uso:** Integração com catálogos de produtos.

---

### Mutations

#### 1. generateShortLink

Ver documentação acima em Queries #4.

#### 2. generateBatchShortLink

Gera múltiplos links de afiliado em lote.

**Argumentos:**

| Nome | Tipo | Obrigatório | Descrição |
|------|------|-------------|-----------|
| `input` | BatchInput | Sim | Lista de URLs |
| `input.links` | [String!] | Sim | URLs originais |

**Retorna:**
- `links` - Links gerados
- `total` - Total de links
- `successCount` - Quantidade de sucessos

#### 3. syncAffiliateStatus

Sincroniza status de afiliado.

---

## Tipos e Enums

### ConversionStatus

Status de uma conversão.

| Valor | Descrição |
|-------|-----------|
| `ALL` | Todos |
| `PENDING` | Pendente |
| `COMPLETED` | Concluído |
| `CANCELLED` | Cancelado |

### DisplayOrderStatus

Status exibido do pedido.

| Valor | Descrição |
|-------|-----------|
| `ALL` | Todos |
| `UNPAID` | Não pago |
| `PENDING` | Pendente |
| `COMPLETED` | Concluído |
| `CANCELLED` | Cancelado |

### ShopType

Tipo de loja.

| Valor | Descrição |
|-------|-----------|
| `ALL` | Todos |
| `SHOPEE_MALL_CB` | Shopee Mall com CB |
| `SHOPEE_MALL_NON_CB` | Shopee Mall sem CB |
| `C2C_CB` | C2C com CB |
| `C2C_NON_CB` | C2C sem CB |
| `PREFERRED_CB` | Preferred com CB |
| `PREFERRED_NON_CB` | Preferred sem CB |

### CategoryType

Tipo de categoria.

| Valor | Descrição |
|-------|-----------|
| `ALL` | Todos |
| `MP` | Marketplace |
| `DP` | Departamento |

### OfferStatus

Status de uma oferta.

| Valor | Descrição |
|-------|-----------|
| `ONGOING` | Em andamento |
| `UPCOMING` | A vir |
| `ENDED` | Encerrada |
| `TERMINATED` | Terminada |
| `PAUSED` | Pausada |

---

## Limitações e Restrições

### Rate Limiting

- **Não documentado oficialmente**
- Recomendado: máximo 10 requisições/segundo
- Implementar retry com exponential backoff

### Paginação

- **scrollId** expira em 30 segundos
- **limit** máximo: 100 itens por página
- Use iteradores para grandes volumes de dados

### Sub-IDs

- Máximo 5 sub-IDs
- Apenas caracteres alfanuméricos
- Erro 11001 se inválido

### Filtros de Tempo

- Timestamps em formato Unix (segundos)
- Período máximo: 90 dias recomendado
- Períodos maiores podem retornar erro

### Campos Opcionais

- Muitos campos são opcionais
- Valores `null` devem ser enviados como `null` (não vazios)

---

## Boas Práticas

### 1. Tratamento de Erros

```python
def safe_api_call(client, query_func, *args, **kwargs):
    """Executa chamada API com tratamento de erros."""
    try:
        result = query_func(*args, **kwargs)

        if "errors" in result:
            error = result["errors"][0]
            error_code = error.get("extensions", {}).get("code")

            if error_code == 10010:
                print("Erro: Parâmetro inválido")
            elif error_code == 10020:
                print("Erro: Assinatura inválida")
            elif error_code == 11001:
                print("Erro: Sub-ID inválido")
            else:
                print(f"Erro {error_code}: {error['message']}")
            return None

        return result

    except Exception as e:
        print(f"Exceção: {e}")
        return None
```

### 2. Paginação Eficiente

```python
# Usar iteradores para grandes volumes
for order in client.iter_conversion_report_orders(
    purchase_time_start=start,
    purchase_time_end=end,
    limit=500  # Maior limite
):
    process_order(order)
    # Não acumula tudo em memória
```

### 3. Cache de Links

```python
import hashlib
import json

def get_cached_link(client, origin_url, sub_ids=None):
    """Retorna link em cache ou gera novo."""
    cache_key = hashlib.md5(
        f"{origin_url}{sub_ids}".encode()
    ).hexdigest()

    # Verificar cache...
    # Se não existir, gerar novo link
    return client.generate_short_link(origin_url, sub_ids)
```

### 4. Retry com Exponential Backoff

```python
import time

def api_call_with_retry(client, query_func, max_retries=3):
    """Tenta chamada API com retry."""
    for attempt in range(max_retries):
        try:
            return query_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
```

---

## Exemplos Completos

### Exemplo 1: Bot de Telegram

```python
from shopee_affiliate_client import ShopeeAffiliateClient
import os

client = ShopeeAffiliateClient(
    app_id=os.getenv("SHOPEE_APP_ID"),
    app_secret=os.getenv("SHOPEE_APP_SECRET")
)

def search_and_generate_link(keyword: str) -> str:
    """Busca produto e gera link de afiliado."""

    # 1. Buscar produto
    products = client.get_product_offers(
        keyword=keyword,
        sort_type=2,  # Maior comissão
        limit=1
    )

    if not products["data"]["productOfferV2"]["nodes"]:
        return "Nenhum produto encontrado"

    product = products["data"]["productOfferV2"]["nodes"][0]
    origin_url = product["itemLink"]

    # 2. Gerar link com sub-IDs
    link = client.generate_short_link(
        origin_url=origin_url,
        sub_ids=["telegram", "bot_search"]
    )

    short_url = link["data"]["generateShortLink"]["shortLink"]

    return f"""
🛒 *{product['itemName']}*
💰 R$ {product['itemPrice']}
📈 Comissão: {product['itemCommissionRate']}%

🔗 {short_url}
    """

# Uso
print(search_and_generate_link("tenis nike"))
```

### Exemplo 2: Relatório Diário

```python
import time
from datetime import datetime

def generate_daily_report():
    """Gera relatório diário de conversões."""

    # Ontem
    yesterday = int(time.time()) - (24 * 60 * 60)
    today = int(time.time())

    # Buscar conversões
    orders = []
    for page in client.iter_conversion_report_pages(
        purchase_time_start=yesterday,
        purchase_time_end=today,
        limit=100
    ):
        data = page["data"]["conversionReport"]["nodes"]
        orders.extend(data)

    # Calcular totais
    total_orders = len(orders)
    total_commission = sum(
        float(o.get("estimatedCommission", 0))
        for o in orders
    )

    # Relatório
    date_str = datetime.fromtimestamp(yesterday).strftime("%Y-%m-%d")

    report = f"""
📊 Relatório Diário - {date_str}

🛒 Pedidos: {total_orders}
💰 Comissão Estimada: R$ {total_commission:.2f}

Detalhes:
"""

    for order in orders[:10]:  # Primeiros 10
        report += f"  • Order {order.get('orderId')}: R$ {order.get('estimatedCommission', 0)}\n"

    return report

print(generate_daily_report())
```

---

## Referências

- **API Playground:** https://open-api.affiliate.shopee.com.br/explorer
- **Documentação Oficial:** https://www.affiliateshopee.com.br/documentacao
- **Portal de Afiliados:** https://affiliate.shopee.com.br/

---

**Última atualização:** 2026-02-16
**Versão da API:** GraphQL (via introspecção)
