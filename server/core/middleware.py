from secrets import token_urlsafe

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware


# TODO: CUSTOM MIDDLEWARE HERE!
middlewareList = []


def registerMiddleware(app: FastAPI) -> None:
    app.add_middleware(SessionMiddleware, secret_key=token_urlsafe(128))
    app.add_middleware(GZipMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=600,
    )
    middlewareList.reverse()
    for middleware in middlewareList:
        app.add_middleware(middleware)
