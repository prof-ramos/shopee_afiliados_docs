# API Shopee Affiliate - Introspecção Completa
> Documentação gerada automaticamente via introspecção GraphQL
## Queries

### brandOffer

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| name | `String` | None |
| commissionRateLower | `String` | None |
| commissionRateUpper | `String` | None |
| periodStartTime | `Int` | None |
| periodEndTime | `Int` | None |
| offerStatus | `[OfferStatus!]` | None |
| orderBy | `BrandOfferOrder` | None |
| page | `Int` | None |
| limit | `Int` | None |

**Retorna:** `Unknown!`

---

### checkAffiliateId

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| affiliateId | `Int64!` | None |
| source | `String!` | None |

**Retorna:** `Unknown!`

---

### conversionReport

checkoutId deprecated
conversionStatus deprecated

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| purchaseTimeStart | `Int64` | None |
| purchaseTimeEnd | `Int64` | None |
| completeTimeStart | `Int64` | None |
| completeTimeEnd | `Int64` | None |
| shopName | `String` | None |
| shopId | `Int64` | None |
| shopType | `[ShopType!]` | None |
| conversionId | `Int64` | None |
| conversionStatus | `ConversionStatus` | None |
| checkoutId | `Int64` | None |
| orderId | `String` | None |
| productName | `String` | None |
| productId | `Int64` | None |
| categoryLv1Id | `Int64` | None |
| categoryLv2Id | `Int64` | None |
| categoryLv3Id | `Int64` | None |
| categoryType | `CategoryType` | None |
| orderStatus | `DisplayOrderStatus` | None |
| buyerType | `BuyerType` | None |
| productType | `ProductType` | None |
| fraudStatus | `FraudStatus` | None |
| device | `DeviceType` | None |
| attributionType | `AttributionType` | None |
| campaignPartnerName | `String` | None |
| campaignType | `CampaignType` | None |
| limit | `Int` | None |
| scrollId | `String` | None |

**Retorna:** `Unknown!`

---

### getItemFeedData

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| datafeedId | `String!` | None |
| offset | `Int` | None |
| limit | `Int` | None |

**Retorna:** `Unknown!`

---

### listItemFeeds

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| feedMode | `FeedMode` | None |

**Retorna:** `Unknown!`

---

### partnerOrderReport

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| purchaseTimeStart | `Int64` | None |
| purchaseTimeEnd | `Int64` | None |
| completeTimeStart | `Int64` | None |
| completeTimeEnd | `Int64` | None |
| limit | `Int` | None |
| searchNextToken | `String` | None |

**Retorna:** `Unknown!`

---

### productOffer

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| categoryLv1Id | `Int64` | None |
| categoryLv2Id | `Int64` | None |
| categoryLv3Id | `Int64` | None |
| productName | `String` | None |
| productId | `Int64` | None |
| offerStatus | `[OfferStatus!]` | None |
| shopName | `String` | None |
| priceLower | `String` | None |
| priceUpper | `String` | None |
| commissionRateLower | `String` | None |
| commissionRateUpper | `String` | None |
| orderBy | `ProductOfferOrder` | None |
| page | `Int` | None |
| limit | `Int` | None |

**Retorna:** `Unknown!`

---

### productOfferV2

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| listType | `Int` | None |
| matchId | `Int64` | None |
| keyword | `String` | None |
| sortType | `Int` | None |
| page | `Int` | None |
| limit | `Int` | None |
| itemId | `Int64` | None |
| shopId | `Int64` | None |
| productCatId | `Int` | None |
| isAMSOffer | `Boolean` | None |
| isKeySeller | `Boolean` | None |

**Retorna:** `Unknown!`

---

### shopOfferV2

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| keyword | `String` | None |
| shopType | `[Int!]` | None |
| sortType | `Int` | None |
| sellerCommCoveRatio | `String` | None |
| page | `Int` | None |
| limit | `Int` | None |
| shopId | `Int64` | None |
| isKeySeller | `Boolean` | None |

**Retorna:** `Unknown!`

---

### shopeeOffer

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| name | `String` | None |
| type | `ShopeeOfferType` | None |
| offerStatus | `[OfferStatus!]` | None |
| commissionRateLower | `String` | None |
| commissionRateUpper | `String` | None |
| periodStartTime | `Int` | None |
| periodEndTime | `Int` | None |
| orderBy | `ShopeeOfferOrder` | None |
| page | `Int` | None |
| limit | `Int` | None |

**Retorna:** `Unknown!`

---

### shopeeOfferV2

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| keyword | `String` | None |
| sortType | `Int` | None |
| page | `Int` | None |
| limit | `Int` | None |

**Retorna:** `Unknown!`

---

### validatedReport

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| validationId | `Int64!` | None |
| limit | `Int` | None |
| scrollId | `String` | None |

**Retorna:** `Unknown!`

---

## Mutations

### generateShortLink

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| input | `Unknown!` | None |

**Retorna:**

- `shortLink`: `None`

---

### generateBatchShortLink

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| input | `Unknown!` | None |

**Retorna:**

- `links`: `None`
- `total`: `None`
- `successCount`: `None`

---

### syncAffiliateStatus

**Argumentos:**

| Argumento | Tipo | Descrição |
|-----------|------|-----------|
| affiliateId | `Unknown!` | None |
| action | `Unknown!` | None |
| source | `Unknown!` | None |

**Retorna:**


---

## Tipos e Enums

### Enum: AttributionType

| Valor | Descrição |
|-------|-----------|
| `ORDERED_IN_SAME_SHOP` | None |
| `ORDERED_IN_DIFFERENT_SHOP` | None |

