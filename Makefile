# Formatting

isort:
	isort $(arg1) .

black:
	black $(arg1) .

format: isort black


# Linting
flake8:
	flake8 .

mypy:
	mypy --namespace-packages --explicit-package-bases --exclude 'alembic' .

test:
	pytest . -vv


# todo_minotor app
create_migration_todo_monitor:
	cd apps/todo_monitor/ && export PYTHONPATH=../../. && alembic revision --autogenerate

migration_todo_monitor:
	cd apps/todo_monitor/ && export PYTHONPATH=../../. && alembic upgrade head



# docker compose
start:
	docker compose up --build

stop:
	docker compose down


lint: flake8 mypy