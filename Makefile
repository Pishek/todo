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
	mypy --namespace-packages --explicit-package-bases .

start:
	docker compose up --build

test:
	pytest . -vv

lint: flake8 mypy