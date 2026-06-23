# ============================================================
# NO ECHO · 文件校验工具
# ============================================================

from fastapi import UploadFile, HTTPException
from app.config import settings

ALLOWED_MIME_TYPES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}
ALLOWED_EXTENSIONS = {".docx"}


async def validate_docx(file: UploadFile) -> None:
    """
    验证上传文件是否为合法 DOCX。
    检查项：MIME Type、文件扩展名、文件大小

    Raises:
        HTTPException 415: 不支持的文件格式
        HTTPException 413: 文件超过大小限制
    """
    # TODO: 实现校验逻辑
    raise NotImplementedError
