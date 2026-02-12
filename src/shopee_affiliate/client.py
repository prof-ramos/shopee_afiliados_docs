from __future__ import annotations

from typing import Any, Dict, List, Optional

from .transport import ShopeeAffiliateTransport
from .validators import validate_sub_ids
from . import queries


class ShopeeAffiliateClient:
    """Cliente para API de Afiliados da Shopee Brasil.

    API estável: mantém interface simples e retorna dict (JSON) como a API.
    """

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        *,
        base_url: str = "https://open-api.affiliate.shopee.com.br/graphql",
        timeout_s: float = 30.0,
    ):
        self.transport = ShopeeAffiliateTransport(
            app_id=app_id,
            app_secret=app_secret,
            base_url=base_url,
            timeout_s=timeout_s,
        )

    # ============== low-level ==============

    def _request(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.transport.request(query, variables=variables)

    # ============== QUERIES ==============

    def get_shopee_offers(
        self,
        keyword: Optional[str] = None,
        sort_type: int = 1,
        page: int = 1,
        limit: int = 10,
    ) -> Dict[str, Any]:
        query = queries.q_shopee_offer_v2(
            keyword=keyword,
            sort_type=sort_type,
            page=page,
            limit=limit,
        )
        return self._request(query)

    def get_shop_offers(
        self,
        keyword: Optional[str] = None,
        shop_id: Optional[int] = None,
        shop_type: Optional[List[int]] = None,
        is_key_seller: bool = False,
        sort_type: int = 1,
        page: int = 1,
        limit: int = 10,
    ) -> Dict[str, Any]:
        query = queries.q_shop_offer_v2(
            keyword=keyword,
            shop_id=shop_id,
            shop_type=shop_type,
            is_key_seller=is_key_seller,
            sort_type=sort_type,
            page=page,
            limit=limit,
        )
        return self._request(query)

    def get_product_offers(
        self,
        keyword: Optional[str] = None,
        shop_id: Optional[int] = None,
        item_id: Optional[int] = None,
        product_cat_id: Optional[int] = None,
        list_type: int = 0,
        match_id: Optional[int] = None,
        sort_type: int = 1,
        page: int = 1,
        limit: int = 10,
    ) -> Dict[str, Any]:
        query = queries.q_product_offer_v2(
            keyword=keyword,
            shop_id=shop_id,
            item_id=item_id,
            product_cat_id=product_cat_id,
            list_type=list_type,
            match_id=match_id,
            sort_type=sort_type,
            page=page,
            limit=limit,
        )
        return self._request(query)

    def get_conversion_report(
        self,
        purchase_time_start: int,
        purchase_time_end: int,
        scroll_id: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        query = queries.q_conversion_report(
            purchase_time_start=purchase_time_start,
            purchase_time_end=purchase_time_end,
            scroll_id=scroll_id,
            limit=limit,
        )
        return self._request(query)

    # ============== MUTATIONS ==============

    def generate_short_link(self, origin_url: str, sub_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        validate_sub_ids(sub_ids)

        query = queries.m_generate_short_link(origin_url=origin_url, sub_ids=sub_ids)
        return self._request(query)
