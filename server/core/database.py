from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from arq import create_pool
from arq.connections import ArqRedis, RedisSettings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from beanie.odm.operators.update.general import Set

from server.core import settings
from server.models import gather_documents


redisPool: Optional[ArqRedis] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = AsyncIOMotorClient(settings.db.uri, uuidRepresentation="standard")
    await init_beanie(
        database=getattr(app.client, settings.db.name),
        document_models=gather_documents(),
    )

    redisPool = await create_pool(
        RedisSettings(host=settings.redis.host, port=settings.redis.port)
    )

    # TODO: initializeDB
    # for name, url in defaultPlatforms:
    #     await Platform.find_one(Platform.name == name).upsert(
    #         Set({Platform.url: url}), on_insert=Platform(name=name, url=url)
    #     )

    yield
    redisPool.close()
