import logging
import re

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["30 per minute"])
limiter.init_app(app)

INJECTION_PATTERNS = [
    r"ignore (previous|all) instructions",
    r"disregard (previous|all) instructions",
    r"do not follow instructions",
    r"dont follow instructions",
    r"ignore this prompt",
    r"bypass (safety|security)",
    r"delete (your )?response",
    r"forget (previous|all) instructions",
    r"override (previous|all) instructions",
    r"prompt injection",
]

HTML_TAG_RE = re.compile(r"<[^>]+>")


def strip_html(value: str) -> str:
    return HTML_TAG_RE.sub("", value)


def contains_prompt_injection(value: str) -> bool:
    lowered = value.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            return True
    return False


def sanitize_value(value):
    if isinstance(value, str):
        return strip_html(value)
    if isinstance(value, dict):
        return {key: sanitize_value(val) for key, val in value.items()}
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    return value


@app.before_request
def sanitize_request_payload():
    if request.method not in ("POST", "PUT", "PATCH"):
        return

    payload = request.get_json(silent=True)
    if payload is None:
        return

    sanitized = sanitize_value(payload)
    payload_text = str(sanitized)
    if contains_prompt_injection(payload_text):
        logger.warning("Prompt injection detected: %s", payload_text)
        return jsonify({"error": "prompt injection detected"}), 400

    request.environ["sanitized_json"] = sanitized


@app.route("/api/prompt", methods=["POST"])
@limiter.limit("30 per minute")
def handle_prompt():
    payload = request.environ.get("sanitized_json") or request.get_json(silent=True) or {}
    prompt = payload.get("prompt")
    if not prompt or not isinstance(prompt, str):
        return jsonify({"error": "Missing or invalid 'prompt' field"}), 400

    return jsonify({"sanitized_prompt": prompt})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
