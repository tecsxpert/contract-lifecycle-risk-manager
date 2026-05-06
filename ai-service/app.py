import logging
import os
import re

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
CORS(app, resources={r"/api/*": {"origins": allowed_origins}, r"/health": {"origins": allowed_origins}})
Talisman(
    app,
    content_security_policy={
        "default-src": ["'none'"],
        "base-uri": ["'self'"],
        "frame-ancestors": ["'none'"],
        "object-src": ["'none'"],
        "script-src": ["'none'"],
        "connect-src": ["'self'"],
    },
    force_https=False,
)
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


def generate_recommendation(prompt: str) -> str:
    lowered = prompt.lower()
    recommendations = []
    if "risk" in lowered or "risk score" in lowered:
        recommendations.append("Review the risk score and add remediation terms.")
    if "payment" in lowered or "net" in lowered or "due" in lowered:
        recommendations.append("Clarify payment terms and add late payment penalties.")
    if "confidential" in lowered or "nda" in lowered or "non-disclosure" in lowered:
        recommendations.append("Confirm confidentiality obligations and audit rights.")
    if not recommendations:
        recommendations.append("Summarize the contract and recommend next steps for review.")
    return " ".join(recommendations)


def generate_report(prompt: str) -> str:
    return (
        "Contract report: This contract appears to carry a moderate risk profile. "
        "Key areas to review are payment terms, vendor obligations, and confidentiality controls. "
        "Follow up with a detailed clause review and compliance check."
    )


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


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "ai-service", "healthy": True})


@app.route("/api/prompt", methods=["POST"])
@limiter.limit("30 per minute")
def handle_prompt():
    payload = request.environ.get("sanitized_json") or request.get_json(silent=True) or {}
    prompt = payload.get("prompt")
    if not prompt or not isinstance(prompt, str):
        return jsonify({"error": "Missing or invalid 'prompt' field"}), 400

    return jsonify({"sanitized_prompt": prompt})


@app.route("/api/recommend", methods=["POST"])
@limiter.limit("30 per minute")
def handle_recommend():
    payload = request.environ.get("sanitized_json") or request.get_json(silent=True) or {}
    prompt = payload.get("prompt")
    if not prompt or not isinstance(prompt, str):
        return jsonify({"error": "Missing or invalid 'prompt' field"}), 400

    recommendation = generate_recommendation(prompt)
    return jsonify({"recommendation": recommendation, "sanitized_prompt": prompt})


@app.route("/api/report", methods=["POST"])
@limiter.limit("30 per minute")
def handle_report():
    payload = request.environ.get("sanitized_json") or request.get_json(silent=True) or {}
    prompt = payload.get("prompt")
    if not prompt or not isinstance(prompt, str):
        return jsonify({"error": "Missing or invalid 'prompt' field"}), 400

    report = generate_report(prompt)
    return jsonify({"report": report, "sanitized_prompt": prompt})


@app.after_request
def set_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "same-origin")
    response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()");
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
