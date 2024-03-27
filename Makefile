# Start containers
up:
	docker compose up

# Stop and remove containers
down:
	docker compose down

# Show logs
logs:
	docker logs apache -f

# Reload apache inside the container
reload-apache:
	docker compose exec -it apache /bin/bash -c "/opt/bitnami/scripts/apache/reload.sh"

# Reload docker and show logs
reload-docker:
	docker compose restart && docker compose logs -f

# Open a shell in the container
shell:
	docker compose exec -it apache /bin/bash 

# Automatic reloading apache when conf/my_vhost.conf is changed
watch:
	./watch.sh

# Run the tests
test:
	./tests.py

# Run the tests and watch for changes
tests-watch:
	./tests-watch.sh 

.PHONY: up down logs reload-apache reload-docker shell watch test tests-watch