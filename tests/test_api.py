"""DevOps Quest - REST API Endpoint Unit & Integration Tests."""

from __future__ import annotations


def test_api_health_endpoint(client):
    """Test GET /api/health returns 200 and health payload."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["checks"]["database"] == "connected"


def test_list_all_challenges(client):
    """Test GET /api/challenges returns list, count, and overall stats."""
    response = client.get("/api/challenges")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()

    assert "count" in data
    assert "challenges" in data
    assert "stats" in data
    assert data["count"] > 0
    assert isinstance(data["challenges"], list)


def test_filter_challenges_by_difficulty(client):
    """Test GET /api/challenges with valid difficulty parameter."""
    response = client.get("/api/challenges?difficulty=Beginner")
    assert response.status_code == 200
    data = response.get_json()
    for item in data["challenges"]:
        assert item["difficulty"] == "Beginner"


def test_filter_challenges_by_invalid_difficulty(client):
    """Test GET /api/challenges with invalid difficulty returns 400."""
    response = client.get("/api/challenges?difficulty=SuperHard")
    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert "error" in data


def test_filter_challenges_by_completed_status(client):
    """Test GET /api/challenges?completed=true returns only completed items."""
    response = client.get("/api/challenges?completed=true")
    assert response.status_code == 200
    data = response.get_json()
    for item in data["challenges"]:
        assert item["is_completed"] == 1


def test_filter_challenges_by_invalid_completed(client):
    """Test GET /api/challenges with invalid completed param returns 400."""
    response = client.get("/api/challenges?completed=notabool")
    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert "error" in data


def test_get_single_challenge(client):
    """Test GET /api/challenges/<id> for an existing challenge."""
    response = client.get("/api/challenges/1")
    assert response.status_code == 200
    data = response.get_json()
    assert "challenge" in data
    assert data["challenge"]["id"] == 1
    assert "title" in data["challenge"]


def test_get_nonexistent_challenge(client):
    """Test GET /api/challenges/<id> for a non-existent challenge returns 404."""
    response = client.get("/api/challenges/99999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_toggle_challenge_status_implicit(client):
    """Test POST /api/challenges/<id>/toggle flips status automatically."""
    # Get current status of challenge 1
    get_res = client.get("/api/challenges/1")
    initial_status = get_res.get_json()["challenge"]["is_completed"]

    # Toggle
    toggle_res = client.post("/api/challenges/1/toggle")
    assert toggle_res.status_code == 200
    new_status = toggle_res.get_json()["challenge"]["is_completed"]
    assert new_status != initial_status

    # Toggle again to verify reversibility
    revert_res = client.post("/api/challenges/1/toggle")
    assert revert_res.status_code == 200
    assert revert_res.get_json()["challenge"]["is_completed"] == initial_status


def test_toggle_challenge_status_explicit_payload(client):
    """Test POST /api/challenges/<id>/toggle with explicit JSON completed payload."""
    response = client.post(
        "/api/challenges/1/toggle",
        json={"completed": True},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    assert response.get_json()["challenge"]["is_completed"] == 1

    response = client.post(
        "/api/challenges/1/toggle",
        json={"completed": False},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    assert response.get_json()["challenge"]["is_completed"] == 0


def test_toggle_challenge_status_invalid_payload(client):
    """Test POST /api/challenges/<id>/toggle with non-boolean payload returns 400."""
    response = client.post(
        "/api/challenges/1/toggle",
        json={"completed": "yes"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_toggle_nonexistent_challenge(client):
    """Test POST /api/challenges/<id>/toggle on non-existent ID returns 404."""
    response = client.post("/api/challenges/99999/toggle")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_challenge_stats_endpoint(client):
    """Test GET /api/stats returns accurate metrics."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.get_json()
    assert "total" in data
    assert "completed" in data
    assert "pending" in data
    assert "completion_rate" in data
    assert data["total"] == data["completed"] + data["pending"]
