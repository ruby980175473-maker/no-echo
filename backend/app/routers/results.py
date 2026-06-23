# ============================================================
# NO ECHO · 结果查询路由
# GET /api/results/{job_id}/summary
# GET /api/results/{job_id}/detail
# GET /api/report/{job_id}/pdf
# ============================================================

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import SummaryResponse, DetailResponse

router = APIRouter()


@router.get("/results/{job_id}/summary", response_model=SummaryResponse)
async def get_summary(job_id: str) -> SummaryResponse:
    """
    返回三类风险的总览卡片数据，供 Results Overview 页渲染。
    """
    # TODO: 聚合三类风险结果，生成总览摘要
    raise NotImplementedError


@router.get("/results/{job_id}/detail", response_model=DetailResponse)
async def get_detail(job_id: str) -> DetailResponse:
    """
    返回段落级详细风险标注，供 Detail Report 页渲染。
    """
    # TODO: 查询 paragraphs + 三类风险表，组装段落级结果
    raise NotImplementedError


@router.get("/report/{job_id}/pdf")
async def export_pdf(job_id: str) -> StreamingResponse:
    """
    生成并返回 PDF 格式的检测报告。
    V1.1 实现，V1.0 返回 501 Not Implemented。
    """
    # TODO: V1.1 实现 PDF 生成（reportlab 或 weasyprint）
    raise NotImplementedError
