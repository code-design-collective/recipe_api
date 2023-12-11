FROM python:3.10-alpine

ENV VERSION=3.10
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONIOENCODING utf8
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache shadow

RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
    mariadb-connector-c-dev \
    jpeg-dev \
    zlib-dev \
    libwebp-dev \
    libffi-dev

WORKDIR /code/

COPY ./manage.py ./manage.py
COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
COPY ./README.md ./README.md
COPY ./recipe_api/ ./recipe_api/
COPY ./apps/ ./apps/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8080

CMD set -xe; \
    python manage.py collectstatic --noinput; \
    python manage.py migrate --noinput; \
    gunicorn recipe_api.wsgi:application --bind 0.0.0.0:8080
