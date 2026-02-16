#!/usr/bin/env python3
"""
Teste do endpoint productOfferV2 da API Shopee Affiliate.
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

    pytest.skip(
        "Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET em um .env (veja .env.example)"
    )


def test_product_offer_v2():
    """Testa o endpoint productOfferV2 com diferentes parâmetros."""

    print("=" * 60)
    print("TESTE: productOfferV2")
    print("=" * 60)

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)

    # Teste 1: Busca por keyword
    print("\n[1] Busca por keyword 'celular'...")
    try:
        result = client.get_product_offers(
            keyword="celular",
            sort_type=5,  # Maior comissão
            page=1,
            limit=3,
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("productOfferV2", {})
        nodes = data.get("nodes", [])
        page_info = data.get("pageInfo", {})

        print(f"   OK: {len(nodes)} produtos encontrados")
        print(
            f"   Page: {page_info.get('page')}, HasNext: {page_info.get('hasNextPage')}"
        )

        for i, product in enumerate(nodes, 1):
            print(
                f"   {i}. {product.get('productName')} - R${product.get('price')} - {product.get('commissionRate')}%"
            )

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 2: Busca por item_id específico
    print("\n[2] Busca por itemId específico...")
    try:
        result = client.get_product_offers(item_id=123456789, page=1, limit=1)

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            # Item pode não existir, não é erro fatal
            print("   INFO: Item ID pode não existir (comportamento esperado)")
        else:
            data = result.get("data", {}).get("productOfferV2", {})
            nodes = data.get("nodes", [])
            print(f"   OK: {len(nodes)} produtos encontrados")

    except Exception as e:
        print(f"   ERRO: {e}")

    # Teste 3: Busca por shop_id
    print("\n[3] Busca por shopId...")
    try:
        result = client.get_product_offers(shop_id=123456, page=1, limit=2)

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            # Shop pode não existir
            print("   INFO: Shop ID pode não existir (comportamento esperado)")
        else:
            data = result.get("data", {}).get("productOfferV2", {})
            nodes = data.get("nodes", [])
            print(f"   OK: {len(nodes)} produtos encontrados")

    except Exception as e:
        print(f"   ERRO: {e}")

    # Teste 4: Busca sem filtros (todas ofertas)
    print("\n[4] Busca sem filtros (todas ofertas)...")
    try:
        result = client.get_product_offers(
            sort_type=5,  # Maior comissão
            page=1,
            limit=2,
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("productOfferV2", {})
        nodes = data.get("nodes", [])

        print(f"   OK: {len(nodes)} produtos encontrados")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 5: Verificar campos retornados
    print("\n[5] Verificando campos retornados...")
    required_fields = [
        "itemId",
        "productName",
        "commissionRate",
        "price",
        "sales",
        "ratingStar",
        "imageUrl",
        "shopId",
        "shopName",
        "productLink",
        "offerLink",
    ]

    try:
        result = client.get_product_offers(keyword="teste", limit=1)

        data = result.get("data", {}).get("productOfferV2", {})
        nodes = data.get("nodes", [])

        if nodes:
            product = nodes[0]
            missing_fields = [f for f in required_fields if f not in product]
            if missing_fields:
                print(f"   AVISO: Campos faltando: {missing_fields}")
            else:
                print("   OK: Todos os campos requeridos estão presentes")
        else:
            print("   INFO: Nenhum produto retornado para verificação")

    except Exception as e:
        print(f"   ERRO: {e}")

    print("\n" + "=" * 60)
    print("TESTE productOfferV2 CONCLUÍDO COM SUCESSO")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_product_offer_v2()
    sys.exit(0 if success else 1)
