#!/usr/bin/env python3
"""
Valida o cliente Python com base nos campos esperados da documentacao.
"""

from pathlib import Path


def expected_fields() -> dict[str, list[str]]:
    return {
        "shopeeOfferV2": [
            "commissionRate",
            "imageUrl",
            "offerLink",
            "originalLink",
            "offerName",
            "offerType",
            "categoryId",
            "collectionId",
            "periodStartTime",
            "periodEndTime",
        ],
        "shopOfferV2": [
            "commissionRate",
            "imageUrl",
            "offerLink",
            "originalLink",
            "shopId",
            "shopName",
            "ratingStar",
            "shopType",
            "remainingBudget",
            "periodStartTime",
            "periodEndTime",
        ],
        "productOfferV2": [
            "itemId",
            "productName",
            "commissionRate",
            "commission",
            "price",
            "priceMin",
            "priceMax",
            "sales",
            "ratingStar",
            "imageUrl",
            "shopId",
            "shopName",
            "shopType",
            "productLink",
            "offerLink",
        ],
        "generateShortLink": ["shortLink"],
    }


def validate_python_client() -> int:
    print("=== Validando Cliente Python ===")
    client_file = Path("examples/python/shopee_affiliate_client.py")

    if not client_file.exists():
        print(f"❌ Arquivo nao encontrado: {client_file}")
        return 1

    content = client_file.read_text(encoding="utf-8")
    total_missing = 0

    for endpoint, fields in expected_fields().items():
        print(f"\n[{endpoint}]")
        for field in fields:
            if field in content:
                print(f"  ✅ {field}")
            else:
                print(f"  ❌ Faltando: {field}")
                total_missing += 1

    if total_missing:
        print(f"\n⚠️ Total de campos faltando: {total_missing}")
        return 2

    print("\n✅ Cliente Python validado com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate_python_client())
