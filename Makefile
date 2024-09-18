CONTAINER_NAME = "fastapi"

bash:
	docker compose exec $(CONTAINER_NAME) bash

build:
	docker compose build

down:
	docker compose down

logs:
	docker compose logs -f $(CONTAINER_NAME)

restart:
	docker compose restart $(CONTAINER_NAME)

shell:
	docker compose exec $(CONTAINER_NAME) python3

up:
	docker compose up -d
