<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-15 | Updated: 2026-02-15 -->

# python

## Purpose
Implementação completa do cliente Python para a API Shopee Affiliate. Contém a classe `ShopeeAffiliateClient` com todos os endpoints implementados e testados.

## Key Files

| File | Description |
|------|-------------|
| `shopee_affiliate_client.py` | Cliente Python completo com todos os endpoints da API |

## For AI Agents

### Working In This Directory
- Este é o coração da implementação Python do projeto
- Todos os outros scripts importam este cliente
- Use `from shopee_affiliate_client import ShopeeAffiliateClient`

### ShopeeAffiliateClient - API Methods

#### Queries
- `get_shopee_offers(keyword, sort_type, page, limit)` - Ofertas da Shopee
- `get_shop_offers(keyword, shop_id, shop_type, ...)` - Ofertas de lojas
- `get_product_offers(keyword, shop_id, item_id, ...)` - Ofertas de produtos
- `get_conversion_report(purchase_time_start, ...)` - Relatório de conversões

#### Mutations
- `generate_short_link(origin_url, sub_ids)` - Gerar link de rastreamento

#### Pagination
- `get_all_conversion_pages(...)` - Busca todas as páginas com scrollId

### Schema Implementation

```python
class ShopeeAffiliateClient:
    def __init__(self, app_id: str, app_secret: str)
    def _generate_signature(self, payload: str, timestamp: int) -> str
    def _get_auth_header(self, payload: str) -> str
    def _request(self, query: str, variables: Optional[Dict]) -> Dict
```

### Authentication
- **Type**: SHA256 Signature
- **Formula**: `SHA256(Credential + Timestamp + Payload + Secret)`
- **Header**: `Authorization: SHA256 Credential=..., Timestamp=..., Signature=...`

### Important Notes

#### conversionReport Schema (DISCOVERED via introspection)
- Structure: `nodes.orders.items[]` (NESTED!)
- Use `itemName` (NOT `productName`)
- Use `itemTotalCommission` (NOT `commissionAmount`)
- Only 3 months of data available
- scrollId expires in 30 seconds

#### generateShortLink Constraints
- subIds must be simple strings: `["s1", "s2", "a", "b"]`
- INVALID: `["email", "canal", "utm", "sub_id_1"]`
- Maximum 5 values per request
- Words like "email" are reserved by the system

### Common Patterns

```python
# Initialize
from shopee_affiliate_client import ShopeeAffiliateClient
client = ShopeeAffiliateClient(app_id, app_secret)

# Search products
products = client.get_product_offers(keyword="iphone", sort_type=5, limit=10)

# Generate short link
short = client.generate_short_link(origin_url=url, sub_ids=["s1", "s2"])

# Get conversion report
report = client.get_conversion_report(start_time, end_time, limit=500)
```

## Dependencies

### External
- `requests` - HTTP client for GraphQL requests
- `hashlib` - SHA256 signature generation
- `json` - Payload serialization
- `time` - Unix timestamps
- `typing` - Type hints (Optional, List, Dict, Any)

### Internal
- Used by all scripts in `../../scripts/`
- Tested by all tests in `../../tests/python/`

<!-- MANUAL: -->
