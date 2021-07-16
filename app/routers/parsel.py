from enum import Enum

from parsel import Selector
from pydantic import BaseModel, AnyUrl
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from .. import config
from .examples import DocumentExamples
from ..dependencies import ReturnStyles, BaseResponse, CacheInfo
from ..util import (
    XPATH,
    CSS,
    REGEX,
    default_user_agent,
    BaseDocumentParser,
    get_data_response_examples,
)

router = APIRouter()


class ParselPathTypes(str, Enum):
    """Valid path_type options for a ParselRequest path."""

    XPATH = XPATH
    CSS = CSS
    REGEX = REGEX


class ParselRequest(BaseModel):
    """Model reporesenting the request a user can send."""

    url: AnyUrl
    path: str
    path_type: ParselPathTypes = ParselPathTypes.XPATH
    user_agent = default_user_agent
    return_style: ReturnStyles = ReturnStyles.BASIC

    class Config:
        schema_extra = {
            "example": {
                "url": f"{config.settings.site_url}/examples/html",
                "path": "/html/body/h1/text()",
                "path_type": XPATH,
                "user_agent": default_user_agent,
                "return_style": ReturnStyles.BASIC,
            }
        }


class ParselDocumentParser(BaseDocumentParser):
    """Parsing logic to extract data from a document using Parsel Selector"""

    def _get_path_data(self):
        """Gets the path content based on the type of path that was requested"""
        data = None
        try:
            selector = Selector(text=self.raw_data)
            if self.path_type == self.XPATH:
                data = selector.xpath(self.path).get()
            elif self.path_type == self.CSS:
                data = selector.css(self.path).get()
            elif self.path_type == self.REGEX:
                data = selector.re(self.path)
        except KeyError:
            self.error_code = 1
            self.error_msg = f"Path error, please enter a valid Path value for the type '{self.path_type}'"
        except Exception as e:
            self.error_code = 2
            self.error_msg = (
                f"There was an error with your Path and Path Type combo: {e}"
            )
        return data.strip() if type(data) == str else data


class ParselResponse(BaseResponse):
    """Response object returning data to the client"""

    request_item: ParselRequest


# Example data to process and show as examples of the output that can be returned to the client.
parsel_verbose_example = {
    "request_item": ParselRequest.Config.schema_extra["example"],
    "request_error": {"200": ["OK", "Request fulfilled, document follows"]},
    "parser_error": {"0": "Success"},
    "used_cache": True,
    "cache_info": CacheInfo.Config.schema_extra["example"],
    "path_data": DocumentExamples.SUBJECT,
    "raw_data": DocumentExamples.HTML,
}


@router.get("/parsel", responses=get_data_response_examples(parsel_verbose_example))
async def parse_data_with_parsel_selectors(request_item: ParselRequest = Depends()):
    """# Parsel

    Test some basic functionality offered by the [Parsel library](https://parsel.readthedocs.io/en/latest/usage.html):

    > Parsel is a BSD-licensed Python library to extract and remove data from HTML and XML using XPath and CSS selectors, optionally combined with regular expressions.
    >
    > Find the Parsel online documentation at [https://parsel.readthedocs.org](https://parsel.readthedocs.org).

    ---
    ### XPATH
    With the XPATH type, we can use the basic Parsel `Selector.xpath("/some/path").get()` functionality to get data from an HTML file.

    ### CSS
    With the CSS type, we can use the basic Parsel `Selector.css("/some/path").get()` functionality to get data from an HTML file.

    ### REGEX
    With the CSS type, we can use the basic Parsel `Selector.re("some pattern.*")` functionality to get data from an HTML file.
    """

    # Create a parser object from the request input
    parser = ParselDocumentParser.from_request_item(request_item)
    await parser.run()

    # Create the return object from the retrevied data
    data = ParselResponse.from_parser(
        request_item=request_item,
        parser=parser,
    )

    # Mutate the return object based on the requested return_style
    if request_item.return_style == ReturnStyles.BASIC:
        return data.as_basic()
    elif request_item.return_style == ReturnStyles.DATA_ONLY:
        return HTMLResponse(data.path_data)
    else:
        return data
