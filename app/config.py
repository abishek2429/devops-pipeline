"""DevOps Quest - Application Configuration.

Supports multiple environments (Development, Testing, Production)
driven by environment variables with secure defaults.
"""

from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    """Base configuration shared across all environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-secret-key-change-in-production")
    DEBUG = False
    TESTING = False

    # Default SQLite database path inside the Flask instance folder
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "instance" / "devops_quest.db"))

    # Server network bindings
    PORT = int(os.getenv("PORT", "5000"))
    HOST = os.getenv("HOST", "0.0.0.0")

    # JSON configuration
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    """Configuration for local development."""

    # Debug is enabled only when explicitly set to '1' or 'true'
    DEBUG = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true")


class TestingConfig(BaseConfig):
    """Configuration for automated test execution."""

    TESTING = True
    DEBUG = False
    # Isolated test database file
    DATABASE_PATH = str(BASE_DIR / "instance" / "test_devops_quest.db")
    SECRET_KEY = "test-secret-key-for-testing-only"


class ProductionConfig(BaseConfig):
    """Configuration for production environments (e.g., Docker, Render)."""

    DEBUG = False
    TESTING = False
    # In production, SECRET_KEY should always be provided via environment variables


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(env_name: str | None = None) -> type[BaseConfig]:
    """Retrieve the configuration class matching the environment name."""
    env = (env_name or os.getenv("FLASK_ENV", "development")).lower()
    return CONFIG_MAP.get(env, DevelopmentConfig)
