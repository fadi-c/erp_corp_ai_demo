from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import os

app = Flask(__name__)
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/all-MiniLM-L6-v2/")
#os.makedirs(MODEL_PATH, exist_ok=True)

if not os.path.exists("MODEL_PATH{hub}"):
    print(f"Model not found, try to download {MODEL_PATH}...")
    model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=MODEL_PATH)
else:
    print(f"Load model from local storage {MODEL_PATH}...")
    model = SentenceTransformer(MODEL_PATH)

@app.route("/embed", methods=["POST"])
def embed():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    vector = model.encode(text).tolist()
    return jsonify({"embedding": vector})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)