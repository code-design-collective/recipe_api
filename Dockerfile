# Use an official Python runtime as a parent image
FROM python:3.9 as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install poetry
RUN pip install poetry

# Copy the dependencies files to the working directory
COPY pyproject.toml poetry.lock* /code/

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the project code into the container
COPY . /code/

# Create and apply database migrations (if needed)
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the Gunicorn port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "recipe_api.wsgi:application", "--bind", "0.0.0.0:8000"]
