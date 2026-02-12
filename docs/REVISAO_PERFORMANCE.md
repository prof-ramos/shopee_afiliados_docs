# Revisao de Performance - Base Python

Data: 2026-02-12  
Fonte de analise: `repomix-output.xml` + leitura direta dos arquivos do repositorio.

## Escopo

Esta revisao cobre:

1. Identificacao de gargalos de desempenho.
2. Verificacao de utilizacao de recursos (CPU, memoria, rede e I/O).
3. Revisao de eficiencia algoritmica.
4. Avaliacao das estrategias de cache.

## Resumo Executivo

Os principais pontos de impacto estao no cliente HTTP e no fluxo de paginacao:

- Requisicoes HTTP sem pooling, sem timeout e sem retry.
- Queries GraphQL montadas por interpolacao de string (menos eficientes para cache/plano no backend).
- Acumulo de paginas inteiras em memoria no fluxo de conversao.
- Logging de payload completo em scripts de teste e exploracao.
- Ausencia de cache aplicado a consultas de leitura repetitivas.

## 1) Gargalos de Desempenho

### 1.1 Camada HTTP sem resiliencia/performance

Arquivo: `examples/python/shopee_affiliate_client.py:49`

- Uso de `requests.post(...)` direto em cada chamada.
- Sem `requests.Session()`, sem reuse de conexoes TCP/TLS.
- Sem `timeout` explicito.
- Sem estrategia de retry para falhas transientes.

Impacto:

- Maior latencia media por chamada.
- Risco de bloqueio em chamadas lentas.
- Menor throughput sob carga.

### 1.2 Query GraphQL dinamica por interpolacao

Arquivos:

- `examples/python/shopee_affiliate_client.py:74`
- `examples/python/shopee_affiliate_client.py:133`
- `examples/python/shopee_affiliate_client.py:202`
- `examples/python/shopee_affiliate_client.py:275`
- `examples/python/shopee_affiliate_client.py:335`

Impacto:

- Menor chance de reaproveitamento de parse/plano no servidor GraphQL.
- Mais custo de serializacao e manutencao de query.

### 1.3 Logging pesado de resposta completa

Arquivos:

- `scripts/explore_schema.py:60`
- `scripts/explore_schema.py:97`
- `scripts/run_all_tests.py:60`
- `tests/python/test_conversion_report.py:72`

Impacto:

- Aumento de CPU para serializacao JSON.
- I/O alto em terminal/log.
- Maior tempo total em scripts de validacao.

## 2) Utilizacao de Recursos

### 2.1 Rede

- Ponto atual: sem pooling e sem retry.
- Efeito: conexoes menos eficientes e fragilidade a oscilacao.

### 2.2 Memoria

Arquivo: `examples/python/shopee_affiliate_client.py:372`

- `get_all_conversion_pages()` acumula tudo em `all_nodes`.
- Complexidade de memoria O(n) no numero total de itens retornados.

### 2.3 CPU e I/O

- Muitas chamadas de `json.dumps(..., indent=2, ensure_ascii=False)` em contexto de depuracao.
- Custo adicional significativo quando respostas crescem.

### 2.4 Confiabilidade da medicao

Arquivo: `tests/python/test_payload_format.py:31`

- Existe erro de sintaxe que impede parte da validacao automatizada.
- Isso reduz a confiabilidade de futuras comparacoes de performance em pipeline.

## 3) Eficiencia Algoritmica

### 3.1 Paginacao de conversao

Arquivo: `examples/python/shopee_affiliate_client.py:351`

- Modelo atual: carregar todas as paginas e juntar tudo.
- Melhor abordagem: iterador (`yield`) por pagina para reduzir memoria e iniciar processamento antes.

### 3.2 Execucao de suite de testes

Arquivo: `scripts/run_all_tests.py:312`

- Testes executam sequencialmente (latencia total cresce linearmente).
- Alguns testes de leitura podem ser concorrentes com limite de workers.

## 4) Estrategias de Cache

Estado atual:

- Nao ha cache de aplicacao para queries de leitura.
- Nao ha memoizacao para introspecoes repetidas.

Oportunidades:

1. Cache TTL curto para consultas de leitura:
   - `shopeeOfferV2`
   - `shopOfferV2`
   - `productOfferV2`
2. Nao cachear:
   - `generateShortLink` (mutacao)
   - `conversionReport` em cenarios de acompanhamento near-real-time

## Recomendacoes Especificas de Otimizacao

### Prioridade Alta

1. Adotar `requests.Session` com pool de conexao, `timeout` e retry exponencial.
2. Migrar todas as queries para GraphQL variables (query estavel + `variables`).
3. Substituir `get_all_conversion_pages()` por iterador e incluir:
   - `max_pages`
   - protecao contra `scrollId` repetido
   - controle de timeout por pagina

### Prioridade Media

4. Criar camada de cache TTL para endpoints de leitura com invalidacao simples.
5. Reduzir payload de log (resumo em vez de dump completo), com `debug` opcional.
6. Paralelizar testes independentes com limite de concorrencia respeitando rate limit da API.

### Prioridade Baixa

7. Instrumentar metricas simples de tempo por chamada e taxa de erro para comparativo continuo.

## Plano de Implementacao (Sugestao)

1. Fase 1:
   - HTTP session + timeout + retry.
   - Refatoracao para GraphQL variables.
2. Fase 2:
   - Paginacao streaming.
   - Reducao de logs verbosos.
3. Fase 3:
   - Cache TTL.
   - Medicao comparativa antes/depois.

## Resultado Esperado

- Menor latencia media por request.
- Menor variacao de tempo em caso de falhas transientes.
- Reducao do pico de memoria em relatorios grandes.
- Melhor previsibilidade operacional em scripts de teste e validacao.
