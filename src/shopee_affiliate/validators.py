from __future__ import annotations

from typing import Iterable, Optional


def validate_sub_ids(sub_ids: Optional[Iterable[str]]) -> None:
    """Valida subIds usados em generateShortLink.

    Observação prática (com base em testes na API):
    - máximo 5 itens
    - usar somente alfanumérico (sem underscore, hífen etc.)

    A API pode rejeitar formatos fora disso com erro 11001 (invalid sub id).
    """

    if not sub_ids:
        return

    sub_ids_list = list(sub_ids)

    if len(sub_ids_list) > 5:
        raise ValueError("sub_ids deve ter no máximo 5 itens")

    invalid = [s for s in sub_ids_list if (not isinstance(s, str) or not s.isalnum())]
    if invalid:
        raise ValueError(
            f"sub_ids contém valores inválidos (use somente letras/números): {invalid}"
        )
