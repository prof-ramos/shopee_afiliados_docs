<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-16 | Updated: 2026-02-16 -->

# graphql

## Purpose
Arquivos de queries GraphQL otimizadas para a API de Afiliados da Shopee. Essas queries foram descobertas via introspecção do schema GraphQL e representam a estrutura correta da API.

## Key Files

| File | Description |
|------|-------------|
| `conversionReport.graphql` | Query para relatório de conversões (últimos 3 meses) |
| `validatedReport.graphql` | Query para relatório de comissões validadas (definitivas) |
| `generateShortLink.graphql` | Query para gerar links encurtados de afiliado |
| `productOfferV2.graphql` | Query para ofertas de produto específico |
| `shopeeOfferV2.graphql` | Query para ofertas gerais da Shopee |
| `shopOfferV2.graphql` | Query para ofertas de loja específica |

## For AI Agents

### Working In This Directory
- **⚠️ AVISO**: Não modifique esses arquivos manualmente sem entender GraphQL
- As queries foram validadas via introspecção do schema
- A documentação oficial da Shopee está desatualizada - estas queries estão corretas
- Se precisar adicionar queries, use introspecção para descobrir o schema correto

### Testing Requirements
- Testes de integração em `tests/python/` validam cada query
- Use o GraphQL Playground da Shopee para testar queries: https://open-api.affiliate.shopee.com.br/explorer

### Common Patterns
```graphql
# Padrão de query
query QueryName($param: Type!) {
  responseField(param: $param) {
    field1
    field2
    nestedField {
      subField
    }
  }
}
```

## GraphQL Queries

### conversionReport.graphql
- **Propósito**: Buscar relatório de conversões de afiliado
- **Limitação**: Retorna apenas últimos 3 meses de dados
- **Paginação**: Usa `scrollId` que expira em 30 segundos

### validatedReport.graphql
- **Propósito**: Buscar relatório de comissões validadas (definitivas)
- **Diferença**: Retorna apenas comissões já validadas pela Shopee (valores definitivos)
- **Paginação**: Usa `scrollId` que expira em 30 segundos

### generateShortLink.graphql
- **Propósito**: Gerar link encurtado com parâmetros de afiliado
- **Limitação**: Não aceita palavras reservadas ("email", "canal", "utm")

### productOfferV2.graphql
- **Propósito**: Buscar ofertas de um produto específico
- **Uso**: Recomendações de produtos em artigos/blogs

### shopeeOfferV2.graphql
- **Propósito**: Buscar ofertas gerais da Shopee
- **Uso**: Landing pages de ofertas diversas

### shopOfferV2.graphql
- **Propósito**: Buscar ofertas de uma loja específica
- **Uso**: Páginas de lojas parceiras

## Dependencies

### Internal
- `../queries.py` - Importa essas queries como strings constantes
- `../client.py` - Usa essas queries nas requisições

### External
- **Shopee GraphQL API** - https://open-api.affiliate.shopee.com.br/graphql

## Schema Discovery

Para descobrir novas queries via introspecção:

```python
import requests

url = "https://open-api.affiliate.shopee.com.br/graphql"
query = """
{
  __schema {
    queryType {
      fields {
        name
        description
      }
    }
  }
}
"""
```

<!-- MANUAL: Notas sobre queries GraphQL podem ser adicionadas abaixo -->
