from flask import Blueprint, request, jsonify
import json, re, time

from services.shared import groq_client as client

recommend_bp = Blueprint("recommend", __name__)


# =========================
# Load Prompt
# =========================
def load_prompt():
    try:
        with open("prompts/recommend_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return """
You are a contract lifecycle monitoring system.

Contract Data:
{text}

Suggest appropriate contract risk management actions in JSON ARRAY.

STRICT RULES:
- Return ONLY JSON ARRAY
- No explanation outside JSON
- Avoid definitive conclusions (use cautious language)
- Provide 2–3 actions max

FORMAT:
[
  {
    "action_type": "LEGAL_REVIEW | RISK_ESCALATION | CONTRACT_MONITORING | COMPLIANCE_CHECK | VENDOR_AUDIT",
    "description": "short explanation",
    "priority": "HIGH | MEDIUM | LOW"
  }
]
"""


PROMPT = load_prompt()


# =========================
# ROUTE
# =========================
@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    """
    Generate contract risk recommendations using AI
    ---
    tags:
      - Contract Recommend

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              example: Contract has unclear payment terms and missing SLA clause

    responses:
      200:
        description: Contract recommendations
    """

    try:
        # ✅ safe JSON
        data = request.get_json(silent=True)

        if not data or "text" not in data:
            return jsonify({
                "error": "Missing 'text' field",
                "example": {
                    "text": "Contract has unclear termination clause"
                }
            }), 400

        text = data["text"]

        # 🔹 prompt
        prompt = PROMPT.replace("{text}", text)

        start = time.time()

        # ✅ correct call
        response = client.generate(prompt)

        end = time.time()

        print("🧠 RAW RESPONSE:", response)

        # =========================
        # JSON PARSE
        # =========================
        try:
            match = re.search(r'\[[\s\S]*\]', response)

            if match:
                parsed = json.loads(match.group())
            else:
                raise ValueError("No JSON")

        except:
            parsed = [
                {
                    "action_type": "CONTRACT_MONITORING",
                    "description": "Unable to parse AI response, review contract input manually.",
                    "priority": "LOW"
                }
            ]

        return jsonify({
            "data": parsed,
            "meta": {
                "model_used": getattr(client, "model", "unknown"),
                "response_time_ms": int((end - start) * 1000)
            }
        }), 200

    except Exception as e:
        print("❌ Recommend error:", e)

        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500