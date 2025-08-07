import pytest
from AUTH.Authentication import app, users, tasks

@pytest.fixture
def client():
    with app.test_client() as client:
        users.clear()  # Clear users before each test
        tasks.clear()  # Clear tasks before each test
        yield client