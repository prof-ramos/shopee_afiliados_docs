"""Shopee Affiliate API client (Brasil).

Este pacote expõe o cliente Python e utilitários de transporte/autenticação.

Import recomendado para uso externo:

    from shopee_affiliate_client import ShopeeAffiliateClient

(o módulo `shopee_affiliate_client` é um wrapper de compatibilidade.)
"""

from .client import ShopeeAffiliateClient

__version__ = "1.0.0"
__all__ = ["ShopeeAffiliateClient"]
