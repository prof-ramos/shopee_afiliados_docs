#!/usr/bin/env python3
"""
Teste do endpoint generateShortLink da API Shopee Affiliate.
"""

import sys
import os
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

    pytest.skip("Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET em um .env (veja .env.example)", allow_module_level=True)


def test_generate_short_link():
    """Testa o endpoint generateShortLink com diferentes parâmetros."""

    print("=" * 60)
    print("TESTE: generateShortLink")
    print("=" * 60)

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)

    # Teste 1: Link básico sem subIds
    print("\n[1] Gerar link básico (sem subIds)...")
    try:
        test_url = "https://shopee.com.br/product-test-123.123"
        result = client.generate_short_link(origin_url=test_url)

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        short_link = (
            result.get("data", {}).get("generateShortLink", {}).get("shortLink")
        )
        print("   OK: Short link gerado")
        print(f"   URL Original: {test_url}")
        print(f"   Short Link: {short_link}")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 2: Link com subIds (formato curto conforme documentação)
    print("\n[2] Gerar link com subIds...")
    try:
        test_url = "https://shopee.com.br/iphone-capa-456.456"
        sub_ids = ["s1", "s2", "s3"]

        result = client.generate_short_link(origin_url=test_url, sub_ids=sub_ids)

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        short_link = (
            result.get("data", {}).get("generateShortLink", {}).get("shortLink")
        )
        print("   OK: Short link gerado com subIds")
        print(f"   URL Original: {test_url}")
        print(f"   Sub IDs: {sub_ids}")
        print(f"   Short Link: {short_link}")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 3: Link com URL de produto real
    print("\n[3] Gerar link para URL de produto real...")
    try:
        real_url = (
            "https://shopee.com.br/Samsung-Galaxy-A54-5G-128GB-i.258921743.123456789"
        )
        result = client.generate_short_link(origin_url=real_url, sub_ids=["t1"])

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        short_link = (
            result.get("data", {}).get("generateShortLink", {}).get("shortLink")
        )
        print("   OK: Short link gerado para produto real")
        print(f"   Short Link: {short_link}")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 4: Link com número máximo de subIds (5)
    print("\n[4] Gerar link com 5 subIds (máximo permitido)...")
    try:
        test_url = "https://shopee.com.br/test-max-subids.789.789"
        sub_ids_max = ["source1", "source2", "source3", "source4", "source5"]

        result = client.generate_short_link(origin_url=test_url, sub_ids=sub_ids_max)

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        short_link = (
            result.get("data", {}).get("generateShortLink", {}).get("shortLink")
        )
        print("   OK: Short link gerado com 5 subIds")
        print(f"   Sub IDs: {sub_ids_max}")
        print(f"   Short Link: {short_link}")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 5: Link de loja
    print("\n[5] Gerar link de loja...")
    try:
        shop_url = "https://shopee.com.br/nike-oficial"
        result = client.generate_short_link(origin_url=shop_url, sub_ids=["n1"])

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        short_link = (
            result.get("data", {}).get("generateShortLink", {}).get("shortLink")
        )
        print("   OK: Short link de loja gerado")
        print(f"   Short Link: {short_link}")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    # Teste 6: Verificar formato do short link
    print("\n[6] Validando formato do short link...")
    try:
        test_url = "https://shopee.com.br/test-format.123.123"
        result = client.generate_short_link(origin_url=test_url)

        if "errors" in result:
            print(f"   ERRO: {result['errors']}")
            return False

        short_link = (
            result.get("data", {}).get("generateShortLink", {}).get("shortLink")
        )

        # Verificar se é uma URL válida do Shopee
        if short_link and (
            "shope.ee" in short_link
            or "shopee.com.br" in short_link
            or "shp.ee" in short_link
        ):
            print("   OK: Short link tem formato válido")
            print(f"   Short Link: {short_link}")
        else:
            print(f"   AVISO: Short link pode ter formato inesperado: {short_link}")

    except Exception as e:
        print(f"   ERRO: {e}")
        return False

    print("\n" + "=" * 60)
    print("TESTE generateShortLink CONCLUÍDO COM SUCESSO")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_generate_short_link()
    sys.exit(0 if success else 1)
