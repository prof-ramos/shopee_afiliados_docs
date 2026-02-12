"""Wrapper de compatibilidade.

Historicamente este repo expunha a classe `ShopeeAffiliateClient` a partir do módulo
`shopee_affiliate_client.py`.

A implementação canônica agora vive em `shopee_affiliate` (pacote), mas mantemos
este arquivo para não quebrar imports existentes.
"""

from shopee_affiliate import ShopeeAffiliateClient

__all__ = ["ShopeeAffiliateClient"]
