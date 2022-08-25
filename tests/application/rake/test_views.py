from tests import app


def test_post():
    with app.test_client() as c:
        rv = c.post(
            "/api/rake",
            json={"text": "text"},
        )
        json_data = rv.get_json()
        data = json_data["data"]
        assert type(data) is list
        assert type(data[0]) is list
        assert data[0][0] >= 0
        assert type(data[0][1]) is str


def test_another_post():
    with app.test_client() as c:
        rv = c.post(
            "/api/rake",
            json={"text": "text", "lang": "ja"},
        )
        json_data = rv.get_json()
        data = json_data["data"]
        assert type(data) is list
        assert type(data[0]) is list
        assert data[0][0] >= 0
        assert type(data[0][1]) is str
