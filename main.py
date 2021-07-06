from typing import Optional
from enum import Enum, IntEnum

from fastapi import FastAPI, Depends
from pydantic import BaseModel, AnyUrl

from util import ParselSelectorRetriever, user_agents

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

    DATA_ONLY = "DATA_ONLY"
    BASIC = "BASIC"
    VERBOSE = "VERBOSE"

    basic_keys = ["selector_item", "status_code", "status_msg", "path_data"]

    @classmethod
    def make_basic(cls, sector_data):
        for key in sector_data.__dict__.copy():
            if key not in cls.basic_keys:
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
                "url": "https://aviperl.me/",
                "path": "/html/body/div/div/main/div/div[1]/div[1]/div[2]/div/div[3]/div/a[2]/text()",
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


@app.get("/")
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


@app.get("/user_agents")
async def get_user_agents():
    return user_agents
