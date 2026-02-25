# Generative IA studies

### To Do List
- [ ] costumer-service
    - [X] criar service
    - [X] rota get customer by email
- [ ] weather-service
    - [X] separar service
    - [ ] converter cron api em job
    - [ ] processamento do job via sqs
- [ ] product-service
    - [X] separar service
    - [X] rota get products by names
- [ ] order-service
    - [X] separar parte da IA nele
    - [X] config mongo-db
    - [X] rota para processar compra de produtos
    - [X] rotal para pegar compras por customer email
    - [ ] interacao com IA
        - [X] rota para chat direto com cliente
        - [X] se o cliente tiver intencao de comprar, processar e gerar a compra 
        - [ ] estrutura para pegar historico de chat
        - [X] Implementar parte que interpreta a intencao do usuario
        - [ ] sugerir melhores dias pra sair baseado na previsao do tempo e na preferencia do cliente 
        - [ ] sugerir produtos climaticos para uma data especial. IA precisa considerar 
                previsao do tempo + produtos disponiveis categoria Weather
        - [ ] sugerir produtos de X categoria
        - [ ] usar paginacao para perguntar pro cliente se ele quer ver mais produtos
- Observability
    - [ ] gerar metricas
    - [ ] config prometheus
    - [ ] criar dashs basicos no grafana
- Tests
    - [ ] testes unitarios para product-service
    - [ ] testes unitarios para customer-service
    - [ ] testes unitarios para forecast-service
    - [ ] testes unitarios para product-service
	- [ ] basic load tests
	- [ ] test end to end apis


fluxo:
    input do usuario no chat
    service identifica a intencao
        llm ajuda para identificar a intencao
            Melhorar essa identificacao de intencao sem precisar da LLM (talvez com regex)
    service busca os dados necessarios
    llm monta a resposta


# TODO make the IA ask for the products if the customer dont say it.
# use memory to remember the context