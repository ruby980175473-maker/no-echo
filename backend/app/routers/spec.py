# ============================================================
# NO ECHO · 规范文件上传路由
# POST /api/spec/upload  → 上传规范文件 → 解析 → 返回 Rule Set
# GET  /api/spec/{id}/ruleset → 获取 Rule Set JSON
# ============================================================

import json
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.modules.spec_parser.spec_parser import (
    UnsupportedSourceType,
    count_rule_fields,
    parse_spec,
)
from app.utils.file_validator import validate_docx

router = APIRouter()
UPLOAD_DIR = Path("uploads")


@router.post(
    "/spec/upload",
    status_code=202,
    summary="上传学校规范文件（Sprint 3A：仅支持 Word 模板）",
)
async def upload_spec(
    file: UploadFile = File(..., description="学校格式模板 .docx 文件"),
):
    """
    接收学校格式规范文件，解析为标准化 Rule Set 并存储。

    Sprint 3A：仅支持 Word 模板（.docx）。
    Sprint 4+：将支持 Word 规范说明文档和 PDF 规范。
    """
    await validate_docx(file)

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="文件内容为空")

    # 保存规范文件
    spec_id  = str(uuid.uuid4())
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    spec_path = UPLOAD_DIR / f"spec_{spec_id}.docx"
    spec_path.write_bytes(content)

    # 解析为 Rule Set
    try:
        rule_set = parse_spec(spec_path)
    except UnsupportedSourceType as e:
        spec_path.unlink(missing_ok=True)
        raise HTTPException(status_code=415, detail=str(e))
    except Exception as e:
        spec_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail=f"规范解析失败（{type(e).__name__}）：{e}",
        )

    # 保存 Rule Set JSON
    json_path = UPLOAD_DIR / f"spec_{spec_id}.json"
    json_path.write_text(rule_set.model_dump_json(indent=2), encoding="utf-8")

    rule_count = count_rule_fields(rule_set)

    return {
        "spec_id":     spec_id,
        "source_type": rule_set.meta.source_type,
        "rules_found": rule_count,
        "message":     f"规范解析完成，识别到 {rule_count} 条格式规则",
        "rule_set":    rule_set.model_dump(),
    }


@router.get(
    "/spec/{spec_id}/ruleset",
    summary="获取已解析的 Rule Set JSON",
)
async def get_ruleset(spec_id: str):
    json_path = UPLOAD_DIR / f"spec_{spec_id}.json"
    if not json_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"spec_id「{spec_id}」不存在或已过期",
        )
    return json.loads(json_path.read_text(encoding="utf-8"))
