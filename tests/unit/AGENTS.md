<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-02-16 | Updated: 2026-02-16 -->

# unit

## Purpose
Testes unitários que validam componentes individuais do módulo `shopee_affiliate` sem fazer chamadas à API externa. Esses testes são rápidos e não requerem credenciais.

## Key Files

| File | Description |
|------|-------------|
| `test_auth.py` | Testa geração de assinatura SHA256 e autenticação |
| `test_validators.py` | Testa validação de dados e schemas |

## For AI Agents

### Working In This Directory
- Testes unitários **NÃO** requerem credenciais da API Shopee
- Todos os testes usam `pytest` e fixtures
- Testes devem ser independentes e isolados
- Use `unittest.mock` para simular dependências externas

### Testing Requirements
```bash
# Rodar apenas testes unitários
pytest tests/unit/ -v

# Rodar testes unitários específicos
pytest tests/unit/test_auth.py -v

# Rodar com cobertura
pytest tests/unit/ --cov=src/shopee_affiliate --cov-report=term-missing
```

### Common Patterns
```python
# Padrão de teste unitário
def test_something():
    # Arrange
    input_data = {...}

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected_result

# Padrão com mock
from unittest.mock import patch, MagicMock

@patch('shopee_affiliate.transport.requests.post')
def test_api_call(mock_post):
    mock_post.return_value.status_code = 200
    # ...teste
```

## Dependencies

### Internal
- `src/shopee_affiliate/` - Código sendo testado

### External
- **pytest** - Framework de testes
- **unittest.mock** - Mock de dependências

## Test Coverage

| Componente | Arquivo de Teste | Cobertura |
|------------|------------------|-----------|
| Autenticação | `test_auth.py` | Assinatura SHA256 |
| Validadores | `test_validators.py` | Schema validation |

<!-- MANUAL: Notas sobre testes unitários podem ser adicionadas abaixo -->
