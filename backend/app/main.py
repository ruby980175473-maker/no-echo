# ============================================================
# NO ECHO · FastAPI 应用入口（Sprint 3A 更新）
# ============================================================

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import upload, status, results, spec   # ← 新增 spec


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    Path("uploads").mkdir(exist_ok=True)
    print(f"[NO ECHO] 后端启动 · sprint=3a · env={settings.environment}")
    yield
    print("[NO ECHO] 后端关闭")


app = FastAPI(
    title="NO ECHO API",
    version="1.0.0-sprint3a",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router,  prefix="/api", tags=["upload"])
app.include_router(status.router,  prefix="/api", tags=["status"])
app.include_router(results.router, prefix="/api", tags=["results"])
app.include_router(spec.router,    prefix="/api", tags=["spec"])    # ← 新增


@app.get("/health", tags=["system"])
async def health_check() -> dict:
    return {"status": "ok", "sprint": "3a", "version": "1.0.0-sprint3a"}
