FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY src/ ./src/

RUN pip install --no-cache-dir -e .

COPY . .

ENV PYTHONPATH=/app/src
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:create_app"]
