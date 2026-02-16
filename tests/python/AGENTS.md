<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-15 | Updated: 2026-02-15 -->

# python

## Purpose
Testes unitários específicos para cada endpoint da API Shopee Affiliate. Cada teste valida um endpoint específico com diferentes parâmetros e cenários.

## Key Files

| File | Description |
|------|-------------|
| `test_shopee_offer_v2.py` | Testes do endpoint shopeeOfferV2 (ofertas da Shopee) |
| `test_shopee_offer.py` | Testes legados do endpoint shopeeOffer |
| `test_shop_offer_v2.py` | Testes do endpoint shopOfferV2 (ofertas de lojas) |
| `test_shop_offer.py` | Testes legados do endpoint shopOffer |
| `test_product_offer_v2.py` | Testes do endpoint productOfferV2 (ofertas de produtos) |
| `test_product_offer.py` | Testes legados do endpoint productOffer |
| `test_generate_short_link.py` | Testes do endpoint generateShortLink |
| `test_conversion_report.py` | Testes do endpoint conversionReport |
| `test_payload_format.py` | Testes de formato de payload |
| `test_payload_simple.py` | Testes de payload simples |
| `test_test_api.py` | Testes do script de API |

## For AI Agents

### Working In This Directory
- Cada arquivo de teste foca em um endpoint específico
- Execute com `pytest tests/python/` ou `python -m pytest tests/python/`
- Alguns testes podem falhar se não houver dados no período

### Test Categories

#### V2 Endpoints (Current)
- `test_shopee_offer_v2.py` - Versão atual do endpoint de ofertas Shopee
- `test_shop_offer_v2.py` - Versão atual do endpoint de ofertas de lojas
- `test_product_offer_v2.py` - Versão atual do endpoint de ofertas de produtos

#### Legacy Endpoints
- `test_shopee_offer.py` - Versão antiga (mantida para compatibilidade)
- `test_shop_offer.py` - Versão antiga (mantida para compatibilidade)
- `test_product_offer.py` - Versão antiga (mantida para compatibilidade)

#### Other Tests
- `test_generate_short_link.py` - Valida geração de links curtos
- `test_conversion_report.py` - Valida relatório de conversões
- `test_payload_*.py` - Valida formato de requisições

### Known Test Failures

#### test_generate_short_link.py
- **Expected Failure**: Testes com `sub_ids=["email", "canal_email"]`
- **Reason**: Palavras reservadas pelo sistema
- **Solution**: Use apenas valores simples como `["s1", "s2"]`

#### test_conversion_report.py
- **Expected**: Retornar 0 conversões se não houver dados no período
- **Reason**: API retorna apenas últimos 3 meses
- **Solution**: Use período mais recente ou dados reais de produção

### Testing Requirements

```bash
# Executar todos os testes
pytest tests/python/

# Executar teste específico
pytest tests/python/test_product_offer_v2.py -v

# Executar com detalhes
pytest tests/python/ -v -s
```

### Common Patterns
- Testes importam `ShopeeAffiliateClient` de `examples.python.shopee_affiliate_client`
- Usam `load_dotenv()` para carregar credenciais
- Validam estrutura da resposta e campos retornados
- Alguns testes verificam erros esperados

## Dependencies

### Internal
- `../../examples/python/shopee_affiliate_client.py` - Cliente sendo testado
- `../../.env` - Credenciais da API

### External
- `pytest` - Framework de testes
- `python-dotenv` - Carregamento de variáveis de ambiente
- `time` - Para timestamps unix em testes de conversão

<!-- MANUAL: -->
