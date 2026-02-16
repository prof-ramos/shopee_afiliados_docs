<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-15 | Updated: 2026-02-15 -->

# examples

## Purpose
Exemplos práticos de uso da API Shopee Affiliate em Python. Contém o cliente completo e scripts de teste para validação dos endpoints.

## Key Files

| File | Description |
|------|-------------|
| `README.md` | Guia de uso dos exemplos com instruções de configuração |
| `test_api.py` | Script de teste rápido da API |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `python/` | Cliente Python e implementação completa (veja `python/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- Use o ambiente virtual `.venv` antes de executar scripts
- Configure o arquivo `.env` na raiz do projeto com suas credenciais
- Execute `python test_api.py` para testar a conexão

### Setup Instructions

```bash
# Criar ambiente virtual
uv venv
source .venv/bin/activate

# Instalar dependências
uv pip install -r ../requirements.txt

# Configurar credenciais (criar .env na raiz)
SHOPEE_APP_ID=seu_app_id
SHOPEE_APP_SECRET=seu_app_secret

# Executar teste
python test_api.py
```

### Testing Requirements
- Execute `test_api.py` para verificar se as credenciais estão corretas
- Verifique se todas as dependências estão instaladas

### Common Patterns
- Use `from shopee_affiliate_client import ShopeeAffiliateClient`
- Instancie com `ShopeeAffiliateClient(app_id, app_secret)`
- Consulte o cliente `python/shopee_affiliate_client.py` para todos os métodos disponíveis

## Dependencies

### Internal
- `../requirements.txt` - Dependências Python necessárias
- `../.env` - Credenciais da API

### External
- `python-dotenv` - Carregamento de variáveis de ambiente
- `requests` - Cliente HTTP para requisições GraphQL

<!-- MANUAL: -->
