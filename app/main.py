from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware


from .util import user_agents
from .routers import dpath, parsel, examples
from . import config

sentry_sdk.init(
    dsn=config.settings.sentry_dsn,
    environment=config.settings.env,
    )

app = FastAPI()
app.include_router(dpath.router)
app.include_router(parsel.router)
app.include_router(examples.router)

try:
    app.add_middleware(SentryAsgiMiddleware)
except Exception:
    # pass silently if the Sentry integration failed
    print(f"Sentry integration failed, sentry_dsn config variable set to: {config.settings.env}")


@app.get("/user_agents", response_class=ORJSONResponse)
async def get_user_agents_list():
    """Returns a list of possible User-Agent examples that can be used. Useful for populating a UI that relies on this API."""
    a = 1/0
    return user_agents


@app.get("/wake")
async def get_user_agents():
    """An endpoint to wake the API up when the server is asleep on services like Heroku."""
    return True
