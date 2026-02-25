# Generative IA studies

### To Do List
- [ ] costumer-service
    - [X] criar service
    - [X] api get customer by email
- [ ] weather-service
    - [X] separar service
    - [ ] converter cron api em job
    - [ ] processamento do job via sqs
- [ ] product-service
    - [X] separar service
    - [X] api get products by names
    - [X] api get products by category
    - [ ] enum category
- [ ] order-service
    - [X] separar parte da IA nele
    - [X] config mongo-db
    - [X] api para processar compra de produtos
    - [X] api para pegar compras por customer email
    - [ ] interacao com IA
        - [X] api para chat direto com cliente
        - [X] Implementar parte que interpreta a intencao do usuario
        - [X] se o cliente tiver intencao de comprar, processar e gerar a compra 
        - [ ] estrutura para salvar historico de chat
            - [ ] estrutura para usar o historico do chat na interacao
        - [ ] sugerir melhores dias pra sair baseado na previsao do tempo e na preferencia do cliente 
        - [ ] sugerir produtos climaticos para uma data especial. IA precisa considerar 
                previsao do tempo + produtos disponiveis categoria Weather
        - [X] sugerir produtos de X categoria
        - [ ] sugerir produtos baseado no historico de compras
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
- [ ] debitos funcionais/tecnicos
    - [ ] cenario de cliente tentar comprar produtos que nao existam
    - [ ] cenario de cliente tentar pedir sugestao de categoria que nao exista
    - [ ] make the IA ask for the products if the customer dont say it
    - [ ] fazer a IA perguntar quais produtos se o cliente falar que quer comprar, mas nao especificar quais
    - [ ] cliente pediu sugestao de produto baseado no historico, mas nao tem compras anteriores


fluxo:
    input do usuario no chat
    service identifica a intencao
        llm ajuda para identificar a intencao
            Melhorar essa identificacao de intencao sem precisar da LLM (talvez com regex)
    service busca os dados necessarios
    llm monta a resposta
