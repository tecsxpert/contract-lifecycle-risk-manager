from flask import Blueprint, request, jsonify
import json, re, time

analyse_bp = Blueprint("analyse", __name__)

def safe_parse(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{[\s\S]*?\}", text)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return None


@analyse_bp.route("/analyse", methods=["POST"])
def analyse():
    """
    Contract Analysis API
    ---
    tags:
      - Contract Analyse

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
        description: Success
        schema:
          type: object
          properties:
            data:
              type: object
            meta:
              type: object

      400:
        description: Bad request

      500:
        description: Server error
    """

    try:
        start = time.time()
        data = request.get_json(silent=True)

        if not data or "text" not in data:
            return jsonify({"error": "text required"}), 400

        text = data["text"]

        # 🔥 Fake AI response (safe for testing)
        response = """
        {
          "summary": "Contract contains potential risks that may affect execution and compliance.",
          "contract_risks": ["Financial risk", "Compliance risk"],
          "key_findings": ["Unclear payment terms", "Missing SLA definition"]
        }
        """

        parsed = safe_parse(response)

        end = time.time()

        return jsonify({
            "data": parsed,
            "meta": {
                "response_time_ms": int((end - start) * 1000)
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500