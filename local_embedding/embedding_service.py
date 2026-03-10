from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import torch
import torch.nn as nn
import os

app = Flask(__name__)

MODEL_PATH = "/app/models/models--sentence-transformers--all-MiniLM-L6-v2/"
if not os.path.exists(MODEL_PATH):
    print(f"Model not found, downloading 'all-MiniLM-L6-v2' to {MODEL_PATH} ...")
    model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=MODEL_PATH)
else:
    print(f"Loading model from local storage {MODEL_PATH} ...")
    model = SentenceTransformer(MODEL_PATH)


# Dimensions
INPUT_DIM = 384    # all-MiniLM-L6-v2
TARGET_DIM = 1536  # dimension DB

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
    print(f"Embedding dimension: {len(vectors)}")

    return jsonify({"embedding": vectors})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)