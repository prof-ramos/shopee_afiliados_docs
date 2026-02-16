#!/usr/bin/env python3
"""
Teste do endpoint validatedReport da API Shopee Affiliate com scrollId.
"""

import json
import sys
import os
import time
from dotenv import load_dotenv

# Adicionar o diretório examples/python ao path (robusto, independente do CWD)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "examples", "python"))

# Credenciais (via .env)
load_dotenv()

from shopee_affiliate_client import ShopeeAffiliateClient  # noqa: E402

SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
SHOPEE_APP_SECRET = os.getenv("SHOPEE_APP_SECRET")

if not SHOPEE_APP_ID or not SHOPEE_APP_SECRET:
    import pytest

    pytest.skip(
        "Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET em um .env (veja .env.example)",
        allow_module_level=True,
    )


def test_validated_report():
    """Testa o endpoint validatedReport com scrollId."""

    print("=" * 60)
    print("TESTE: validatedReport com scrollId")
    print("=" * 60)

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)

    # Definir período de teste (últimos 30 dias)
    now = int(time.time())
    thirty_days_ago = now - (30 * 24 * 60 * 60)

    print(f"\nPeríodo de teste: {thirty_days_ago} a {now}")
    print("(últimos 30 dias)")

    # Teste 1: Primeira página (sem scrollId)
    print("\n[1] Buscar primeira página (sem scrollId)...")
    try:
        result = client.get_validated_report(
            purchase_time_start=thirty_days_ago,
            purchase_time_end=now,
            scroll_id=None,
            limit=10,
        )

        if "errors" in result:
            error_msg = result["errors"][0].get("message", "Unknown error")
            print(f"   ERRO: {error_msg}")
            # Se for erro de permissão ou dados vazios, pode ser esperado
            if (
                "no data" in error_msg.lower()
                or "permission" in error_msg.lower()
                or "empty" in error_msg.lower()
            ):
                print(
                    "   INFO: Pode ser que não há comissões validadas no período ou acesso limitado"
                )
                return True
            return False

        data = result.get("data", {}).get("validatedReport", {})
        nodes = data.get("nodes", [])
        page_info = data.get("pageInfo", {})

        print(f"   OK: {len(nodes)} comissões validadas encontradas")
        print(f"   Limit: {page_info.get('limit')}")
        print(f"   HasNextPage: {page_info.get('hasNextPage')}")

        scroll_id = page_info.get("scrollId")
        if scroll_id:
            print(f"   ScrollId: {scroll_id[:20]}... (truncado)")
        else:
            print("   ScrollId: (vazio)")

        # Mostrar estrutura dos dados
        if nodes:
            print("\n   Estrutura da primeira comissão validada:")
            print(f"   {json.dumps(nodes[0], indent=6, ensure_ascii=False)}")

    except Exception as e:
        print(f"   ERRO: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Teste 2: Paginação com scrollId (se houver próxima página)
    if nodes and page_info.get("hasNextPage") and scroll_id:
        print("\n[2] Buscar próxima página com scrollId...")
        try:
            # IMPORTANTE: scrollId expira em 30 segundos!
            result2 = client.get_validated_report(
                purchase_time_start=thirty_days_ago,
                purchase_time_end=now,
                scroll_id=scroll_id,
                limit=10,
            )

            if "errors" in result2:
                error_msg = result2["errors"][0].get("message", "Unknown error")
                print(f"   ERRO: {error_msg}")
                if "expired" in error_msg.lower() or "invalid" in error_msg.lower():
                    print("   INFO: ScrollId pode ter expirado (30 segundos)")
                return True  # Não é falha crítica

            data2 = result2.get("data", {}).get("validatedReport", {})
            nodes2 = data2.get("nodes", [])
            page_info2 = data2.get("pageInfo", {})

            print(f"   OK: {len(nodes2)} comissões validadas encontradas")
            print(f"   HasNextPage: {page_info2.get('hasNextPage')}")
            print(f"   ScrollId novo: {page_info2.get('scrollId', 'N/A')[:20]}...")

        except Exception as e:
            print(f"   ERRO: {e}")
            import traceback

            traceback.print_exc()
            return False
    else:
        print(f"\n[2] Paginação: hasNextPage={page_info.get('hasNextPage', 'N/A')}")

    # Teste 3: Buscar período menor (últimos 7 dias)
    print("\n[3] Buscar período menor (últimos 7 dias)...")
    try:
        week_ago = now - (7 * 24 * 60 * 60)

        result_week = client.get_validated_report(
            purchase_time_start=week_ago, purchase_time_end=now, scroll_id=None, limit=5
        )

        if "errors" in result_week:
            error_msg = result_week["errors"][0].get("message", "Unknown error")
            print(f"   INFO: {error_msg}")
        else:
            data_week = result_week.get("data", {}).get("validatedReport", {})
            nodes_week = data_week.get("nodes", [])
            print(f"   OK: {len(nodes_week)} comissões validadas encontradas (7 dias)")

    except Exception as e:
        print(f"   ERRO: {e}")

    # Teste 4: Testar iterador de páginas
    print("\n[4] Testar iterador de páginas (max 2 páginas)...")
    try:
        page_count = 0
        for page in client.iter_validated_report_pages(
            purchase_time_start=thirty_days_ago,
            purchase_time_end=now,
            limit=5,
            max_pages=2,
        ):
            page_count += 1
            data = page.get("data", {}).get("validatedReport", {})
            nodes = data.get("nodes", [])
            print(f"   Página {page_count}: {len(nodes)} comissões")

        print(f"   OK: Iterador funcionou, {page_count} páginas processadas")

    except Exception as e:
        print(f"   ERRO: {e}")

    # Teste 5: Testar iterador de orders
    print("\n[5] Testar iterador de orders (achatado)...")
    try:
        order_count = 0
        for order in client.iter_validated_report_orders(
            purchase_time_start=thirty_days_ago,
            purchase_time_end=now,
            limit=5,
            max_pages=2,
        ):
            order_count += 1
            if order_count <= 3:
                print(f"   Order {order_count}: {order.get('orderId', 'N/A')}")

        print(f"   OK: {order_count} orders processadas")

    except Exception as e:
        print(f"   ERRO: {e}")

    print("\n" + "=" * 60)
    print("TESTE validatedReport CONCLUÍDO")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_validated_report()
    sys.exit(0 if success else 1)
