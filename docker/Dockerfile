FROM python:3.12-slim

RUN useradd -m django

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY docker/docker-entrypoint.sh /opt/docker-entrypoint.sh
RUN chmod +x /opt/docker-entrypoint.sh

USER django
WORKDIR /app
COPY backend/requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/opt/docker-entrypoint.sh"]