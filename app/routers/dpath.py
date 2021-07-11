from enum import Enum
import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel, AnyUrl
from fastapi.responses import HTMLResponse
import dpath.util
import xmltodict

from ..util import get_data_response_examples, JSON, XML, default_user_agent, SelectorRetriever
from ..dependencies import ReturnStyles

router = APIRouter()


class DpathPathTypes(str, Enum):
    """Valid options for a DpathSelector path."""

    JSON = JSON
    XML = XML
 

class DpathSelector(BaseModel):
    url: AnyUrl
    path: str
    path_type: DpathPathTypes = DpathPathTypes.JSON
    user_agent = default_user_agent
    return_style: ReturnStyles = ReturnStyles.BASIC

    class Config:
        schema_extra = {
            "example": {
                "url": "http://parsel.aviperl.me/examples/json",
                "path": "/note/subject",
                "path_type": "JSON",
                "user_agent": default_user_agent,
                "return_style": "BASIC",
            }
        }


class DpathRetriever(SelectorRetriever):
    def _get_path_data(self):
        """Gets the path content based on the type of path that was requested"""
        data = None
        try:
            if self.path_type == self.JSON:
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


@router.get("/dpath")  # , responses=get_data_response_examples())
async def parse_data_with_dpath_paths(selector_item: DpathSelector = Depends()):
    retriever = DpathRetriever.from_selector_item(selector_item)
    await retriever.run()
    data = DpathRetriever.from_retriever(
        selector_item=selector_item,
        retriever=retriever,
    )

    if selector_item.return_style == ReturnStyles.BASIC:
        return ReturnStyles.make_basic(data)
    elif selector_item.return_style == ReturnStyles.DATA_ONLY:
        return HTMLResponse(data.path_data)
    else:
        return data
