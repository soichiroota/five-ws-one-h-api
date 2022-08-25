import pytest

from five_ws_one_h_api import create_app

app = create_app()


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
