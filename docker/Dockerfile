# docker/Dockerfile
FROM python:3.9-slim-bookworm AS builder

WORKDIR /app

# Pas besoin de gcc si pas de compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Configuration des timeouts
ENV PIP_DEFAULT_TIMEOUT=1000
ENV PIP_RETRIES=5

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# Deuxième étape
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

RUN mkdir -p data/raw data/processed logs backups \
    analysis/reports visualization/outputs

COPY . .

CMD ["python", "scripts/run_pipeline.py", "--pages", "30", "--visuals"]