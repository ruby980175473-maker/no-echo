# ============================================================
# NO ECHO · DOCX 解析模块
# 职责：将 .docx 文件解析为结构化段落数组
# 技术：python-docx（格式属性提取）+ Mammoth（纯文本提取）
# 参考：docs/TDD/NO_ECHO_TDD_V1.0.md § 5.1
# ============================================================

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedParagraph:
    index:             int
    text:              str
    heading_level:     Optional[int]   = None
    style_name:        Optional[str]   = None
    font_name:         Optional[str]   = None
    font_size_pt:      Optional[float] = None
    line_spacing:      Optional[float] = None
    first_line_indent: Optional[float] = None


@dataclass
class ParseResult:
    paragraphs: list[ParsedParagraph]
    raw_text:   str    # Mammoth 提取的纯文本，供 NLP 模块使用


def parse_docx(file_path: str) -> ParseResult:
    """
    解析 DOCX 文件，返回结构化段落列表。

    Args:
        file_path: 本地临时文件路径

    Returns:
        ParseResult

    Raises:
        ValueError: 文件不是合法 DOCX
        RuntimeError: 解析过程中发生致命错误
    """
    # TODO: 实现
    # 1. docx.Document(file_path) 打开文件
    # 2. 遍历 doc.paragraphs，提取样式属性
    # 3. 调用 _get_heading_level() 判断标题层级
    # 4. 调用 _normalize_line_spacing() 归一化行距
    # 5. 用 mammoth 提取纯文本
    # 注意：空段落跳过；try/except 处理格式异常
    raise NotImplementedError


def _get_heading_level(style_name: str) -> Optional[int]:
    """从 Word 段落样式名提取标题层级（1/2/3），正文返回 None"""
    # TODO: 实现样式名映射（中英文兼容："Heading 1" / "标题 1"）
    raise NotImplementedError


def _normalize_line_spacing(value, rule) -> Optional[float]:
    """将 python-docx 的行距原始值统一归一化为倍数（如 1.5、2.0）"""
    # TODO: 处理 WD_LINE_SPACING.MULTIPLE / EXACTLY / AT_LEAST 三种情况
    raise NotImplementedError
