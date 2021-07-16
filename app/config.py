from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    site_url: AnyUrl = (
        "http://localhost"  # Used in examples, set as url for this hosted instance
    )

    request_cache_max_len: int = (
        50  # Number of items that can be stored in the request cache
    )
    request_cache_max_age_seconds: int = (
        60  # Number of seconds a cached request should survive
    )


settings = Settings()
