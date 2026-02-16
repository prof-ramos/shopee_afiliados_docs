# Resultado da Investigação: validationId

**Data**: 2026-02-16
**Status**: ⚠️ Inconclusivo (falta de dados na conta de teste)

---

## Descobertas

### Estrutura do conversionReport

```graphql
conversionReport → ConversionReportConnection {
  nodes: [ConversionReportNode]!
  pageInfo: PageInfo!
}

ConversionReportNode {
  orders: [ConversionReportOrder!]!
}

ConversionReportOrder {
  orderId: String!           # ← Possível validationId
  shopType: ShopType!
  orderStatus: DisplayOrderStatus!
  items: [ConversionReportItem!]!
}
```

### Campos Disponíveis

**Tipo `ConversionReportOrder`:**
- `orderId` (String)
- `shopType` (ShopType)
- `orderStatus` (DisplayOrderStatus)
- `items` (Lista de itens)

**Campos NÃO disponíveis:**
- ❌ `checkoutId`
- ❌ `conversionId`
- ❌ `orderSn`

---

## Hipóteses Testadas

Nenhuma hipótese pôde ser testada porque **não há conversões na conta de teste** (período de 90 dias).

### Hipóteses pendentes de teste:

1. **validationId = orderId**
   - Mais provável (único campo ID disponível)
   - Requer dados reais para teste

2. **validationId de outro endpoint**
   - Pode vir de webhook/notificação
   - Pode estar em outro campo não documentado

---

## Conclusão

**Não foi possível descobrir o `validationId` porque:**

1. A conta de teste não tem conversões
2. Não há documentação oficial disponível
3. O endpoint `validatedReport` requer um `validationId` específico

---

## Recomendações

### Imediato

1. **Usar `conversionReport`** (já funciona)
   - Tem todos os filtros necessários
   - Retorna dados de conversões
   - 100% funcional

2. **Monitorar `partnerOrderReport`**
   - Aceita filtros de tempo
   - Pode ser substituto direto
   - Atualmente retorna "access deny" (erro 10031)

### Futuro

Quando houver dados reais de conversões:

1. **Testar orderId como validationId**
   ```python
   query = """
   query {
     validatedReport(
       validationId: "ORDER_ID_DO_CONVERSIONREPORT"
       limit: 10
     ) { ... }
   }
   """
   ```

2. **Consultar suporte Shopee**
   - Perguntar como obter `validationId`
   - Solicitar exemplos de uso

3. **Verificar webhooks**
   - A Shopee pode enviar notificações com `validationId`

---

## Alternativa: partnerOrderReport

Se disponível no futuro:

```python
# Este endpoint tem filtros de tempo!
query {
  partnerOrderReport(
    purchaseTimeStart: 1700000000
    purchaseTimeEnd: 1700000000
    limit: 100
  ) {
    nodes { ... }
  }
}
```

**Status atual:** Erro 10031 (access deny)
**Possível causa:** Requer permissão especial ou nível mais alto de afiliado

---

## Arquivos Gerados

- `docs/REPORTS_ANALYSIS.md` - Análise completa dos endpoints
- `docs/PLANO_VALIDATION_ID.md` - Plano de investigação
- `docs/API_INTROSPECTION.md` - Documentação da API via introspecção
- `tests/investigate_validation_id.py` - Script de investigação
- `tests/full_introspection.py` - Script de introspecção completa

---

## Próximos Passos

- [x] Remover validatedReport quebrado (Opção 1) - ✅ FEITO
- [x] Criar plano para investigar validationId (Opção 3) - ✅ FEITO
- [ ] Testar hipóteses quando houver dados de conversão
- [ ] Consultar suporte Shopee sobre validationId
- [ ] Implementar partnerOrderReport quando disponível
