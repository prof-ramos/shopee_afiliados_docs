#!/usr/bin/env python3
"""
Teste do endpoint shopOfferV2 da API Shopee Affiliate.
"""

import sys
import os
from dotenv import load_dotenv

# Adicionar o diretório examples/python ao path (robusto, independente do CWD)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "examples", "python"))

from shopee_affiliate_client import ShopeeAffiliateClient  # noqa: E402

# Credenciais (via .env)
load_dotenv()
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
SHOPEE_APP_SECRET = os.getenv("SHOPEE_APP_SECRET")

if not SHOPEE_APP_ID or not SHOPEE_APP_SECRET:
    import pytest
    pytest.skip("Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET em um .env (veja .env.example)")

def test_shop_offer_v2():
    """Testa o endpoint shopOfferV2 com diferentes parâmetros."""

    print("=" * 60)
    print("TESTE: shopOfferV2")
    print("=" * 60)

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)

    # Teste 1: Busca por shop_type (Official shops)
    print("\n[1] Busca lojas oficiais (shopType=[1])...")
    try:
        result = client.get_shop_offers(
            shop_type=[1],  # Official shops
            sort_type=2,  # Maior comissão
            page=1,
            limit=3
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopOfferV2", {})
        nodes = data.get("nodes", [])
        page_info = data.get("pageInfo", {})

        print(f"   OK: {len(nodes)} lojas encontradas")
        print(f"   Page: {page_info.get('page')}, HasNext: {page_info.get('hasNextPage')}")

        for i, shop in enumerate(nodes, 1):
            print(f"   {i}. {shop.get('shopName')} - {shop.get('shopType')} - {shop.get('commissionRate')}%")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 2: Busca por shop_type (Preferred shops)
    print("\n[2] Busca lojas preferidas (shopType=[2])...")
    try:
        result = client.get_shop_offers(
            shop_type=[2],  # Preferred shops
            sort_type=2,
            limit=3
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopOfferV2", {})
        nodes = data.get("nodes", [])

        print(f"   OK: {len(nodes)} lojas encontradas")

        for i, shop in enumerate(nodes, 1):
            print(f"   {i}. {shop.get('shopName')}")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 3: Busca por keyword
    print("\n[3] Busca por keyword 'nike'...")
    try:
        result = client.get_shop_offers(
            keyword="nike",
            sort_type=2,
            limit=3
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopOfferV2", {})
        nodes = data.get("nodes", [])

        print(f"   OK: {len(nodes)} lojas encontradas")

        for i, shop in enumerate(nodes, 1):
            print(f"   {i}. {shop.get('shopName')} - ShopID: {shop.get('shopId')}")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 4: Busca sem filtros
    print("\n[4] Busca sem filtros (todas lojas)...")
    try:
        result = client.get_shop_offers(
            sort_type=1,  # latest
            limit=3
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopOfferV2", {})
        nodes = data.get("nodes", [])

        print(f"   OK: {len(nodes)} lojas encontradas")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 5: Verificar campos retornados
    print("\n[5] Verificando campos retornados...")
    required_fields = [
        'commissionRate', 'imageUrl', 'offerLink', 'originalLink',
        'shopId', 'shopName', 'ratingStar', 'shopType',
        'remainingBudget', 'periodStartTime', 'periodEndTime'
    ]

    try:
        result = client.get_shop_offers(
            shop_type=[1, 2],  # Official + Preferred
            limit=1
        )

        data = result.get("data", {}).get("shopOfferV2", {})
        nodes = data.get("nodes", [])

        if nodes:
            shop = nodes[0]
            missing_fields = [f for f in required_fields if f not in shop]
            if missing_fields:
                print(f"   AVISO: Campos faltando: {missing_fields}")
            else:
                print("   OK: Todos os campos requeridos estão presentes")
        else:
            print("   INFO: Nenhuma loja retornada para verificação")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 6: Testar isKeySeller
    print("\n[6] Testando isKeySeller=true...")
    try:
        result = client.get_shop_offers(
            is_key_seller=True,
            limit=3
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopOfferV2", {})
        nodes = data.get("nodes", [])

        print(f"   OK: {len(nodes)} key sellers encontradas")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 7: Testar múltiplos shop_type
    print("\n[7] Testando múltiplos shopType [1, 2, 4]...")
    try:
        result = client.get_shop_offers(
            shop_type=[1, 2, 4],  # Official + Preferred + Preferred Plus
            limit=3
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopOfferV2", {})
        nodes = data.get("nodes", [])

        print(f"   OK: {len(nodes)} lojas encontradas")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    print("\n" + "=" * 60)
    print("TESTE shopOfferV2 CONCLUÍDO COM SUCESSO")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_shop_offer_v2()
    sys.exit(0 if success else 1)
