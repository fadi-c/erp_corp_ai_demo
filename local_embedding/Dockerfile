FROM python:3.12-bullseye

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    git \
    build-essential \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip


WORKDIR /app


COPY local_embedding/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


#RUN mkdir -p /root/.cache/huggingface


COPY local_embedding/embedding_service.py /app

EXPOSE 5000

CMD ["python", "-u", "embedding_service.py"]