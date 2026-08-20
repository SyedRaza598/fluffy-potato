from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.db.seed import seed_first_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as db:
        await seed_first_admin(db)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health_check():
    return {"status": "ok"}
