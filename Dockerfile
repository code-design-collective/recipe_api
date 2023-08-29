FROM python:3.9-slim-buster

ENV VERSION=3.10
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONIOENCODING utf8
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install --no-install-recommends \
        build-essential && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code/

COPY ./manage.py ./manage.py
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
COPY ./recipe_api/ ./recipe_api/
# Move to apps dir
COPY ./recipes/ ./recipes/
COPY ./users/ ./users/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "recipe_api.wsgi:application"]