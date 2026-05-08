from flask import Blueprint, request, Response, stream_with_context
import time

from services.shared import groq_client as client

stream_bp = Blueprint("stream", __name__)


# =========================
# Load Prompt Safely
# =========================
def load_prompt():
    try:
        with open("prompts/report_stream_prompt.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return """
You are a contract lifecycle risk analysis system.

Generate a streaming contract risk report.

Contract Data:
{text}

Give:
- Title
- Executive Summary
- Risk level
- Key findings
- Recommendations
"""


PROMPT = load_prompt()


# =========================
# STREAM ROUTE
# =========================
@stream_bp.route("/report-stream", methods=["GET"])
def report_stream():
    """
    Stream AI-generated contract risk report (SSE)
    ---
    tags:
      - Contract Stream

    parameters:
      - name: text
        in: query
        type: string
        required: true
        example: Contract has unclear liability clause and missing SLA terms

    responses:
      200:
        description: Streaming response
    """

    text = request.args.get("text")

    if not text:
        return {"error": "Missing 'text' query param"}, 400

    def generate():
        start_time = time.time()

        try:
            prompt = PROMPT.replace("{text}", text)

            # 🔹 AI call
            output = client.generate(prompt)

            # 🔹 Start event
            yield "event: start\ndata: Stream started\n\n"

            # 🔹 Stream chunks
            for line in output.split("\n"):
                if line.strip():
                    yield f"event: chunk\ndata: {line}\n\n"
                    time.sleep(0.03)

            end_time = time.time()

            # 🔹 Meta
            yield f"""event: meta
data: {{
  "model": "{getattr(client, '_working_model', 'unknown')}",
  "response_time_ms": {int((end_time - start_time) * 1000)}
}}
\n\n"""

            # 🔹 Done
            yield "event: done\ndata: [DONE]\n\n"

        except Exception as e:
            yield f"""event: error
data: {{
  "message": "{str(e)}"
}}
\n\n"""

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )