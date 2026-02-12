from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from .transport import ShopeeAffiliateTransport
from .validators import validate_sub_ids


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
        query = f"""
        query {{
          shopeeOfferV2(
            keyword: {json.dumps(keyword) if keyword else 'null'}
            sortType: {sort_type}
            page: {page}
            limit: {limit}
          ) {{
            nodes {{
              commissionRate
              imageUrl
              offerLink
              originalLink
              offerName
              offerType
              categoryId
              collectionId
              periodStartTime
              periodEndTime
            }}
            pageInfo {{
              page
              limit
              hasNextPage
            }}
          }}
        }}
        """
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
        shop_type_str = str(shop_type) if shop_type else "[]"
        keyword_str = json.dumps(keyword) if keyword else "null"
        shop_id_str = shop_id if shop_id else "null"

        query = f"""
        query {{
          shopOfferV2(
            keyword: {keyword_str}
            shopId: {shop_id_str}
            shopType: {shop_type_str}
            isKeySeller: {str(is_key_seller).lower()}
            sortType: {sort_type}
            page: {page}
            limit: {limit}
          ) {{
            nodes {{
              commissionRate
              imageUrl
              offerLink
              originalLink
              shopId
              shopName
              ratingStar
              shopType
              remainingBudget
              periodStartTime
              periodEndTime
            }}
            pageInfo {{
              page
              limit
              hasNextPage
            }}
          }}
        }}
        """
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
        keyword_str = json.dumps(keyword) if keyword else "null"
        shop_id_str = shop_id if shop_id else "null"
        item_id_str = item_id if item_id else "null"
        product_cat_id_str = product_cat_id if product_cat_id else "null"
        match_id_str = match_id if match_id else "null"

        query = f"""
        query {{
          productOfferV2(
            keyword: {keyword_str}
            shopId: {shop_id_str}
            itemId: {item_id_str}
            productCatId: {product_cat_id_str}
            listType: {list_type}
            matchId: {match_id_str}
            sortType: {sort_type}
            page: {page}
            limit: {limit}
          ) {{
            nodes {{
              itemId
              productName
              commissionRate
              commission
              price
              priceMin
              priceMax
              sales
              ratingStar
              imageUrl
              shopId
              shopName
              shopType
              productLink
              offerLink
            }}
            pageInfo {{
              page
              limit
              hasNextPage
            }}
          }}
        }}
        """
        return self._request(query)

    def get_conversion_report(
        self,
        purchase_time_start: int,
        purchase_time_end: int,
        scroll_id: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        scroll_id_param = f'scrollId: {json.dumps(scroll_id)}' if scroll_id is not None else ""

        query = f"""
        query {{
          conversionReport(
            purchaseTimeStart: {purchase_time_start}
            purchaseTimeEnd: {purchase_time_end}
            {scroll_id_param}
            limit: {limit}
          ) {{
            nodes {{
              orders {{
                orderId
                shopType
                orderStatus
                items {{
                  itemId
                  itemName
                  itemTotalCommission
                  itemPrice
                  shopId
                  shopName
                  qty
                  globalCategoryLv1Name
                  globalCategoryLv2Name
                  globalCategoryLv3Name
                  imageUrl
                  itemSellerCommission
                  itemSellerCommissionRate
                }}
              }}
            }}
            pageInfo {{
              limit
              hasNextPage
              scrollId
            }}
          }}
        }}
        """
        return self._request(query)

    # ============== MUTATIONS ==============

    def generate_short_link(self, origin_url: str, sub_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        validate_sub_ids(sub_ids)

        sub_ids_str = json.dumps(sub_ids) if sub_ids else "[]"
        origin_url_escaped = json.dumps(origin_url)

        query = f"""
        mutation {{
          generateShortLink(
            input: {{
              originUrl: {origin_url_escaped}
              subIds: {sub_ids_str}
            }}
          ) {{
            shortLink
          }}
        }}
        """
        return self._request(query)
