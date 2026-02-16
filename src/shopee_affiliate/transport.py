from __future__ import annotations

import json
import time
import random
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from .auth import build_authorization_header


@dataclass
class RetryConfig:
    max_attempts: int = 4
    backoff_base_s: float = 0.4
    retry_statuses: tuple[int, ...] = (429, 500, 502, 503, 504)


class ShopeeAffiliateTransport:
    """Camada HTTP + autenticação.

    Responsabilidades:
    - montar payload JSON canônico (separators=(',', ':'))
    - gerar header Authorization
    - executar POST com timeout
    - retry simples com backoff
    """

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        base_url: str = "https://open-api.affiliate.shopee.com.br/graphql",
        *,
        timeout_s: float = 30.0,
        retry: RetryConfig | None = None,
        session: requests.Session | None = None,
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = base_url
        self.timeout_s = timeout_s
        self.retry = retry or RetryConfig()
        self.session = session or requests.Session()

    def request(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables

        payload_str = json.dumps(payload, separators=(",", ":"))

        last_exc: Exception | None = None
        for attempt in range(1, self.retry.max_attempts + 1):
            # Recalcula Authorization a cada tentativa (timestamp novo)
            headers = {
                "Authorization": build_authorization_header(
                    self.app_id, self.app_secret, payload_str
                ),
                "Content-Type": "application/json",
            }

            try:
                resp = self.session.post(
                    self.base_url,
                    headers=headers,
                    data=payload_str,
                    timeout=self.timeout_s,
                )

                # Rate limit / transient errors
                if (
                    resp.status_code in self.retry.retry_statuses
                    and attempt < self.retry.max_attempts
                ):
                    sleep_s: float | None = None

                    # Respeita Retry-After quando presente
                    ra = resp.headers.get("Retry-After")
                    if ra:
                        try:
                            sleep_s = float(ra)
                        except ValueError:
                            sleep_s = None

                    if sleep_s is None:
                        # backoff exponencial + jitter leve
                        base = self.retry.backoff_base_s * (2 ** (attempt - 1))
                        jitter = (0.15 * base) * (0.5 - random.random()) * 2
                        sleep_s = max(0.0, base + jitter)

                    time.sleep(sleep_s)
                    continue

                resp.raise_for_status()
                return resp.json()

            except requests.RequestException as e:
                last_exc = e
                if attempt < self.retry.max_attempts:
                    base = self.retry.backoff_base_s * (2 ** (attempt - 1))
                    jitter = (0.15 * base) * (0.5 - random.random()) * 2
                    time.sleep(max(0.0, base + jitter))
                    continue
                raise

        # Não deveria chegar aqui
        raise RuntimeError("Falha inesperada no transport") from last_exc
