from typing import Optional
from enum import Enum, IntEnum

from fastapi import FastAPI
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


class SelectorItem(BaseModel):
    url: AnyUrl
    path: str = "/html"
    path_type: PathTypes = PathTypes.XPATH
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"

    class Config:
        schema_extra = {
            "example": {
                "url": "https://aviperl.me/",
                "path": "/html/body/div/div/main/div/div[1]/div[1]/div[2]/div/div[3]/div/a[2]/text()",
                "path_type": "XPATH",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            }
        }

class SelectorData(BaseModel):
    selector_item: SelectorItem
    status_code: int
    status_msg: tuple
    path_data: Optional[str]

    @classmethod
    def from_parsel_selector_retriever(
        cls, selector_item: SelectorItem, retriever: ParselSelectorRetriever
    ):
        return cls(
            selector_item=selector_item,
            status_code=retriever.status_code,
            status_msg=retriever.status_msg,
            path_data=retriever.path_data,
        )


class SelectorDataVerbose(SelectorData):
    raw_data: Optional[str]

    @classmethod
    def from_parsel_selector_retriever(
        cls, selector_item: SelectorItem, retriever: ParselSelectorRetriever
    ):
        return cls(
            selector_item=selector_item,
            status_code=retriever.status_code,
            status_msg=retriever.status_msg,
            path_data=retriever.path_data,
            raw_data=retriever.raw_data,
        )


@app.post("/", response_model=SelectorData)
async def get_data(selector_item: SelectorItem):
    retriever = ParselSelectorRetriever.from_selector_item(selector_item)
    await retriever.run()
    return SelectorData.from_parsel_selector_retriever(
        selector_item=selector_item, retriever=retriever
    )


@app.post("/data_only")
async def get_data_only(selector_item: SelectorItem):
    """Works the same as the root endpoint, but only the path_data is returned."""
    retriever = ParselSelectorRetriever.from_selector_item(selector_item)
    await retriever.run()
    return retriever.path_data


@app.post("/verbose", response_model=SelectorDataVerbose)
async def get_data_verbose(selector_item: SelectorItem):
    """Works the same as the root endpoint, but more data is returned."""
    retriever = ParselSelectorRetriever.from_selector_item(selector_item)
    await retriever.run()
    return SelectorDataVerbose.from_parsel_selector_retriever(
        selector_item=selector_item, retriever=retriever
    )

@app.get("/user_agents")
async def get_user_agents():
    return user_agents
