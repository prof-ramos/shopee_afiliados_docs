"""Introspecção GraphQL do campo partnerOrderReport.

Executa: python tests/introspect_partner_order.py
"""
import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from shopee_affiliate import ShopeeAffiliateClient
from dotenv import load_dotenv

load_dotenv()

# Introspection query para partnerOrderReport
INTROSPECTION_QUERY = """
query {
  __type(name: "Query") {
    fields {
      name
      args {
        name
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
      type {
        name
        kind
        fields {
          name
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
  }
}
"""

PARTNER_ORDER_INTROSPECTION = """
query {
  __schema {
    queryType {
      fields {
        name
        args {
          name
          type {
            name
            kind
            ofType {
              name
            }
          }
        }
        type {
          name
          fields {
            name
            type {
              name
              kind
              ofType {
                name
                kind
                fields {
                  name
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

# Query mais direcionada para partnerOrderReport
FOCUSED_INTROSPECTION = """
query GetPartnerOrderReportType {
  __type(name: "Query") {
    fields {
      name
      args {
        name
        type {
          name
        }
      }
    }
  }
}
"""

QUERY_TEST = """
query {
  partnerOrderReport(
    purchaseTimeStart: 1700000000
    purchaseTimeEnd: 1700000000
    limit: 1
  ) {
    nodes {
      __typename
    }
  }
}
"""


def introspect_partner_order():
    """Investiga a estrutura de partnerOrderReport."""
    client = ShopeeAffiliateClient(
        app_id=os.getenv("SHOPEE_APP_ID", ""),
        app_secret=os.getenv("SHOPEE_APP_SECRET", ""),
    )

    print("=" * 60)
    print("INTROSPECÇÃO: partnerOrderReport")
    print("=" * 60)

    # Primeiro, tentar uma query simples para ver a estrutura
    print("\n1. Testando query simples...")
    try:
        result = client._request(QUERY_TEST)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro na query simples: {e}")

    # Tentar introspecção completa
    print("\n2. Introspecção do schema Query...")
    try:
        result = client._request(INTROSPECTION_QUERY)
        # Encontrar partnerOrderReport
        query_type = result.get("data", {}).get("__type", {})
        fields = query_type.get("fields", [])

        for field in fields:
            if field["name"] == "partnerOrderReport":
                print("\n" + "=" * 60)
                print("PARTNER ORDER REPORT ENCONTRADO!")
                print("=" * 60)
                print(json.dumps(field, indent=2, ensure_ascii=False))

                # Analisar os argumentos
                print("\n" + "-" * 60)
                print("ARGUMENTOS:")
                print("-" * 60)
                for arg in field.get("args", []):
                    print(f"  - {arg['name']}: {arg['type'].get('name', 'N/A')}")

                # Analisar o tipo de retorno
                print("\n" + "-" * 60)
                print("TIPO DE RETORNO:")
                print("-" * 60)
                return_type = field.get("type", {})
                print(f"  Nome: {return_type.get('name', 'N/A')}")
                print(f"  Kind: {return_type.get('kind', 'N/A')}")

                if return_type.get("fields"):
                    print("\n  CAMPOS:")
                    for f in return_type.get("fields", []):
                        print(f"    - {f['name']}: {f['type'].get('name', 'N/A')}")

                return field
    except Exception as e:
        print(f"Erro na introspecção: {e}")

    return None


if __name__ == "__main__":
    introspect_partner_order()
