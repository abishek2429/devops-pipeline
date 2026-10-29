"""DevOps Quest - Route & Web View Integration Tests."""

from __future__ import annotations


def test_dashboard_renders_successfully(client):
    """Test that the main dashboard returns 200 OK and contains core UI elements."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "DevOps Quest" in html
    assert "Challenge Tracker" in html
    assert "Overall Completion" in html
    assert "Containerize a Python Web App" in html


def test_dashboard_filter_by_difficulty(client):
    """Test filtering dashboard items by difficulty level."""
    response = client.get("/?difficulty=Beginner")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "Containerize a Python Web App" in html


def test_root_health_endpoint(client):
    """Test that GET /health returns 200 OK with valid JSON structure."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "devops-quest"
    assert data["checks"]["database"] == "connected"
    assert "timestamp" in data
    assert "version" in data


def test_web_form_toggle_fallback(client):
    """Test fallback HTML form submission redirects back to dashboard."""
    response = client.post("/challenges/1/toggle", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_404_html_error_page(client):
    """Test requesting a non-existent route returns 404 and friendly HTML."""
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    html = response.get_data(as_text=True)
    assert "Quest Not Found" in html
    assert "404" in html


def test_404_json_error_for_api(client):
    """Test requesting a non-existent API route returns 404 JSON."""
    response = client.get("/api/does-not-exist")
    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert "error" in data
    assert data["status_code"] == 404
