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

# Install PyTorch with CUDA first (largest dependency)
RUN pip install --no-cache-dir torch==2.6.0 --index-url https://download.pytorch.org/whl/cu121

# Install core scientific packages
RUN pip install --no-cache-dir numpy>=1.24.0 unsloth==2025.3.15

# Install remaining dependencies without reinstalling Python
RUN poetry install --no-interaction --no-ansi --without dev --no-root

# Copy source code
COPY ./src /app