FROM python:3.11-slim-buster as poetry
WORKDIR /app/

RUN apt-get update && apt-get install -y curl

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org/ | \
    POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    python -m venv /opt/venv && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-interaction --no-ansi -vvv

ENV PYTHONPATH=/app

CMD ["poetry", "run"]