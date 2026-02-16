#!/usr/bin/env python3
"""
Teste do endpoint productOfferV2 da API Shopee Affiliate.
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
        "Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET em um .env (veja .env.example)"
    )


def main():
    client = ShopeeAffiliateClient(APP_ID, APP_SECRET)

    print("=== Testando productOfferV2 ===")
    print('Buscando produtos com keyword="celular"...')

    try:
        result = client.get_product_offers(
            keyword="celular",
            sort_type=5,  # Maior comissão
            limit=5,
        )

        # Verifica se teve erro
        if "errors" in result:
            print(f"\n❌ ERRO: {result['errors']}")
            return 1

        data = result.get("data", {}).get("productOfferV2", {})
        nodes = data.get("nodes", [])
        page_info = data.get("pageInfo", {})

        print(f"\n✅ SUCESSO: Encontrados {len(nodes)} produtos")
        print(f"Página {page_info.get('page')} de {page_info.get('limit')} itens")
        print(f"HasNextPage: {page_info.get('hasNextPage')}")

        print("\nProdutos encontrados:")
        for i, p in enumerate(nodes[:5], 1):
            name = p.get("productName", "N/A")[:60]
            price = p.get("price", "N/A")
            commission = p.get("commission", "N/A")
            commission_rate = p.get("commissionRate", "N/A")
            shop = p.get("shopName", "N/A")
            print(f"  {i}. {name}")
            print(f"     Preço: {price} | Comissão: {commission} ({commission_rate}%)")
            print(f"     Loja: {shop}")

        return 0

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
