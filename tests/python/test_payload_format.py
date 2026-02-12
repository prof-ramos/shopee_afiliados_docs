#!/usr/bin/env python3
"""
Verifica formato de payload da API Shopee Affiliate.
"""

import hashlib
import json
import time

app_id = '18360190851'
app_secret = 'EX4IKYDSUTTBJQRCCL63KCHU66HCOJ3C'
timestamp = int(time.time())

# Payload como Python gera
payload_python = {
    "query": "query shopeeOfferV2 { keyword: \"roupas\", sortType: 2, page: 1, limit: 5 }"
}

sign_factor_python = f'{app_id}{timestamp}{payload_python}{app_secret}'
signature_python = hashlib.sha256(sign_factor_python.encode()).hexdigest()

print("=== Python (json.dumps) ===")
print(f"Sign factor: {sign_factor_python}")
print(f"Payload: {payload_python}")
print(f"Signature (hex): {signature_python}")

# Payload esperado no formato final
# A API espera payload no formato JSON sem escape especial
# Com parâmetros separados por espaço, não por vírgula

payload_expected = '{\"query\": \"query shopeeOfferV2 { keyword: \"roupas\", \"sortType\": 2, \"page\": 1, \"limit\": 5 }\"
'
