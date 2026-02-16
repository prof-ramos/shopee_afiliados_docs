<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-15 | Updated: 2026-02-15 -->

# scripts

## Purpose
Scripts de automação e exploração do schema GraphQL da API Shopee Affiliate. Usados para descobrir campos disponíveis via introspecção e validar implementações.

## Key Files

| File | Description |
|------|-------------|
| `explore_schema.py` | Script principal de exploração de schema via introspecção GraphQL |
| `run_all_tests.py` | Suite completa de testes automatizados (9 testes) |
| `update_client_from_docs.py` | Atualiza o cliente Python baseado na documentação |

## For AI Agents

### Working In This Directory
- Execute scripts da raiz do projeto: `python scripts/explore_schema.py`
- Certifique-se de que o ambiente virtual está ativado
- O diretório `examples/python` é adicionado ao path automaticamente

### explore_schema.py

**Propósito**: Descobrir campos disponíveis nos endpoints GraphQL

**Funcionalidades**:
- Introspecção de `conversionReport` e seus tipos aninhados
- Introspecção de `productOfferV2`
- Listagem de todos os campos disponíveis no tipo Query
- Testes de query com dados reais

**Uso**:
```bash
python scripts/explore_schema.py
```

### run_all_tests.py

**Propósito**: Executar suite completa de testes da API

**Testes incluídos**:
1. shopeeOfferV2 (keyword)
2. shopeeOfferV2 (todas)
3. shopOfferV2 (lojas)
4. productOfferV2 (keyword)
5. productOfferV2 (shop_id)
6. generateShortLink (complexo) - falha esperada
7. generateShortLink (simples)
8. conversionReport (7 dias)
9. conversionReport (estrutura)

**Resultado atual**: 77.8% de sucesso (7/9 testes)

### Common Patterns
- Scripts usam `sys.path.insert(0, ...)` para importar o cliente
- Sempre carregam variáveis de ambiente com `load_dotenv()`
- Usam introspecção GraphQL para descobrir tipos

## Dependencies

### Internal
- `examples/python/shopee_affiliate_client.py` - Cliente principal
- `../.env` - Credenciais da API

### External
- `python-dotenv` - Carregamento de variáveis de ambiente
- `time` - Para timestamps unix
- `json` - Para formatação de respostas

<!-- MANUAL: -->
