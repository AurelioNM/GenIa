# Generative IA studies

### To Do List
- gen-ia
    - [ ] implementar guardrails
    - transformar em tools os seguintes fluxos
        - [X] processar compra
        - [X] sugerir produto baseado em categoria
        - [X] sugerir produto baseado em historico de compras
        - [X] sugestao baseada no clima
        - [X] reponder Q&A do tarantino
    - MCP server
        - [ ] subir service novo como MCP server
            - input: Qual e a frase/sabedoria do dia?
            - output: {server pega uma frase aleatoria e devolve}
- Observability
    - [ ] gerar metricas
    - [ ] config prometheus
    - [ ] criar dashs basicos no grafana
- Tests
	- [X] test end to end chat intantions
    - [X] testes unitarios para product-service
    - [ ] testes unitarios para customer-service
    - [ ] testes unitarios para forecast-service
    - [ ] testes unitarios para product-service
	- [ ] basic load tests
- Debitos funcionais/tecnicos
    - [ ] cenario de cliente tentar comprar produtos que nao existam
    - [ ] cenario de cliente tentar pedir sugestao de categoria que nao exista
    - [ ] fazer a IA perguntar quais produtos se o cliente falar que quer comprar, mas nao especificar quais
    - [ ] cliente pediu sugestao de produto baseado no historico, mas nao tem compras anteriores

Ver padrao langchain expression language
    chain = prompt | model

Usar padrao Langchain V1
    https://docs.langchain.com/oss/python/releases/langchain-v1

MCP
    Fazer o MCP client
        https://github.com/alejandro-ao/mcp-client-python/blob/master/api/mcp_client.py

    Usar MCP de conversao de moeda
        https://medium.com/@sin4ch/building-a-simple-exchange-rate-mcp-server-using-fastmcp-c87d7a454545
        https://github.com/wesbos/currency-conversion-mcp

    Como definir um fallback em caso de erro no MCP server, ou mensagens guiando a llm sobre como lidar com o erro
        Talvez perguntar pro usuario se ele gostaria de re-tentar o pedido
    Como o time de GenIa esta lidando com seguranca/autorizacao

Langfuse para observabilidade na LLM
    https://github.com/langfuse/langfuse?tab=readme-ov-file

Ver curso LangGraph

Separar order-service:
    purchase mcp server
    chat-agent-service

melhorar criacao de documentos + upload
    - script para gerar csv de Q&A
    - rota para upload de documento
    - script para upload de documento

scriptar criacao de vector_index

Exemplo configurando agent com tools
    currency_agent = LlmAgent(
        name="currency_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a smart currency conversion assistant.

        For currency conversion requests:
        1. Use `get_fee_for_payment_method()` to find transaction fees
        2. Use `get_exchange_rate()` to get currency conversion rates
        3. Check the "status" field in each tool's response for errors
        4. Calculate the final amount after fees based on the output from `get_fee_for_payment_method` and `get_exchange_rate` methods and provide a clear breakdown.
        5. First, state the final converted amount.
            Then, explain how you got that result by showing the intermediate amounts. Your explanation must include: the fee percentage and its
            value in the original currency, the amount remaining after the fee, and the exchange rate used for the final conversion.

        If any tool returns status "error", explain the issue to the user clearly.
        """,
        tools=[get_fee_for_payment_method, get_exchange_rate],
    )

Exemplo error message para tool
    "A tool that retrieves product data could return a response that says "No product data found for product ID XXX. Ask the customer to confirm the product name, and look up the product ID by name to confirm you have the correct ID.""