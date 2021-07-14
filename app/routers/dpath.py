from enum import Enum
import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel, AnyUrl
from fastapi.responses import HTMLResponse
import dpath.util
import xmltodict

from ..util import (
    get_data_response_examples,
    JSON,
    XML,
    default_user_agent,
    BaseDocumentParser,
    get_data_response_examples,
)
from ..dependencies import ReturnStyles, BaseResponse
from .examples import DocumentExamples

router = APIRouter()


class DpathPathTypes(str, Enum):
    """Valid path_type options for a DpathRequest path."""

    JSON = JSON
    XML = XML


class DpathRequest(BaseModel):
    """Model reporesenting the request a user can send."""

    url: AnyUrl
    path: str
    path_type: DpathPathTypes = DpathPathTypes.JSON
    user_agent = default_user_agent
    return_style: ReturnStyles = ReturnStyles.BASIC

    class Config:
        schema_extra = {
            "example": {
                "url": "http://localhost/examples/json",
                "path": "/note/subject",
                "path_type": "JSON",
                "user_agent": default_user_agent,
                "return_style": "BASIC",
            }
        }


class DpathDocumentParser(BaseDocumentParser):
    """Parsing logic to extract data from a document using Dpath"""

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


class DpathResponse(BaseResponse):
    """Response object returning data to the client"""

    request_item: DpathRequest


# Example data to process and show as examples of the output that can be returned to the client.
dpath_verbose_example = {
    "request_item": DpathRequest.Config.schema_extra["example"],
    "request_error": {"200": ["OK", "Request fulfilled, document follows"]},
    "parser_error": {"0": "Success"},
    "path_data": DocumentExamples.SUBJECT,
    "raw_data": DocumentExamples.JSON,
}


@router.get("/dpath", responses=get_data_response_examples(dpath_verbose_example))
async def parse_data_with_dpath_paths(request_item: DpathRequest = Depends()):
    """# Dpath

    Test some basic functionality offered by the [Dpath library](https://pypi.org/project/dpath/):

    > A python library for accessing and searching dictionaries via /slashed/paths ala xpath.
    >
    > Basically it lets you glob over a dictionary as if it were a filesystem.
    > It allows you to specify globs (ala the bash eglob syntax, through some advanced fnmatch.fnmatch magic) to access dictionary elements, and provides some facility for filtering those results.

    ---
    ### JSON
    With the JSON type, we can use the basic Dpath functionality to get data from a JSON file.

    ### XML
    The XML type converts an XML document with the [xmltodict](https://pypi.org/project/xmltodict/) library:

    > `xmltodict` is a Python module that makes working with XML feel like you are working with [JSON](http://docs.python.org/library/json.html), as in this ["spec"](http://www.xml.com/pub/a/2006/05/31/converting-between-xml-and-json.html)
    """

    # Create a parser object from the selector input
    parser = DpathDocumentParser.from_request_item(request_item)
    await parser.run()

    # Create the return object from the retrevied data
    data = DpathResponse.from_parser(
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
