"""Integration tests for database queries and FastHTML routes."""

import os
import sys
from pathlib import Path

from starlette.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "python-package"))
sys.path.insert(0, str(PROJECT_ROOT / "report"))
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-dashboard-tests")

from dashboard import app  # noqa: E402
from employee_events import Employee, Team  # noqa: E402


def test_employee_queries_return_dashboard_data():
    """Employee queries return names, events, notes, and model inputs."""
    employee = Employee()

    assert employee.names()
    assert employee.username(1) == [("Alex Martinez",)]
    assert not employee.event_counts(1).empty
    assert not employee.notes(1).empty
    assert list(employee.model_data(1).columns) == [
        "positive_events",
        "negative_events",
    ]


def test_team_queries_return_dashboard_data():
    """Team queries return names, events, notes, and member model inputs."""
    team = Team()

    assert team.names()
    expected_name = dict((identifier, name) for name, identifier in team.names())[2]
    assert team.username(2) == [(expected_name,)]
    assert not team.event_counts(2).empty
    assert not team.notes(2).empty
    assert not team.model_data(2).empty


def test_employee_dashboard_renders_two_visualizations():
    """The employee route includes its dynamic title and both charts."""
    response = TestClient(app).get("/employee/2")

    assert response.status_code == 200
    assert "Employee Performance" in response.text
    assert response.text.count("data:image") == 2


def test_team_dashboard_renders_two_visualizations():
    """The team route includes its dynamic title and both charts."""
    response = TestClient(app).get("/team/2")

    assert response.status_code == 200
    assert "Team Performance" in response.text
    assert response.text.count("data:image") == 2


def test_filter_form_redirects_to_requested_profile():
    """Submitting the filters routes to the selected entity dashboard."""
    response = TestClient(app).post(
        "/update_data",
        data={"profile_type": "Team", "user-selection": "2"},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/team/2"
