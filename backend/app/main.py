# ============================================================
# NO ECHO · FastAPI 应用入口
# ============================================================

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import upload, status, results


# ── 生命周期：启动时加载重型资源 ──────────────────────────────
@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """
    在 FastAPI 启动时执行：
    1. 预加载 sentence-transformers 模型（避免首次请求时的冷启动延迟）
    2. 初始化 Supabase 客户端
    在关闭时：释放资源
    """
    # TODO: 预加载 sentence-transformers 模型
    # from sentence_transformers import SentenceTransformer
    # app.state.embedding_model = SentenceTransformer(
    #     settings.embedding_model_name,
    #     cache_folder=settings.model_cache_dir
    # )

    # TODO: 初始化 Supabase 客户端
    # from supabase import create_client
    # app.state.supabase = create_client(settings.supabase_url, settings.supabase_anon_key)

    print(f"[startup] NO ECHO backend ready · env={settings.environment}")
    yield
    # TODO: 清理资源（如需要）
    print("[shutdown] NO ECHO backend shutting down")


# ── FastAPI 应用实例 ───────────────────────────────────────────
app = FastAPI(
    title="NO ECHO API",
    description="论文预检平台后端 API · 重复风险 × AIGC风险 × 格式检查",
    version="1.0.0",
    docs_url="/docs" if not settings.is_production else None,  # 生产环境关闭 Swagger
    redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan,
)

# ── CORS 配置 ─────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # TODO: 生产环境替换为实际域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 路由注册 ──────────────────────────────────────────────────
app.include_router(upload.router,  prefix="/api",  tags=["upload"])
app.include_router(status.router,  prefix="/api",  tags=["status"])
app.include_router(results.router, prefix="/api",  tags=["results"])


# ── 健康检查 ──────────────────────────────────────────────────
@app.get("/health", tags=["system"])
async def health_check() -> dict:
    """Nginx 和 Docker healthcheck 使用此接口"""
    return {"status": "ok", "version": "1.0.0"}
