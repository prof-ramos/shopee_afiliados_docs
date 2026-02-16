<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-15 | Updated: 2026-02-15 -->

# docs

## Purpose
Documentação completa da API Shopee Affiliate. Contém guias atualizados com schema correto descoberto via introspecção, exemplos de uso e análise de erros.

## Key Files

| File | Description |
|------|-------------|
| `GUIA_COMPLETO.md` | Guia principal com todos os endpoints documentados e resultados dos testes |
| `ATUALIZACAO_FINAL.md` | Documentação completa da atualização final do schema |
| `SCHEMA_DESCOBERTO.md` | Schema GraphQL descoberto via introspecção |
| `PESQUISA_SCHEMA_RESUMO.md` | Resumo da pesquisa de schema |
| `REVISAO_PERFORMANCE.md` | Análise de performance da API |
| `docs_shopee_affiliate.md` | Documentação original da API |

## For AI Agents

### Working In This Directory
- A documentação oficial da Shopee está desatualizada
- Use `GUIA_COMPLETO.md` como referência principal
- O schema foi descoberto via introspecção GraphQL
- Os campos corretos diferem da documentação oficial

### Schema Correto (Descoberto)

#### conversionReport
- Estrutura: `nodes.orders.items[]` (ANINHADA)
- Use `itemName` (não `productName`)
- Use `itemTotalCommission` (não `commissionAmount`)
- Use `globalCategoryLv*Name` (não `categoryLv*Name`)

#### generateShortLink
- subIds válidos: `["s1", "s2", "a", "b", "promo1"]`
- subIds INVÁLIDOS: `["email", "canal", "utm", "sub_id_1"]`
- Limite: 5 valores por requisição

### Limitações Importantes
- **3 meses**: conversionReport retorna apenas últimos 3 meses
- **30 segundos**: scrollId expira rapidamente
- **77.8%** de sucesso na suite de testes (7/9)

### Common Patterns
- Consulte `GUIA_COMPLETO.md` para exemplos de código
- Use `SCHEMA_DESCOBERTO.md` para entender a estrutura dos dados
- Verifique `REVISAO_PERFORMANCE.md` para otimizações

## Dependencies

### Internal
- `examples/python/shopee_affiliate_client.py` - Cliente Python implementado
- `scripts/explore_schema.py` - Script usado para descobrir o schema

### External
- [API Playground](https://open-api.affiliate.shopee.com.br/explorer)
- [Documentação Oficial](https://www.affiliateshopee.com.br/documentacao/index)

<!-- MANUAL: -->
