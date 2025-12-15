import pytest
from unittest.mock import MagicMock
from main import app   # import your Flask app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_main_route(client, monkeypatch):
    # Create a fake BigQuery client
    fake_client = MagicMock()

    # Mock load_table_from_uri to return a fake job
    fake_job = MagicMock()
    fake_job.result.return_value = None
    fake_client.load_table_from_uri.return_value = fake_job

    # Mock get_table to return a fake table with num_rows
    fake_table = MagicMock()
    fake_table.num_rows = 42
    fake_client.get_table.return_value = fake_table

    # Monkeypatch the default client in your route
    monkeypatch.setattr("main.client", fake_client)

    # Call the Flask route
    response = client.get("/")

    # Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"data": 42}

    # Verify BigQuery methods were called
    fake_client.load_table_from_uri.assert_called_once()
    fake_client.get_table.assert_called_once()
