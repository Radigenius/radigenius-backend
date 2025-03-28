FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=300
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app


# Create a separate layer for pip and poetry installation (rarely changes)
RUN pip install --upgrade pip && \
  pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Install remaining dependencies without reinstalling Python
RUN poetry install --no-interaction --no-ansi --without dev --no-root

# Copy source code
COPY ./src /app