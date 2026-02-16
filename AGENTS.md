<!-- Generated: 2026-02-15 | Updated: 2026-02-15 -->

# shopee_afiliados_docs

## Purpose
Repositório de documentação e exemplos para a API de Afiliados da Shopee Brasil. Contém cliente Python completo, testes validados, scripts de exploração de schema e guias detalhados de uso.

## Key Files

| File | Description |
|------|-------------|
| `.env` | Credenciais da API (SHOPEE_APP_ID, SHOPEE_APP_SECRET) - não commitar no git |
| `.gitignore` | Regras de exclusão do git (inclui .env, .venv, __pycache__) |
| `requirements.txt` | Dependências Python (python-dotenv, requests) |
| `.claude/settings.local.json` | Configurações locais do Claude Code |
| `.omc/project-memory.json` | Memória de projeto do oh-my-claudecode |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `docs/` | Documentação completa da API Shopee Affiliate (veja `docs/AGENTS.md`) |
| `examples/` | Exemplos de uso em Python (veja `examples/AGENTS.md`) |
| `scripts/` | Scripts de automação e exploração de schema (veja `scripts/AGENTS.md`) |
| `tests/` | Suíte de testes Python validados (veja `tests/AGENTS.md`) |
| `archive/` | Arquivos arquivados do projeto (veja `archive/AGENTS.md`) |
| `.omc/` | Estado do oh-my-claudecode (autoplilot, sessões, checkpoints) |
| `.claude/` | Configurações do Claude Code |
| `.git/` | Repositório git |

## For AI Agents

### Working In This Directory
- Este é um projeto Python para integração com API GraphQL da Shopee
- Use o ambiente virtual `.venv` para executar comandos Python
- As credenciais devem estar configuradas no arquivo `.env`
- Documentação oficial da Shopee está desatualizada - confie nos schemas descobertos via introspecção

### Testing Requirements
- Execute `python scripts/run_all_tests.py` para validar todos os endpoints
- Use `pytest` para testes unitários específicos
- Verifique se SHOPEE_APP_ID e SHOPEE_APP_SECRET estão configurados antes de testar

### Common Patterns
- Cliente Python principal: `examples/python/shopee_affiliate_client.py`
- Queries GraphQL usam autenticação SHA256 com timestamp
- Paginação usa scrollId que expira em 30 segundos
- conversionReport retorna dados apenas dos últimos 3 meses

## Dependencies

### External
- **Python 3.13+** - Linguagem principal
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **requests** - Cliente HTTP para requisições GraphQL
- **pytest** - Framework de testes (via uv pip install)

### API Endpoints
- **Base URL**: `https://open-api.affiliate.shopee.com.br/graphql`
- **Autenticação**: SHA256 Signature (Credential + Timestamp + Payload + Secret)

## Project Context

### Status Atual
- Cliente Python: **COMPLETO** ✅
- Testes: **77.8% de sucesso** (7/9 testes passando)
- Documentação: **ATUALIZADA** com schema correto descoberto via introspecção

### Limitações Conhecidas
1. `generateShortLink`: não aceita palavras reservadas ("email", "canal", "utm")
2. `conversionReport`: apenas últimos 3 meses de dados disponíveis
3. `scrollId`: expira em 30 segundos, limitando paginação em relatórios grandes

### Links Úteis
- [API Playground](https://open-api.affiliate.shopee.com.br/explorer)
- [Documentação Oficial](https://www.affiliateshopee.com.br/documentacao/index)
- [Solicitar Acesso](https://help.shopee.com.br/portal/webform/bbce78695c364ba18c9cbceb74ec9091)

<!-- MANUAL: Custom project notes can be added below -->
