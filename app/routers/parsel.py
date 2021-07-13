from enum import Enum

from pydantic import BaseModel, AnyUrl
from fastapi import APIRouter, Depends
from parsel import Selector
from fastapi.responses import HTMLResponse

from ..util import (
    XPATH,
    CSS,
    REGEX,
    default_user_agent,
    BaseDocumentParser,
    get_data_response_examples,
)
from ..dependencies import ReturnStyles, RequestError, ParserError
from .examples import DocumentExamples

router = APIRouter()


class ParselPathTypes(str, Enum):
    """Valid options for a ParselSelector path."""

    XPATH = XPATH
    CSS = CSS
    REGEX = REGEX


class ParselSelector(BaseModel):
    url: AnyUrl
    path: str
    path_type: ParselPathTypes = ParselPathTypes.XPATH
    user_agent = default_user_agent
    return_style: ReturnStyles = ReturnStyles.BASIC

    class Config:
        schema_extra = {
            "example": {
                "url": "http://parsel.aviperl.me/examples/html",
                "path": "/html/body/h1/text()",
                "path_type": "XPATH",
                "user_agent": default_user_agent,
                "return_style": "BASIC",
            }
        }


class ParselRetriever(BaseDocumentParser):
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


class SelectorData(BaseModel):
    selector_item: ParselSelector
    request_error: RequestError
    parser_error: ParserError
    path_data: str = None
    raw_data: str = None

    @classmethod
    def from_retriever(
        cls,
        selector_item: ParselSelector,
        retriever: ParselRetriever,
    ):
        return cls(
            selector_item=selector_item,
            request_error=RequestError(
                code=retriever.status_code, msg=retriever.status_msg
            ),
            parser_error=ParserError(
                code=retriever.error_code, msg=retriever.error_msg
            ),
            path_data=retriever.path_data,
            raw_data=retriever.raw_data,
        )


verbose_example = {
    "selector_item": ParselSelector.Config.schema_extra["example"],
    "request_error": {"200": ["OK", "Request fulfilled, document follows"]},
    "parser_error": {"0": "Success"},
    "path_data": DocumentExamples.SUBJECT,
    "raw_data": DocumentExamples.HTML,
}


@router.get("/parsel", responses=get_data_response_examples(verbose_example))
async def parse_data_with_parsel_selectors(selector_item: ParselSelector = Depends()):
    retriever = ParselRetriever.from_selector_item(selector_item)
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
