# ============================================================
# NO ECHO · Rule Set 数据模型
# Sprint 3A 核心产物
#
# 设计原则：
# - 每条规则都是 RuleField（含 value / source / confidence）
# - value 永远是标准化技术值（float/str/bool），从不是自然语言
# - None 表示"规范未要求此项"，Compare Engine 自动跳过
# ============================================================

from __future__ import annotations
from typing import Optional, Union
from pydantic import BaseModel, Field


class RuleField(BaseModel):
    """
    单条规则字段的完整表示。

    value    : 标准化后的技术值，例如 12.0、"黑体"、"center"、True
    source   : 来源描述，例如 "template.docx · style[Heading 1].font.size"
    confidence: 解析置信度（0-1）。模板直读 ≈ 0.95，自然语言解析 ≈ 0.7，推断 ≈ 0.4
    """
    value: Union[str, float, int, bool, None]
    source: str
    confidence: float = Field(ge=0.0, le=1.0)


# ── 页面设置规则 ───────────────────────────────────────────────
class PageLayoutRule(BaseModel):
    paper_size: Optional[RuleField] = None           # "A4" / "A3" / "Letter"
    margin_top_cm: Optional[RuleField] = None
    margin_bottom_cm: Optional[RuleField] = None
    margin_left_cm: Optional[RuleField] = None
    margin_right_cm: Optional[RuleField] = None
    binding_gutter_cm: Optional[RuleField] = None
    header_distance_cm: Optional[RuleField] = None
    footer_distance_cm: Optional[RuleField] = None


# ── 标题规则 ───────────────────────────────────────────────────
class HeadingRule(BaseModel):
    font_name: Optional[RuleField] = None            # "黑体" / "Times New Roman"
    font_size_pt: Optional[RuleField] = None         # 16.0
    bold: Optional[RuleField] = None                 # True / False
    align: Optional[RuleField] = None                # "left" / "center" / "right" / "justify"
    space_before_pt: Optional[RuleField] = None
    space_after_pt: Optional[RuleField] = None


class HeadingsRule(BaseModel):
    heading1: Optional[HeadingRule] = None
    heading2: Optional[HeadingRule] = None
    heading3: Optional[HeadingRule] = None
    heading4: Optional[HeadingRule] = None


# ── 正文规则 ───────────────────────────────────────────────────
class BodyRule(BaseModel):
    font_name: Optional[RuleField] = None
    font_size_pt: Optional[RuleField] = None
    line_spacing_rule: Optional[RuleField] = None    # "fixed" / "multiple" / "at_least"
    line_spacing_pt: Optional[RuleField] = None      # 22.0（fixed模式时为磅值，multiple模式时为倍数）
    first_line_indent_chars: Optional[RuleField] = None  # 2.0（字符数）
    align: Optional[RuleField] = None


# ── 摘要规则 ───────────────────────────────────────────────────
class AbstractRule(BaseModel):
    cn_required: Optional[RuleField] = None          # True / False
    en_required: Optional[RuleField] = None
    keywords_cn_min: Optional[RuleField] = None      # 3
    keywords_cn_max: Optional[RuleField] = None      # 8
    keywords_en_min: Optional[RuleField] = None
    keywords_en_max: Optional[RuleField] = None


# ── 参考文献规则 ───────────────────────────────────────────────
class ReferencesRule(BaseModel):
    style_standard: Optional[RuleField] = None       # "GB/T 7714-2015"
    numbering_style: Optional[RuleField] = None      # "sequential"
    citation_format: Optional[RuleField] = None      # "brackets" / "superscript"


# ── Rule Set 元信息 ────────────────────────────────────────────
class RuleSetMeta(BaseModel):
    version: str = "1.0"
    school_name: Optional[str] = None
    source_type: str                                 # "word_template" / "word_spec" / "pdf_spec"
    source_files: list[str] = Field(default_factory=list)
    extractor_version: str = "sprint3a"


# ── Rule Set 根模型 ────────────────────────────────────────────
class RuleSet(BaseModel):
    """
    NO ECHO 统一规则集（Rule Set）

    Specification Parser 的输出，Compare Engine 的输入之一。
    所有叶节点均为 RuleField，value 始终是标准化技术值。

    数据流：
    学校规范文件 → Specification Parser → RuleSet
                                               ↓
                              Document Model + RuleSet → Compare Engine → Violations
    """
    meta: RuleSetMeta
    page_layout: Optional[PageLayoutRule] = None
    headings: Optional[HeadingsRule] = None
    body: Optional[BodyRule] = None
    abstract: Optional[AbstractRule] = None
    references: Optional[ReferencesRule] = None
