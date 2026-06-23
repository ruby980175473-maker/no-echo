# ============================================================
# NO ECHO · GPTZero API 封装
# 参考：docs/ADR/NO_ECHO_ADR_V1.0.md ADR-007
# ============================================================

import httpx
from typing import TypedDict


class SentenceScore(TypedDict):
    sentence:       str
    generated_prob: float


class GptzeroResult(TypedDict):
    completely_generated_prob: float
    sentences:                 list[SentenceScore]


async def call_gptzero_api(text: str, api_key: str) -> GptzeroResult:
    """
    调用 GPTZero /v2/predict/text 接口，返回段落级 AI 生成概率和句子级详情。

    容错：
    - 超时默认 30s，由调用方（detector.py）负责 retry 逻辑
    - multilingual=True 启用多语言支持（中文）

    Args:
        text:    待检测文本（单个段落）
        api_key: GPTZero API Key

    Returns:
        GptzeroResult
    """
    # TODO: 实现
    # endpoint = "https://api.gptzero.me/v2/predict/text"
    # headers  = {"x-api-key": api_key, "Content-Type": "application/json"}
    # payload  = {"document": text, "multilingual": True}
    raise NotImplementedError
