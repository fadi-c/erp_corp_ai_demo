FROM python:3.12-slim

RUN useradd -m django

COPY docker/docker-entrypoint.sh /opt/
RUN chmod +x /opt/docker-entrypoint.sh

USER django
WORKDIR /app
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/opt/docker-entrypoint.sh"]