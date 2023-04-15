# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Install dependencies using Poetry
RUN poetry config virtualenvs.create true \
  && poetry config virtualenvs.in-project true \
  && poetry install --no-dev --no-interaction --no-ansi

# Activate the virtual environment created by Poetry
ENV PATH="/app/.venv/bin:${PATH}"
