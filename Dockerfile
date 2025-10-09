FROM python:3.12-slim

# ENV POETRY_HOME="/opt/poetry" \
#     POETRY_VIRTUALENVS_IN_PROJECT=true \
#     POETRY_NO_INTERACTION=1 \
#     PATH="$POETRY_HOME/bin:$PATH"

# RUN curl -sSL https://install.python-poetry.org | python3 -

RUN pip install poetry

WORKDIR /code

# COPY pyproject.toml poetry.lock ./

# RUN poetry install --no-root

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]