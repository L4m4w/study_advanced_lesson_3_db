FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_NO_INTERACTION=1

WORKDIR /code

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock* /code/

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY ./app /code/app

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]