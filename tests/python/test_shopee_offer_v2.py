#!/usr/bin/env python3
"""
Teste do endpoint shopeeOfferV2 da API Shopee Affiliate.
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
        allow_module_level=True,
        "Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET em um .env (veja .env.example)"
    )


def test_shopee_offer_v2():
    """Testa o endpoint shopeeOfferV2 com diferentes parâmetros."""

    print("=" * 60)
    print("TESTE: shopeeOfferV2")
    print("=" * 60)

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)

    # Teste 1: Busca por keyword
    print("\n[1] Busca por keyword 'moda'...")
    try:
        result = client.get_shopee_offers(
            keyword="moda",
            sort_type=2,  # Maior comissão
            page=1,
            limit=3,
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopeeOfferV2", {})
        nodes = data.get("nodes", [])
        page_info = data.get("pageInfo", {})

        print(f"   OK: {len(nodes)} ofertas encontradas")
        print(
            f"   Page: {page_info.get('page')}, HasNext: {page_info.get('hasNextPage')}"
        )

        for i, offer in enumerate(nodes, 1):
            print(f"   {i}. {offer.get('offerName')} - {offer.get('commissionRate')}%")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 2: Busca sem keyword (todas ofertas)
    print("\n[2] Busca sem keyword (todas ofertas)...")
    try:
        result = client.get_shopee_offers(
            sort_type=1,  # LATEST_DESC
            page=1,
            limit=3,
        )

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopeeOfferV2", {})
        nodes = data.get("nodes", [])

        print(f"   OK: {len(nodes)} ofertas encontradas")

        for i, offer in enumerate(nodes, 1):
            print(f"   {i}. {offer.get('offerName')}")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 3: Testar diferentes sort_type
    print("\n[3] Testando sort_type=1 (LATEST_DESC)...")
    try:
        result = client.get_shopee_offers(keyword="beleza", sort_type=1, limit=2)

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopeeOfferV2", {})
        nodes = data.get("nodes", [])

        print(f"   OK: {len(nodes)} ofertas encontradas")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    print("\n[4] Testando sort_type=2 (HIGHEST_COMMISSION_DESC)...")
    try:
        result = client.get_shopee_offers(keyword="casa", sort_type=2, limit=2)

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        data = result.get("data", {}).get("shopeeOfferV2", {})
        nodes = data.get("nodes", [])

        print(f"   OK: {len(nodes)} ofertas encontradas")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 5: Verificar campos retornados
    print("\n[5] Verificando campos retornados...")
    required_fields = [
        "commissionRate",
        "imageUrl",
        "offerLink",
        "originalLink",
        "offerName",
        "offerType",
        "categoryId",
        "collectionId",
        "periodStartTime",
        "periodEndTime",
    ]

    try:
        result = client.get_shopee_offers(keyword="teste", limit=1)

        data = result.get("data", {}).get("shopeeOfferV2", {})
        nodes = data.get("nodes", [])

        if nodes:
            offer = nodes[0]
            missing_fields = [f for f in required_fields if f not in offer]
            if missing_fields:
                print(f"   AVISO: Campos faltando: {missing_fields}")
            else:
                print("   OK: Todos os campos requeridos estão presentes")
        else:
            print("   INFO: Nenhuma oferta retornada para verificação")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 6: Paginação
    print("\n[6] Testando paginação...")
    try:
        result = client.get_shopee_offers(keyword="eletronicos", page=1, limit=2)

        data = result.get("data", {}).get("shopeeOfferV2", {})
        page_info = data.get("pageInfo", {})

        if page_info.get("hasNextPage"):
            # Buscar página 2
            result2 = client.get_shopee_offers(keyword="eletronicos", page=2, limit=2)

            data2 = result2.get("data", {}).get("shopeeOfferV2", {})
            nodes2 = data2.get("nodes", [])

            print(f"   OK: Página 2 retornou {len(nodes2)} ofertas")
        else:
            print(
                f"   OK: Paginação funcionando (hasNextPage: {page_info.get('hasNextPage')})"
            )

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    print("\n" + "=" * 60)
    print("TESTE shopeeOfferV2 CONCLUÍDO COM SUCESSO")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_shopee_offer_v2()
    sys.exit(0 if success else 1)
