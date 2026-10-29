"""DevOps Quest - REST API Endpoints.

Provides JSON endpoints for health checks, challenge management,
and progress metrics.
"""

from __future__ import annotations

import datetime
from flask import Blueprint, jsonify, request
from app.db import (
    check_db_health,
    get_all_challenges,
    get_challenge_by_id,
    get_challenge_stats,
    toggle_challenge_status,
)


api_bp = Blueprint("api", __name__, url_prefix="/api")


def health_check_handler():
    """Health check endpoint logic returning JSON status."""
    is_db_healthy = check_db_health()
    status_code = 200 if is_db_healthy else 503

    payload = {
        "status": "healthy" if is_db_healthy else "unhealthy",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "version": "1.0.0",
        "service": "devops-quest",
        "checks": {
            "database": "connected" if is_db_healthy else "disconnected",
        },
    }
    return jsonify(payload), status_code


@api_bp.route("/health", methods=["GET"])
def api_health():
    """API health check endpoint."""
    return health_check_handler()


@api_bp.route("/challenges", methods=["GET"])
def list_challenges():
    """Retrieve challenges with optional filtering by difficulty and completion status."""
    difficulty = request.args.get("difficulty")
    completed_param = request.args.get("completed")

    completed = None
    if completed_param is not None:
        if completed_param.lower() in ("true", "1"):
            completed = True
        elif completed_param.lower() in ("false", "0"):
            completed = False
        else:
            return jsonify({"error": "Invalid completed filter. Use true, false, 1, or 0."}), 400

    valid_difficulties = ("Beginner", "Intermediate", "Advanced")
    if difficulty and difficulty.capitalize() in valid_difficulties:
        difficulty = difficulty.capitalize()
    elif difficulty:
        return jsonify({"error": f"Invalid difficulty. Allowed: {', '.join(valid_difficulties)}"}), 400

    challenges = get_all_challenges(difficulty=difficulty, completed=completed)
    stats = get_challenge_stats()

    return jsonify({
        "count": len(challenges),
        "challenges": challenges,
        "stats": stats,
    }), 200


@api_bp.route("/challenges/<int:challenge_id>", methods=["GET"])
def get_challenge(challenge_id: int):
    """Retrieve a single challenge by ID."""
    challenge = get_challenge_by_id(challenge_id)
    if not challenge:
        return jsonify({"error": f"Challenge with ID {challenge_id} not found."}), 404

    return jsonify({"challenge": challenge}), 200


@api_bp.route("/challenges/<int:challenge_id>/toggle", methods=["POST"])
def toggle_challenge(challenge_id: int):
    """Toggle or set the completion status of a challenge."""
    completed = None
    if request.is_json and request.json:
        explicit_completed = request.json.get("completed")
        if explicit_completed is not None:
            if not isinstance(explicit_completed, bool):
                return jsonify({"error": "'completed' must be a boolean."}), 400
            completed = explicit_completed

    updated = toggle_challenge_status(challenge_id, completed=completed)
    if not updated:
        return jsonify({"error": f"Challenge with ID {challenge_id} not found."}), 404

    stats = get_challenge_stats()
    return jsonify({
        "message": "Challenge status updated successfully.",
        "challenge": updated,
        "stats": stats,
    }), 200


@api_bp.route("/stats", methods=["GET"])
def challenge_stats():
    """Retrieve current challenge completion statistics."""
    return jsonify(get_challenge_stats()), 200

