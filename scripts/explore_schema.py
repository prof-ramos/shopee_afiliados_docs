#!/usr/bin/env python3
"""
Script de exploração de schema GraphQL da API Shopee Affiliate.

Usa introspecção para descobrir campos disponíveis nos endpoints.
"""

import json
import sys
import os
import time

# Import do client (preferencial: módulo instalado; fallback: examples/python)
try:
    from shopee_affiliate_client import ShopeeAffiliateClient
except ModuleNotFoundError:
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, os.path.join(ROOT, "examples", "python"))
    from shopee_affiliate_client import ShopeeAffiliateClient

from dotenv import load_dotenv

# Carregar credenciais
load_dotenv()
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
# aceita alias
SHOPEE_APP_SECRET = os.getenv("SHOPEE_APP_SECRET") or os.getenv("SHOPEE_SECRET")


def introspect_conversion_report():
    """Testa diferentes campos para descobrir o schema correto de conversionReport."""

    print("=" * 70)
    print("EXPLORANDO SCHEMA: conversionReport")
    print("=" * 70)

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)

    now = int(time.time())
    week_ago = now - (7 * 24 * 60 * 60)

    # Teste 1: Query com o campo "orders" (sugerido no erro anterior)
    print("\n[1] Testando com campo 'orders' (últimos 7 dias)...")
    query1 = f"""
    query {{
      conversionReport(
        purchaseTimeStart: {week_ago}
        purchaseTimeEnd: {now}
        limit: 5
      ) {{
        nodes {{
          __typename
        }}
        pageInfo {{
          limit
          hasNextPage
          scrollId
        }}
      }}
    }}
    """

    try:
        result = client._request(query1)
        print("   Resultado:", json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"   Erro: {e}")

    # Teste 2: Query com campo orders e seus subcampos
    print("\n[2] Testando com campo 'orders' e subcampos...")
    query2 = f"""
    query {{
      conversionReport(
        purchaseTimeStart: {week_ago}
        purchaseTimeEnd: {now}
        limit: 5
      ) {{
        nodes {{
          __typename
          orders {{
            orderId
            shopType
            orderStatus
          }}
        }}
        pageInfo {{
          limit
          hasNextPage
          scrollId
        }}
      }}
    }}
    """

    try:
        result = client._request(query2)
        if "errors" in result:
            print("   Erros encontrados:")
            for err in result["errors"]:
                print(f"   - {err.get('message', 'Unknown error')}")
        else:
            print("   Resultado:", json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"   Erro: {e}")

    # Teste 3: Introspecção completa de ConversionReportOrder
    print("\n[3] Introspecção completa de ConversionReportOrder...")
    introspection_query = """
    query {
      __type(name: "ConversionReportOrder") {
        name
        fields {
          name
          description
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
    """

    try:
        result = client._request(introspection_query)
        if "errors" in result:
            print("   Erros na introspecção:")
            for err in result["errors"]:
                print(f"   - {err.get('message', 'Unknown error')}")
        else:
            type_info = result.get("data", {}).get("__type", {})
            if type_info:
                print(f"   Tipo: {type_info.get('name')}")
                fields = type_info.get("fields", [])
                print(f"   Campos ({len(fields)}):")
                for field in fields:
                    type_name = field.get("type", {}).get("name") or field.get(
                        "type", {}
                    ).get("ofType", {}).get("name", "Unknown")
                    desc = field.get("description", "")
                    print(
                        f"   - {field.get('name')}: {type_name}"
                        + (f" // {desc}" if desc else "")
                    )
            else:
                print("   Tipo não encontrado")
    except Exception as e:
        print(f"   Erro: {e}")

    # Teste 4: Introspecção de ConversionReportOrderItem
    print("\n[4] Introspecção de ConversionReportOrderItem...")
    introspection_query2 = """
    query {
      __type(name: "ConversionReportOrderItem") {
        name
        fields {
          name
          description
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
    """

    try:
        result = client._request(introspection_query2)
        if "errors" in result:
            print("   Erros na introspecção:")
            for err in result["errors"]:
                print(f"   - {err.get('message', 'Unknown error')}")
        else:
            type_info = result.get("data", {}).get("__type", {})
            if type_info:
                print(f"   Tipo: {type_info.get('name')}")
                fields = type_info.get("fields", [])
                print(f"   Campos ({len(fields)}):")
                for field in fields:
                    type_name = field.get("type", {}).get("name") or field.get(
                        "type", {}
                    ).get("ofType", {}).get("name", "Unknown")
                    desc = field.get("description", "")
                    print(
                        f"   - {field.get('name')}: {type_name}"
                        + (f" // {desc}" if desc else "")
                    )
            else:
                print("   Tipo não encontrado")
    except Exception as e:
        print(f"   Erro: {e}")

    # Teste 5: Query real com dados
    print("\n[5] Query real para obter dados de conversão...")
    query5 = f"""
    query {{
      conversionReport(
        purchaseTimeStart: {week_ago}
        purchaseTimeEnd: {now}
        limit: 10
      ) {{
        nodes {{
          orders {{
            orderId
            shopType
            orderStatus
            items {{
              itemId
              productName
              commissionAmount
            }}
          }}
        }}
        pageInfo {{
          limit
          hasNextPage
          scrollId
        }}
      }}
    }}
    """

    try:
        result = client._request(query5)
        if "errors" in result:
            print("   Erros:")
            for err in result["errors"]:
                print(f"   - {err.get('message')}")
        else:
            data = result.get("data", {}).get("conversionReport", {})
            nodes = data.get("nodes", [])
            print(f"   OK: {len(nodes)} conversões retornadas")
            if nodes:
                for i, node in enumerate(nodes[:3], 1):
                    orders = node.get("orders", [])
                    print(f"   Node {i}: {len(orders)} order(s)")
                    for order in orders[:2]:
                        print(
                            f"     - OrderID: {order.get('orderId')}, Status: {order.get('orderStatus')}"
                        )
    except Exception as e:
        print(f"   Erro: {e}")