### Enum: BrandOfferOrder

| Valor | Descrição |
|-------|-----------|
| `NEWEST` | None |
| `HIGEST_COMMISSION_RATE` | None |
| `ENDING_SOON` | None |

### Enum: BuyerType

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `NEW` | None |
| `EXISTING` | None |

### Enum: CampaignType

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `SELLER_OPEN_CAMPAIGN` | None |
| `SELLER_TARGET_CAMPAIGN` | None |
| `MCN_CAMPAIGN` | None |
| `NON_SELLER_CAMPAIGN` | None |

### Enum: CategoryType

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `MP` | None |
| `DP` | None |

### Enum: ConversionStatus

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `PENDING` | None |
| `COMPLETED` | None |
| `CANCELLED` | None |

### Enum: DeltaDataUpdateType

| Valor | Descrição |
|-------|-----------|
| `UNKNOWN` | None |
| `NEW` | None |
| `UPDATE` | None |
| `DELETE` | None |

### Enum: DeviceType

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `APP` | None |
| `WEB` | None |

### Enum: DisplayItemStatus

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `TO_BE_COMPLETED` | None |
| `COMPLETED` | None |
| `CANCEL` | None |
| `COMPLETED_PARTIAL_REFUNDED` | None |

### Enum: DisplayOrderStatus

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `UNPAID` | None |
| `PENDING` | None |
| `COMPLETED` | None |
| `CANCELLED` | None |

### Enum: FeedMode

| Valor | Descrição |
|-------|-----------|
| `FULL` | None |
| `DELTA` | None |

### Enum: FraudStatus

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `UNVERIFIED` | None |
| `VERIFIED` | None |
| `FRAUD` | None |

### Enum: OfferStatus

| Valor | Descrição |
|-------|-----------|
| `ONGOING` | None |
| `UPCOMING` | None |
| `ENDED` | None |
| `TERMINATED` | None |
| `PAUSED` | None |

### Enum: OfferType

| Valor | Descrição |
|-------|-----------|
| `SHOPEE` | None |
| `PRODUCT` | None |
| `BRAND` | None |

### Enum: ProductOfferOrder

| Valor | Descrição |
|-------|-----------|
| `HIGHEST_COMMISSION_RATE` | None |

### Enum: ProductType

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `MP` | None |
| `DP` | None |

### Enum: RateUnit

| Valor | Descrição |
|-------|-----------|
| `PERCENT` | None |
| `DECIMAL` | None |

### Enum: ShopType

| Valor | Descrição |
|-------|-----------|
| `None` | None |
| `ALL` | None |
| `SHOPEE_MALL_CB` | None |
| `SHOPEE_MALL_NON_CB` | None |
| `C2C_CB` | None |
| `C2C_NON_CB` | None |
| `PREFERRED_CB` | None |
| `PREFERRED_NON_CB` | None |

### Enum: ShopeeOfferOrder

| Valor | Descrição |
|-------|-----------|
| `NEWEST` | None |
| `HIGEST_COMMISSION_RATE` | None |
| `ENDING_SOON` | None |

### Enum: ShopeeOfferType

| Valor | Descrição |
|-------|-----------|
| `ALL` | None |
| `HOMEPAGE` | None |
| `CAMPAIGN` | None |
| `SHOP` | None |
| `CATEGORY` | None |

### Enum: __DirectiveLocation

A Directive can be adjacent to many parts of the GraphQL language, a
__DirectiveLocation describes one such possible adjacencies.

| Valor | Descrição |
|-------|-----------|
| `QUERY` | Location adjacent to a query operation. |
| `MUTATION` | Location adjacent to a mutation operation. |
| `SUBSCRIPTION` | Location adjacent to a subscription operation. |
| `FIELD` | Location adjacent to a field. |
| `FRAGMENT_DEFINITION` | Location adjacent to a fragment definition. |
| `FRAGMENT_SPREAD` | Location adjacent to a fragment spread. |
| `INLINE_FRAGMENT` | Location adjacent to an inline fragment. |
| `SCHEMA` | Location adjacent to a schema definition. |
| `SCALAR` | Location adjacent to a scalar definition. |
| `OBJECT` | Location adjacent to an object type definition. |
| `FIELD_DEFINITION` | Location adjacent to a field definition. |
| `ARGUMENT_DEFINITION` | Location adjacent to an argument definition. |
| `INTERFACE` | Location adjacent to an interface definition. |
| `UNION` | Location adjacent to a union definition. |
| `ENUM` | Location adjacent to an enum definition. |
| `ENUM_VALUE` | Location adjacent to an enum value definition. |
| `INPUT_OBJECT` | Location adjacent to an input object type definition. |
| `INPUT_FIELD_DEFINITION` | Location adjacent to an input object field definition. |

### Enum: __TypeKind

An enum describing what kind of type a given `__Type` is.

| Valor | Descrição |
|-------|-----------|
| `SCALAR` | Indicates this type is a scalar. |
| `OBJECT` | Indicates this type is an object. `fields` and `interfaces` are valid fields. |
| `INTERFACE` | Indicates this type is an interface. `fields` and `possibleTypes` are valid fields. |
| `UNION` | Indicates this type is a union. `possibleTypes` is a valid field. |
| `ENUM` | Indicates this type is an enum. `enumValues` is a valid field. |
| `INPUT_OBJECT` | Indicates this type is an input object. `inputFields` is a valid field. |
| `LIST` | Indicates this type is a list. `ofType` is a valid field. |
| `NON_NULL` | Indicates this type is a non-null. `ofType` is a valid field. |

