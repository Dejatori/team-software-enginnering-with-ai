"""
Test module for flask_app API endpoints.
This module contains tests for the greeting API functionality.
"""

import pytest
from flask_app import app


def test_greet_basic():
    """Test basic functionality of the greeting endpoint with standard names."""
    with app.test_client() as client:
        test_names = ["David", "Alice", "Bob"]

        for name in test_names:
            response = client.get(f"/api/greet/{name}")
            data = response.get_json()

            assert response.status_code == 200
            assert data["message"] == f"Hello, {name}!"


def test_greet_special_chars():
    """Test handling of names containing special characters."""
    with app.test_client() as client:
        special_names = ["John Doe", "Jane-Smith", "O'Reilly"]

        for name in special_names:
            response = client.get(f"/api/greet/{name}")
            data = response.get_json()

            assert response.status_code == 200
            assert data["message"] == f"Hello, {name}!"


def test_greet_empty_name():
    """Test behavior when empty or blank names are provided."""
    with app.test_client() as client:
        # Testing with empty string - this will actually result in a 404
        # as Flask won't match the route, so removed from tests

        # Testing with blank space
        response = client.get("/api/greet/ ")
        data = response.get_json()

        assert response.status_code == 200
        assert data["message"] == f"Hello,  !"


def test_greet_long_name():
    """Test the endpoint with unusually long name parameters."""
    with app.test_client() as client:
        long_names = ["A" * 100, "B" * 200]

        for name in long_names:
            response = client.get(f"/api/greet/{name}")
            data = response.get_json()

            assert response.status_code == 200
            assert data["message"] == f"Hello, {name}!"


def test_greet_content_type():
    """Verify the API returns the correct content type (application/json)."""
    with app.test_client() as client:
        response = client.get("/api/greet/David")

        assert response.status_code == 200
        assert response.content_type == "application/json"


@pytest.mark.xfail(reason="Flask will return 404 for empty name route")
def test_greet_empty_route():
    """
    Test behavior when accessing the route with no name parameter.
    This test is expected to fail as Flask will return 404 for this route.
    """
    with app.test_client() as client:
        response = client.get("/api/greet/")
        assert response.status_code == 404
