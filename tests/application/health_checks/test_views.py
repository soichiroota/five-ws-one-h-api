from tests import app


def test_get():
    with app.test_client() as c:
        rv = c.get("/", json={})
        json_data = rv.get_json()
        assert json_data.get("message") == "Hello World!"
