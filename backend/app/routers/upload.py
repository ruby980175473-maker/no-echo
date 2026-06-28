# ============================================================
# NO ECHO · 上传路由（Sprint 2 更新）
# Sprint 1: 接收文件 → 保存本地
# Sprint 2: 接收文件 → 保存本地 → 解析为 DocumentModel → 存 JSON
# ============================================================

import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.models.schemas import UploadResponse
from app.modules.parser.docx_parser import parse_document
from app.utils.file_validator import validate_docx

router = APIRouter()

UPLOAD_DIR = Path("uploads")


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=202,
    summary="上传论文 DOCX 文件（Sprint 2：上传后自动解析为 DocumentModel）",
)
async def upload_file(
    file: UploadFile = File(...),
    template: UploadFile | None = File(default=None),
) -> UploadResponse:
    # ── Step 1: 校验格式 ──────────────────────────────────────
    await validate_docx(file)

    # ── Step 2: 读取并校验大小 ────────────────────────────────
    content = await file.read()
    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"文件太大（{len(content)/1024/1024:.1f}MB），最大 {settings.max_file_size_mb}MB",
        )
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="文件内容为空")

    # ── Step 3: 保存 DOCX 到本地 ──────────────────────────────
    job_id = str(uuid.uuid4())
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    docx_path = UPLOAD_DIR / f"{job_id}.docx"
    docx_path.write_bytes(content)

    # ── Step 4: 解析为 DocumentModel 并保存 JSON ─────────────
    # Sprint 2 新增：所有后续检测模块读此 JSON，不再重新解析 Word
    # TODO[S2-DB]: 同时写入 Supabase jobs 表（status="parsed"）
    try:
        doc_model = parse_document(docx_path)
        json_content = doc_model.model_dump_json(indent=2)
        json_path = UPLOAD_DIR / f"{job_id}.json"
        json_path.write_text(json_content, encoding="utf-8")
        parse_summary = (
            f"解析完成：{doc_model.metadata.heading_count} 个标题，"
            f"{doc_model.metadata.paragraph_count} 段正文，"
            f"{doc_model.metadata.reference_count} 条参考文献"
        )
    except Exception as e:
        # 解析失败不影响上传结果（文件已保存），记录错误
        parse_summary = f"文件已保存，解析异常（{type(e).__name__}）"

    size_kb = len(content) / 1024
    return UploadResponse(
        job_id=job_id,
        status="pending",
        message=f"上传成功：{file.filename}（{size_kb:.0f} KB）｜{parse_summary}",
    )
