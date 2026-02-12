#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

move_back() {
  src="$1"
  dst="$2"
  if [ -e "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    mv "$src" "$dst"
    echo "OK: $src -> $dst"
  else
    echo "SKIP: $src não existe"
  fi
}

move_back "docs/ATUALIZACAO_FINAL.md" "ATUALIZACAO_FINAL.md"
move_back "docs/docs_shopee_affiliate.md" "docs_shopee_affiliate.md"
move_back "docs/GUIA_COMPLETO.md" "GUIA_COMPLETO.md"
move_back "docs/PESQUISA_SCHEMA_RESUMO.md" "PESQUISA_SCHEMA_RESUMO.md"
move_back "docs/SCHEMA_DESCOBERTO.md" "SCHEMA_DESCOBERTO.md"

move_back "scripts/explore_schema.py" "explore_schema.py"
move_back "scripts/update_client_from_docs.py" "update_client_from_docs.py"
move_back "scripts/run_all_tests.py" "run_all_tests.py"

move_back "tests/python/test_conversion_report.py" "test_conversion_report.py"
move_back "tests/python/test_generate_short_link.py" "test_generate_short_link.py"
move_back "tests/python/test_payload_format.py" "test_payload_format.py"
move_back "tests/python/test_payload_simple.py" "test_payload_simple.py"
move_back "tests/python/test_product_offer_v2.py" "test_product_offer_v2.py"
move_back "tests/python/test_product_offer.py" "test_product_offer.py"
move_back "tests/python/test_shop_offer_v2.py" "test_shop_offer_v2.py"
move_back "tests/python/test_shop_offer.py" "test_shop_offer.py"
move_back "tests/python/test_shopee_offer_v2.py" "test_shopee_offer_v2.py"
move_back "tests/python/test_shopee_offer.py" "test_shopee_offer.py"
move_back "tests/python/test_short_link.py" "test_short_link.py"

echo "Rollback concluído."