def introspect_all_query_types():
    """Explora todos os tipos de query disponíveis no schema."""
    print("\n" + "=" * 70)
    print("EXPLORANDO SCHEMA: Tipos de Query")
    print("=" * 70)

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)

    # Introspecção do tipo Query
    print("\n[1] Introspecção do tipo Query (root)...")
    introspection_query = """
    query {
      __type(name: "Query") {
        name
        fields {
          name
          description
          type {
            name
            kind
          }
        }
      }
    }
    """

    try:
        result = client._request(introspection_query)
        if "errors" in result:
            print("   Erros:")
            for err in result["errors"]:
                print(f"   - {err.get('message')}")
        else:
            type_info = result.get("data", {}).get("__type", {})
            if type_info:
                print(f"   Tipo: {type_info.get('name')}")
                fields = type_info.get("fields", [])
                print(f"   Campos disponíveis ({len(fields)}):")
                for field in fields:
                    field_name = field.get("name")
                    field_type = field.get("type", {}).get("name", "Unknown")
                    print(f"   - {field_name}: {field_type}")
            else:
                print("   Tipo não encontrado")
    except Exception as e:
        print(f"   Erro: {e}")


def introspect_product_offer_v2():
    """Explora schema de productOfferV2."""
    print("\n" + "=" * 70)
    print("EXPLORANDO SCHEMA: productOfferV2")
    print("=" * 70)

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)

    # Teste 1: Introspecção do tipo ProductOfferV2Node
    print("\n[1] Introspecção de ProductOfferV2Node...")
    introspection_query = """
    query {
      __type(name: "ProductOfferV2Node") {
        name
        fields {
          name
          description
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
    """

    try:
        result = client._request(introspection_query)
        if "errors" in result:
            print("   Erros:")
            for err in result["errors"]:
                print(f"   - {err.get('message')}")
        else:
            type_info = result.get("data", {}).get("__type", {})
            if type_info:
                print(f"   Tipo: {type_info.get('name')}")
                fields = type_info.get("fields", [])
                print(f"   Campos disponíveis ({len(fields)}):")
                for field in fields:
                    field_name = field.get("name")
                    field_type = field.get("type", {})
                    type_name = field_type.get("name") or field_type.get(
                        "ofType", {}
                    ).get("name", "Unknown")
                    desc = field.get("description", "")
                    print(
                        f"   - {field_name}: {type_name}"
                        + (f" // {desc}" if desc else "")
                    )
            else:
                print("   Tipo não encontrado")
    except Exception as e:
        print(f"   Erro: {e}")

    # Teste 2: Query real para ver estrutura retornada
    print("\n[2] Query real de productOfferV2...")
    query2 = """
    query {
      productOfferV2(
        keyword: "celular"
        sortType: 5
        page: 1
        limit: 2
      ) {
        nodes {
          __typename
        }
        pageInfo {
          page
          limit
        }
      }
    }
    """

    try:
        result = client._request(query2)
        if "errors" in result:
            print("   Erros:")
            for err in result["errors"]:
                print(f"   - {err.get('message')}")
        else:
            print("   OK: Query bem-sucedida")
    except Exception as e:
        print(f"   Erro: {e}")


if __name__ == "__main__":
    if SHOPEE_APP_ID and SHOPEE_APP_SECRET:
        introspect_conversion_report()
        introspect_all_query_types()
        introspect_product_offer_v2()
    else:
        print("ERRO: Credenciais não encontradas no arquivo .env")
        print("Certifique-se de que SHOPEE_APP_ID e SHOPEE_APP_SECRET estão definidos.")
