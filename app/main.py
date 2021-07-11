from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .util import user_agents
from .routers import dpath, parsel, examples

app = FastAPI()
app.include_router(dpath.router)
app.include_router(parsel.router)
app.include_router(examples.router)


@app.get("/user_agents", response_class=ORJSONResponse)
async def get_user_agents_list():
    """Returns a list of possible User-Agent examples that can be used. Useful for populating a UI that relies on this API."""
    return user_agents


@app.get("/wake")
async def get_user_agents():
    """An endpoint to wake the API up when the server is asleep on services like Heroku."""
    return True
