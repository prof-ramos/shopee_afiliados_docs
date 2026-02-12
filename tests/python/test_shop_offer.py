#!/usr/bin/env python3
"""
Teste do endpoint shopOfferV2 da API Shopee Affiliate.
"""

import sys
import json
sys.path.insert(0, 'examples/python')
from shopee_affiliate_client import ShopeeAffiliateClient

# Configuração
APP_ID = '18360190851'
APP_SECRET = 'EX4IKYDSUTTBJQRCCL63KCHU66HCOJ3C'

def main():
    client = ShopeeAffiliateClient(APP_ID, APP_SECRET)

    print('=== Testando shopOfferV2 ===')
    print('Buscando lojas oficiais...')

    try:
        result = client.get_shop_offers(
            shop_type=[1],  # Official shops
            sort_type=2,    # Maior comissão
            limit=5
        )

        # Verifica se teve erro
        if 'errors' in result:
            print(f'\n❌ ERRO: {result["errors"]}')
            return 1

        data = result.get('data', {}).get('shopOfferV2', {})
        nodes = data.get('nodes', [])
        page_info = data.get('pageInfo', {})

        print(f'\n✅ SUCESSO: Encontradas {len(nodes)} lojas')
        print(f'Página {page_info.get("page")} de {page_info.get("limit")} itens')
        print(f'HasNextPage: {page_info.get("hasNextPage")}')

        print('\nLojas encontradas:')
        for i, s in enumerate(nodes[:5], 1):
            name = s.get('shopName', 'N/A')[:60]
            shop_id = s.get('shopId', 'N/A')
            commission_rate = s.get('commissionRate', 'N/A')
            rating = s.get('ratingStar', 'N/A')
            shop_type = s.get('shopType', 'N/A')
            print(f'  {i}. {name}')
            print(f'     ShopID: {shop_id} | Tipo: {shop_type} | Avaliação: {rating}⭐')
            print(f'     Comissão: {commission_rate}%')

        return 0

    except Exception as e:
        print(f'\n❌ ERRO: {e}')
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
