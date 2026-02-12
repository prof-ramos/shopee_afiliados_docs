# shopee_afiliados_docs

Repositorio organizado para documentacao, scripts utilitarios e testes da API de afiliados Shopee.

## Estrutura

- `docs/`: guias e documentacao tecnica
- `scripts/`: scripts de exploracao, validacao e suporte
- `tests/python/`: testes Python
- `examples/`: exemplos de uso
- `archive/`: log de organizacao, backups e rollback

## Ambiente

- Python com `uv` e virtualenv em `.venv/`

## Comandos rapidos

```bash
# Verificar Python no venv via uv
uv run --python .venv/bin/python python -V

# Rodar suite principal (ajuste conforme necessidade)
uv run --python .venv/bin/python python scripts/run_all_tests.py
```

## Organizacao aplicada

- Log: `archive/ORGANIZATION_LOG_2026-02-12.md`
- Rollback: `archive/undo_organization_2026-02-12.sh`

## Documentos tecnicos

- Revisao de performance: `docs/REVISAO_PERFORMANCE.md`
