from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    env: str = "dev"
    sentry_dsn: AnyUrl = None  # Open an account at https://sentry.io/ to be assigned a dsn.

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
