"""Queries/mutations GraphQL centralizadas.

Motivação:
- reduzir f-strings enormes espalhadas no client
- facilitar manutenção quando o schema mudar

As queries/mutations base ficam em `src/shopee_affiliate/graphql/*.graphql`.
As funções aqui carregam e injetam parâmetros de forma segura.
"""

from __future__ import annotations

import json
from importlib import resources
from typing import List, Optional


def _load(name: str) -> str:
    return (
        resources.files("shopee_affiliate.graphql")
        .joinpath(name)
        .read_text(encoding="utf-8")
    )


def _render(template: str, mapping: dict[str, str]) -> str:
    out = template
    for key, value in mapping.items():
        out = out.replace("{{" + key + "}}", value)
    return out


_SHOPEE_OFFER_V2 = _load("shopeeOfferV2.graphql")
_SHOP_OFFER_V2 = _load("shopOfferV2.graphql")
_PRODUCT_OFFER_V2 = _load("productOfferV2.graphql")
_CONVERSION_REPORT = _load("conversionReport.graphql")
_VALIDATED_REPORT = _load("validatedReport.graphql")
_GENERATE_SHORT_LINK = _load("generateShortLink.graphql")


def q_shopee_offer_v2(
    *, keyword: Optional[str], sort_type: int, page: int, limit: int
) -> str:
    return _render(
        _SHOPEE_OFFER_V2,
        {
            "keyword": json.dumps(keyword) if keyword else "null",
            "sortType": str(sort_type),
            "page": str(page),
            "limit": str(limit),
        },
    )


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
    return _render(
        _SHOP_OFFER_V2,
        {
            "keyword": json.dumps(keyword) if keyword else "null",
            "shopId": str(shop_id) if shop_id else "null",
            "shopType": str(shop_type) if shop_type else "[]",
            "isKeySeller": str(is_key_seller).lower(),
            "sortType": str(sort_type),
            "page": str(page),
            "limit": str(limit),
        },
    )


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
    return _render(
        _PRODUCT_OFFER_V2,
        {
            "keyword": json.dumps(keyword) if keyword else "null",
            "shopId": str(shop_id) if shop_id else "null",
            "itemId": str(item_id) if item_id else "null",
            "productCatId": str(product_cat_id) if product_cat_id else "null",
            "listType": str(list_type),
            "matchId": str(match_id) if match_id else "null",
            "sortType": str(sort_type),
            "page": str(page),
            "limit": str(limit),
        },
    )


def q_conversion_report(
    *,
    purchase_time_start: int,
    purchase_time_end: int,
    scroll_id: Optional[str],
    limit: int,
) -> str:
    # Como o `scrollId` é um argumento opcional, injetamos uma linha inteira ou vazio.
    scroll_id_line = (
        f"scrollId: {json.dumps(scroll_id)}" if scroll_id is not None else ""
    )

    return _render(
        _CONVERSION_REPORT,
        {
            "purchaseTimeStart": str(purchase_time_start),
            "purchaseTimeEnd": str(purchase_time_end),
            "scrollIdLine": scroll_id_line,
            "limit": str(limit),
        },
    )


def q_validated_report(
    *,
    purchase_time_start: int,
    purchase_time_end: int,
    scroll_id: Optional[str],
    limit: int,
) -> str:
    # Como o `scrollId` é um argumento opcional, injetamos uma linha inteira ou vazio.
    scroll_id_line = (
        f"scrollId: {json.dumps(scroll_id)}" if scroll_id is not None else ""
    )

    return _render(
        _VALIDATED_REPORT,
        {
            "purchaseTimeStart": str(purchase_time_start),
            "purchaseTimeEnd": str(purchase_time_end),
            "scrollIdLine": scroll_id_line,
            "limit": str(limit),
        },
    )


def m_generate_short_link(*, origin_url: str, sub_ids: Optional[List[str]]) -> str:
    return _render(
        _GENERATE_SHORT_LINK,
        {
            "originUrl": json.dumps(origin_url),
            "subIds": json.dumps(sub_ids) if sub_ids else "[]",
        },
    )
