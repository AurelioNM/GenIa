VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

.PHONY: venv

# SETUP
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
	else \
		echo "Virtual environment already exists."; \
	fi

setup:
	$(PIP) install -r requirements.txt

update-deps:
	make down && docker-compose up --build -d

# RUN
run:
	docker-compose up -d

down:
	docker-compose down


# LLM
llm-clean-volume:
	make down && docker volume rm genia_ollama_vol

llm-pull-model:
	docker exec -it order-llm-ollama ollama pull llama3
# 	docker exec -it order-llm-ollama ollama pull nomic-embed-text
	

llm-list-models:
	docker exec -it order-llm-ollama ollama list


# SERVICE UTILS
log:
	@SERVICE=$(filter-out $@,$(MAKECMDGOALS)); \
	if [ -z "$$SERVICE" ]; then \
		echo "❌ Usage: make $@ <service>"; \
		exit 1; \
	fi; \
	docker logs -f $$SERVICE-service

test:
	@SERVICE=$(filter-out $@,$(MAKECMDGOALS)); \
	if [ -z "$$SERVICE" ]; then \
		echo "❌ Usage: make $@ <service>"; \
		exit 1; \
	fi; \
	SERVICE_DIR=$${SERVICE}-service; \
	if [ ! -d "$$SERVICE_DIR" ]; then \
		echo "❌ Service '$$SERVICE_DIR' not found"; \
		exit 1; \
	fi; \
	cd "$$SERVICE_DIR" && ls $$SERVICE_DIR && pytest -vv -s

coverage:
	@SERVICE=$(filter-out $@,$(MAKECMDGOALS)); \
	if [ -z "$$SERVICE" ]; then \
		echo "❌ Usage: make $@ <service>"; \
		exit 1; \
	fi; \
	SERVICE_DIR=$${SERVICE}-service; \
	if [ ! -d "$$SERVICE_DIR" ]; then \
		echo "❌ Service '$$SERVICE_DIR' not found"; \
		exit 1; \
	fi; \
	cd "$$SERVICE_DIR" && pytest . -v --cov=. && coverage html

lint:
	@SERVICE=$(filter-out $@,$(MAKECMDGOALS)); \
	if [ -z "$$SERVICE" ]; then \
		echo "❌ Usage: make $@ <service>"; \
		exit 1; \
	fi; \
	SERVICE_DIR=$${SERVICE}-service; \
	if [ ! -d "$$SERVICE_DIR" ]; then \
		echo "❌ Service '$$SERVICE_DIR' not found"; \
		exit 1; \
	fi; \
	cd "$$SERVICE_DIR" && pylint . --ignore=venv

%:
	@:
