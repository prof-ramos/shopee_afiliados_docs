# Politica de Seguranca

Este documento descreve as politicas e procedimentos de seguranca para o projeto Shopee Afiliados Docs.

## Versoes Suportadas

Atualmente, fornecemos atualizacoes de seguranca apenas para a versao mais recente do projeto.

## Reportando Vulnerabilidades

Acreditamos que trabalhar com pesquisadores de seguranca responsaveis e crucial para manter a seguranca de nossos usuarios. Agradecemos seus esforcos para revelar vulnerabilidades de forma responsavel.

### Como Reportar

**Nao** crie issues publicas no GitHub para vulnerabilidades de seguranca.

Em vez disso, envie um email para:

**Email:** `security@shopeeafiliadosdocs.com`

### O Que Incluir

Para nos ajudar a resolver o problema rapidamente, inclua:

- Descricao detalhada da vulnerabilidade
- Passos para reproduzir a vulnerabilidade
- Versao afetada
- Possiveis solucoes (se conhecidas)
- Seu nome/contato (opcional, para reconhecimento)

### Processo

1. **Confirmacao**: Responderemos ao seu email dentro de 48 horas confirmando o recebimento
2. **Analise**: Investigaremos a vulnerabilidade e determinaremos a severidade
3. **Correcao**: Trabalharemos em uma correcao
4. **Divulgacao**: Divulgaremos publicamente apos a correcao estar disponivel

### Coordenacao de Divulgacao

Geralmente, aguardamos ate que a correcao esteja disponivel antes de tornar a vulnerabilidade publica. Se voce quiser divulgar antes, entre em acordo conosco sobre os prazos.

## Politica de Privacidade

### Credenciais e Segredos

**IMPORTANTE:** Este projeto usa credenciais da API Shopee Affiliate. Nunca commit credenciais no repositorio!

- O arquivo `.env` esta no `.gitignore` e nunca deve ser commitado
- Use variaveis de ambiente para todas as credenciais
- Nunca exiba logs com credenciais completas
- Use mascaramento de logs para segredos (ex: `APP_SECRET[:10] + "..."`)

### Dados do Usuario

Este projeto:
- Nao coleta dados pessoais de usuarios
- Nao armazena informacoes sensiveis em servidores externos
- Nao faz tracking de usuarios

## Dependencias

### Gerenciamento de Dependencias

O projeto usa as seguintes dependencias principais:

- `python-dotenv>=1.0.0` - Carregamento de variaveis de ambiente
- `requests>=2.32.0` - Cliente HTTP para chamadas de API

### Atualizacoes de Seguranca

- As dependencias sao auditadas regularmente
- Atualizacoes de seguranca serao aplicadas assim que disponiveis
- Use `uv pip install --upgrade -r requirements.txt` para atualizar

### Auditando Dependencias

Para auditar dependencias por vulnerabilidades conhecidas:

```bash
# Instalar ferramentas de seguranca
pip install safety

# Verificar vulnerabilidades
safety check -r requirements.txt
```

## Melhores Praticas de Seguranca

### Para Desenvolvedores

1. **Nunca commit credenciais**
   - Use `.env` para variaveis de ambiente locais
   - Use variaveis de ambiente em producao
   - Verifique o `.gitignore` antes de cada commit

2. **Revise as mudancas**
   - Revise seu proprio diff antes de commitar
   - Certifique-se de que nenhum segredo foi adicionado

3. **Use branches de seguranca**
   - Crie branches separados para correcoes de seguranca
   - Siga o processo de code review

### Para Usuarios

1. **Proteja suas credenciais**
   - Nunca compartilhe seu `SHOPEE_APP_ID` e `SHOPEE_APP_SECRET`
   - Use arquivos `.env` separados para ambientes diferentes
   - Revogue credenciais vazadas imediatamente

2. **Mantenha dependencias atualizadas**
   - Atualize regularmente: `uv pip install --upgrade -r requirements.txt`

3. **Monitore seu uso da API**
   - Fique de olho em atividades suspeitas
   - Configure alertas se a API fornecer

## Vulnerabilidades Conhecidas

Nenhuma vulnerabilidade conhecida no momento.

Consulte nossa pagina de [Security Advisories](https://github.com/SEU_USUARIO/shopee_afiliados_docs/security/advisories) para atualizacoes.

## Contato de Seguranca

Para questoes gerais de seguranca:

- **Email:** `security@shopeeafiliadosdocs.com`
- **PGP Key:** [Disponivel sob solicitacao]

Para emergencias de seguranca, use o mesmo endereco de email com o assunto "URGENT".

## Agradecimentos

Gostariamos de agradecer a todos os pesquisadores de seguranca que ajudam a manter o projeto seguro contribuindo com relatorios de vulnerabilidades responsaveis.

## Recursos Adicionais

- [Politica de Seguranca da Shopee](https://shopee.com.br/legal/privacy-policy)
- [Documentacao de Autenticacao da API](https://open-api.affiliate.shopee.com.br/docs)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)

---

Ultima atualizacao: 16 de Fevereiro de 2026
