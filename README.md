# Generative IA studies

### To Do List
- gen-ia
    - [ ] implementar guardrails
    - transformar em tools os seguintes fluxos
        - [ ] processar compra
        - [ ] sugerir produto baseado em categoria
        - [ ] sugerir produto baseado em historico de compras
        - [ ] sugerir produto baseado em historico de compras
        - [ ] reponder Q&A do tarantino
    - [ ] implementar MCP
- Observability
    - [ ] gerar metricas
    - [ ] config prometheus
    - [ ] criar dashs basicos no grafana
- Tests
    - [X] testes unitarios para product-service
    - [ ] testes unitarios para customer-service
    - [ ] testes unitarios para forecast-service
    - [ ] testes unitarios para product-service
	- [ ] basic load tests
	- [ ] test end to end apis
- [ ] debitos funcionais/tecnicos
    - [ ] cenario de cliente tentar comprar produtos que nao existam
    - [ ] cenario de cliente tentar pedir sugestao de categoria que nao exista
    - [ ] fazer a IA perguntar quais produtos se o cliente falar que quer comprar, mas nao especificar quais
    - [ ] cliente pediu sugestao de produto baseado no historico, mas nao tem compras anteriores


Chat - Casos de teste
PURCHASE_PRODUCT
I would like to buy 1 Catnip and 5 Xuru

SUGGEST_PRODUCT_BASED_ON_CATEGORY
Suggest me products on the PETS category

SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY
Suggest me products that match with my purchase history

SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER
I want to go for a walk on a rainy day

TARANTINO_QUESTION
Did Tarantino won the oscar? If yes, with movies?

UNKNOWN
Tell me how to do backflips