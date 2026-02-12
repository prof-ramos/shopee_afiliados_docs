# Pesquisa: Documentação Atualizada Shopee Affiliate API

## Resumo das Descobertas

### Data: 12/02/2026
### Método: Introspecção GraphQL + Testes com credenciais válidas

---

## 🔍 Objetivo

Descobrir o schema atual da API Shopee Affiliate, já que a documentação oficial está desatualizada e os sites de documentação requerem login de afiliado.

## ✅ Descobertas Principais

### 1. Schema Real de `conversionReport`

**Estrutura correta:**
```
conversionReport {
  nodes {
    orders {              # ← Campo agregador, não campos diretos
      orderId
      shopType
      orderStatus
      items {              # ← Itens dentro de orders
        itemId
        itemName             # ← Use este (não productName)
        itemTotalCommission  # ← Use este (não commissionAmount)
        itemPrice
        qty
        globalCategoryLv1Name
        globalCategoryLv2Name
        globalCategoryLv3Name
        ...
      }
    }
  }
  pageInfo {
    scrollId    # ← Expira em 30 segundos!
    hasNextPage
    limit
  }
}
```

### 2. Campos Corretos vs Documentação

| Documentação (❌ Incorreto) | API Real (✅ Correto) |
|------------------------------|---------------------------|
| `productName` | `itemName` |
| `commissionAmount` | `itemTotalCommission` |
| Campos diretos em `nodes` | `nodes.orders.items` |
| `page` parâmetro | ❌ Não suportado |

### 3. Campos Deprecated

Evitar usar:
- `categoryLv1Name`, `categoryLv2Name`, `categoryLv3Name`
  → Use: `globalCategoryLv1Name`, `globalCategoryLv2Name`, `globalCategoryLv3Name`
- `itemCommission`
  → Use: `itemTotalCommission`
- `grossBrandCommission`
  → Use: `itemTotalCommission`

### 4. Novos Endpoints Descobertos

A API tem **12 endpoints** no total:

| Endpoint | Descrição |
|----------|------------|
| `brandOffer` | Ofertas de marcas |
| `shopOfferV2` | Ofertas de lojas V2 |
| `shopeeOfferV2` | Ofertas da Shopee V2 |
| `productOfferV2` | Ofertas de produtos V2 |
| `conversionReport` | Relatório de conversões |
| **`validatedReport`** | Relatório validado ⭐ NOVO |
| **`partnerOrderReport`** | Relatório de pedidos parceiro ⭐ NOVO |
| **`listItemFeeds`** | Listar feeds de itens ⭐ NOVO |
| **`getItemFeedData`** | Obter dados de feed ⭐ NOVO |
| `checkAffiliateId` | Verificar ID de afiliado |

### 5. Limitações Importantes

1. **Limite temporal de 3 meses** (Erro 11001)
   - `conversionReport` só retorna dados dos últimos 3 meses
   - Tentar buscar dados mais antigos retorna erro

2. **scrollId expira em 30 segundos**
   - Paginação com `scrollId` deve ser rápida
   - Nãoideal para grandes relatórios sem processamento intermediário

3. **Rate limit: 2000 requisições/hora**

## 📁 Arquivos Criados/Atualizados

### Criados
- `scripts/explore_schema.py` - Script de exploração do schema
- `SCHEMA_DESCOBERTO.md` - Documentação completa do schema descoberto
- `PESQUISA_SCHEMA_RESUMO.md` - Este arquivo

### Atualizados
- `examples/python/shopee_affiliate_client.py` - Cliente com schema correto
  - ✅ `get_conversion_report()` atualizado com `nodes.orders.items`
  - ✅ Documentação atualizada com campos corretos

## 🧪 Testes Realizados

Todos os endpoints foram testados com sucesso:

| Endpoint | Status |
|-----------|----------|
| shopeeOfferV2 | ✅ Funcionando |
| shopOfferV2 | ✅ Funcionando |
| productOfferV2 | ✅ Funcionando |
| generateShortLink | ✅ Funcionando (fix: `json.dumps` para `subIds`) |
| conversionReport | ✅ Funcionando (schema corrigido) |

## 📋 Próximos Passos Sugeridos

1. Explorar novos endpoints:
   - `validatedReport` - Possivelmente mais robusto que `conversionReport`
   - `partnerOrderReport` - Pode ter dados adicionais
   - `listItemFeeds` / `getItemFeedData` - Funcionalidade de feeds

2. Implementar paginação robusta para `scrollId` de 30s:
   ```python
   def get_all_with_timeout_handling(start, end):
       all_nodes = []
       scroll_id = None
       while True:
           result = client.get_conversion_report(start, end, scroll_id)
           all_nodes.extend(result["nodes"])
           if not result["pageInfo"]["hasNextPage"]:
               break
           # IMPORTANTE: scrollId expira em 30s
           scroll_id = result["pageInfo"]["scrollId"]
           # Processar antes da próxima requisição
           time.sleep(1)
       return all_nodes
   ```

3. Criar exemplo de uso do `validatedReport`

## 🎯 Conclusão

A documentação oficial da Shopee Affiliate API está **desatualizada** em relação ao schema atual. Os principais problemas encontrados foram:

1. **Nomes de campos incorretos** (`productName` vs `itemName`)
2. **Estrutura hierárquica não documentada** (`nodes.orders.items`)
3. **Campos deprecated ainda documentados**
4. **Novos endpoints não mencionados**

Recomenda-se usar **introspecção GraphQL** para validar campos antes de implementar em produção.
