# ============================================================
# NO ECHO · AIGC 风险检测模块
# 职责：调用 GPTZero API，返回段落级 AI 生成概率
# 技术：GPTZero API /v2/predict/text
# 参考：docs/TDD/NO_ECHO_TDD_V1.0.md § 5.4
# ============================================================

from __future__ import annotations
from app.modules.parser.docx_parser import ParsedParagraph
from app.models.schemas import AigcRisk, RiskLevel
from app.services.gptzero import call_gptzero_api


async def detect_aigc_risk(
    paragraphs: list[ParsedParagraph],
    api_key: str,
) -> dict[int, AigcRisk]:
    """
    逐段调用 GPTZero API，返回 {paragraph_index: AigcRisk} 映射。

    容错策略：
    - API 超时 (>30s)：该段落标记为未检测，不中断整体流程
    - API 429 Rate Limit：指数退避重试，最多 3 次
    - API 5xx：记录 warning，跳过该段落

    Returns:
        dict[int, AigcRisk]: key 为段落 index
    """
    # TODO: 实现
    raise NotImplementedError


def _assign_aigc_risk_level(ai_probability: float) -> RiskLevel:
    """根据 AI 概率分配风险等级"""
    if ai_probability >= 0.80:
        return "high"
    if ai_probability >= 0.50:
        return "medium"
    if ai_probability >= 0.20:
        return "low"
    return "none"
