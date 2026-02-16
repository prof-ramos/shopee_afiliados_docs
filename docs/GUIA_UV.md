# Guia de Uso do uv

**uv** é um gerenciador de pacotes Python ultra-rápido escrito em Rust. É 10-100x mais rápido que pip e substitui pip, pip-tools, virtualenv, e outros.

## Por que uv?

| Característica | pip | uv |
|----------------|-----|-----|
| **Velocidade** | lento | ⚡ 10-100x mais rápido |
| **Cache** | manual | automático |
| **Lockfiles** | requires pip-tools | nativo |
| **Resolução** | lenta | instantânea |
| **Instalação** | já vem com Python | 1 comando |

## Instalação

### macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Homebrew (macOS)

```bash
brew install uv
```

## Uso Básico

### Criar Ambiente Virtual

```bash
# Criar .venv no diretório atual
uv venv

# Especificar Python version
uv venv --python 3.11
```

### Instalar Pacotes

```bash
# Instalar pacote
uv pip install requests

# Instalar do pyproject.toml (modo editável)
uv pip install -e .

# Instalar dependências de desenvolvimento
uv pip install pytest ruff
```

### Comandos Comuns

```bash
# Listar pacotes instalados
uv pip list

# Verificar vulnerabilidades
uv pip check

# Desinstalar pacote
uv pip uninstall requests

# Atualizar pacote
uv pip install --upgrade requests
```

## Integração com pyproject.toml

O projeto já usa `pyproject.toml` com formato padrão:

```toml
[project]
name = "shopee-afiliados-docs"
version = "0.1.0"
dependencies = [
  "requests>=2.32.0",
  "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0.0",
  "ruff>=0.6.0",
]
```

### Instalar com dev dependencies:

```bash
uv pip install -e ".[dev]"
```

## Docker com uv

```dockerfile
FROM python:3.10-slim

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Criar ambiente virtual
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependências
COPY pyproject.toml .
RUN uv pip install -e .

CMD ["python"]
```

## CI/CD

### GitHub Actions

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v1

- name: Install dependencies
  run: |
    uv pip install -e .
    uv pip install pytest
```

## Troubleshooting

### uv: command not found

```bash
# Adicionar ao PATH (macOS/Linux)
export PATH="$HOME/.local/bin:$PATH"

# Adicionar ao .bashrc ou .zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Conflito com pip

```bash
# Desinstalar pip se usar uv exclusivamente
uv pip uninstall pip

# Ou manter ambos (funciona normalmente)
```

## Links Úteis

- **Documentação oficial**: https://docs.astral.sh/uv/
- **GitHub**: https://github.com/astral-sh/uv
- **Comparativo**: https://docs.astral.sh/uv/comparison/
- **Instalação**: https://docs.astral.sh/uv/getting-started/installation/

## Migração de pip → uv

| Comando pip | Comando uv |
|-------------|------------|
| `pip install requests` | `uv pip install requests` |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip install -e .` | `uv pip install -e .` |
| `pip list` | `uv pip list` |
| `virtualenv .venv` | `uv venv` |

## Notas Importantes

1. **uv é compatível com pip** - Ambos podem coexistir
2. **Cache automático** - uv cacheia pacotes em `~/.cache/uv`
3. **Python version** - uv pode instalar Python automaticamente se necessário
4. **Virtual environments** - uv gerencia `.venv` automaticamente

## Exemplos Práticos

### Projeto Shopee Affiliate

```bash
# 1. Clone o projeto
git clone https://github.com/prof-ramos/shopee_afiliados_docs.git
cd shopee_afiliados_docs

# 2. Crie ambiente virtual
uv venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Instale dependências
uv pip install -e .

# 4. Execute testes
pytest tests/ -v

# 5. Execute lint
ruff check src/
ruff format src/
```

## Performance

Comparativo de instalação de 100 pacotes:

| Ferramenta | Tempo | Speedup |
|------------|-------|---------|
| pip (sem cache) | 30s | 1x |
| pip (com cache) | 5s | 6x |
| **uv (cache automático)** | **0.3s** | **100x** |
