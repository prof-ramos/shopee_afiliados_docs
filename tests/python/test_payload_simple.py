#!/usr/bin/env python3
"""
Testa formato de payload da API Shopee Affiliate.
"""

import json
import hashlib
import time

# Para este teste de assinatura, qualquer valor serve.
# Se você tiver .env configurado, ele usa suas credenciais; caso contrário usa dummy.
import os
from dotenv import load_dotenv

load_dotenv()
app_id = os.getenv("SHOPEE_APP_ID", "DUMMY_APP_ID")
app_secret = os.getenv("SHOPEE_APP_SECRET", "DUMMY_APP_SECRET")
timestamp = int(time.time())

# Payload Python (com json.dumps)
payload_python = {
    "query": "query shopeeOfferV2 { keyword: \"roupas\", sortType: 2, page: 1, limit: 5 }"
}

sign_factor_python = f'{app_id}{timestamp}{payload_python}{app_secret}'
signature_python = hashlib.sha256(sign_factor_python.encode()).hexdigest()

print('=== Python (json.dumps) ===')
print(f'Payload: {payload_python}')
print(f'Sign factor: {sign_factor_python}')
print(f'Signature (hex): {signature_python}')

print()
print('Esperado pela API (formato com separadores por espaço):')
expected_payload_api = '{"query": "query shopeeOfferV2 { keyword: \"roupas\", \"sortType\": 2, \"page\": 1, \"limit\": 5 }"}'
print(f'Formato esperado: {expected_payload_api}')
print()
