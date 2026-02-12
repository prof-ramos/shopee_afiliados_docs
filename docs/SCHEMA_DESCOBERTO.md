# Schema GraphQL API Shopee Affiliate - Descoberto via Introspecção

**Data**: 12/02/2026
**Método**: Introspecção GraphQL com credenciais válidas

## Query Root (12 endpoints)

| Campo | Tipo | Descrição |
|--------|-------|------------|
| `brandOffer` | - | Ofertas de marcas |
| `shopOfferV2` | - | Ofertas de lojas V2 |
| `shopeeOffer` | - | Ofertas da Shopee (legado?) |
| `shopeeOfferV2` | - | Ofertas da Shopee V2 |
| `productOffer` | - | Ofertas de produtos (legado?) |
| `productOfferV2` | - | Ofertas de produtos V2 |
| `conversionReport` | - | Relatório de conversões |
| `validatedReport` | - | Relatório validado (NOVO) |
| `checkAffiliateId` | - | Verificar ID de afiliado |
| `partnerOrderReport` | - | Relatório de pedidos de parceiro (NOVO) |
| `listItemFeeds` | - | Listar feeds de itens (NOVO) |
| `getItemFeedData` | - | Obter dados de feed de itens (NOVO) |

## conversionReport Schema (CORRIGIDO)

### Importante
- **Limite temporal**: Apenas últimos 3 meses (erro 11001)
- **Estrutura**: `nodes` contém um campo `orders` (não campos diretos)
- **Paginação**: Usa `scrollId` com expiração de 30 segundos

### Tipo: ConversionReportOrder (4 campos)

| Campo | Tipo | Descrição |
|-------|-------|------------|
| `orderId` | String! | ID do pedido |
| `shopType` | ShopType (ENUM) | Tipo da loja |
| `orderStatus` | DisplayOrderStatus (ENUM) | Status do pedido |
| `items` | [ConversionReportOrderItem] | Lista de itens do pedido |

### Tipo: ConversionReportOrderItem (33 campos)

| Campo | Tipo | Descrição | Nota |
|-------|-------|------------|-------|
| `shopId` | Int64 | ID da loja | |
| `shopName` | String | Nome da loja | |
| `completeTime` | Int64 | Timestamp de conclusão | |
| `promotionId` | String | ID da promoção | |
| `modelId` | Int64 | ID do modelo | |
| `itemId` | Int64 | ID do item | ⭐ Use este, não `productName` |
| `itemName` | String | Nome do item | ⭐ Use este, não `productName` |
| `itemPrice` | String | Preço do item | |
| `displayItemStatus` | String | Status do item exibido | |
| `actualAmount` | String | Valor atual | |
| `refundAmount` | String | Valor reembolsado | |
| `qty` | Int | Quantidade | |
| `imageUrl` | String | URL da imagem | |
| `itemCommission` | String | Comissão do item | ⚠️ Deprecated |
| `grossBrandCommission` | String | Comissão bruta da marca | ⚠️ Deprecated |
| `itemTotalCommission` | String | Comissão total do item | ⭐ Use este |
| `itemSellerCommission` | String | Comissão do vendedor | |
| `itemSellerCommissionRate` | String | Taxa de comissão do vendedor | |
| `itemShopeeCommissionCapped` | String | Comissão da Shopee capped | |
| `itemShopeeCommissionRate` | String | Taxa de comissão da Shopee | |
| `itemNotes` | String | Notas do item | |
| `categoryLv1Name` | String | Categoria nível 1 | ⚠️ Deprecated |
| `categoryLv2Name` | String | Categoria nível 2 | ⚠️ Deprecated |
| `categoryLv3Name` | String | Categoria nível 3 | ⚠️ Deprecated |
| `globalCategoryLv1Name` | String | Categoria global nível 1 | ⭐ Use este |
| `globalCategoryLv2Name` | String | Categoria global nível 2 | ⭐ Use este |
| `globalCategoryLv3Name` | String | Categoria global nível 3 | ⭐ Use este |
| `fraudStatus` | String | Status de fraude | |
| `fraudReason` | String | Motivo da fraude | |
| `attributionType` | String | Tipo de atribuição | |
| `channelType` | String | Tipo de canal | |
| `campaignPartnerName` | String | Nome do parceiro da campanha | |
| `campaignType` | String | Tipo de campanha | |

### Query Correta para conversionReport

```graphql
query {
  conversionReport(
    purchaseTimeStart: 1738362000  # Unix timestamp
    purchaseTimeEnd: 1738966800       # Unix timestamp
    scrollId: "abc123"              # Opcional, da página anterior
    limit: 500                        # Máx 500
  ) {
    nodes {
      orders {
        orderId
        shopType
        orderStatus
        items {
          itemId
          itemName                          # Use este campo
          itemTotalCommission               # Use este campo
          itemPrice
          shopId
          shopName
          qty
          globalCategoryLv1Name
          globalCategoryLv2Name
          globalCategoryLv3Name
        }
      }
    }
    pageInfo {
      limit
      hasNextPage
      scrollId
    }
  }
}
```

## Diferenças da Documentação Oficial

### Campos incorretos na docs:
- ❌ `productName` → ✅ `itemName`
- ❌ `commissionAmount` → ✅ `itemTotalCommission`
- ❌ Campos diretos em `nodes` → ✅ Use `nodes.orders.items`
- ❌ `page` parameter → ❌ Não suportado

### Campos não documentados (novos):
- ✅ `validatedReport` endpoint
- ✅ `partnerOrderReport` endpoint
- ✅ `listItemFeeds` endpoint
- ✅ `getItemFeedData` endpoint
- ✅ `brandOffer` endpoint
- ✅ `items` dentro de `orders`
- ✅ `globalCategory*` fields (versão não-deprecated)

## Enums Descobertos

### ShopType
Valores possíveis para tipo de loja.

### DisplayOrderStatus
Valores possíveis para status do pedido exibido.

## Mutation Disponível

### generateShortLink
```graphql
mutation {
  generateShortLink(
    input: {
      originUrl: "https://shopee.com.br/produto"
      subIds: ["s1", "s2"]  # Array de strings, max 5
    }
  ) {
    shortLink
  }
}
```

## Notas Importantes

1. **Limite de 3 meses**: `conversionReport` só retorna dados dos últimos 3 meses
2. **scrollId expira em 30s**: Use rapidamente ou perde a paginação
3. **Campos deprecated**: Evite `categoryLv*Name`, `itemCommission`, `grossBrandCommission`
4. **Sem parâmetro page**: `conversionReport` não suporta paginação por número, apenas scrollId
