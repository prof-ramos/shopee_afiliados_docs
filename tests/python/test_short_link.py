#!/usr/bin/env python3
"""
Teste do endpoint generateShortLink da API Shopee Affiliate.
"""

import sys
import json
sys.path.insert(0, 'examples/python')
from shopee_affiliate_client import ShopeeAffiliateClient

# Configuração (via .env)
import os
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("SHOPEE_APP_ID")
APP_SECRET = os.getenv("SHOPEE_APP_SECRET")

if not APP_ID or not APP_SECRET:
    import pytest
    pytest.skip("Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET em um .env (veja .env.example)")

def main():
    client = ShopeeAffiliateClient(APP_ID, APP_SECRET)

    print('=== Testando generateShortLink ===')

    # URL de exemplo de produto da Shopee
    test_url = 'https://shopee.com.br/product-test-12345'
    
    print(f'Gerando link curto para: {test_url}')

    try:
        # SubIDs devem ser strings numéricas ou alfanuméricas simples
        result = client.generate_short_link(
            origin_url=test_url,
            sub_ids=['12345', '67890']
        )

        # Verifica se teve erro
        if 'errors' in result:
            print(f'\n❌ ERRO: {result["errors"]}')
            return 1

        data = result.get('data', {}).get('generateShortLink', {})
        short_link = data.get('shortLink', '')

        if short_link:
            print(f'\n✅ SUCESSO: Link curto gerado!')
            print(f'   Original: {test_url}')
            print(f'   ShortLink: {short_link}')
        else:
            print('\n⚠️  Resposta vazia ou sem shortLink')
            print(f'   Resposta completa: {json.dumps(result, indent=2, ensure_ascii=False)}')

        return 0

    except Exception as e:
        print(f'\n❌ ERRO: {e}')
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
