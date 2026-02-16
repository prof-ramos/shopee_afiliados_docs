# Diagramas de Fluxo - API Shopee Affiliate

**Versão:** 0.1.0
**Data:** 2026-02-16

---

## Índice

1. [Fluxo de Autenticação](#fluxo-de-autenticação)
2. [Fluxo de Geração de Link](#fluxo-de-geração-de-link)
3. [Fluxo de Consulta de Ofertas](#fluxo-de-consulta-de-ofertas)
4. [Fluxo de Rastreamento de Comissões](#fluxo-de-rastreamento-de-comissões)
5. [Fluxo de Relatórios](#fluxo-de-relatórios)
6. [Arquitetura do Cliente](#arquitetura-do-cliente)

---

## Fluxo de Autenticação

```mermaid
sequenceDiagram
    participant App as Aplicação
    participant Client as ShopeeAffiliateClient
    participant Auth as Auth Module
    participant API as API Shopee

    App->>Client: new Client(app_id, app_secret)
    Client->>Client: armazena credenciais

    App->>Client: get_shopee_offers()
    Client->>Auth: generate_signature()

    Auth->>Auth: timestamp = now()
    Auth->>Auth: message = f"{app_id}{timestamp}"
    Auth->>Auth: hmac_sha256(app_secret, message)
    Auth->>Auth: return signature

    Client->>Client: adiciona headers:
    Client->>Client: - app_id
    Client->>Client: - timestamp
    Client->>Client: - signature

    Client->>API: POST /graphql
    Note over Client,API: Query + Headers de autenticação

    API->>API: valida signature
    API-->>Client: 200 OK + dados
    Client-->>App: ofertas retornadas
```

---

## Fluxo de Geração de Link

```mermaid
flowchart TD
    Start([Início]) --> Input[URL do Produto]
    Input --> ValidateSubIDs{Sub-IDs?}

    ValidateSubIDs -->|Sim| CheckSubIDs[Validar Sub-IDs]
    ValidateSubIDs -->|Não| BuildQuery

    CheckSubIDs -->|Inválido| Error[Erro 11001]
    CheckSubIDs -->|Válido| BuildQuery[Montar Query GraphQL]

    BuildQuery --> Sign[Assinar Requisição]
    Sign --> Send[Enviar para API]

    Send --> APIResponse{Resposta da API}

    APIResponse -->|Erro| ErrorHandler[Tratar Erro]
    APIResponse -->|Sucesso| Extract[Extrair Short Link]

    Extract --> Cache[Armazenar em Cache]
    Cache --> End([Retornar s.shopee.com.br])

    ErrorHandler --> Error
```

---

## Fluxo de Consulta de Ofertas

```mermaid
flowchart LR
    A[Usuário] --> B{Tipo de Busca?}

    B -->|Destaque| C[shopeeOfferV2]
    B -->|Loja| D[shopOfferV2]
    B -->|Produto| E[productOfferV2]

    C --> F[API Shopee]
    D --> F
    E --> F

    F --> G{Resultado?}
    G -->|Vazio| H[Retornar vazio]
    G -->|Dados| I[Processar Ofertas]

    I --> J[Filtrar por Comissão]
    J --> K[Ordenar]
    K --> L[Paginar]
    L --> M[Retornar Lista]
```

---

## Fluxo de Rastreamento de Comissões

```mermaid
sequenceDiagram
    participant User as Usuário
    participant Bot as Bot Telegram
    participant API as API Shopee
    participant Cookie as Cookie Browser

    Note over User,Cookie: Fase 1: Descoberta
    Bot->>API: productOfferV2(keyword="tenis")
    API-->>Bot: Lista de produtos

    Note over User,Cookie: Fase 2: Geração de Link
    Bot->>API: generateShortLink(productId=123)
    API-->>Bot: s.shopee.com.br/abc123

    Note over User,Cookie: Fase 3: Clique
    User->>Bot: Clica no link
    Bot->>User: Redireciona para s.shopee.com.br/abc123

    Note over User,Cookie: Fase 4: Atribuição
    s.shopee.com.br/abc123->>Cookie: Define cookie 7d
    Cookie->>Cookie: affiliate_id=USER123

    Note over User,Cookie: Fase 5: Compra
    User->>User: Navega e compra
    User->>Cookie: Cookie enviado com pedido

    Note over User,Cookie: Fase 6: Comissão
    Cookie->>API: Conversão registrada
    API-->>Bot: conversionReport mostra comissão
```

---

## Fluxo de Relatórios

```mermaid
flowchart TD
    Start([Início]) --> ChooseReport{Tipo de Relatório?}

    ChooseReport -->|Conversões| CR[conversionReport]
    ChooseReport -->|Validadas| VR[validatedReport<br/>❌ Não disponível]
    ChooseReport -->|Parceiro| PR[partnerOrderReport<br/>❌ Sem acesso]

    CR --> SetPeriod[Definir Período]
    SetPeriod --> CallAPI[Chamar API com filtros]

    CallAPI --> HasNext{Próxima Página?}
    HasNext -->|Sim| Process[Processar Dados]
    HasNext -->|Não| End([Fim])

    Process --> Accumulate[Acumular Resultados]
    Accumulate --> GetScroll[Obter scrollId]
    GetScroll --> CallAPI

    VR --> Error[Endpoint requer validationId]
    PR --> Error2[Erro 10031: Access Deny]
```

---

## Fluxo de Rastreamento com Sub-IDs

```mermaid
stateDiagram-v2
    [*] --> Descoberta: Bot busca produto
    Descoberta --> LinkGerado: generateShortLink()

    LinkGerado --> SubIDs: subIds=["tg","grupo"]
    SubIDs --> LinkCriado: s.shopee.com.br/xyz

    state LinkCriado {
        [*] --> AguardandoClique
        AguardandoClique --> CliqueRecebido: Usuário clica

        CliqueRecebido --> Redirecionamento: Redireciona p/ Shopee
        Redirecionamento --> CookieDefinido: Cookie 7 dias

        CookieDefinido --> Navegacao: Usuário navega
        Navegacao --> Compra: Compra realizada
    }

    LinkCriado --> Conversao: Conversão registrada
    Conversao --> Relatorio: conversionReport
    Relatorio --> [*]: utm_content=tg.grupo

    note right of SubIDs
        Sub-IDs são concatenados
        com "." no relatório
    end note
```

---

## Arquitetura do Cliente

```mermaid
classDiagram
    class ShopeeAffiliateClient {
        -app_id: str
        -app_secret: str
        -transport: ShopeeAffiliateTransport
        +get_shopee_offers()
        +get_shop_offers()
        +get_product_offers()
        +generate_short_link()
        +get_conversion_report()
        +iter_conversion_report_pages()
    }

    class ShopeeAffiliateTransport {
        -app_id: str
        -app_secret: str
        -base_url: str
        +request()
        -_sign_request()
    }

    class AuthModule {
        +generate_signature()
        +build_headers()
    }

    class QueriesModule {
        +q_shopee_offer_v2()
        +q_shop_offer_v2()
        +q_product_offer_v2()
        +q_conversion_report()
        +m_generate_short_link()
        +_render()
        +_load()
    }

    class Validators {
        +validate_sub_ids()
    }

    ShopeeAffiliateClient --> ShopeeAffiliateTransport
    ShopeeAffiliateClient --> QueriesModule
    ShopeeAffiliateClient --> Validators
    ShopeeAffiliateTransport --> AuthModule
    QueriesModule --> AuthModule
```

---

## Fluxo de Paginação com ScrollId

```mermaid
sequenceDiagram
    participant Client as Cliente
    participant API as API Shopee

    Note over Client,API: Primeira página
    Client->>API: conversionReport(limit=100)
    API-->>Client: nodes[0..99] + scrollId="abc123"
    Client->>Client: Processa página 1

    Note over Client,API: Segunda página
    Client->>API: conversionReport(scrollId="abc123")
    API-->>Client: nodes[100..199] + scrollId="def456"
    Client->>Client: Processa página 2

    Note over Client,API: Última página
    Client->>API: conversionReport(scrollId="def456")
    API-->>Client: nodes[] + hasNextPage=false
    Client->>Client: Fim da paginação
```

---

## Fluxo de Tratamento de Erros

```mermaid
flowchart TD
    Start([Chamada API]) --> Response{Resposta}

    Response -->|200 OK| CheckErrors{Tem Errors?}
    Response -->|4xx/5xx| Retry

    CheckErrors -->|Sim| GetCode{Código Erro}
    CheckErrors -->|Não| Success

    GetCode -->|10010| ParamError[Parâmetro inválido]
    GetCode -->|10020| AuthError[Assinatura inválida]
    GetCode -->|11001| SubIDError[Sub-ID inválido]
    GetCode -->|Outro| GenericError[Erro genérico]

    ParamError --> Log[Logar erro]
    AuthError --> Log
    SubIDError --> Log
    GenericError --> Log

    Log --> Fail([Falha])

    Retry --> Count{Tentativas < 3?}
    Count -->|Sim| Wait[Exponential Backoff]
    Count -->|Não| Fail

    Wait --> Start

    Success --> End([Sucesso])
```

---

## Ciclo de Vida do Link de Afiliado

```mermaid
timeline
    title Ciclo de Vida do Link de Afiliado
    section Descoberta
        Bot busca produto : productOfferV2("tenis")<br/>Retorna: Lista com comissão
    section Geração
        Bot gera link : generateShortLink(url, subIds)<br/>Retorna: s.shopee.com.br/abc123
    section Clique
        Usuário clica : Bot envia link<br/>Redirecionamento para Shopee
    section Atribuição
        Cookie depositado :affiliate_id definido<br/>Validade: 7 dias
    section Compra
        Usuário compra : Qualquer produto no período<br/>Registra conversão
    section Comissão
        Conversão registrada : conversionReport mostra<br/>utmc_content=sub_ids
```

---

## Integração com Bot Telegram

```mermaid
flowchart LR
    User[Usuário Telegram] --> Command[Comando /buscar]
    Command --> Bot[Bot Python]

    Bot --> Search[productOfferV2]
    Search --> Results[Lista de Produtos]

    Results --> Format[Formatar Mensagem]
    Format --> Link[generateShortLink<br/>subIds=["telegram"]]

    Link --> Send[Enviar para Usuário]
    Send --> User

    User --> Click[Clicar no Link]
    Click --> Track[Rastreamento Iniciado]
    Track --> Comm[Comissão Registrada]
```

---

## Fluxo de Cache de Links

```mermaid
flowchart TD
    Start([Solicita Link]) --> CheckCache{Cache Hit?}

    CheckCache -->|Sim| ReturnCache[Retornar Link Cacheado]
    CheckCache -->|Não| Generate[Gerar Novo Link]

    Generate --> API[Chamar API]
    API --> Success{Sucesso?}

    Success -->|Sim| Save[Salvar no Cache]
    Success -->|Não| Error[Retornar Erro]

    Save --> ReturnAPI[Retornar Link Novo]

    ReturnCache --> End([Fim])
    ReturnAPI --> End
    Error --> End

    style ReturnCache fill:#90EE90
    style ReturnAPI fill:#87CEEB
    style Error fill:#FFB6C1
```

---

**Última atualização:** 2026-02-16
