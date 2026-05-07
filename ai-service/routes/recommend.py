from flask import Blueprint, jsonify, request
from services.groq_service import generate_response
from datetime import datetime

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend_contract():

    payload = request.environ.get("sanitized_json") or request.get_json(silent=True) or {}

    contract_text = payload.get("text")

    if not contract_text:
        return jsonify({
            "error": "Missing contract text"
        }), 400

    with open("prompts/recommend_prompt.txt", "r") as file:
        prompt = file.read()

    result = generate_response(prompt, contract_text)

    return jsonify({
        "generated_at": datetime.utcnow().isoformat(),
        "response": result
    })