#!/usr/bin/env python3
"""
Suite de testes completos para API Shopee Affiliate.

Testa todos os endpoints e funcionalidades do cliente Python.
"""

import json
import sys
import os
import time
from dotenv import load_dotenv

# Adicionar o diretório examples/python ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples', 'python'))

from shopee_affiliate_client import ShopeeAffiliateClient

# Carregar credenciais
load_dotenv()
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
SHOPEE_APP_SECRET = os.getenv("SHOPEE_APP_SECRET")


class TestRunner:
    """Executa todos os testes da API Shopee."""

    def __init__(self, client: ShopeeAffiliateClient):
        self.client = client
        self.results = {
            "passed": [],
            "failed": [],
            "errors": []
        }

    def print_header(self, text):
        """Imprime cabeçalho de teste."""
        print(f"\n{'=' * 70}")
        print(f"  {text}")
        print('=' * 70)

    def print_result(self, test_name, success, message="", data=None):
        """Registra e imprime resultado de um teste."""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "data": data,
            "timestamp": int(time.time())
        }

        if success:
            self.results["passed"].append(result)
            print(f"  ✅ PASSOU: {message}")
        else:
            self.results["failed"].append(result)
            print(f"  ❌ FALHOU: {message}")

        if data:
            print(f"  📊 Dados: {json.dumps(data, ensure_ascii=False)}")

        return result

    def test_1_shopee_offers(self):
        """Testa shopeeOfferV2 - Ofertas da Shopee."""
        self.print_header("TESTE 1: shopeeOfferV2 - Ofertas da Shopee")

        try:
            # Teste com keyword
            result = self.client.get_shopee_offers(
                keyword="roupas",
                sort_type=2,  # Maior comissão
                page=1,
                limit=5
            )

            if "errors" in result:
                self.print_result("shopeeOfferV2 com keyword", False,
                                   f"Erros: {result['errors']}")
                return

            data = result.get("data", {}).get("shopeeOfferV2", {})
            nodes = data.get("nodes", [])

            self.print_result("shopeeOfferV2 com keyword", True,
                                f"{len(nodes)} ofertas encontradas",
                                {"offers": len(nodes), "example": nodes[0] if nodes else None})

        except Exception as e:
            self.print_result("shopeeOfferV2 com keyword", False, f"Exceção: {str(e)}")

    def test_2_shopee_offers_all(self):
        """Testa shopeeOfferV2 - Sem filtros."""
        self.print_header("TESTE 2: shopeeOfferV2 - Todas as ofertas")

        try:
            result = self.client.get_shopee_offers(
                sort_type=2,
                limit=3
            )

            if "errors" in result:
                self.print_result("shopeeOfferV2 todas", False,
                                   f"Erros: {result['errors']}")
                return

            nodes = result.get("data", {}).get("shopeeOfferV2", {}).get("nodes", [])
            self.print_result("shopeeOfferV2 todas", True,
                                f"{len(nodes)} ofertas encontradas")

        except Exception as e:
            self.print_result("shopeeOfferV2 todas", False, f"Exceção: {str(e)}")

    def test_3_shop_offers(self):
        """Testa shopOfferV2 - Ofertas de lojas."""
        self.print_header("TESTE 3: shopOfferV2 - Ofertas de Lojas")

        try:
            # Teste com shop_type
            result = self.client.get_shop_offers(
                shop_type=[1],  # Official shops
                sort_type=2,  # Maior comissão
                limit=5
            )

            if "errors" in result:
                self.print_result("shopOfferV2 com shopType", False,
                                   f"Erros: {result['errors']}")
                return

            data = result.get("data", {}).get("shopOfferV2", {})
            nodes = data.get("nodes", [])

            self.print_result("shopOfferV2 com shopType", True,
                                f"{len(nodes)} lojas encontradas",
                                {"shops": len(nodes), "example": nodes[0] if nodes else None})

        except Exception as e:
            self.print_result("shopOfferV2 com shopType", False, f"Exceção: {str(e)}")

    def test_4_product_offers(self):
        """Testa productOfferV2 - Ofertas de produtos."""
        self.print_header("TESTE 4: productOfferV2 - Ofertas de Produtos")

        try:
            # Teste com keyword
            result = self.client.get_product_offers(
                keyword="iphone",
                sort_type=5,  # Maior comissão
                limit=5
            )

            if "errors" in result:
                self.print_result("productOfferV2 com keyword", False,
                                   f"Erros: {result['errors']}")
                return

            data = result.get("data", {}).get("productOfferV2", {})
            nodes = data.get("nodes", [])

            self.print_result("productOfferV2 com keyword", True,
                                f"{len(nodes)} produtos encontrados",
                                {"products": len(nodes), "example": nodes[0] if nodes else None})

        except Exception as e:
            self.print_result("productOfferV2 com keyword", False, f"Exceção: {str(e)}")

    def test_5_product_offers_by_shop(self):
        """Testa productOfferV2 - Por shop_id."""
        self.print_header("TESTE 5: productOfferV2 - Por Shop")

        try:
            result = self.client.get_product_offers(
                shop_id=123456,  # Shop ID genérico
                limit=3
            )

            if "errors" in result:
                self.print_result("productOfferV2 por shopId", False,
                                   f"Erros: {result['errors']}")
                return

            nodes = result.get("data", {}).get("productOfferV2", {}).get("nodes", [])
            self.print_result("productOfferV2 por shopId", True,
                                f"{len(nodes)} produtos encontrados")

        except Exception as e:
            self.print_result("productOfferV2 por shopId", False, f"Exceção: {str(e)}")

    def test_6_generate_short_link(self):
        """Testa generateShortLink - Geração de link curto."""
        self.print_header("TESTE 6: generateShortLink - Gerar Link Curto")

        try:
            result = self.client.generate_short_link(
                origin_url="https://shopee.com.br/product/123456",
                sub_ids=["promo1", "canal_email"]  # 2 sub-IDs
            )

            if "errors" in result:
                self.print_result("generateShortLink básico", False,
                                   f"Erros: {result['errors']}")
                return

            short_link = result.get("data", {}).get("generateShortLink", {}).get("shortLink")
            self.print_result("generateShortLink básico", True,
                                f"Link gerado: {short_link}",
                                {"shortLink": short_link})

        except Exception as e:
            self.print_result("generateShortLink básico", False, f"Exceção: {str(e)}")

    def test_7_short_link_no_subids(self):
        """Testa generateShortLink - Sem sub-IDs."""
        try:
            result = self.client.generate_short_link(
                origin_url="https://shopee.com.br/product/789012"
            )

            if "errors" in result:
                self.print_result("generateShortLink sem subIds", False,
                                   f"Erros: {result['errors']}")
                return

            short_link = result.get("data", {}).get("generateShortLink", {}).get("shortLink")
            self.print_result("generateShortLink sem subIds", True,
                                f"Link gerado: {short_link}")

        except Exception as e:
            self.print_result("generateShortLink sem subIds", False, f"Exceção: {str(e)}")

    def test_8_conversion_report_empty(self):
        """Testa conversionReport - Período recente (vazio)."""
        self.print_header("TESTE 8: conversionReport - Últimos 7 dias")

        try:
            now = int(time.time())
            week_ago = now - (7 * 24 * 60 * 60)

            result = self.client.get_conversion_report(
                purchase_time_start=week_ago,
                purchase_time_end=now,
                limit=10
            )

            if "errors" in result:
                self.print_result("conversionReport 7 dias", False,
                                   f"Erros: {result['errors']}")
                return

            data = result.get("data", {}).get("conversionReport", {})
            nodes = data.get("nodes", [])

            self.print_result("conversionReport 7 dias", True,
                                f"{len(nodes)} conversões retornadas")

        except Exception as e:
            self.print_result("conversionReport 7 dias", False, f"Exceção: {str(e)}")

    def test_9_conversion_report_structure(self):
        """Testa estrutura do conversionReport com dados."""
        self.print_header("TESTE 9: conversionReport - Estrutura")

        try:
            now = int(time.time())
            three_days_ago = now - (3 * 24 * 60 * 60)

            result = self.client.get_conversion_report(
                purchase_time_start=three_days_ago,
                purchase_time_end=now,
                limit=5
            )

            if "errors" in result:
                self.print_result("conversionReport estrutura", False,
                                   f"Erros: {result['errors']}")
                return

            data = result.get("data", {}).get("conversionReport", {})
            nodes = data.get("nodes", [])

            # Verificar estrutura correta
            has_orders = False
            total_orders = 0
            total_items = 0

            for node in nodes:
                orders = node.get("orders", [])
                if orders:
                    has_orders = True
                    total_orders += len(orders)
                    for order in orders:
                        items = order.get("items", [])
                        total_items += len(items)

            self.print_result("conversionReport estrutura", has_orders,
                                f"Orders: {total_orders}, Items: {total_items}",
                                {"hasOrders": has_orders, "totalOrders": total_orders, "totalItems": total_items})

        except Exception as e:
            self.print_result("conversionReport estrutura", False, f"Exceção: {str(e)}")

    def run_all_tests(self):
        """Executa todos os testes."""
        print("\n" + "=" * 70)
        print("  SUITE DE TESTES COMPLETA - API SHOPEE AFFILIATE")
        print("=" * 70)
        print(f"  Timestamp: {int(time.time())}")
        print(f"  App ID: {SHOPEE_APP_ID}")

        # Executar todos os testes
        self.test_1_shopee_offers()
        self.test_2_shopee_offers_all()
        self.test_3_shop_offers()
        self.test_4_product_offers()
        self.test_5_product_offers_by_shop()
        self.test_6_generate_short_link()
        self.test_7_short_link_no_subids()
        self.test_8_conversion_report_empty()
        self.test_9_conversion_report_structure()

        # Imprimir resumo final
        self.print_summary()

    def print_summary(self):
        """Imprime resumo dos testes."""
        print("\n" + "=" * 70)
        print("  RESUMO DOS TESTES")
        print("=" * 70)

        passed = len(self.results["passed"])
        failed = len(self.results["failed"])

        print(f"\n  ✅ TESTES PASSOU: {passed}")
        print(f"  ❌ TESTES FALHARAM: {failed}")
        print(f"  📊 TOTAL: {passed + failed}")
        print(f"  📈 TAXA DE SUCESSO: {(passed/(passed+failed)*100):.1f}%")

        if failed == 0:
            print("\n  🎉 TODOS OS TESTES PASSARAM!")
        else:
            print(f"\n  ⚠️  {failed} teste(s) falharam")


if __name__ == "__main__":
    if not SHOPEE_APP_ID or not SHOPEE_APP_SECRET:
        print("ERRO: Credenciais não encontradas no arquivo .env")
        print("Certifique-se de que SHOPEE_APP_ID e SHOPEE_APP_SECRET estão definidos.")
        sys.exit(1)

    client = ShopeeAffiliateClient(SHOPEE_APP_ID, SHOPEE_APP_SECRET)
    runner = TestRunner(client)
    runner.run_all_tests()
