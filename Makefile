postgres:
	docker run --name postgres14 -p 5432:5432 -e POSTGRES_USER=test -e POSTGRES_PASSWORD=testpwd -d postgres:14-alpine

createdb:
	docker exec -it postgres14 createdb --username test --owner=test note

dropdb:
	docker exec -it postgres14 dropdb note

migrateup:
	alembic upgrade +1

migratedown:
	alembic downgrade -1

new_migrate:
	@read -p "Enter migration name: " name; \
		alembic revision -m $$name

start_server:
	uvicorn app:app --reload

ssl:
	@read -p "Enter length: " len;\
		openssl rand -base64 $$len


.PHONY:  migrateup, migratedown, new_migrate, ssl, start_server
