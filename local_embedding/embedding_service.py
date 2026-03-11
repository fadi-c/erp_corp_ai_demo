from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import torch
import torch.nn as nn
import os
import time

app = Flask(__name__)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
HF_TOKEN = os.getenv("HF_TOKEN") 
MODEL_PATH = "/app/models/models--sentence-transformers--all-MiniLM-L6-v2/"

INPUT_DIM = 384
TARGET_DIM = 1536

print("[embedding] Loading embedding model...")

if os.path.exists(MODEL_PATH):
    print(f"[embedding] Loading model from local storage: {MODEL_PATH}")
    model = SentenceTransformer(MODEL_PATH, local_files_only=True)
else:
    print(f"[embedding] Model not found locally. Downloading {MODEL_NAME} with HF token...")
    for attempt in range(5):
        try:
            model = SentenceTransformer(
                MODEL_NAME,
                cache_folder=MODEL_PATH
            )
            print("[embedding] Model downloaded successfully")
            break
        except Exception as e:
            print(f"[WARN] Failed to load model (attempt {attempt+1}/5): {e}")
            time.sleep(5)
    else:
        raise RuntimeError("Cannot load embedding model after 5 retries")

projection = nn.Linear(INPUT_DIM, TARGET_DIM)
normalize = nn.functional.normalize

@app.route("/embed", methods=["POST"])
def embed():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    vector = model.encode(text, convert_to_tensor=True)

    with torch.no_grad():
        vector_proj = projection(vector)
        vector_proj = normalize(vector_proj, p=2, dim=0)

    vectors = vector_proj.tolist()
    print(f"[embedding] Embedding dimension: {len(vectors)}")

    return jsonify({"embedding": vectors})

if __name__ == "__main__":
    print("[embedding] Starting Flask server on 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)