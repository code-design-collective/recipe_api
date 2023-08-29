FROM python:3.9 as requirements-stage

EXPOSE 5432

ENV PYTHONUNBUFFERED=1 \
    PORT=5432

# RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     libmariadbclient-dev \
#     libjpeg62-turbo-dev \
#     zlib1g-dev \
#     libwebp-dev \
#  && rm -rf /var/lib/apt/lists/*

# Install the application server.
# RUN pip install "gunicorn==20.0.4"

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# COPY ./recipe_api /code/recipe_api
# RUN python manage.py collectstatic --noinput --clear

# Start Gunicorn
CMD set -xe; python manage.py migrate --noinput; gunicorn recipe_api.wsgi:application
