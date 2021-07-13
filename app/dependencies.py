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
