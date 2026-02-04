setup:
	pip3 install -r requirements.txt

run:
	docker-compose up --build product-service

down:
	docker-compose down

clean-db:
	docker-compose down && docker volume rm product-service_product_database_vol 

coverage:
	pytest . -v --cov=. && coverage html

test:
	pytest -vv -s

lint:
	pylint . --ignore=venv
