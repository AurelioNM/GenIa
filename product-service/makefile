setup:
	pip3 install -r requirements.txt

run:
	docker-compose up --build product-service

coverage:
	pytest . -v --cov=. && coverage html

test:
	pytest -vv -s

lint:
	pylint . --ignore=venv
