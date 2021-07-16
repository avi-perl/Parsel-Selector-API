from app import config
from app.util import CacheItem
from enum import Enum
from datetime import datetime, timedelta

from pydantic import BaseModel

# TODO get rid of this trash, this should be in BaseResponse and ReturnStyles.make_basic() should be removed.
basic_format_keys = ["request_error", "path_data", "used_cache"]


class ReturnStyles(str, Enum):
    """Valid options for a SelectorItem path."""

    BASIC = "BASIC"
    DATA_ONLY = "DATA_ONLY"
    VERBOSE = "VERBOSE"

    @classmethod
    def make_basic(
        cls,
        sector_data,
        basic_keys=basic_format_keys,
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


class CacheInfo(BaseModel):
    original_request_time: datetime
    age: timedelta
    time_remaining: timedelta
    retrieved_count: int

    class Config:
        offset = timedelta(seconds=35)
        schema_extra = {
            "example": {
                "original_request_time": datetime.now() - offset,
                "age": offset,
                "time_remaining": timedelta(
                    seconds=config.settings.request_cache_max_age_seconds
                )
                - offset,
                "retrieved_count": 1,
            }
        }

    @classmethod
    def from_cached_item(cls, cached_item):
        if not cached_item:
            return None
        return cls(
            original_request_time=cached_item.created_datetime,
            age=cached_item.age,
            time_remaining=cached_item.time_remaining,
            retrieved_count=cached_item.retrieved_count,
        )


class BaseResponse(BaseModel):
    request_error: RequestError
    parser_error: ParserError
    used_cache: bool = False
    cache_info: CacheInfo = None
    path_data: str = None
    raw_data: str = None

    basic_format_keys = basic_format_keys

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
            used_cache=True if parser.cached_item else False,
            cache_info=CacheInfo.from_cached_item(parser.cached_item),
        )

    def as_basic(self):
        """Remove the keys that we do not want in a 'basic' formatted version of a SelectorData model"""
        return_data = self.__dict__.copy()
        for key in self.__dict__.keys():
            if key not in self.basic_format_keys:
                del return_data[key]
        return return_data
