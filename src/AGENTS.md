<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-16 | Updated: 2026-02-16 -->

# src

## Purpose
Diretório contendo o código fonte principal do pacote Python `shopee_affiliate`. Esta estrutura segue o padrão "src layout" recomendado para projetos Python, onde o pacote principal fica dentro do diretório `src/`.

## Key Files

| File | Description |
|------|-------------|
| `shopee_affiliate_client.py` | Ponto de entrada alternativo do cliente (symlink para src/shopee_affiliate/) |
| `shopee_affiliados_docs.egg-info/` | Metadados do pacote gerados pelo setuptools |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `shopee_affiliate/` | Módulo principal do cliente Python (veja `shopee_affiliate/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- Este diretório usa o layout "src-layout" do Python
- O pacote principal é `shopee_affiliate` (não `shopee_affiliate_client`)
- Para instalação em modo desenvolvimento: `pip install -e .`
- O arquivo `setup.py` ou `pyproject.toml` na raiz define como este pacote é construído

### Testing Requirements
- Testes unitários estão em `tests/unit/`
- Testes de integração estão em `tests/python/`
- Sempre instale o pacote em modo editável antes de rodar testes

### Common Patterns
- Imports devem usar `from shopee_affiliate import ...`
- O módulo expõe `ShopeeAffiliateClient` como interface principal

## Dependencies

### Internal
- `examples/python/` - Contém exemplos de uso que importam deste pacote
- `tests/` - Testes que validam este código

### External
- **python-dotenv** - Carregamento de variáveis de ambiente (.env)
- **requests** - Cliente HTTP para requisições GraphQL
- **typing** - Hints de tipo para Python 3.10+

## Build Instructions

```bash
# Instalar em modo desenvolvimento
pip install -e .

# Ou com uv
uv pip install -e .

# Empacotar para distribuição
python -m build

# Verificar pacote
twine check dist/*
```

<!-- MANUAL: Notas específicas do layout src podem ser adicionadas abaixo -->
