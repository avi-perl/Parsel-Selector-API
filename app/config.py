from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):

    env: str = "dev"
    debug: bool = False
    app_title: str = "Parsel Selector API"
    redoc_url: str = "/"
    docs_url: str = "/docs"
    app_description: str = f"An API for selecting part of a document on the web based on a path to the content. <br><br> **Documentation** <ul><li>[Redoc Documentation]({redoc_url})</li><li>[Interactive Swagger Documentation]({docs_url})</li></ul>"
    sentry_dsn: AnyUrl = (
        None  # Open an account at https://sentry.io/ to be assigned a dsn.
    )

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
