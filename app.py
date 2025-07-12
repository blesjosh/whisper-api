from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)
model = whisper.load_model("base")  # Options: tiny, base, small, medium, large

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    file = request.files['file']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        file.save(temp.name)
        result = model.transcribe(temp.name)
        os.unlink(temp.name)

    return jsonify({"transcript": result["text"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
