# ============================================================
# NO ECHO · FastAPI 依赖注入（Dependency Injection）
# ============================================================

from fastapi import Request
from supabase import Client


def get_supabase(request: Request) -> Client:
    """从 app.state 获取 Supabase 客户端（lifespan 中初始化）"""
    return request.app.state.supabase


def get_embedding_model(request: Request):
    """从 app.state 获取 sentence-transformers 模型"""
    return request.app.state.embedding_model
