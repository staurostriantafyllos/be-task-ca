FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --without dev

COPY . /app

RUN poetry install --only-root

CMD ["poetry", "run", "start"]
