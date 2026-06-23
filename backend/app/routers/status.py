# ============================================================
# NO ECHO · 进度查询路由
# GET /api/status/{job_id}
# ============================================================

from fastapi import APIRouter
from app.models.schemas import StatusResponse

router = APIRouter()


@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str) -> StatusResponse:
    """
    轮询检测任务进度。
    前端在 processing 页面每 3 秒调用一次，
    直到 status == "completed" 或 "failed"。

    Args:
        job_id: 上传时返回的任务 UUID

    Returns:
        StatusResponse: 含各模块完成状态和预计剩余秒数
    """
    # TODO: 从数据库查询 job 状态并返回
    raise NotImplementedError
