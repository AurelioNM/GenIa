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
        - [ ] sugerir melhores dias pra sair baseado no gosto do cliente e na previsao do tempo
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
