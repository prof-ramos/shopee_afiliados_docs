# Roadmap - Shopee Affiliate API Client

**Status**: Ativo - v0.1.0

---

## Visão Geral

Cliente Python não-oficial para API de Afiliados da Shopee Brasil com foco em:
- Estabilidade e compatibilidade com a API oficial
- Performance otimizada (usando uv e regex pré-compilado)
- Documentação completa e exemplos de uso
- Testes automatizados abrangentes

---

## ✅ Concluído

### v0.1.0 (Atual)

**Core:**
- ✅ Cliente Python básico para API Shopee Affiliate
- ✅ Autenticação SHA256 com assinatura dinâmica
- ✅ 5 endpoints implementados e testados:
  - `shopeeOfferV2` - Ofertas em destaque
  - `shopOfferV2` - Ofertas de lojas
  - `productOfferV2` - Busca de produtos
  - `generateShortLink` - Links de afiliado
  - `conversionReport` - Relatório de conversões

**Performance:**
- ✅ Função `_render()` otimizada com `re.sub()` (8.46x mais rápido)
- ✅ Cache de templates GraphQL
- ✅ Suporte a paginação eficiente

**Qualidade:**
- ✅ 16 testes automatizados (unitários + integração)
- ✅ CI/CD com GitHub Actions
- ✅ Lint com ruff
- ✅ Gerenciador de pacotes uv (10-100x mais rápido que pip)

**Documentação:**
- ✅ README.md com exemplos de uso
- ✅ Guia completo do uv (docs/GUIA_UV.md)
- ✅ Documentação de rastreamento de comissões (docs/RASTREAMENTO_COMISSOES.md)
- ✅ Análise de performance (docs/OTIMIZACAO_DESEMPENHO.md)
- ✅ Introspecção completa da API (docs/API_INTROSPECTION.md)

**Correções:**
- ✅ Removido `validatedReport` incorreto (não aceita filtros de tempo)
- ✅ Corrigido bug em `_render()` com templates GraphQL contendo `{ }`

---

## 🚧 Em Progresso

### Documentação

- ⏳ Atualizar AGENTS.md em src/shopee_affiliate/
- ⏳ Documentar estrutura completa dos tipos GraphQL

---

## 🎯 Próximos Passos

### Quando houver dados de conversão na conta de teste:

1. **Testar orderId como validationId**
   - Verificar se `orderId` do `conversionReport` funciona como `validationId`
   - Se funcionar, reimplementar `get_validated_report(validation_id)`

2. **Consultar suporte Shopee**
   - Perguntar como obter `validationId` válido
   - Solicitar exemplos de uso do `validatedReport`
   - Perguntar sobre requisitos para acesso ao `partnerOrderReport`

3. **Implementar partnerOrderReport**
   - Criar `partnerOrderReport.graphql`
   - Adicionar suporte no cliente Python
   - Este endpoint aceita filtros de tempo e pode substituir `validatedReport`

---

## 🔮 Futuro

### v0.2.0 (Planejado)

**Novos Endpoints:**
- [ ] `brandOffer` - Ofertas de marcas
- [ ] `generateBatchShortLink` - Links em lote
- [ ] `checkAffiliateId` - Verificar status de afiliado

**Melhorias:**
- [ ] Cache de links gerados (evitar re-geração)
- [ ] Retry automático com exponential backoff
- [ ] Suporte a assíncrono (async/await)
- [ ] Type hints completas com mypy

**Documentação:**
- [ ] Guias de uso avançado
- [ ] Exemplos de integração com web frameworks (FastAPI, Flask)
- [ ] Tutoriais em vídeo

### v0.3.0 (Futuro)

**Recursos Avançados:**
- [ ] Webhooks para notificações de conversão
- [ ] Dashboard de métricas
- [ ] Exportação de relatórios (CSV, Excel)
- [ ] Sistema de cache distribuído

**Performance:**
- [ ] Pool de conexões HTTP
- [ ] Compressão de requisições
- [ ] Query batching

---

## 🐛 Problemas Conhecidos

### validatedReport

**Status:** Removido na v0.1.0

**Problema:** O endpoint `validatedReport` da API requer um `validationId` obrigatório, mas não há documentação sobre como obtê-lo.

**Solução temporária:** Usar `conversionReport` que tem os mesmos dados de conversão.

**Planejamento:**
- Quando houver dados reais, testar se `orderId` funciona como `validationId`
- Consultar suporte Shopee para esclarecimento

### partnerOrderReport

**Status:** Não implementado

**Problema:** Retorna erro 10031 (access deny) - possivelmente requer permissão especial.

**Planejamento:** Implementar quando disponível, pois aceita filtros de tempo como `conversionReport`.

---

## 📝 Notas de Versão

### v0.1.0 (2026-02-16)

**Adicionado:**
- Cliente Python básico para API Shopee Affiliate
- 5 endpoints principais
- Suporte a paginação
- Geração de links de afiliado com sub-IDs
- Testes automatizados
- CI/CD com GitHub Actions
- Documentação completa
- Gerenciador uv

**Removido:**
- `validatedReport` (implementação incorreta)

**Corrigido:**
- Bug em `_render()` com templates GraphQL contendo `{ }`
- CI/CD para usar `uv --system`

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas prioritárias:

1. **Testes** - Mais cobertura de cenários edge case
2. **Documentação** - Exemplos de uso, tutoriais
3. **Performance** - Benchmarks, otimizações
4. **Type Safety** - Mypy, type hints

---

## 📄 Licença

MIT - ver [LICENSE](LICENSE)

---

**Última atualização:** 2026-02-16
