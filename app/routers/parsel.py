from enum import Enum

from pydantic import BaseModel, AnyUrl
from fastapi import APIRouter, Depends
from parsel import Selector
from fastapi.responses import HTMLResponse

from ..util import XPATH, CSS, REGEX, default_user_agent, SelectorRetriever
from ..dependencies import ReturnStyles

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


class ParselRetriever(SelectorRetriever):
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
            elif self.path_type == self.JSON:
                json_dict = json.loads(
                    self.raw_data
                )  # Convert JSON to python dictionary
                data = dpath.util.get(
                    json_dict, self.path
                )  # Get the content of the dictionary based on the path provided
            elif self.path_type == self.XML:
                # Convert the xml into a valid python dictionary so we can parse it the same way we parse JSON
                print(self.raw_data)
                try:
                    xml_dict = xmltodict.parse(self.raw_data)
                except Exception:
                    self.error_code = 3
                    self.error_msg = (
                        "Error parsing XML data. Are you sure the data is valid XML?"
                    )
                    return data
                data = dpath.util.get(xml_dict, self.path)
        except KeyError:
            self.error_code = 1
            self.error_msg = f"Path error, please enter a valid Path value for the type '{self.path_type}'"
        except Exception as e:
            self.error_code = 2
            self.error_msg = (
                f"There was an error with your Path and Path Type combo: {e}"
            )
        return data.strip() if type(data) == str else data


@router.get("/parsel")  # , responses=get_data_response_examples())
async def parse_data_with_parsel_selectors(selector_item: ParselSelector = Depends()):
    retriever = ParselRetriever.from_selector_item(selector_item)
    await retriever.run()
    data = ParselRetriever.from_retriever(
        selector_item=selector_item,
        retriever=retriever,
    )

    if selector_item.return_style == ReturnStyles.BASIC:
        return ReturnStyles.make_basic(data)
    elif selector_item.return_style == ReturnStyles.DATA_ONLY:
        return HTMLResponse(data.path_data)
    else:
        return data
