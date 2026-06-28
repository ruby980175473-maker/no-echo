# ============================================================
# NO ECHO · Word 模板提取器（Sprint 3A）
# 职责：从 .docx 格式模板中直接读取样式属性，生成 Rule Set。
# 模板读取的置信度最高（0.95），因为直接来自 Word 样式定义。
#
# Sprint 4 将新增 word_spec_extractor（自然语言规范解析）。
# ============================================================

from __future__ import annotations
from pathlib import Path
from typing import Optional

from docx import Document
from docx.oxml.ns import qn

from app.modules.spec_parser.models import (
    RuleField, RuleSet, RuleSetMeta,
    PageLayoutRule, HeadingRule, HeadingsRule, BodyRule,
)
from app.modules.spec_parser.normalizer import (
    normalize_pt, normalize_cm, normalize_align,
    normalize_line_spacing, normalize_paper_size,
    normalize_first_line_indent_to_chars,
)

# 模板直读的置信度（直接从 Word 样式属性读取，高确定性）
_TEMPLATE_CONFIDENCE = 0.95

# 各标题层级的可能样式名（中英文 Word 安装兼容）
_HEADING_STYLE_NAMES: dict[int, list[str]] = {
    1: ["Heading 1", "标题 1", "标题1", "heading 1", "一级标题"],
    2: ["Heading 2", "标题 2", "标题2", "heading 2", "二级标题"],
    3: ["Heading 3", "标题 3", "标题3", "heading 3", "三级标题"],
    4: ["Heading 4", "标题 4", "标题4", "heading 4"],
}

# 正文可能的样式名
_BODY_STYLE_NAMES = ["Normal", "正文", "Body Text", "default", "Default"]


# ── 内部工具函数 ───────────────────────────────────────────────

def _rf(value, source: str) -> Optional[RuleField]:
    """若 value 非 None，创建 RuleField；否则返回 None"""
    if value is None:
        return None
    return RuleField(value=value, source=source, confidence=_TEMPLATE_CONFIDENCE)


def _get_style(doc, names: list[str]):
    """按备选名列表查找样式，返回第一个找到的，否则返回 None"""
    for name in names:
        try:
            return doc.styles[name]
        except KeyError:
            continue
    return None


def _get_east_asia_font(style) -> Optional[str]:
    """
    从样式 XML 中提取东亚字体名（中文字体存储在 w:rFonts w:eastAsia 属性中）。
    python-docx 的 style.font.name 只返回拉丁字体，中文字体需要从 XML 读取。
    """
    try:
        rPr = style.element.find(qn("w:rPr"))
        if rPr is None:
            return None
        rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None:
            return None
        return rFonts.get(qn("w:eastAsia")) or None
    except Exception:
        return None


def _get_font_name(style) -> Optional[str]:
    """
    获取样式的字体名称：优先东亚字体（中文），回退拉丁字体。
    """
    ea = _get_east_asia_font(style)
    if ea:
        return ea
    return style.font.name or None


# ── 各格式分类的提取函数 ───────────────────────────────────────

def _extract_page_layout(doc, source_file: str) -> PageLayoutRule:
    """从文档节（Section）提取页面布局规则"""
    section = doc.sections[0]
    src = f"{source_file} · sections[0]"

    width_cm  = normalize_cm(section.page_width)
    height_cm = normalize_cm(section.page_height)
    paper     = normalize_paper_size(width_cm, height_cm) if width_cm and height_cm else None

    return PageLayoutRule(
        paper_size=_rf(paper, src + ".page_size"),
        margin_top_cm=_rf(normalize_cm(section.top_margin),       src + ".top_margin"),
        margin_bottom_cm=_rf(normalize_cm(section.bottom_margin),  src + ".bottom_margin"),
        margin_left_cm=_rf(normalize_cm(section.left_margin),      src + ".left_margin"),
        margin_right_cm=_rf(normalize_cm(section.right_margin),    src + ".right_margin"),
        header_distance_cm=_rf(normalize_cm(section.header_distance), src + ".header_distance"),
        footer_distance_cm=_rf(normalize_cm(section.footer_distance), src + ".footer_distance"),
    )


def _extract_heading_rule(doc, level: int, source_file: str) -> Optional[HeadingRule]:
    """提取指定层级标题的格式规则"""
    style = _get_style(doc, _HEADING_STYLE_NAMES.get(level, []))
    if style is None:
        return None

    src = f"{source_file} · style[{style.name}]"

    font_name  = _get_font_name(style)
    font_size  = normalize_pt(style.font.size)
    align      = normalize_align(style.paragraph_format.alignment)
    space_bef  = normalize_pt(style.paragraph_format.space_before)
    space_aft  = normalize_pt(style.paragraph_format.space_after)

    return HeadingRule(
        font_name=_rf(font_name,  src + ".font.name"),
        font_size_pt=_rf(font_size, src + ".font.size"),
        bold=_rf(style.font.bold,  src + ".font.bold"),
        align=_rf(align,           src + ".paragraph_format.alignment"),
        space_before_pt=_rf(space_bef, src + ".paragraph_format.space_before"),
        space_after_pt=_rf(space_aft,  src + ".paragraph_format.space_after"),
    )


def _extract_body_rule(doc, source_file: str) -> Optional[BodyRule]:
    """提取正文（Normal 样式）的格式规则"""
    style = _get_style(doc, _BODY_STYLE_NAMES)
    if style is None:
        return None

    src = f"{source_file} · style[Normal]"

    font_name  = _get_font_name(style)
    font_size  = normalize_pt(style.font.size)
    align      = normalize_align(style.paragraph_format.alignment)
    ls_rule, ls_val = normalize_line_spacing(style.paragraph_format)
    indent_chars = normalize_first_line_indent_to_chars(
        style.paragraph_format.first_line_indent, font_size
    )

    return BodyRule(
        font_name=_rf(font_name,  src + ".font.name"),
        font_size_pt=_rf(font_size, src + ".font.size"),
        line_spacing_rule=_rf(ls_rule,  src + ".paragraph_format.line_spacing_rule"),
        line_spacing_pt=_rf(ls_val,     src + ".paragraph_format.line_spacing"),
        first_line_indent_chars=_rf(indent_chars, src + ".paragraph_format.first_line_indent"),
        align=_rf(align, src + ".paragraph_format.alignment"),
    )


# ── 主入口 ─────────────────────────────────────────────────────

def extract_from_word_template(file_path: Path) -> RuleSet:
    """
    从 Word 模板 (.docx) 提取格式规则，生成 Rule Set。

    Sprint 3A 提取范围：
    ✅ 页面布局（纸张、页边距）
    ✅ 标题格式（H1/H2/H3）
    ✅ 正文格式（字体、行距、缩进）
    ⏳ 封面、目录、参考文献规则（Sprint 4）
    """
    doc         = Document(str(file_path))
    source_file = file_path.name

    return RuleSet(
        meta=RuleSetMeta(
            school_name=None,           # 无法从模板自动推断学校名称
            source_type="word_template",
            source_files=[source_file],
        ),
        page_layout=_extract_page_layout(doc, source_file),
        headings=HeadingsRule(
            heading1=_extract_heading_rule(doc, 1, source_file),
            heading2=_extract_heading_rule(doc, 2, source_file),
            heading3=_extract_heading_rule(doc, 3, source_file),
        ),
        body=_extract_body_rule(doc, source_file),
    )
