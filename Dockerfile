FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
RUN pip install "gunicorn==21.2.0"
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "recipe_api.wsgi:application", "--bind", "0.0.0.0:8000"]

