FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app 
COPY . /app

RUN uv venv && uv sync

ENV PATH="/app/.venv/bin:$PATH"

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080" ]