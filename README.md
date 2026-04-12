# Generative IA studies

### Backlog
- Observability
    - [ ] Langfuse para observabilidade na LLM - https://github.com/langfuse/langfuse?tab=readme-ov-file
    - [ ] gerar metricas
    - [ ] config prometheus
    - [ ] criar dashs basicos no grafana
- Tests
	- [X] test end to end chat intantions
	- [X] k6 performance tests - weather-service
- Debitos funcionais/tecnicos
    - [ ] cliente pediu sugestao de produto baseado no historico, mas nao tem compras anteriores
    - [ ] fazer a IA perguntar quais produtos se o cliente falar que quer comprar, mas nao especificar quais
    - [ ] cenario de cliente tentar comprar produtos que nao existam
    - [ ] cenario de cliente tentar pedir sugestao de categoria que nao exista
    - [ ] melhorar criacao de documentos + upload
        - script para gerar csv de Q&A
        - rota para upload de documento
        - script para upload de documento


Ver padrao langchain expression language
    chain = prompt | model

Usar padrao Langchain V1
    https://docs.langchain.com/oss/python/releases/langchain-v1

MCP
    Usar MCP de conversao de moeda
        https://medium.com/@sin4ch/building-a-simple-exchange-rate-mcp-server-using-fastmcp-c87d7a454545
        https://github.com/wesbos/currency-conversion-mcp

    Como definir um fallback em caso de erro no MCP server, ou mensagens guiando a llm sobre como lidar com o erro
        Talvez perguntar pro usuario se ele gostaria de re-tentar o pedido


Exemplo error message para tool
    "A tool that retrieves product data could return a response that says "No product data found for product ID XXX. Ask the customer to confirm the product name, and look up the product ID by name to confirm you have the correct ID.""