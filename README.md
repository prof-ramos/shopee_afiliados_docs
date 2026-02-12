# shopee_afiliados_docs

Repositorio organizado para documentacao, scripts utilitarios e testes da API de afiliados Shopee.

## Estrutura

- `docs/`: guias e documentacao tecnica
- `src/`: implementação canônica do cliente (instalável via `uv pip install -e .`)
- `scripts/`: scripts de exploracao, validacao e suporte
- `tests/`: testes (unit em `tests/unit/`; integrações antigas em `tests/python/`)
- `examples/`: exemplos de uso
- `archive/`: log de organizacao, backups e rollback

## Ambiente

- Python >= 3.10
- Recomendado: `uv` + venv em `.venv/`

### Setup (uv)

```bash
# 1) criar venv
uv venv .venv

# 2) instalar dependências (modo pacote, via pyproject)
uv pip install -e ".[dev]"

# 3) credenciais
cp .env.example .env
# edite .env e preencha SHOPEE_APP_ID / SHOPEE_APP_SECRET
```

### Comandos rápidos

```bash
# Verificar Python no venv via uv
uv run --python .venv/bin/python python -V

# Rodar suite principal
uv run --python .venv/bin/python python scripts/run_all_tests.py
```

> Obs.: o `scripts/run_all_tests.py` tenta importar o client via pacote (src/) e, se não estiver instalado, cai no fallback `examples/python`.
>
> Nota sobre `subIds` (generateShortLink): apesar de a doc permitir strings livres, na prática a API pode rejeitar certos formatos (ex.: underscore). Este repo assume `subIds` apenas com letras/números (ex.: `campanhaA`, `bannerB`).

## Organizacao aplicada

- Log: `archive/ORGANIZATION_LOG_2026-02-12.md`
- Rollback: `archive/undo_organization_2026-02-12.sh`

## Documentos tecnicos

- Endpoints 100% testados: `docs/ENDPOINTS_TESTADOS.md`
- Arquitetura: `docs/ARCHITECTURE.md`
- Revisao de performance: `docs/REVISAO_PERFORMANCE.md`
