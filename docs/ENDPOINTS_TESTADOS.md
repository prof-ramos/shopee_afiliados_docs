# Endpoints 100% testados e funcionais (este repo)

Este documento lista **apenas** os endpoints cobertos pela implementação atual do cliente e pela suíte de integração `scripts/run_all_tests.py`.

## ✅ Lista de endpoints testados

| Método (Python) | Endpoint GraphQL | Template | Status |
|---|---|---|---|
| `get_shopee_offers()` | `shopeeOfferV2` | `src/shopee_affiliate/graphql/shopeeOfferV2.graphql` | ✅ OK |
| `get_shop_offers()` | `shopOfferV2` | `src/shopee_affiliate/graphql/shopOfferV2.graphql` | ✅ OK |
| `get_product_offers()` | `productOfferV2` | `src/shopee_affiliate/graphql/productOfferV2.graphql` | ✅ OK |
| `generate_short_link()` | `generateShortLink` | `src/shopee_affiliate/graphql/generateShortLink.graphql` | ✅ OK |
| `get_conversion_report()` | `conversionReport` | `src/shopee_affiliate/graphql/conversionReport.graphql` | ✅ OK *(pode retornar vazio dependendo da conta/período)* |

## ♻️ Helpers de performance (mesmo endpoint)

| Método (Python) | Descrição |
|---|---|
| `iter_conversion_report_pages()` | Itera página a página (stream) sem acumular tudo em memória |
| `iter_conversion_report_orders()` | Itera `orders` “achatados” a partir das páginas |

## Observações importantes

- A API pode ter **outros endpoints** no Playground (ex.: `validatedReport`). Eles **não** são garantidos por este repo enquanto não forem implementados e adicionados ao runner.
- `conversionReport` pode retornar `nodes=[]` dependendo do período e do estado da conta — isso não significa falha do client.
