"""DevOps Quest - Pytest Fixtures & Test Setup.

Provides isolated test client, database lifecycle management,
and test-specific configurations.
"""

from __future__ import annotations

import os
import tempfile
try:
    import pytest
    fixture = pytest.fixture
except ImportError:
    def fixture(func):
        return func
from app import create_app
from app.db import init_db


@fixture
def app():
    """Create and configure a Flask application instance for testing."""
    # Create a temporary file to serve as the SQLite database
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    test_config = {
        "TESTING": True,
        "DEBUG": False,
        "DATABASE_PATH": db_path,
        "SECRET_KEY": "test-secret-key-for-pytest",
    }

    application = create_app(config_name="testing", test_config=test_config)

    with application.app_context():
        init_db(application, db_path=db_path)

    yield application

    # Cleanup temporary test database
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@fixture
def client(app):
    """Test client for issuing requests against the application."""
    return app.test_client()


@fixture
def runner(app):
    """CLI test runner for Flask CLI commands."""
    return app.test_cli_runner()
