# Plano de Investigação: validationId

**Objetivo**: Descobrir como obter um `validationId` válido para usar o endpoint `validatedReport`

## Status Atual

O endpoint `validatedReport` existe e funciona, mas requer um `validationId` que ainda não sabemos como obter.

**Argumentos corretos do validatedReport:**
```graphql
query {
  validatedReport(
    validationId: Int64!  # OBRIGATÓRIO - valor desconhecido
    limit: Int
    scrollId: String
  ) {
    nodes {
      orders {
        orderId
        ...
      }
    }
  }
}
```

## Hipóteses sobre validationId

### Hipótese 1: ID de conversão do conversionReport
O `validationId` pode ser obtido a partir de uma conversão no `conversionReport`.

**Passos para validar:**
1. Buscar dados do `conversionReport`
2. Procurar por campos com "validation", "id" ou similares
3. Testar se algum campo serve como `validationId`

```python
# Teste
result = client.get_conversion_report(...)
nodes = result['data']['conversionReport']['nodes']
# Procurar por campos com ID
for node in nodes:
    print(json.dumps(node, indent=2))
    # Verificar se há conversionId, orderSn, etc.
```

### Hipótese 2: ID de pedido (orderId)
O `validationId` pode ser simplesmente o `orderId`.

**Passos para validar:**
1. Obter um `orderId` do `conversionReport`
2. Usar como `validationId` no `validatedReport`
3. Verificar se retorna dados

```python
# Teste
order_id = "123456789"
result = client._request("""
query {
  validatedReport(
    validationId: %s
    limit: 10
  ) { ... }
}
""" % order_id)
```

### Hipótese 3: ID específico de validação (obtido via outro endpoint)
Pode existir um endpoint ou webhook que fornece os `validationId`s.

**Possíveis fontes:**
- Webhooks da Shopee
- Endpoint de notificações
- Painel do afiliado (web scraping)
- API de sincronização

### Hipótese 4: Campo oculto no conversionReport
O `conversionReport` pode ter um campo que não estamos buscando.

**Ação:**
- Fazer introspecção completa do tipo retornado por `conversionReport`
- Buscar TODOS os campos disponíveis
- Procurar por anything com "validation" no nome

## Plano de Ação

### Fase 1: Investigação via Introspecção

1. **Introspecção profunda do conversionReport**
   ```python
   # Query de introspecção específica
   query {
     __type(name: "ConversionReportNode") {
       fields {
         name
         type {
           name
           fields {
             name
           }
         }
       }
     }
   }
   ```

2. **Buscar dados reais do conversionReport**
   - Obter uma amostra de conversões
   - Examinar TODOS os campos retornados
   - Documentar cada campo e seu possível significado

### Fase 2: Testes Práticos

1. **Testar com conversionId**
   ```python
   result = client.get_conversion_report(
       conversion_id=123456,  # Se disponível
       limit=1
   )
   ```

2. **Testar com orderId**
   ```python
   query = """
   query {
     validatedReport(validationId: %s, limit: 1) {
       nodes { __typename }
     }
   }
   """ % order_id
   ```

3. **Testar com checkoutId**
   ```python
   query = """
   query {
     validatedReport(validationId: %s, limit: 1) {
       nodes { __typename }
     }
   }
   """ % checkout_id
   ```

### Fase 3: Consulta à Documentação

1. **Verificar documentação oficial da Shopee**
   - https://www.affiliateshopee.com.br/documentacao
   - https://open-api.affiliate.shopee.com.br/explorer

2. **Procurar por exemplos de uso**
   - Repositórios GitHub
   - Fóruns de desenvolvedores
   - Comunidade de afiliados

### Fase 4: Contato com Suporte

Se as fases anteriores não resolverem:
- Abrir ticket no portal de afiliados
- Perguntar sobre como obter `validationId`
- Solicitar exemplos de uso

## Critérios de Sucesso

O plano será considerado bem-sucedido quando:
- ✅ Descobrirmos como obter um `validationId` válido
- ✅ Conseguirmos chamar `validatedReport` com sucesso
- ✅ Implementarmos o suporte no cliente Python
- ✅ Documentarmos o processo

## Alternativa: partnerOrderReport

Se `validatedReport` não for viável, `partnerOrderReport` pode ser a alternativa:

**Vantagens:**
- Aceita filtros de tempo (`purchaseTimeStart/End`)
- Interface similar ao `conversionReport`
- Possivelmente mais atual

**Desvantagens:**
- Requer permissão especial (erro 10031)
- Pode não estar disponível para todos os afiliados
- Documentação limitada

## Próximos Passos

1. ✅ **Fase 1**: Executar introspecção profunda
2. ⏳ **Fase 2**: Testar hipóteses práticas
3. ⏳ **Fase 3**: Consultar documentação
4. ⏳ **Fase 4**: Contatar suporte (se necessário)

---

**Data de criação**: 2026-02-16
**Status**: 🔄 Em andamento
**Prioridade**: Média (conversionReport está funcionando)
