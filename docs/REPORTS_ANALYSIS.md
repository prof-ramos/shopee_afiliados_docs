# Análise de Relatórios - API Shopee Affiliate

**Data**: 2026-02-16
**Status**: 🚨 BUG CRÍTICO ENCONTRADO

---

## Resumo Executivo

A introspecção completa da API revelou que o endpoint `validatedReport` está sendo usado **INCORRETAMENTE** no código atual.

---

## Endpoints Disponíveis

### 1. conversionReport ✅

**Status**: Funcionando corretamente

**Argumentos**: (muitos filtros disponíveis)
- `purchaseTimeStart` / `purchaseTimeEnd`
- `completeTimeStart` / `completeTimeEnd`
- `shopName`, `shopId`, `shopType`
- `conversionId`, `conversionStatus`
- `orderId`, `productName`, `productId`
- `categoryLv1Id`, `categoryLv2Id`, `categoryLv3Id`, `categoryType`
- `orderStatus`, `buyerType`, `productType`, `fraudStatus`
- `device`, `attributionType`, `campaignPartnerName`, `campaignType`
- `limit`, `scrollId`

**Uso**: Relatório de conversões (comissões estimadas)

**Implementação atual**: ✅ CORRETA

---

### 2. validatedReport ❌ **INCORRETO**

**Status**: CÓDIGO ATUAL ESTÁ ERRADO!

**Argumentos CORRETOS** (segundo introspecção):
- `validationId`: Int64! (OBRIGATÓRIO)
- `limit`: Int
- `scrollId`: String

**Argumentos INCORRETOS** (usados no código atual):
- ❌ `purchaseTimeStart` - **NÃO EXISTE**
- ❌ `purchaseTimeEnd` - **NÃO EXISTE**

**Erro retornado pela API**:
```
Unknown argument "purchaseTimeStart" on field "validatedReport"
Código: 10010
```

**Problema**:
- Não sabemos como obter um `validationId` válido
- O teste `test_validated_report.py` pode estar passando falsamente (sem dados reais)

**Implementação atual**: ❌ PRECISA SER CORRIGIDA

---

### 3. partnerOrderReport ⚠️

**Status**: Não disponível (erro de permissão)

**Argumentos**:
- `purchaseTimeStart` / `purchaseTimeEnd`
- `completeTimeStart` / `completeTimeEnd`
- `limit`
- `searchNextToken`

**Erro retornado**:
```
error [10031]: access deny
```

**Possível causa**:
- Requer permissão especial ou nível de afiliado mais alto
- Pode estar em fase de testes/rollout

**Implementação atual**: ❌ NÃO IMPLEMENTADO

---

## Problemas Encontrados

### Arquivo: `src/shopee_affiliate/graphql/validatedReport.graphql`

```graphql
# ❌ INCORRETO
query {
  validatedReport(
    purchaseTimeStart: {{purchaseTimeStart}}  # ❌ NÃO ACEITO
    purchaseTimeEnd: {{purchaseTimeEnd}}      # ❌ NÃO ACEITO
    {{scrollIdLine}}
    limit: {{limit}}
  ) {
    ...
  }
}
```

### Arquivo: `src/shopee_affiliate/queries.py`

```python
# ❌ INCORRETO
def q_validated_report(
    *,
    purchase_time_start: int,   # ❌ NÃO USADO
    purchase_time_end: int,     # ❌ NÃO USADO
    scroll_id: Optional[str],
    limit: int,
) -> str:
    return _render(
        _VALIDATED_REPORT,
        {
            "purchaseTimeStart": str(purchase_time_start),  # ❌ INVALID
            "purchaseTimeEnd": str(purchase_time_end),      # ❌ INVALID
            "scrollIdLine": scroll_id_line,
            "limit": str(limit),
        },
    )
```

### Arquivo: `src/shopee_affiliate/client.py`

```python
# ❌ INCORRETO
def get_validated_report(
    self,
    purchase_time_start: int,   # ❌ PARÂMETRO INÚTIL
    purchase_time_end: int,     # ❌ PARÂMETRO INÚTIL
    scroll_id: Optional[str] = None,
    limit: int = 10,
) -> Dict[str, Any]:
    """Retorna relatório de comissões validadas (definitivas).

    Diferente de conversionReport, este endpoint retorna apenas comissões
    que já foram validadas pela Shopee, ou seja, valores definitivos.
    """
    query = queries.q_validated_report(  # ❌ CHAMA FUNÇÃO ERRADA
        purchase_time_start=purchase_time_start,
        purchase_time_end=purchase_time_end,
        scroll_id=scroll_id,
        limit=limit,
    )
    return self._request(query)
```

---

## Recomendações

### Opção 1: Remover validatedReport (Recomendado)

Como não sabemos como obter `validationId`, a melhor opção é:

1. **Manter apenas `conversionReport`** - funciona corretamente
2. **Remover** `validatedReport` do código (graphql, queries, client)
3. **Documentar** que `partnerOrderReport` pode ser adicionado no futuro

**Vantagens**:
- Código limpo e funcional
- Sem endpoints quebrados
- Foco no que funciona

**Desvantagens**:
- Perda da funcionalidade "comissões validadas" (mas nunca funcionou mesmo)

---

### Opção 2: Refactor validatedReport

Se descobrirmos como obter `validationId`:

1. Mudar assinatura para aceitar `validation_id` em vez de `purchase_time_start/end`
2. Adicionar método auxiliar para obter `validationId` (se possível)
3. Manter `conversionReport` como relatório principal

---

### Opção 3: Implementar partnerOrderReport

Se o usuário obtiver acesso/permissão:

1. Criar `partnerOrderReport.graphql`
2. Adicionar `q_partner_order_report()` em queries.py
3. Adicionar `get_partner_order_report()` em client.py
4. Este pode ser o substituto ideal para `validatedReport`

---

## Plano de Ação Imediato

1. ✅ Introspecção completa - FEITO
2. ⏳ Corrigir/remover código de `validatedReport`
3. ⏳ Atualizar documentação
4. ⏳ Atualizar testes
5. ⏳ Commit com correções

---

## Testes Executados

```bash
# Teste comparativo
python tests/test_reports_comparison.py

# Resultados:
# ✅ conversionReport               - OK
# ❌ validatedReport (params tempo)  - ERRO: Unknown argument
# ❌ validatedReport (validationId)  - ERRO: invalid validation id
# ❌ partnerOrderReport              - ERRO: access deny
```

---

## Arquivos Gerados

- `docs/introspection_raw.json` - JSON bruto da introspecção
- `docs/API_INTROSPECTION.md` - Documentação Markdown gerada
- `tests/test_reports_comparison.py` - Teste comparativo
- `tests/introspect_partner_order.py` - Script de introspecção
- `tests/full_introspection.py` - Script de introspecção completa

---

## Próximos Passos

Aguardando decisão do usuário:
- [ ] Opção 1: Remover validatedReport
- [ ] Opção 2: Refactor para usar validationId
- [ ] Opção 3: Implementar partnerOrderReport
- [ ] Outra abordagem?

---

## Referências

- **Introspecção completa**: `docs/API_INTROSPECTION.md`
- **JSON bruto**: `docs/introspection_raw.json`
- **Teste comparativo**: `tests/test_reports_comparison.py`
