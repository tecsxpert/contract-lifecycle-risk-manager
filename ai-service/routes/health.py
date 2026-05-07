from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint("health", __name__)

START_TIME = datetime.utcnow()

@health_bp.route("/health", methods=["GET"])
def health():

    uptime = datetime.utcnow() - START_TIME

    return jsonify({
        "status": "UP",
        "service": "Contract Lifecycle AI Service",
        "model": "llama-3.3-70b-versatile",
        "uptime_seconds": uptime.total_seconds()
    })