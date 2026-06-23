# ============================================================
# NO ECHO · 风险评分聚合逻辑
# 将三类检测结果聚合为总览卡片和段落级风险映射
# 参考：docs/TDD/NO_ECHO_TDD_V1.0.md § 5.5
# ============================================================

from app.models.schemas import RiskLevel, RiskSummaryCard, FormatIssue


def compute_similarity_summary(risks: list) -> RiskSummaryCard:
    """根据重复风险列表生成总览卡片"""
    # TODO: 统计 high/medium 数量，映射到 risk_level 和 risk_star
    raise NotImplementedError


def compute_aigc_summary(risks: list) -> RiskSummaryCard:
    """根据 AIGC 风险列表生成总览卡片"""
    raise NotImplementedError


def compute_format_summary(issues: list[FormatIssue]) -> RiskSummaryCard:
    """根据格式问题列表生成总览卡片"""
    raise NotImplementedError


def assign_similarity_risk_level(score: float, risk_type: str) -> RiskLevel:
    """根据相似度分数和风险类型分配等级"""
    if risk_type == "internal":
        return "high"
    if risk_type == "web" and score >= 0.90:
        return "high"
    if risk_type == "web" and score >= 0.75:
        return "medium"
    if risk_type == "academic" and score >= 0.85:
        return "high"
    if risk_type == "paraphrase" and score >= 0.85:
        return "medium"
    return "low"
