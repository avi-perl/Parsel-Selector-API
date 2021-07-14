import json

import dpath.util
import xmltodict
from fastapi.testclient import TestClient
from parsel import Selector

from .main import app
from .dependencies import BaseResponse, RequestError, ParserError
from .routers.dpath import DpathResponse, DpathRequest


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


def test_as_basic():
    """Verify that the function to format a response in "basic" is functioning"""
    request = DpathRequest(
        url="http://localhost/examples/json",
        path="/note/subject",
        path_type="JSON",
        user_agent="some user agent",
        return_style="BASIC",
    )
    response = DpathResponse(
        request_item=request,
        request_error=RequestError(code=0, msg=["error", "some error msg"]),
        parser_error=ParserError(code=0, msg="some error msg"),
        path_data="some path data",
        raw_data="some raw data",
    )
    basic_format_keys = response.basic_format_keys.sort()
    basic_format_response_keys = list(response.as_basic()).sort()
    # Assert that after the response is processed, the keys that are returned are only the keys we specified.
    assert basic_format_keys == basic_format_response_keys
