# ============================================================
# NO ECHO · 上传路由
# POST /api/upload
# ============================================================

from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.schemas import UploadResponse

router = APIRouter()


@router.post("/upload", response_model=UploadResponse, status_code=202)
async def upload_file(
    file: UploadFile = File(...),
    template: UploadFile | None = File(default=None),
) -> UploadResponse:
    """
    接收用户上传的论文 DOCX 文件（以及可选的格式模板），
    验证格式和大小后存入 Supabase Storage，
    创建检测任务记录并触发异步检测流程。

    Args:
        file: 论文 DOCX 文件（必填）
        template: 格式模板 DOCX 文件（可选）

    Returns:
        UploadResponse: 含 job_id 和初始状态

    Raises:
        HTTPException 415: 文件格式不支持
        HTTPException 413: 文件超过大小限制
    """
    # TODO: 实现
    # 1. 校验 MIME Type 是否为 DOCX
    # 2. 校验文件大小是否超过 settings.max_file_size_mb
    # 3. 上传文件到 Supabase Storage
    # 4. 在 jobs 表创建记录（status=pending）
    # 5. 触发异步检测任务
    raise NotImplementedError
