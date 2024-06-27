from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from db.config import db
from api.routers import cart_router
from api.models_init import CartUser
from redis import asyncio as aioredis
from config import settings



async def startup():
    await init_beanie(
        database=db,
        document_models=[
            CartUser,
        ]
    )
    app.include_router(cart_router)
    redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}",
                              encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


async def shutdown():
    # Add any shutdown logic here, if needed
    pass


app = FastAPI(on_startup=[startup], on_shutdown=[shutdown], title="Корзина пользователя")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
