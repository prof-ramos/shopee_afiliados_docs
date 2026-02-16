#!/usr/bin/env python3
"""
Investigação Fase 1: Introspecção profunda do conversionReport

Objetivo: Descobrir todos os campos disponíveis e identificar possíveis validationId

Executa: python tests/investigate_validation_id.py
"""
import json
import os
import sys
import time
from dotenv import load_dotenv

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from shopee_affiliate import ShopeeAffiliateClient

load_dotenv()

SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID", "")
SHOPEE_APP_SECRET = os.getenv("SHOPEE_APP_SECRET", "")

if not SHOPEE_APP_ID or not SHOPEE_APP_SECRET:
    print("ERRO: Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET")
    sys.exit(1)


def print_section(title: str):
    """Imprime uma seção formatada."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def investigate_conversion_report_type(client: ShopeeAffiliateClient):
    """Investiga a estrutura completa do tipo conversionReport."""
    print_section("FASE 1: INTROSPECÇÃO DO CONVERSIONREPORT")

    # Introspecção do tipo conversionReport
    query = """
    query {
      __type(name: "Query") {
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
                type {
                  name
                  kind
                  ofType {
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
                          fields {
                            name
                            type {
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
          }
        }
      }
    }
    """

    result = client._request(query)

    # Encontrar conversionReport
    query_type = result.get("data", {}).get("__type", {})
    fields = query_type.get("fields", [])

    conversion_report_field = None
    for field in fields:
        if field["name"] == "conversionReport":
            conversion_report_field = field
            break

    if not conversion_report_field:
        print("❌ conversionReport não encontrado!")
        return None

    # Analisar estrutura profunda
    print("✅ conversionReport encontrado!")
    print("\nEstrutura de tipos:")

    # Navegar até o tipo final
    type_info = conversion_report_field.get("type")

    # Atravessar NON_NULL
    while type_info and type_info.get("kind") == "NON_NULL":
        type_info = type_info.get("ofType")

    if type_info and type_info.get("kind") == "OBJECT":
        object_name = type_info.get("name")
        print(f"  Tipo: {object_name}")

        # Buscar campos do objeto
        fields = type_info.get("fields", [])

        print(f"\n  Campos encontrados: {len(fields)}")

        for field in fields:
            field_name = field.get("name")
            field_type = resolve_type(field.get("type"))
            print(f"    - {field_name}: {field_type}")

            # Se tiver campos aninhados, mostrar
            nested_type = field.get("type")
            while nested_type and nested_type.get("kind") in ["NON_NULL", "LIST"]:
                nested_type = nested_type.get("ofType")

            if nested_type and nested_type.get("kind") == "OBJECT":
                nested_fields = nested_type.get("fields", [])
                if nested_fields:
                    print(f"      Subcampos:")
                    for nf in nested_fields[:10]:  # Limitar a 10
                        nf_name = nf.get("name")
                        nf_type = resolve_type(nf.get("type"))
                        print(f"        - {nf_name}: {nf_type}")
                    if len(nested_fields) > 10:
                        print(f"        ... (+{len(nested_fields) - 10} mais)")

    return conversion_report_field


def resolve_type(type_obj: dict) -> str:
    """Resolve o nome do tipo GraphQL."""
    if not type_obj:
        return "Unknown"

    kind = type_obj.get("kind")

    if kind == "NON_NULL":
        return resolve_type(type_obj.get("ofType")) + "!"
    elif kind == "LIST":
        return f"[{resolve_type(type_obj.get('ofType'))}]"
    else:
        return type_obj.get("name", "Unknown")


def get_real_conversion_data(client: ShopeeAffiliateClient):
    """Busca dados reais do conversionReport."""
    print_section("FASE 2: DADOS REAIS DO CONVERSIONREPORT")

    now = int(time.time())
    week_ago = now - (7 * 24 * 60 * 60)

    # Buscar campos disponíveis (apenas os que existem)
    query = """
    query {
      conversionReport(
        purchaseTimeStart: %d
        purchaseTimeEnd: %d
        limit: 1
      ) {
        nodes {
          __typename
          orders {
            __typename
            orderId
            shopType
            orderStatus
            items {
              __typename
              itemId
              itemName
            }
          }
        }
      }
    }
    """ % (week_ago, now)

    result = client._request(query)

    if "errors" in result:
        error = result["errors"][0]
        print(f"❌ ERRO: {error['message']}")
        return None

    data = result.get("data", {}).get("conversionReport", {})
    nodes = data.get("nodes", [])

    if not nodes:
        print("⚠️  Nenhum dado encontrado no período")
        return None

    print(f"✅ {len(nodes)} conversões encontradas")

    # Mostrar estrutura completa
    print("\n📋 Estrutura completa dos dados:")
    print(json.dumps(nodes[0], indent=2, ensure_ascii=False))

    # Extrair possíveis IDs
    print("\n🔍 Possíveis validationId encontrados:")

    for node in nodes:
        orders = node.get("orders", [])

        for order in orders:
            order_id = order.get("orderId")

            print(f"\n  Order:")
            print(f"    orderId: {order_id}")
            print(f"    shopType: {order.get('shopType')}")
            print(f"    orderStatus: {order.get('orderStatus')}")

    return nodes


def test_validation_id_hypotheses(client: ShopeeAffiliateClient, nodes: list):
    """Testa hipóteses sobre validationId."""
    print_section("FASE 3: TESTAR HIPÓTESES")

    if not nodes:
        print("⚠️  Sem dados para testar")
        return

    # Extrair valores para teste
    test_values = []

    for node in nodes:
        orders = node.get("orders", [])
        for order in orders:
            order_id = order.get("orderId")

            if order_id:
                test_values.append(("orderId", order_id))

            break  # Apenas um order para teste
        break

    # Testar cada valor
    results = {}

    for name, value in test_values[:5]:  # Limitar a 5 testes
        print(f"\n🧪 Testando {name} = {value}")

        query = """
        query {
          validatedReport(
            validationId: %s
            limit: 1
          ) {
            nodes {
              __typename
            }
          }
        }
        """ % value

        result = client._request(query)

        if "errors" in result:
            error = result["errors"][0]
            error_msg = error['message']
            error_code = error.get('extensions', {}).get('code', 'N/A')

            print(f"  ❌ ERRO: {error_msg}")
            print(f"  Código: {error_code}")

            results[name] = {"value": value, "status": "error", "message": error_msg}
        else:
            data = result.get("data", {}).get("validatedReport", {})
            nodes = data.get("nodes", [])

            print(f"  ✅ SUCESSO! {len(nodes)} nós retornados")
            print(f"  🎯 ESTE É O CAMPO CORRETO: {name}")

            results[name] = {"value": value, "status": "success", "nodes": len(nodes)}

    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)

    for name, result in results.items():
        status = "✅ SUCESSO" if result["status"] == "success" else "❌ ERRO"
        print(f"{name}: {status}")
        if result["status"] == "error":
            print(f"  Mensagem: {result['message']}")
        else:
            print(f"  Valor: {result['value']}")
            print(f"  Nós: {result['nodes']}")

    return results


def main():
    """Executa todas as fases da investigação."""
    print_section("INVESTIGAÇÃO validationId")
    print("API Shopee Affiliate\n")

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)

    # Fase 1: Introspecção
    investigate_conversion_report_type(client)

    # Fase 2: Dados reais
    nodes = get_real_conversion_data(client)

    # Fase 3: Testar hipóteses
    results = test_validation_id_hypotheses(client, nodes)

    # Conclusão
    print_section("CONCLUSÃO")

    success_found = any(r["status"] == "success" for r in results.values()) if results else False

    if success_found:
        print("🎉 ENCONTRAMOS O validationId CORRETO!")
        print("\nPróximos passos:")
        print("1. Implementar suporte no cliente Python")
        print("2. Adicionar método get_validated_report(validation_id)")
        print("3. Atualizar documentação")
    else:
        print("⚠️  Nenhuma hipótese funcionou")
        print("\nPróximos passos:")
        print("1. Consultar documentação oficial da Shopee")
        print("2. Entrar em contato com o suporte")
        print("3. Considerar usar partnerOrderReport (se disponível)")

    print()


if __name__ == "__main__":
    main()
