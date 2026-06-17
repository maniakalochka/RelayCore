import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

from app.auth.routers import (
    auth_router,
    register_router,
    reset_pwd_router,
    users_router,
    verify_router,
)
from app.core.config import settings
from app.db.session import AsyncSessionLocal, engine
from app.infrastructure.rabbitmq.connection import RabbitMQ
from app.nodes.router import router as node_router

http_bearer = HTTPBearer(auto_error=False)

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    log.info("Starting up...")
    rabbit = RabbitMQ(settings.RABBITMQ_URL)
    await rabbit.connect()
    app.state.rabbit = rabbit
    app.state.engine = engine
    app.state.session_factory = AsyncSessionLocal
    yield
    log.info("Shutting down...")
    await rabbit.close()
    await engine.dispose()


app = FastAPI(
    title="Auth Service",
    description="Service for user authentication",
    lifespan=lifespan,
)

app.include_router(
    auth_router, prefix="/auth/jwt", tags=["auth"], dependencies=[Depends(http_bearer)]
)
app.include_router(register_router, prefix="/auth", tags=["auth"])
app.include_router(reset_pwd_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(verify_router, prefix="/auth", tags=["auth"])
app.include_router(node_router, prefix="/nodes", tags=["nodes"])

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
