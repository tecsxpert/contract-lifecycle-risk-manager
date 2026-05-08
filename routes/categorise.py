from flask import Blueprint, request, jsonify
import time

from services.shared import groq_client as client

categorise_bp = Blueprint("categorise", __name__)


@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    """
    Contract Risk Categorisation API
    ---
    tags:
      - Contract Categorise

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              example: Contract has unclear liability clause and missing SLA terms

    responses:
      200:
        description: Success
    """

    try:
        data = request.get_json(silent=True)

        if not data or "text" not in data:
            return jsonify({"error": "text required"}), 400

        text = data["text"]

        start = time.time()

        # =========================
        # AI PROMPT
        # =========================
        prompt = f"""
You are a contract lifecycle risk classifier.

Classify the following contract text into EXACTLY ONE category only.

Categories:
- Compliance Risk
- Financial Risk
- Operational Risk
- Legal Risk
- Other

Text:
{text}

Return ONLY one category name from the list.
"""

        # =========================
        # AI CALL
        # =========================
        ai_response = client.generate(prompt)

        category = ai_response.strip().split("\n")[0]

        end = time.time()

        return jsonify({
            "category": category,
            "meta": {
                "response_time_ms": int((end - start) * 1000),
                "model_used": getattr(client, "model", "unknown")
            }
        }), 200

    except Exception as e:
        print("❌ Categorise error:", e)

        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500