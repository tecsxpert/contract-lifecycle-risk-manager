from flask import Blueprint, request, jsonify
from services.job_service import create_job, update_job, get_job, run_async
from services.shared import groq_client as groq
import requests
import json
import re

report_bp = Blueprint("report", __name__)


# =========================
# SAFE JSON EXTRACTOR
# =========================
def extract_json(response):
    try:
        response = re.sub(r"```json|```", "", response).strip()
        match = re.search(r"\{[\s\S]*\}", response)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None


# =========================
# CORE AI LOGIC (CONTRACT)
# =========================
def generate_report_logic(text):
    prompt = f"""
You are a contract lifecycle risk analysis system.

Analyze the contract input and generate a structured contract risk report.

STRICT RULES:
- Return ONLY JSON
- No markdown
- No explanation outside JSON
- Avoid definitive conclusions (use cautious risk language)

FORMAT:
{{
  "title": "Contract Risk Report",
  "summary": "short summary",
  "risk_level": "Low/Medium/High/Critical",
  "key_findings": ["finding1", "finding2"],
  "recommendations": ["rec1", "rec2"]
}}

Contract Data:
{text}
"""

    try:
        response = groq.generate(prompt)
        print("🧠 RAW RESPONSE:", response)

        parsed = extract_json(response)
        if parsed:
            return parsed

    except Exception as e:
        print("❌ AI ERROR:", e)

    # fallback
    return {
        "title": "Contract Risk Report",
        "summary": "Unable to generate structured contract report",
        "risk_level": "Unknown",
        "key_findings": [text],
        "recommendations": ["Perform manual contract review"]
    }


# =========================
# BACKGROUND JOB
# =========================
def process_job(job_id, text, webhook_url=None):
    try:
        result = generate_report_logic(text)

        update_job(job_id, {
            "status": "completed",
            "result": result
        })

        # ✅ webhook validation
        if webhook_url and webhook_url.startswith("http"):
            try:
                requests.post(
                    webhook_url,
                    json={
                        "job_id": job_id,
                        "status": "completed",
                        "result": result
                    },
                    timeout=5
                )
            except Exception as e:
                print("⚠️ Webhook failed:", e)
        else:
            print("⚠️ Invalid webhook URL, skipped")

    except Exception as e:
        update_job(job_id, {
            "status": "failed",
            "error": str(e)
        })


# =========================
# CREATE JOB
# =========================
@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    """
    Generate contract risk report asynchronously
    ---
    tags:
      - Contract Report

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
            webhook_url:
              type: string
              example: https://webhook.site/your-id

    responses:
      200:
        description: Job created
    """

    data = request.get_json(silent=True)

    if not data or "text" not in data:
        return jsonify({
            "error": "text field is required",
            "example": {
                "text": "Contract has missing termination clause"
            }
        }), 400

    text = data["text"]
    webhook_url = data.get("webhook_url")

    # ✅ create job
    job_id = create_job()

    # ✅ run async
    run_async(process_job, (job_id, text, webhook_url))

    return jsonify({
        "job_id": job_id,
        "status": "processing"
    })


# =========================
# JOB STATUS
# =========================
@report_bp.route("/job-status/<job_id>", methods=["GET"])
def job_status(job_id):
    """
    Get contract report job status
    ---
    tags:
      - Contract Report

    parameters:
      - name: job_id
        in: path
        type: string
        required: true
        description: Job ID returned from /generate-report
        example: abc123

    responses:
      200:
        description: Job status
      404:
        description: Invalid job_id
    """

    job = get_job(job_id)

    if not job:
        return jsonify({
            "error": "Invalid job_id",
            "hint": "Use job_id from /generate-report"
        }), 404

    return jsonify(job)