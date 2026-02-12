# shopee_afiliados_docs

[![Endpoints testados](https://img.shields.io/badge/endpoints%20testados-5%2F5-brightgreen)](docs/ENDPOINTS_TESTADOS.md)
[![Testes unit (pytest)](https://img.shields.io/badge/pytest-unit%2011%20passed-brightgreen)](tests/unit)

Repositório organizado para **documentação**, **scripts utilitários** e um **cliente Python modular** da API de Afiliados Shopee (GraphQL).

## Estrutura

- `docs/`: guias e documentacao tecnica
- `src/`: implementação canônica do cliente (instalável via `uv pip install -e .`)
- `scripts/`: scripts de exploracao, validacao e suporte
- `tests/`: testes (unit em `tests/unit/`; integrações antigas em `tests/python/`)
- `examples/`: exemplos de uso
- `archive/`: log de organizacao, backups e rollback

## Comece aqui

### Requisitos
- Python >= 3.10
- Recomendado: **uv** + venv em `.venv/`

### Setup (uv)

```bash
# 1) criar venv
uv venv .venv

# 2) instalar dependências (modo pacote)
uv pip install -e ".[dev]"

# 3) credenciais
cp .env.example .env
# edite .env e preencha SHOPEE_APP_ID / SHOPEE_APP_SECRET (ou SHOPEE_SECRET)
```

### Rodar testes

```bash
# Unit tests (rápidos, sem rede)
uv run --python .venv/bin/python -m pytest

# Integração (chama a API de verdade)
uv run --python .venv/bin/python python scripts/run_all_tests.py
```

> Nota sobre `subIds` (generateShortLink): na prática a API pode rejeitar certos formatos (ex.: underscore). Este repo assume `subIds` apenas com letras/números (ex.: `campanhaA`, `bannerB`).

## Exemplos

- Export CSV (stream, sem estourar RAM):

```bash
uv run --python .venv/bin/python python examples/python/export_conversion_report_csv.py \
  --days 30 --out conversion_report.csv
```

## Organizacao aplicada

- Log: `archive/ORGANIZATION_LOG_2026-02-12.md`
- Rollback: `archive/undo_organization_2026-02-12.sh`

## Documentos tecnicos

- Endpoints 100% testados: `docs/ENDPOINTS_TESTADOS.md`
- Arquitetura: `docs/ARCHITECTURE.md`
- Revisao de performance: `docs/REVISAO_PERFORMANCE.md`
