FROM python:3.9 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./recipe_api /code/recipe_api
# RUN python manage.py collectstatic --noinput --clear

# Start Gunicorn
CMD set -xe; python manage.py migrate --noinput; gunicorn lds_www.wsgi:application
