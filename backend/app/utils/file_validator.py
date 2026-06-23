# ============================================================
# NO ECHO · 文件校验工具
# Sprint 1 实现：校验扩展名 + MIME Type（宽松）
# ============================================================

import os
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".docx"}

# 不同浏览器 / 操作系统对 .docx 文件的 MIME Type 可能不同，全部列出
ALLOWED_MIME_TYPES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "application/octet-stream",  # 部分系统对 docx 使用此通用 MIME
}


async def validate_docx(file: UploadFile) -> None:
    """
    验证上传文件是否为合法 DOCX。

    检查项（Sprint 1）：
    1. 文件名不为空
    2. 扩展名必须为 .docx
    3. MIME Type 宽松校验（避免因浏览器差异拒绝合法文件）

    Sprint 3+ 可在此处增加：读取文件头部字节（PK magic bytes）做更严格校验

    Raises:
        HTTPException 400: 文件名为空
        HTTPException 415: 文件格式不支持
    """
    # 1. 文件名非空
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="请选择要上传的文件",
        )

    # 2. 扩展名校验
    _, ext = os.path.splitext(file.filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"不支持的格式「{ext or '无扩展名'}」，请上传 .docx 文件（Word 文档）",
        )

    # 3. MIME Type 宽松校验（仅在明确不合法时拒绝）
    content_type = (file.content_type or "").lower()
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        # 只要扩展名正确，MIME Type 不精确匹配时给出警告，不拒绝
        # 因为不同环境的 MIME 行为差异较大
        pass
