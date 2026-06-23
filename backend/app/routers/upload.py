# ============================================================
# NO ECHO · 上传路由
# Sprint 1 实现：接收文件 → 校验 → 保存到本地 → 返回 job_id
#
# Sprint 2+ 需要替换的地方（已用 # TODO[S2] 标注）：
#   - 本地 UPLOAD_DIR 替换为 Supabase Storage
#   - 在 jobs 数据库表中创建记录
#   - 触发异步检测任务
# ============================================================

import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.models.schemas import UploadResponse
from app.utils.file_validator import validate_docx

router = APIRouter()

# Sprint 1: 本地临时存储目录
# TODO[S2]: 替换为 Supabase Storage（supabase.storage.from_("uploads").upload(...)）
UPLOAD_DIR = Path("uploads")


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=202,
    summary="上传论文 DOCX 文件",
    description="校验文件格式和大小，保存到本地，返回任务 ID。Sprint 1 不触发任何检测逻辑。",
)
async def upload_file(
    file: UploadFile = File(..., description="论文 .docx 文件（必填，最大 20MB）"),
    template: UploadFile | None = File(default=None, description="格式模板 .docx（可选）"),
) -> UploadResponse:
    # ── Step 1: 校验文件格式 ──────────────────────────────────
    await validate_docx(file)

    # ── Step 2: 读取文件内容到内存 ────────────────────────────
    content = await file.read()

    # ── Step 3: 校验文件大小 ──────────────────────────────────
    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        size_mb = len(content) / 1024 / 1024
        raise HTTPException(
            status_code=413,
            detail=(
                f"文件太大（{size_mb:.1f}MB），"
                f"最大支持 {settings.max_file_size_mb}MB"
            ),
        )

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="文件内容为空，请重新选择文件")

    # ── Step 4: 生成唯一任务 ID ───────────────────────────────
    job_id = str(uuid.uuid4())

    # ── Step 5: 保存文件到本地 ────────────────────────────────
    # TODO[S2]: 替换为：
    #   supabase = request.app.state.supabase
    #   supabase.storage.from_("uploads").upload(f"{job_id}.docx", content)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / f"{job_id}.docx"
    file_path.write_bytes(content)

    # ── Step 6: 在数据库创建 job 记录 ─────────────────────────
    # TODO[S2]: 替换为：
    #   supabase.table("jobs").insert({
    #       "id": job_id, "status": "pending",
    #       "file_name": file.filename, "file_path": str(file_path)
    #   }).execute()

    size_kb = len(content) / 1024
    return UploadResponse(
        job_id=job_id,
        status="pending",
        message=f"上传成功：{file.filename}（{size_kb:.0f} KB）",
    )
