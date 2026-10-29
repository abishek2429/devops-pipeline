"""DevOps Quest - Web Views & UI Routes.

Renders modern dark-themed HTML views and handles web form interactions.
"""

from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for
from app.db import get_all_challenges, get_challenge_stats, toggle_challenge_status


web_bp = Blueprint("web", __name__)


@web_bp.route("/", methods=["GET"])
def dashboard():
    """Render the main DevOps Quest challenge tracker dashboard."""
    difficulty = request.args.get("difficulty")
    challenges = get_all_challenges(difficulty=difficulty)
    stats = get_challenge_stats()

    return render_template(
        "index.html",
        challenges=challenges,
        stats=stats,
        current_difficulty=difficulty or "all",
    )


@web_bp.route("/challenges/<int:challenge_id>/toggle", methods=["POST"])
def toggle_challenge_form(challenge_id: int):
    """Fallback route for standard HTML form toggling without JavaScript."""
    toggle_challenge_status(challenge_id)
    return redirect(url_for("web.dashboard"))
