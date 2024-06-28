from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from server import __name__, __version__
from server.core import settings
from server.core.database import lifespan
from server.core.middleware import registerMiddleware

app = FastAPI(
    debug=settings.debug_mode,
    title=__name__,
    version=__version__,
    lifespan=lifespan,
)

registerMiddleware(app)


@app.get("/")
async def root():
    return settings.model_dump()


# app.mount("/assets", StaticFiles(directory="public/assets"), name="static")


# @app.get("/", include_in_schema=False)
# def svelte_homepage():
#     return FileResponse("public/index.html")


# @app.get("/favicon.ico")
# def favicon():
#     return FileResponse("public/assets/images/favicon.ico")
