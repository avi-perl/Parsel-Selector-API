from typing import Optional
from enum import Enum, IntEnum

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, AnyUrl

from .util import ParselSelectorRetriever, user_agents

app = FastAPI()


class PathTypes(str, Enum):
    """Valid options for a SelectorItem path."""

    XPATH = ParselSelectorRetriever.XPATH
    CSS = ParselSelectorRetriever.CSS
    REGEX = ParselSelectorRetriever.REGEX
    JSON = ParselSelectorRetriever.JSON
    XML = ParselSelectorRetriever.XML


class ReturnStyles(str, Enum):
    """Valid options for a SelectorItem path."""

    BASIC = "BASIC"
    DATA_ONLY = "DATA_ONLY"
    VERBOSE = "VERBOSE"

    @classmethod
    def make_basic(
        cls,
        sector_data,
        basic_keys=["selector_item", "status_code", "status_msg", "path_data"],
    ):
        """Remove the keys that we do not want in a 'basic' formatted version of a SelectorData model"""
        keys = (
            sector_data.copy().keys()
            if isinstance(sector_data, dict)
            else sector_data.__dict__.copy()
        )
        for key in keys:
            if key not in basic_keys:
                if isinstance(sector_data, dict):
                    del sector_data[key]
                else:
                    del sector_data.__dict__[key]
        return sector_data


class SelectorItem(BaseModel):
    url: AnyUrl
    path: str
    path_type: PathTypes = PathTypes.XPATH
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    return_style: ReturnStyles = ReturnStyles.BASIC

    class Config:
        schema_extra = {
            "example": {
                "url": "http://parsel.aviperl.me/examples/html",
                "path": "/html/body/h1/text()",
                "path_type": "XPATH",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                "return_style": "BASIC",
            }
        }


class SelectorData(BaseModel):
    selector_item: SelectorItem
    status_code: int
    status_msg: tuple
    path_data: str = None
    raw_data: str = None

    @classmethod
    def from_retriever(
        cls,
        selector_item: SelectorItem,
        retriever: ParselSelectorRetriever,
    ):
        return cls(
            selector_item=selector_item,
            status_code=retriever.status_code,
            status_msg=retriever.status_msg,
            path_data=retriever.path_data,
            raw_data=retriever.raw_data,
        )


class DocumentExamples:
    """Example data for example pages"""

    _html_h1_content = "You scraped me 🤕"
    HTML = f"<html><head><title>Title of the HTML example.</title></head><body><h1>{_html_h1_content}</h1></body></html>"


def get_data_response_examples():
    """Generates the example responses for the docs while trying to be as dynamic as possible."""
    verbose_example = {
        "selector_item": SelectorItem.Config.schema_extra["example"],
        "status_code": 200,
        "status_msg": ["OK", "Request fulfilled, document follows"],
        "path_data": DocumentExamples._html_h1_content,
        "raw_data": DocumentExamples.HTML,
    }
    data_responses = {
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "examples": {
                        "BASIC": {
                            "summary": "BASIC",
                            "value": ReturnStyles.make_basic(verbose_example.copy()),
                        },
                        "DATA_ONLY": {
                            "summary": "DATA_ONLY",
                            "value": verbose_example.get("path_data", "string"),
                        },
                        "VERBOSE": {
                            "summary": "VERBOSE",
                            "value": verbose_example,
                        },
                    }
                }
            },
        },
    }
    return data_responses


@app.get("/", responses=get_data_response_examples())
async def get_data(selector_item: SelectorItem = Depends()):
    retriever = ParselSelectorRetriever.from_selector_item(selector_item)
    await retriever.run()
    data = SelectorData.from_retriever(
        selector_item=selector_item,
        retriever=retriever,
    )

    if selector_item.return_style == ReturnStyles.BASIC:
        return ReturnStyles.make_basic(data)
    elif selector_item.return_style == ReturnStyles.DATA_ONLY:
        return data.path_data
    else:
        return data


@app.get("/examples/html", response_class=HTMLResponse)
async def return_html_example():
    """Returns a basic HTML response for testing."""
    return HTMLResponse(content=DocumentExamples.HTML, status_code=200)


@app.get("/user_agents")
async def get_user_agents_list():
    """Returns a list of possible User-Agent examples that can be used. Useful for populating a UI that relies on this API."""
    return user_agents


@app.get("/wake")
async def get_user_agents():
    """An endpoint to wake the API up when the server is asleep on services like Heroku."""
    return True
