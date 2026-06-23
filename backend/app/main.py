# ============================================================
# NO ECHO · FastAPI 应用入口
# Sprint 1: 只启用上传路由，其余路由 NotImplementedError 不影响启动
# ============================================================

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import upload, status, results


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """
    服务启动时：
    - Sprint 1: 创建本地 uploads 目录
    - Sprint 2+: 初始化 Supabase 客户端
    - Sprint 3+: 预加载 sentence-transformers 模型
    """
    # Sprint 1: 确保本地上传目录存在
    Path("uploads").mkdir(exist_ok=True)
    print(f"[NO ECHO] 后端启动成功 · 环境={settings.environment}")
    print(f"[NO ECHO] 文件大小限制={settings.max_file_size_mb}MB")
    print(f"[NO ECHO] 上传目录=./uploads/")

    # TODO[S2]: 初始化 Supabase 客户端
    # from supabase import create_client
    # _app.state.supabase = create_client(settings.supabase_url, settings.supabase_anon_key)

    # TODO[S3]: 预加载 sentence-transformers 模型
    # from sentence_transformers import SentenceTransformer
    # _app.state.embedding_model = SentenceTransformer(settings.embedding_model_name)

    yield

    print("[NO ECHO] 后端关闭")


app = FastAPI(
    title="NO ECHO API",
    description="本科论文预检平台 · 重复风险 × AIGC风险 × 格式检查",
    version="1.0.0-sprint1",
    docs_url="/docs",   # 开发阶段保持开启，方便调试
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS（允许前端 localhost:3000 跨域访问）───────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 路由注册 ──────────────────────────────────────────────────
app.include_router(upload.router,  prefix="/api", tags=["upload"])
app.include_router(status.router,  prefix="/api", tags=["status"])
app.include_router(results.router, prefix="/api", tags=["results"])


# ── 健康检查（Docker / Nginx healthcheck 使用）────────────────
@app.get("/health", tags=["system"])
async def health_check() -> dict:
    return {
        "status": "ok",
        "sprint": 1,
        "version": "1.0.0-sprint1",
    }
