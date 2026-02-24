# Generative IA studies

### To Do List
- [ ] costumer-service
    - [X] criar service
    - [X] rota get customer by email
- [ ] weather-service
    - [X] separar service
- [ ] product-service
    - [X] separar service
    - [X] rota get products by names
- [ ] order-service
    - [X] separar parte da IA nele
    - [X] config mongo-db
    - [X] rota para processar compra de produtos
    - [X] rotal para pegar compras por customer email
    - [ ] interacao com IA
        - [ ] rota para chat com cliente
        - [ ] estrutura para pegar historico de chat
        - [ ] Mapear como ficara a parte de intencao
        - [ ] sugerir melhores dias pra sair baseado na previsao do tempo e na preferencia do cliente 
        - [ ] sugerir produtos climaticos para uma data especial. IA precisa considerar 
                previsao do tempo + produtos disponiveis categoria Weather
        - [ ] sugerir produtos de X categoria
        - [ ] usar paginacao para perguntar pro cliente se ele quer ver mais produtos
        - [ ] se o cliente tiver intencao de comprar, processar e gerar a compra 
- Observability
    - [ ] gerar metricas
    - [ ] config prometheus
    - [ ] criar dashs basicos no grafana
- Tests
	- [ ] basic load tests
	- [ ] test end to end apis

fluxo:
    input do usuario no chat
    service precisa identificar a intencao (Sugestao de produto, Sugestao de dia para sair, efetivar compra)
        llm ajuda para identificar a intencao
    service busca os dados necessarios
    llm monta a resposta

Possiveis intencoes:
    CREATE_ORDER

    SUGGEST_PRODUCT_BASED_ON_CATEGORY
    SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY
    SUGGEST_PRODUCT_BASED_ON_WEATHER

    SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER