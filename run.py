"""DevOps Quest - Local Development Server Entry Point.

Safe execution script for local developer workstations.
Production environments should execute via Gunicorn WSGI server.
"""

from __future__ import annotations

import os

try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if present
    load_dotenv()
except ImportError:
    pass

from app import create_app

environment = os.getenv("FLASK_ENV", "development")
app = create_app(environment)

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    # Debug mode is governed by app configuration, never hardcoded to True
    debug_mode = app.config.get("DEBUG", False)

    print(f"Starting DevOps Quest ({environment}) on http://{host}:{port}")
    print(f"Safe Debug Mode: {debug_mode}")
    app.run(host=host, port=port, debug=debug_mode)
