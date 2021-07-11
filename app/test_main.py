import json

from fastapi.testclient import TestClient
from parsel import Selector
import dpath.util
import xmltodict

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
    assert selector.xpath("/html/body/div/span[3]/text()").get() is not None


def test_example_css():
    response = client.get("/examples/html")
    data = response.text
    # Verify that elements needed for further tests and documentation are returned with the path we expect.
    selector = Selector(text=data)
    assert selector.css("body > div > span:nth-child(5)").get() is not None


def test_example_regex():
    response = client.get("/examples/html")
    data = response.text
    # Verify that elements needed for further tests and documentation are returned with the path we expect.
    selector = Selector(text=data)
    assert selector.re("<span><strong>.*:<\/strong> (.*)<\/span>") is not None


def test_example_json():
    response = client.get("/examples/json")
    data = response.text
    # Verify that elements needed for further tests and documentation are returned with the path we expect.
    json_dict = json.loads(data)
    assert dpath.util.get(json_dict, "/note/subject") is not None


def test_example_xml():
    response = client.get("/examples/xml")
    data = response.text
    # Verify that elements needed for further tests and documentation are returned with the path we expect.
    assert dpath.util.get(xmltodict.parse(data), "/note/subject") is not None
