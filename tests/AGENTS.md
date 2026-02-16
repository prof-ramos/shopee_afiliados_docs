<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-15 | Updated: 2026-02-15 -->

# tests

## Purpose
Suíte completa de testes Python para validar os endpoints da API Shopee Affiliate. Todos os testes foram executados e validados com resultados documentados.

## Key Files

| File | Description |
|------|-------------|
| `run_all_tests.py` | Script que executa todos os 9 testes da suite |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `python/` | Testes unitários específicos de cada endpoint (veja `python/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- Execute `python tests/run_all_tests.py` da raiz do projeto
- Certifique-se de que as credenciais estão configuradas no `.env`
- Os testes validam todos os endpoints principais da API

### Test Results (Documentados em docs/GUIA_COMPLETO.md)

| # | Teste | Status |
|---|-------|--------|
| 1 | shopeeOfferV2 (keyword) | ✅ Passou |
| 2 | shopeeOfferV2 (todas) | ✅ Passou |
| 3 | shopOfferV2 (lojas) | ✅ Passou |
| 4 | productOfferV2 (keyword) | ✅ Passou |
| 5 | productOfferV2 (shop_id) | ✅ Passou |
| 6 | generateShortLink (complexo) | ❌ Falha esperada ("invalid sub id") |
| 7 | generateShortLink (simples) | ✅ Passou |
| 8 | conversionReport (7 dias) | ✅ Passou |
| 9 | conversionReport (estrutura) | ⚠️ Sem dados no período |

**Taxa de Sucesso**: 77.8% (7/9 testes)

### Testing Requirements
- Sempre execute com credenciais válidas no `.env`
- Verifique se `SHOPEE_APP_ID` e `SHOPEE_APP_SECRET` estão configurados
- Use pytest ou execute diretamente o script `run_all_tests.py`

### Common Patterns
- Cada teste valida um endpoint específico
- Testes usam o cliente `examples/python/shopee_affiliate_client.py`
- Erros esperados são documentados e analisados

## Dependencies

### Internal
- `examples/python/shopee_affiliate_client.py` - Cliente sendo testado
- `python/*.py` - Testes unitários específicos
- `../.env` - Credenciais da API

### External
- `pytest` - Framework de testes (opcional, pode executar diretamente)
- `python-dotenv` - Carregamento de credenciais

<!-- MANUAL: -->
