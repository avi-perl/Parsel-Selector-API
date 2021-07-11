from typing import Dict
from enum import Enum

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, Response, ORJSONResponse
from pydantic import BaseModel, AnyUrl

from .util import (
    ParselSelectorRetriever,
    user_agents,
    get_data_response_examples,
    DocumentExamples,
)

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
        basic_keys=["selector_item", "request_error", "path_data"],
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

class RequestError(BaseModel):
    code: int
    msg: list

class ParserError(BaseModel):
    code: int
    msg: str

class SelectorData(BaseModel):
    selector_item: SelectorItem
    request_error: RequestError
    parser_error: ParserError
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
            request_error=RequestError(code=retriever.status_code, msg=retriever.status_msg),
            parser_error=ParserError(code=retriever.error_code, msg=retriever.error_msg),
            path_data=retriever.path_data,
            raw_data=retriever.raw_data,
        )


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
        return HTMLResponse(data.path_data)
    else:
        return data


@app.get("/examples/html", response_class=HTMLResponse)
async def return_html_example():
    """Returns a basic HTML response for testing."""
    return HTMLResponse(content=DocumentExamples.HTML)


@app.get("/examples/json", response_class=ORJSONResponse)
async def return_html_example():
    """Returns a basic JSON response for testing."""
    return DocumentExamples.JSON


@app.get("/examples/xml", response_class=HTMLResponse)
async def return_html_example():
    """Returns a basic JSON response for testing."""
    return Response(content=DocumentExamples.XML, media_type="application/xml")


@app.get("/user_agents", response_class=ORJSONResponse)
async def get_user_agents_list():
    """Returns a list of possible User-Agent examples that can be used. Useful for populating a UI that relies on this API."""
    return user_agents


@app.get("/wake")
async def get_user_agents():
    """An endpoint to wake the API up when the server is asleep on services like Heroku."""
    return True
