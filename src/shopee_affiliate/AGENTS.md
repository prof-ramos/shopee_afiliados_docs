<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-16 | Updated: 2026-02-16 -->

# shopee_affiliate

## Purpose
Módulo principal do cliente Python para a API de Afiliados da Shopee Brasil. Implementa autenticação, transporte HTTP, validação de dados e queries GraphQL.

## Key Files

| File | Description |
|------|-------------|
| `__init__.py` | Exporta `ShopeeAffiliateClient` e exceções públicas |
| `client.py` | Classe principal `ShopeeAffiliateClient` com métodos para todas as queries |
| `auth.py` | Módulo de autenticação com geração de assinatura SHA256 |
| `transport.py` | Cliente HTTP wrapper para requests com tratamento de erros |
| `validators.py` | Validadores de dados e schemas de entrada/saída |
| `queries.py` | Queries GraphQL como strings constantes |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `graphql/` | Arquivos `.graphql` com queries otimizadas (veja `graphql/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- **Não modifique** os arquivos `.graphql` manualmente - eles são gerados/atualizados via introspecção
- A assinatura SHA256 requer: `Credential + Timestamp + Payload + Secret`
- Timestamp deve estar em milissegundos UNIX
- Todos os métodos do `ShopeeAffiliateClient` retornam dados já validados

### Testing Requirements
- Testes unitários em `tests/unit/test_auth.py` e `tests/unit/test_validators.py`
- Testes de integração em `tests/python/`
- Use credenciais de teste (não use credenciais de produção)

### Common Patterns
```python
# Padrão de autenticação
signature = hashlib.sha256(f"{app_id}{timestamp}{payload}{app_secret}".encode()).hexdigest()

# Padrão de erro
if response.status_code != 200:
    raise ShopeeAffiliateAPIError(f"API Error: {response.text}")

# Padrão de validação
if not data.get("data"):
    raise ShopeeAffiliateValidationError("Invalid response structure")
```

## Dependencies

### Internal
- `graphql/` - Queries GraphQL usadas pelo cliente

### External
- **hashlib** - Geração de assinatura SHA256
- **requests** - Cliente HTTP para requisições
- **dotenv** - Carregamento de credenciais do .env
- **typing** - Type hints (Optional, Dict, Any, etc.)

## API Methods

### Queries Disponíveis
- `conversion_report()` - Relatório de conversões (últimos 3 meses)
- `validated_report()` - Relatório de comissões validadas (definitivas)
- `generate_short_link()` - Gera link encurtado de afiliado (suporta até 5 sub-IDs)
- `product_offer_v2()` - Ofertas de produto específico
- `shopee_offer_v2()` - Ofertas gerais da Shopee
- `shop_offer_v2()` - Ofertas de loja específica

### Iteradores (Paginação Automática)
- `iter_conversion_report_pages()` - Itera páginas de conversionReport
- `iter_conversion_report_orders()` - Itera orders individuais de conversionReport
- `iter_validated_report_pages()` - Itera páginas de validatedReport
- `iter_validated_report_orders()` - Itera orders individuais de validatedReport

### Exceções
- `ShopeeAffiliateError` - Base exception
- `ShopeeAffiliateAPIError` - Erros de requisição HTTP
- `ShopeeAffiliateValidationError` - Erros de validação de dados
- `ShopeeAffiliateAuthError` - Erros de autenticação

<!-- MANUAL: Notas sobre implementação podem ser adicionadas abaixo -->
