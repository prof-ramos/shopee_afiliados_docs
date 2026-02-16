# Contribuindo para o Shopee Afiliados Docs

Obrigado por considerar contribuir com o projeto Shopee Afiliados Docs! Este guia fornece informacoes importantes sobre como contribuir.

## Indice

- [Como Contribuir](#como-contribuir)
- [Setup do Ambiente](#setup-do-ambiente)
- [Workflow de Desenvolvimento](#workflow-de-desenvolvimento)
- [Padroes de Codigo](#padroes-de-codigo)
- [Padroes de Commit](#padroes-de-commit)
- [Reportando Bugs](#reportando-bugs)
- [Sugerindo Melhorias](#sugerindo-melhorias)

## Como Contribuir

Existem muitas formas de contribuir:

- Reportando bugs
- Sugerindo novas funcionalidades
- Enviando pull requests com correcoes ou melhorias
- Melhorando a documentacao
- Compartilhando o projeto

## Setup do Ambiente

### Prerequisitos

- Python 3.11 ou superior
- uv (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Fork o repositorio**

   Clique no botao "Fork" no canto superior direito da pagina do GitHub e clone seu fork:

   ```bash
   git clone https://github.com/SEU_USUARIO/shopee_afiliados_docs.git
   cd shopee_afiliados_docs
   ```

2. **Configure o ambiente virtual**

   ```bash
   # Criar ambiente virtual com uv
   uv venv

   # Ativar o ambiente virtual
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate  # Windows
   ```

3. **Instale as dependencias**

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configure as credenciais**

   Crie um arquivo `.env` na raiz do projeto com suas credenciais da API Shopee:

   ```bash
   SHOPEE_APP_ID=seu_app_id_aqui
   SHOPEE_APP_SECRET=seu_app_secret_aqui
   ```

   **IMPORTANTE:** Nunca commit o arquivo `.env`! Ele ja esta no `.gitignore`.

## Workflow de Desenvolvimento

### 1. Crie uma branch

Crie uma branch para sua contribuicao:

```bash
git checkout -b feature/sua-feature
# ou
git checkout -b fix/seu-bugfix
```

### 2. Faca suas alteracoes

- Escreva codigo claro e legivel
- Adicione comentarios quando necessario
- Siga os padroes de codigo definidos abaixo
- Teste suas alteracoes

### 3. Execute os testes

Antes de enviar seu PR, execute a suite de testes:

```bash
# Executar todos os testes
uv run --python .venv/bin/python python scripts/run_all_tests.py

# Executar teste individual
uv run --python .venv/bin/python python tests/python/test_shopee_offer.py
```

### 4. Commit suas alteracoes

Use padroes de commit convencionais (veja abaixo).

### 5. Push e Pull Request

```bash
git push origin feature/sua-feature
```

Entao abra um Pull Request no GitHub com uma descricao clara das suas alteracoes.

## Padroes de Codigo

### Python

Seguimos as diretrizes **PEP 8** para codigo Python:

- Use 4 espacos para indentacao (nao tabs)
- Linhas com maximo de 79 caracteres
- Use aspas duplas para strings e docstrings
- Nomes de funcoes e variaveis em snake_case
- Nomes de classes em PascalCase
- Adicione docstrings para todas as classes e funcoes publicas

#### Exemplo:

```python
def buscar_ofertas(keyword: str, limit: int = 10) -> Dict[str, Any]:
    """
    Busca ofertas na API Shopee Affiliate.

    Args:
        keyword: Palavra-chave para busca
        limit: Numero maximo de resultados (padrao: 10)

    Returns:
        Dicionario com os resultados da busca
    """
    # Implementacao
    pass
```

### Formatacao

- Use type hints para funcoes e metodos
- Use constants em UPPER_CASE para valores imutaveis
- Mantenha funcoes pequenas e focadas em uma responsabilidade

## Padroes de Commit

Usamos **Conventional Commits** para mensagens de commit:

```
<tipo>(<escopo>): <descricao curta>

[opcional: descricao longa]

[opcional: footer]
```

### Tipos de Commit

- `feat`: Nova funcionalidade
- `fix`: Correcao de bug
- `docs`: Alteracao na documentacao
- `style`: Alteracao de formatacao (nao afeta logica)
- `refactor`: Refatoracao de codigo
- `test`: Adicao ou alteracao de testes
- `chore`: Alteracoes em build, deps, configuracao
- `perf`: Melhoria de performance
- `ci`: Alteracoes em CI/CD

### Exemplos

```bash
feat(client): adicionar suporte a paginacao em conversionReport

Fixes #123

Implementa paginacao usando scrollId para buscar todas
as paginas do relatorio de conversao.
```

```bash
fix(client): corrigir geracao de assinatura SHA256

O timestamp estava sendo gerado antes do payload,
causando erro de autenticacao na API.
```

```bash
docs: atualizar guia de instalacao com novos requisitos

Adiciona informacao sobre Python 3.11+ e uv.
```

## Reportando Bugs

Antes de reportar um bug, verifique se ja existe uma issue aberta.

### Template para Bug Report

```markdown
## Descricao do Bug

Breve descricao do problema.

## Passos para Reproduzir

1. Va para '...'
2. Clique em '....'
3. Role para '....'
4. Veja o erro

## Comportamento Esperado

Descricao do que voce esperava que acontecesse.

## Comportamento Atual

Descricao do que realmente aconteceu.

## Ambiente

- OS: [ex. macOS 14.0]
- Python: [ex. 3.11.5]
- Versao: [ex. 1.0.0]

## Logs Relevantes

Cole aqui quaisquer logs ou mensagens de erro relevantes.

## Possivel Solucao

Se voce tiver uma ideia de como corrigir, compartilhe aqui.
```

## Sugerindo Melhorias

Nos adoramos receber sugestoes de melhorias!

### Template para Feature Request

```markdown
## Descricao da Funcionalidade

Descricao clara e concisa da funcionalidade proposta.

## Motivacao

Por que esta funcionalidade seria util? Qual problema ela resolve?

## Exemplos de Uso

Se possivel, forneca exemplos de como a funcionalidade seria usada.

## Possivel Implementacao

Se voce tiver ideias sobre como implementar, compartilhe aqui.
```

## Code Review

Todos os Pull Requests passam por code review. Ao receber feedback:

- Mantenha uma mente aberta e colaborativa
- Faca perguntas se algo nao estiver claro
- Adicione "LGTM" (Looks Good To Me) quando aprovar uma mudanca

## Comportamento

Seja respeitoso e construtivo em todas as interacoes. Valorizamos:

- Comunicacao clara e empatica
- Colaboracao e apoio mutuo
- Aprendizado constante
- Diversidade de perspectivas

## Recursos Adicionais

- [Documentacao da API Shopee Affiliate](https://open-api.affiliate.shopee.com.br/docs)
- [API Explorer](https://open-api.affiliate.shopee.com.br/explorer)
- [Guia PEP 8](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

Duvidas? Abra uma issue ou entre em contato com os mantenedores!
