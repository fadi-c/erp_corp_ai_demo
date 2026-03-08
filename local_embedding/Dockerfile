FROM python:3.12-slim

RUN pip install --upgrade pip
COPY local_embedding/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY local_embedding/embedding_service.py /app

EXPOSE 5000
CMD ["python", "embedding_service.py"]