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

Fazer o MCP client
    https://github.com/alejandro-ao/mcp-client-python/blob/master/api/mcp_client.py

Usar MCP de conversao de moeda
    https://medium.com/@sin4ch/building-a-simple-exchange-rate-mcp-server-using-fastmcp-c87d7a454545
    https://github.com/wesbos/currency-conversion-mcp

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