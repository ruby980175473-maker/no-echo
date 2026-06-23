# ============================================================
# NO ECHO · Bing Search API 封装
# 参考：docs/ADR/NO_ECHO_ADR_V1.0.md ADR-005
# ============================================================

import httpx
from typing import TypedDict


class SearchResult(TypedDict):
    url:     str
    title:   str
    snippet: str


async def search_web(query: str, api_key: str, count: int = 3) -> list[SearchResult]:
    """
    调用 Bing Search API v7，返回前 n 条结果的 URL / 标题 / 摘要。

    Args:
        query:   搜索词（论文关键片段，≤50字）
        api_key: Bing Search API Key（来自 settings）
        count:   返回结果数量，默认 3

    Returns:
        list[SearchResult]

    Raises:
        httpx.TimeoutException: API 超时（由调用方处理）
        httpx.HTTPStatusError: API 返回非 2xx（由调用方处理）
    """
    # TODO: 实现
    # endpoint = "https://api.bing.microsoft.com/v7.0/search"
    # headers  = {"Ocp-Apim-Subscription-Key": api_key}
    # params   = {"q": query, "count": count, "mkt": "zh-CN"}
    raise NotImplementedError
