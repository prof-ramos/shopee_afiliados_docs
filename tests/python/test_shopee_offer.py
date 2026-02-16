#!/usr/bin/env python3
"""
Teste do endpoint shopeeOfferV2 da API Shopee Affiliate.
"""

import sys

sys.path.insert(0, "examples/python")
from shopee_affiliate_client import ShopeeAffiliateClient

# Configuração (via .env)
import os
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("SHOPEE_APP_ID")
APP_SECRET = os.getenv("SHOPEE_APP_SECRET")

if not APP_ID or not APP_SECRET:
    import pytest

    pytest.skip(
        allow_module_level=True,
        "Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET em um .env (veja .env.example)"
    )


def main():
    client = ShopeeAffiliateClient(APP_ID, APP_SECRET)

    print("=== Testando shopeeOfferV2 ===")
    print('Buscando ofertas da Shopee com keyword="moda"...')

    try:
        result = client.get_shopee_offers(
            keyword="moda",
            sort_type=2,  # Maior comissão
            limit=5,
        )

        # Verifica se teve erro
        if "errors" in result:
            print(f"\n❌ ERRO: {result['errors']}")
            return 1

        data = result.get("data", {}).get("shopeeOfferV2", {})
        nodes = data.get("nodes", [])
        page_info = data.get("pageInfo", {})

        print(f"\n✅ SUCESSO: Encontradas {len(nodes)} ofertas")
        print(f"Página {page_info.get('page')} de {page_info.get('limit')} itens")
        print(f"HasNextPage: {page_info.get('hasNextPage')}")

        print("\nOfertas encontradas:")
        for i, o in enumerate(nodes[:5], 1):
            name = o.get("offerName", "N/A")[:60]
            offer_type = o.get("offerType", "N/A")
            commission_rate = o.get("commissionRate", "N/A")
            print(f"  {i}. {name}")
            print(f"     Tipo: {offer_type} | Comissão: {commission_rate}%")

        return 0

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
