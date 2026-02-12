"""Queries/mutations GraphQL centralizadas.

Motivação:
- reduzir f-strings enormes espalhadas no client
- facilitar manutenção quando o schema mudar

As funções aqui retornam strings GraphQL prontas para envio.
"""

from __future__ import annotations

import json
from typing import List, Optional


def q_shopee_offer_v2(*, keyword: Optional[str], sort_type: int, page: int, limit: int) -> str:
    return f"""
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


def q_shop_offer_v2(
    *,
    keyword: Optional[str],
    shop_id: Optional[int],
    shop_type: Optional[List[int]],
    is_key_seller: bool,
    sort_type: int,
    page: int,
    limit: int,
) -> str:
    shop_type_str = str(shop_type) if shop_type else "[]"
    keyword_str = json.dumps(keyword) if keyword else "null"
    shop_id_str = shop_id if shop_id else "null"

    return f"""
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


def q_product_offer_v2(
    *,
    keyword: Optional[str],
    shop_id: Optional[int],
    item_id: Optional[int],
    product_cat_id: Optional[int],
    list_type: int,
    match_id: Optional[int],
    sort_type: int,
    page: int,
    limit: int,
) -> str:
    keyword_str = json.dumps(keyword) if keyword else "null"
    shop_id_str = shop_id if shop_id else "null"
    item_id_str = item_id if item_id else "null"
    product_cat_id_str = product_cat_id if product_cat_id else "null"
    match_id_str = match_id if match_id else "null"

    return f"""
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


def q_conversion_report(
    *,
    purchase_time_start: int,
    purchase_time_end: int,
    scroll_id: Optional[str],
    limit: int,
) -> str:
    scroll_id_param = f"scrollId: {json.dumps(scroll_id)}" if scroll_id is not None else ""

    return f"""
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


def m_generate_short_link(*, origin_url: str, sub_ids: Optional[List[str]]) -> str:
    sub_ids_str = json.dumps(sub_ids) if sub_ids else "[]"
    origin_url_escaped = json.dumps(origin_url)

    return f"""
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
