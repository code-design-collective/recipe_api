FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "recipe_api.wsgi:application"]
