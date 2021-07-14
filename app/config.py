from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    site_url: AnyUrl = "http://localhost"  # Used in examples


settings = Settings()