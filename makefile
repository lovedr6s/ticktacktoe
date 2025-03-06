start-dev:
	uv run flask --app app --debug run --port 8001

start:
	uv run flask --app app --port 8001

install:
	uv sync