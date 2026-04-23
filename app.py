from flask import Flask, request, jsonify
from flask_cors import CORS
from cracker import crack_password
from generator.generator import generate_password

app = Flask(__name__)
CORS(app)


# ── Generator ────────────────────────────────────────────────────────────────

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()

    length = data.get("length")
    char_type_enabled = data.get("char_types", {})
    excluded_chars = set(data.get("excluded_chars", ""))

    if not isinstance(length, int) or length <= 0:
        return jsonify({"error": "Invalid length."}), 400

    if not any(char_type_enabled.values()):
        return jsonify({"error": "At least one character type must be enabled."}), 400

    try:
        password = generate_password(length, char_type_enabled, excluded_chars)
        return jsonify({"password": password})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ── Cracker ──────────────────────────────────────────────────────────────────

@app.route("/api/crack", methods=["POST"])
def crack():
    data = request.get_json()
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "No password provided."}), 400

    result = crack_password(password)
    return jsonify(result)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
