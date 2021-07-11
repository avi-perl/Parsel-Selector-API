from fastapi.testclient import TestClient
from parsel import Selector

from .main import app

client = TestClient(app)


def test_wake():
    response = client.get("/wake")
    assert response.status_code == 200


def test_user_agents():
    response = client.get("/user_agents")
    data = response.json()
    # Verify that the returned object is a list, and that all of its elements are strings.
    assert bool(data)
    assert isinstance(data, list)
    assert all(isinstance(elem, str) for elem in data)


def test_example_html():
    response = client.get("/examples/html")
    data = response.text
    # Verify that elements needed for further tests and documentation are returned with the path we expect.
    selector = Selector(text=data)
    assert selector.xpath("/html/body/h1").get() is not None