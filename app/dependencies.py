from enum import Enum

from pydantic import BaseModel


class ReturnStyles(str, Enum):
    """Valid options for a SelectorItem path."""

    BASIC = "BASIC"
    DATA_ONLY = "DATA_ONLY"
    VERBOSE = "VERBOSE"

    @classmethod
    def make_basic(
        cls,
        sector_data,
        basic_keys=["request_error", "path_data"],
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


class RequestError(BaseModel):
    code: int
    msg: list


class ParserError(BaseModel):
    code: int
    msg: str


class BaseResponse(BaseModel):
    request_error: RequestError
    parser_error: ParserError
    path_data: str = None
    raw_data: str = None

    basic_format_keys = ["request_error", "path_data"]

    @classmethod
    def from_parser(
        cls,
        request_item,
        parser,
    ):
        return cls(
            request_item=request_item,
            request_error=RequestError(code=parser.status_code, msg=parser.status_msg),
            parser_error=ParserError(code=parser.error_code, msg=parser.error_msg),
            path_data=parser.path_data,
            raw_data=parser.raw_data,
        )

    def as_basic(self):
        """Remove the keys that we do not want in a 'basic' formatted version of a SelectorData model"""
        return_data = self.__dict__.copy()
        for key in self.__dict__.keys():
            if key not in self.basic_format_keys:
                del return_data[key]
        return return_data
