"""DevOps Quest - Application Factory.

Initializes the Flask application, registers blueprints, configures error handlers,
and manages database lifecycles.
"""

from __future__ import annotations

import os
from flask import Flask, jsonify, render_template, request
from app.config import get_config
from app.db import close_db, init_db
from app.routes.api import api_bp, health_check_handler
from app.routes.web import web_bp


def create_app(config_name: str | None = None, test_config: dict | None = None) -> Flask:
    """Create and configure an instance of the Flask application using the factory pattern."""
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration class
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Override with test configuration if provided
    if test_config:
        app.config.update(test_config)

    # Ensure instance folder exists for SQLite file storage
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize SQLite database schema and seed data
    with app.app_context():
        init_db(app)

    # Register database connection teardown
    app.teardown_appcontext(close_db)

    # Register blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)

    # Direct /health endpoint at root level
    app.add_url_rule("/health", endpoint="health_check", view_func=health_check_handler, methods=["GET"])

    # Register human-readable error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app: Flask) -> None:
    """Register custom 404 and 500 error handlers supporting both HTML and JSON."""

    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Resource not found", "status_code": 404}), 404
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal server error", "status_code": 500}), 500
        return render_template("500.html"), 500
