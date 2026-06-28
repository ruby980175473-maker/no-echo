# ============================================================
# NO ECHO · Document Model（文档统一数据模型）
# Sprint 2 核心产物
#
# 设计原则：
# - 所有检测模块（格式、重复、AIGC、引用）只读此模型
# - 不允许重新解析 Word 文件
# - 每个字段都有明确语义，None / 空列表代表"未找到"
# ============================================================

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class HeadingItem(BaseModel):
    """文档中的标题条目"""
    index: int                      # 在 doc.paragraphs 中的位置
    level: int                      # 标题层级：1 / 2 / 3
    text: str                       # 标题文字
    numbering: Optional[str] = None # 编号部分，如 "1.1"；无编号则为 None


class ParagraphItem(BaseModel):
    """正文段落（含摘要段落，不含标题）"""
    index: int          # 在 doc.paragraphs 中的位置
    text: str
    style_name: str     # Word 段落样式名，如 "Normal"
    char_count: int     # 文字字符数（含标点，不含空格）


class ImageItem(BaseModel):
    """图片信息"""
    index: int                      # 文档中第几张图（从 1 起）
    caption: Optional[str] = None   # 图题文字（如"图1-1 研究框架"）
    paragraph_index: int            # 图片所在段落的 index


class TableItem(BaseModel):
    """表格信息"""
    index: int                      # 文档中第几张表（从 1 起）
    caption: Optional[str] = None   # 表题（Sprint 2 暂留 None）
    rows: int
    cols: int
    paragraph_index: int            # 表格位置（-1 表示暂未精确定位）


class DocumentMetadata(BaseModel):
    """文档元信息"""
    file_name: str
    file_size_bytes: int
    word_count: int         # 词数（CJK 字符各计 1 词，英文按空格分词）
    char_count: int         # 字符数（不含空白）
    paragraph_count: int    # 正文段落数（不含标题）
    heading_count: int
    image_count: int
    table_count: int
    reference_count: int
    has_abstract_cn: bool
    has_abstract_en: bool
    has_keywords_cn: bool
    has_keywords_en: bool


class DocumentModel(BaseModel):
    """
    NO ECHO 统一文档模型（Document Model）

    Word → DocxParser → DocumentModel（JSON）
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    FormatChecker    SimilarityChecker       AigcChecker
    """
    title: Optional[str] = None
    abstract_cn: Optional[str] = None
    abstract_en: Optional[str] = None
    keywords_cn: list[str] = Field(default_factory=list)
    keywords_en: list[str] = Field(default_factory=list)
    headings: list[HeadingItem] = Field(default_factory=list)
    paragraphs: list[ParagraphItem] = Field(default_factory=list)
    images: list[ImageItem] = Field(default_factory=list)
    tables: list[TableItem] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    metadata: DocumentMetadata
