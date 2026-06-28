# ============================================================
# NO ECHO · Specification Parser 主入口
# Sprint 3A：仅支持 Word 模板模式
# Sprint 4+：新增 Word 规范说明、PDF 规范
# ============================================================

from __future__ import annotations
from pathlib import Path
from app.modules.spec_parser.models import RuleSet
from app.modules.spec_parser.word_template_extractor import extract_from_word_template


class UnsupportedSourceType(Exception):
    """不支持的规范文件类型"""
    pass


SUPPORTED_EXTENSIONS = {
    ".docx": "word_template",
    # ".pdf": "pdf_spec",    # Sprint 5
}


def parse_spec(file_path: str | Path) -> RuleSet:
    """
    解析学校规范文件，生成标准化 Rule Set。

    当前支持（Sprint 3A）：
    - Word 模板 (.docx) → 直接读取样式属性

    计划支持：
    - Word 规范说明 (.docx) → 正则 + NLP 解析（Sprint 4）
    - PDF 规范 (.pdf)        → pdfplumber + 解析（Sprint 5）

    Args:
        file_path: 规范文件路径

    Returns:
        RuleSet: 标准化规则集

    Raises:
        UnsupportedSourceType: 文件格式不支持
        FileNotFoundError: 文件不存在
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    ext = file_path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedSourceType(
            f"不支持的格式「{ext}」，Sprint 3A 仅支持 .docx 格式模板"
        )

    return extract_from_word_template(file_path)


def count_rule_fields(rule_set: RuleSet) -> int:
    """统计 Rule Set 中非 None 的 RuleField 数量"""
    count = 0

    def _count(obj):
        nonlocal count
        if isinstance(obj, dict):
            if {"value", "source", "confidence"}.issubset(obj.keys()):
                count += 1
            else:
                for v in obj.values():
                    _count(v)
        elif isinstance(obj, list):
            for item in obj:
                _count(item)

    _count(rule_set.model_dump())
    return count
