"""
Cliente Python para API Shopee Affiliate

Exemplos de uso das principais operações da API.
"""

import hashlib
import json
import time
from typing import Optional, List, Dict, Any
import requests


class ShopeeAffiliateClient:
    """Cliente para API de Afiliados da Shopee Brasil."""

    def __init__(self, app_id: str, app_secret: str):
        self.base_url = "https://open-api.affiliate.shopee.com.br/graphql"
        self.app_id = app_id
        self.app_secret = app_secret

    def _generate_signature(self, payload: str, timestamp: int) -> str:
        """
        Gera assinatura SHA256 para autenticação.

        Fórmula: SHA256(Credential + Timestamp + Payload + Secret)
        """
        sign_factor = f"{self.app_id}{timestamp}{payload}{self.app_secret}"
        return hashlib.sha256(sign_factor.encode()).hexdigest()

    def _get_auth_header(self, payload: str) -> str:
        """Constroi o header Authorization."""
        timestamp = int(time.time())
        signature = self._generate_signature(payload, timestamp)
        return f"SHA256 Credential={self.app_id}, Timestamp={timestamp}, Signature={signature}"

    def _request(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """Executa requisição GraphQL."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        payload_str = json.dumps(payload, separators=(",", ":"))
        headers = {
            "Authorization": self._get_auth_header(payload_str),
            "Content-Type": "application/json"
        }

        response = requests.post(self.base_url, headers=headers, data=payload_str)
        response.raise_for_status()
        return response.json()

    # ============== QUERIES ==============

    def get_shopee_offers(
        self,
        keyword: Optional[str] = None,
        sort_type: int = 1,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Busca ofertas da Shopee.

        Args:
            keyword: Buscar por nome da oferta
            sort_type: 1=LATEST_DESC, 2=HIGHEST_COMMISSION_DESC
            page: Número da página
            limit: Quantidade por página (máx 500)

        Returns:
            Dict com nodes e pageInfo
        """
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
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Busca ofertas de lojas.

        Args:
            keyword: Buscar por nome da loja
            shop_id: Buscar por ID da loja
            shop_type: [1]=Official, [2]=Preferred, [4]=Preferred Plus
            is_key_seller: Filtrar key sellers
            sort_type: 1=latest, 2=commission, 3=popular
            page: Número da página
            limit: Quantidade por página

        Returns:
            Dict com nodes e pageInfo
        """
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
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Busca ofertas de produtos.

        Args:
            keyword: Buscar por nome do produto
            shop_id: Buscar por ID da loja
            item_id: Buscar por ID do produto
            product_cat_id: Filtrar por categoria (nível 1, 2 ou 3)
            list_type: 0=ALL, 1=HIGHEST_COMMISSION, 2=TOP_PERFORMING, etc.
            match_id: ID correspondente para listType específico
            sort_type: 1=relevance, 2=sales, 3=price_desc, 4=price_asc, 5=commission
            page: Número da página
            limit: Quantidade por página

        Returns:
            Dict com nodes e pageInfo
        """
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
        limit: int = 500
    ) -> Dict[str, Any]:
        """
        Busca relatório de conversão.

        ATENÇÃO: scrollId é válido por apenas 30 segundos!
        IMPORTANTE: Apenas dados dos últimos 3 meses são disponíveis.

        Schema correto (descoberto via introspecção):
        - nodes.orders[] - Lista de pedidos
        - orders.items[] - Itens de cada pedido
        - Use 'itemName' (não 'productName')
        - Use 'itemTotalCommission' (não 'commissionAmount')

        Args:
            purchase_time_start: Timestamp de início
            purchase_time_end: Timestamp de fim
            scroll_id: ID de paginação (obtido na primeira query)
            limit: Quantidade por página (máx 500)

        Returns:
            Dict com nodes e pageInfo (incluindo scrollId para próxima página)
        """
        if scroll_id is not None:
            scroll_id_param = f'scrollId: "{scroll_id}"'
        else:
            scroll_id_param = ''

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

    def generate_short_link(
        self,
        origin_url: str,
        sub_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Gera link curto de rastreamento.

        REGRAS DE subIds (Testado em 16/02/2026):
        - Apenas letras (A-Z, a-z) e números (0-9) são permitidos
        - SEM underscore, hífen, ponto ou caracteres especiais
        - SEM espaços ou acentos
        - Arrays com 6+ itens são aceitos (contrário à documentação)
        - Palavras como "email", "canal", "source" funcionam

        ✅ VÁLIDOS: ["s1", "s2", "promo1", "email", "canal", "subId"]
        ❌ INVÁLIDOS: ["sub_id", "test-1", "utm_source", "café", "a b"]

        Args:
            origin_url: URL original do produto Shopee
            sub_ids: Lista de sub IDs para tracking (apenas letras e números)

        Returns:
            Dict com shortLink gerado
        """
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

    # ============== PAGINAÇÃO COM SCROLLID ==============

    def get_all_conversion_pages(
        self,
        purchase_time_start: int,
        purchase_time_end: int,
        limit: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Busca todas as páginas do relatório de conversão.

        IMPORTANTE: O scrollId expira em 30 segundos!
        Para relatórios grandes, considere buscar menos páginas ou
        processar cada página antes de buscar a próxima.

        Args:
            purchase_time_start: Timestamp de início
            purchase_time_end: Timestamp de fim
            limit: Itens por página

        Returns:
            Lista com todos os nós de todas as páginas
        """
        all_nodes = []
        scroll_id = None

        while True:
            response = self.get_conversion_report(
                purchase_time_start, purchase_time_end, scroll_id, limit
            )

            if "errors" in response:
                raise Exception(f"API Error: {response['errors']}")

            data = response["data"]["conversionReport"]
            all_nodes.extend(data["nodes"])

            page_info = data["pageInfo"]
            if not page_info["hasNextPage"]:
                break

            scroll_id = page_info["scrollId"]

        return all_nodes


# ============== EXEMPLOS DE USO ==============

def example_usage():
    """Exemplos de uso do cliente Shopee Affiliate."""

    # Configuração (use variáveis de ambiente em produção!)
    APP_ID = "seu_app_id"
    APP_SECRET = "seu_app_secret"

    client = ShopeeAffiliateClient(APP_ID, APP_SECRET)

    # 1. Buscar ofertas da Shopee
    print("=== Ofertas da Shopee ===")
    offers = client.get_shopee_offers(
        keyword="roupas",
        sort_type=2,  # Maior comissão
        page=1,
        limit=5
    )
    print(json.dumps(offers, indent=2, ensure_ascii=False))

    # 2. Buscar ofertas de lojas oficiais
    print("\n=== Lojas Oficiais ===")
    shops = client.get_shop_offers(
        shop_type=[1],  # Official shops
        sort_type=2,  # Maior comissão
        limit=5
    )
    print(json.dumps(shops, indent=2, ensure_ascii=False))

    # 3. Buscar produtos por palavra-chave
    print("\n=== Produtos ===")
    products = client.get_product_offers(
        keyword="iphone",
        sort_type=5,  # Maior comissão
        limit=5
    )
    print(json.dumps(products, indent=2, ensure_ascii=False))

    # 4. Gerar link curto
    print("\n=== Link Curto ===")
    short_link = client.generate_short_link(
        origin_url="https://shopee.com.br/produto-exemplo",
        sub_ids=["promo1", "canalEmail"]  # Use apenas letras e números (sem underscore)
    )
    print(json.dumps(short_link, indent=2, ensure_ascii=False))

    # 5. Relatório de conversão (últimos 7 dias)
    print("\n=== Relatório de Conversão ===")
    import time
    now = int(time.time())
    week_ago = now - (7 * 24 * 60 * 60)

    try:
        # Primeira página
        report = client.get_conversion_report(
            purchase_time_start=week_ago,
            purchase_time_end=now,
            limit=10
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))

        # Se tiver mais páginas, usar scrollId
        if report["data"]["conversionReport"]["pageInfo"]["hasNextPage"]:
            scroll_id = report["data"]["conversionReport"]["pageInfo"]["scrollId"]
            print(f"\nPróxima página com scrollId: {scroll_id}")
    except Exception as e:
        print(f"Erro ao buscar relatório: {e}")


if __name__ == "__main__":
    example_usage()
