# ============================================================
# NO ECHO · Semantic Scholar API 封装（免费，无需 Key）
# 用于学术资源相似度检测
# ============================================================

import httpx
from typing import TypedDict


class PaperResult(TypedDict):
    paper_id: str
    title:    str
    abstract: str
    url:      str


async def search_papers(query: str, limit: int = 3) -> list[PaperResult]:
    """
    调用 Semantic Scholar Graph API 搜索相关论文。

    Args:
        query: 搜索词
        limit: 返回论文数量

    Returns:
        list[PaperResult]
    """
    # TODO: 实现
    # endpoint = "https://api.semanticscholar.org/graph/v1/paper/search"
    # params   = {"query": query, "limit": limit, "fields": "title,abstract,url"}
    raise NotImplementedError
