FROM python:3.12-slim


WORKDIR /app

ENV PYTHONUNBUFFERED=1
COPY docker/docker-entrypoint.sh /opt/
RUN chmod +x /opt/docker-entrypoint.sh
ENTRYPOINT [ "/opt/docker-entrypoint.sh" ]
#CMD ["gunicorn", "core.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]