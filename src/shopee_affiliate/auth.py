from __future__ import annotations

import hashlib
import time


def generate_signature(app_id: str, app_secret: str, payload: str, timestamp: int) -> str:
    """SHA256(AppId + Timestamp + Payload + Secret)."""
    sign_factor = f"{app_id}{timestamp}{payload}{app_secret}"
    return hashlib.sha256(sign_factor.encode()).hexdigest()


def build_authorization_header(app_id: str, app_secret: str, payload: str, *, timestamp: int | None = None) -> str:
    ts = int(time.time()) if timestamp is None else int(timestamp)
    signature = generate_signature(app_id, app_secret, payload, ts)
    return f"SHA256 Credential={app_id}, Timestamp={ts}, Signature={signature}"
