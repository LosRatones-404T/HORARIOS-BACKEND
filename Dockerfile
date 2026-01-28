FROM python:3.13-alpine

# Prevents Python from writing pyc files to disk and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required to build some Python packages
# Alpine uses apk instead of apt-get
RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    curl

# Copy only dependency files first for better layer caching
COPY pyproject.toml poetry.lock* /app/

# Install Poetry and project dependencies (no dev)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev \
    && rm -rf /root/.cache/pypoetry

# Copy application code
COPY . /app

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
