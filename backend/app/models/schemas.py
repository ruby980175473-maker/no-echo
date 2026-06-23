# ============================================================
# NO ECHO · Pydantic 数据模型
# 与前端 frontend/lib/types/index.ts 保持同步
# ============================================================

from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field
import uuid

# ── 枚举类型 ──────────────────────────────────────────────────
JobStatus        = Literal["pending", "parsing", "checking", "completed", "failed"]
RiskLevel        = Literal["high", "medium", "low", "none"]
SimilarityRiskType = Literal["web", "academic", "internal", "paraphrase"]


# ── 上传接口 ──────────────────────────────────────────────────
class UploadResponse(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: JobStatus = "pending"
    message: str


# ── 进度查询 ──────────────────────────────────────────────────
class ProgressDetail(BaseModel):
    parsing:      bool = False
    format_check: bool = False
    similarity:   bool = False
    aigc:         bool = False

class StatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    progress: ProgressDetail
    estimated_seconds_remaining: Optional[int] = None


# ── 总览摘要 ──────────────────────────────────────────────────
class RiskSummaryCard(BaseModel):
    risk_level:          RiskLevel
    risk_star:           int = Field(ge=1, le=5)
    affected_paragraphs: Optional[int] = None
    issue_count:         Optional[int] = None
    description:         str

class SummaryResponse(BaseModel):
    job_id:       str
    file_name:    str
    completed_at: str
    summary: dict[str, RiskSummaryCard]


# ── 段落级结果 ────────────────────────────────────────────────
class SentenceDetail(BaseModel):
    text:        str
    probability: float = Field(ge=0.0, le=1.0)

class SimilarityRisk(BaseModel):
    risk_level:       RiskLevel
    risk_type:        SimilarityRiskType
    source_url:       Optional[str]    = None
    source_title:     Optional[str]    = None
    matched_text:     Optional[str]    = None
    similarity_score: Optional[float]  = Field(default=None, ge=0.0, le=1.0)
    suggestion:       Optional[str]    = None

class AigcRisk(BaseModel):
    risk_level:       RiskLevel
    ai_probability:   float = Field(ge=0.0, le=1.0)
    sentence_details: Optional[list[SentenceDetail]] = None

class ParagraphRisks(BaseModel):
    similarity: Optional[SimilarityRisk] = None
    aigc:       Optional[AigcRisk]       = None

class ParagraphResult(BaseModel):
    id:            str
    index:         int
    text:          str
    heading_level: Optional[int] = None
    risks:         ParagraphRisks


# ── 格式问题 ──────────────────────────────────────────────────
class FormatIssue(BaseModel):
    section:         str
    issue_type:      str
    description:     str
    expected:        Optional[str] = None
    actual:          Optional[str] = None
    paragraph_index: Optional[int] = None

class DetailResponse(BaseModel):
    job_id:        str
    paragraphs:    list[ParagraphResult]
    format_issues: list[FormatIssue]
