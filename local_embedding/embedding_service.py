import os
import time
from flask import Flask, request, jsonify
import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

INPUT_DIM = 384
TARGET_DIM = 1536

HF_TOKEN = os.getenv("HF_TOKEN")
CACHE_DIR = os.getenv("SENTENCE_TRANSFORMERS_HOME", "/app/models")

os.environ["SENTENCE_TRANSFORMERS_HOME"] = CACHE_DIR
os.environ["HF_HOME"] = CACHE_DIR
os.environ["TRANSFORMERS_CACHE"] = CACHE_DIR

torch.manual_seed(42)

projection = nn.Linear(INPUT_DIM, TARGET_DIM)
normalize = nn.functional.normalize

print("[embedding] Loading embedding model...")
print("[embedding] Cache dir:", CACHE_DIR)

for attempt in range(5):
    try:

        model = SentenceTransformer(
            MODEL_NAME,
            device="cpu",
            cache_folder=CACHE_DIR,
            token=HF_TOKEN,
            trust_remote_code=False,
        )

        print("[embedding] Model ready")
        break

    except Exception as e:

        print(f"[WARN] load failed {attempt+1}/5:", e)
        time.sleep(5)

else:
    raise RuntimeError("Cannot load embedding model")


@app.route("/embed", methods=["POST"])
def embed():

    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    vector = model.encode(text, convert_to_tensor=True)

    with torch.no_grad():
        vector_proj = projection(vector)
        vector_proj = normalize(vector_proj, p=2, dim=0)

    embedding = vector_proj.tolist()

    return jsonify({"embedding": embedding, "dimension": len(embedding)})


if __name__ == "__main__":
    print("[embedding] Starting Flask server")
    app.run(host="0.0.0.0", port=5000)
