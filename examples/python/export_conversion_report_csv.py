#!/usr/bin/env python3
"""Exporta conversionReport para CSV sem estourar RAM.

- Processa página a página usando iteradores do client.
- Requer .env com SHOPEE_APP_ID e SHOPEE_APP_SECRET (ou SHOPEE_SECRET).

Uso:
  uv run --python .venv/bin/python python examples/python/export_conversion_report_csv.py \
    --days 30 --out conversion_report.csv

Dica:
  Se quiser limitar páginas (debug): --max-pages 2
"""

from __future__ import annotations

import argparse
import csv
import os
import time
from dotenv import load_dotenv

from shopee_affiliate_client import ShopeeAffiliateClient


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=30, help="Janela retroativa em dias")
    p.add_argument("--out", type=str, default="conversion_report.csv", help="Arquivo CSV de saída")
    p.add_argument("--max-pages", type=int, default=None, help="Limita número de páginas (debug)")
    p.add_argument("--limit", type=int, default=500, help="Itens por página (máx 500)")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    load_dotenv()
    app_id = os.getenv("SHOPEE_APP_ID")
    secret = os.getenv("SHOPEE_APP_SECRET") or os.getenv("SHOPEE_SECRET")
    if not app_id or not secret:
        raise SystemExit("Defina SHOPEE_APP_ID e SHOPEE_APP_SECRET (ou SHOPEE_SECRET) no .env")

    client = ShopeeAffiliateClient(app_id, secret)

    now = int(time.time())
    start = now - (args.days * 24 * 60 * 60)

    fieldnames = [
        "orderId",
        "orderStatus",
        "shopType",
        "itemId",
        "itemName",
        "qty",
        "itemPrice",
        "itemTotalCommission",
        "shopId",
        "shopName",
        "globalCategoryLv1Name",
        "globalCategoryLv2Name",
        "globalCategoryLv3Name",
        "imageUrl",
    ]

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()

        exported = 0
        for order in client.iter_conversion_report_orders(
            purchase_time_start=start,
            purchase_time_end=now,
            limit=args.limit,
            max_pages=args.max_pages,
        ):
            items = order.get("items") or []
            for item in items:
                row = {
                    "orderId": order.get("orderId"),
                    "orderStatus": order.get("orderStatus"),
                    "shopType": order.get("shopType"),
                    "itemId": item.get("itemId"),
                    "itemName": item.get("itemName"),
                    "qty": item.get("qty"),
                    "itemPrice": item.get("itemPrice"),
                    "itemTotalCommission": item.get("itemTotalCommission"),
                    "shopId": item.get("shopId"),
                    "shopName": item.get("shopName"),
                    "globalCategoryLv1Name": item.get("globalCategoryLv1Name"),
                    "globalCategoryLv2Name": item.get("globalCategoryLv2Name"),
                    "globalCategoryLv3Name": item.get("globalCategoryLv3Name"),
                    "imageUrl": item.get("imageUrl"),
                }
                w.writerow(row)
                exported += 1

    print(f"OK: exportados {exported} itens para {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
