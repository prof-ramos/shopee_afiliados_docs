#!/usr/bin/env python3
"""
Teste simples da API Shopee Affiliate
"""

import os
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent / "python"))

from dotenv import load_dotenv
from shopee_affiliate_client import ShopeeAffiliateClient

# Carregar variáveis de ambiente
load_dotenv()

APP_ID = os.getenv("SHOPEE_APP_ID")
APP_SECRET = os.getenv("SHOPEE_APP_SECRET")

if not APP_ID or not APP_SECRET:
    print("❌ Erro: Configure SHOPEE_APP_ID e SHOPEE_APP_SECRET no .env")
    sys.exit(1)

print(f"🔑 AppID: {APP_ID}")
print(f"🔑 Secret: {APP_SECRET[:10]}...")

client = ShopeeAffiliateClient(APP_ID, APP_SECRET)

# Teste 1: Buscar ofertas da Shopee
print("\n📦 Teste 1: Buscar ofertas da Shopee...")
try:
    result = client.get_shopee_offers(limit=3)
    if "errors" in result:
        print(f"❌ Erro na API: {result['errors']}")
    else:
        offers = result["data"]["shopeeOfferV2"]["nodes"]
        print(f"✅ Sucesso! Encontradas {len(offers)} ofertas")
        for i, offer in enumerate(offers, 1):
            print(
                f"   {i}. {offer['offerName'][:50]}... ({offer['commissionRate']}% comissão)"
            )
except Exception as e:
    print(f"❌ Exceção: {e}")

# Teste 2: Gerar link curto
print("\n🔗 Teste 2: Gerar link curto...")
try:
    result = client.generate_short_link(origin_url="https://shopee.com.br/")
    if "errors" in result:
        print(f"❌ Erro na API: {result['errors']}")
    else:
        short_link = result["data"]["generateShortLink"]["shortLink"]
        print(f"✅ Sucesso! Link gerado: {short_link}")
except Exception as e:
    print(f"❌ Exceção: {e}")

print("\n✨ Testes concluídos!")
