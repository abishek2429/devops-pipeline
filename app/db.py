"""DevOps Quest - Database Management & Access Layer.

Handles SQLite database initialization, safe schema migrations, seed data,
and parameterized queries for the challenge tracker.
"""

from __future__ import annotations

import os
import sqlite3
from typing import Any
from flask import Flask, current_app, g


DEFAULT_CHALLENGES = [
    (
        "Containerize a Python Web App",
        "Write a multi-stage Dockerfile using a non-root user and minimal runtime dependencies.",
        "Beginner",
        "Docker",
        1,
    ),
    (
        "Automate CI with GitHub Actions",
        "Create a workflow that checks out code, runs Ruff linter, and executes Pytest test suites.",
        "Beginner",
        "CI/CD",
        1,
    ),
    (
        "Audit Image Vulnerabilities with Trivy",
        "Integrate Aqua Trivy security scanner to detect CRITICAL CVEs before image distribution.",
        "Intermediate",
        "DevSecOps",
        0,
    ),
    (
        "Publish Images to GitHub Container Registry",
        "Build and tag OCI-compliant container images with Git SHA and push to GHCR securely.",
        "Intermediate",
        "Artifacts",
        0,
    ),
    (
        "Continuous Deployment with Health Checks",
        "Configure automated deployments to Render web service triggered by verified pipeline runs.",
        "Intermediate",
        "CD",
        0,
    ),
    (
        "Application Health & Observability",
        "Implement a reliable /health endpoint verifying runtime, database connectivity, and version.",
        "Beginner",
        "Observability",
        1,
    ),
]


def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict[str, Any]:
    """Convert SQLite row tuples to dictionaries for easy serialization."""
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


def get_db(db_path: str | None = None) -> sqlite3.Connection:
    """Retrieve or establish an active SQLite database connection for the current request.

    Uses Flask's application context `g` for connection pooling per request.
    """
    if "db" not in g:
        target_path = db_path or current_app.config.get("DATABASE_PATH")
        if not target_path:
            raise ValueError("DATABASE_PATH is not configured.")

        # Ensure parent directory exists for file-based databases
        if target_path != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)

        g.db = sqlite3.connect(
            target_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False,
        )
        g.db.row_factory = dict_factory
        # Enable foreign key constraints
        g.db.execute("PRAGMA foreign_keys = ON;")

    return g.db


def close_db(exception: BaseException | None = None) -> None:
    """Close the database connection at the end of the Flask request lifecycle."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app: Flask | None = None, db_path: str | None = None) -> None:
    """Initialize database tables and seed baseline challenges if empty."""
    target_path = db_path or (app.config.get("DATABASE_PATH") if app else None)
    if not target_path:
        raise ValueError("DATABASE_PATH is required to initialize the database.")

    if target_path != ":memory:":
        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)

    conn = sqlite3.connect(target_path)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    difficulty TEXT NOT NULL CHECK(difficulty IN ('Beginner', 'Intermediate', 'Advanced')),
                    category TEXT NOT NULL,
                    is_completed INTEGER NOT NULL DEFAULT 0 CHECK(is_completed IN (0, 1)),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # Check if seed challenges are needed
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM challenges;")
            count = cursor.fetchone()[0]

            if count == 0:
                conn.executemany(
                    """
                    INSERT INTO challenges (title, description, difficulty, category, is_completed)
                    VALUES (?, ?, ?, ?, ?);
                    """,
                    DEFAULT_CHALLENGES,
                )
    finally:
        conn.close()


def get_all_challenges(difficulty: str | None = None, completed: bool | None = None) -> list[dict[str, Any]]:
    """Fetch all challenges from the database with optional filtering."""
    db = get_db()
    query = "SELECT id, title, description, difficulty, category, is_completed, created_at FROM challenges WHERE 1=1"
    params: list[Any] = []

    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)

    if completed is not None:
        query += " AND is_completed = ?"
        params.append(1 if completed else 0)

    query += " ORDER BY id ASC;"
    cursor = db.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()


def get_challenge_by_id(challenge_id: int) -> dict[str, Any] | None:
    """Fetch a single challenge by its ID using parameterized query."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, title, description, difficulty, category, is_completed, created_at FROM challenges WHERE id = ?;",
        (challenge_id,),
    )
    return cursor.fetchone()


def toggle_challenge_status(challenge_id: int, completed: bool | None = None) -> dict[str, Any] | None:
    """Toggle or explicitly set the completion status of a challenge."""
    db = get_db()
    cursor = db.cursor()

    current = get_challenge_by_id(challenge_id)
    if not current:
        return None

    if completed is None:
        new_status = 0 if current["is_completed"] == 1 else 1
    else:
        new_status = 1 if completed else 0

    with db:
        db.execute(
            "UPDATE challenges SET is_completed = ? WHERE id = ?;",
            (new_status, challenge_id),
        )

    return get_challenge_by_id(challenge_id)


def get_challenge_stats() -> dict[str, Any]:
    """Calculate summary statistics for dashboard progress tracking."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) AS total, SUM(is_completed) AS completed FROM challenges;")
    row = cursor.fetchone()

    total = row["total"] or 0
    completed = row["completed"] or 0
    pending = total - completed
    percentage = round((completed / total) * 100, 1) if total > 0 else 0.0

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": percentage,
    }


def check_db_health() -> bool:
    """Execute a simple query to verify database connectivity."""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1;")
        return cursor.fetchone() is not None
    except Exception:
        return False
