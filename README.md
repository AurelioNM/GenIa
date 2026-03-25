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

Tools - Uma boa docstring de tool deve ter:
    O que a tool faz (alto nível)
    Quando usar
    Explicação dos parâmetros (semântica!)
    Output (especialmente se não for óbvio)
    Exemplo: 
        def set_light_values(
        brightness: int,
        color_temp: str,
        context: ToolContext) -> dict[str, int | str]:
            """This tool sets the brightness and color temperature of the room lights
            in the user's current location.

            Args:
                brightness: Light level from 0 to 100. Zero is off and 100 is full
                            brightness.
                color_temp: Color temperature of the light fixture, which can be
                            'daylight', 'cool' or 'warm'.
                context: A ToolContext object used to retrieve the user's location.

            Returns:
                A dictionary containing the set brightness and color temperature.
            """
            user_room_id = context.state["room_id"]
            # This is an imaginary room lighting control API
            room = light_system.get_room(user_room_id)
            response = room.set_lights(brightness, color_temp)
            return {"tool_response": response}
    