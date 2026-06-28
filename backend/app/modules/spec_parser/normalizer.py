# ============================================================
# NO ECHO · Normalizer 层
# Sprint 3A 核心设计
#
# 职责：将任意来源的格式描述值转换为统一的技术标准值。
# Compare Engine 永远比较标准值，不处理自然语言。
#
# 输入示例 → 输出示例：
#   "小四"        → 12.0  (pt)
#   "三号"        → 16.0  (pt)
#   "两端对齐"    → "justify"
#   "居中"        → "center"
#   Pt(16)        → 16.0
#   914400 EMU    → 2.54  (cm)
# ============================================================

from __future__ import annotations
from typing import Optional, Tuple

# ── 中文字号名 → 磅值映射 ──────────────────────────────────────
CN_SIZE_TO_PT: dict[str, float] = {
    "初号": 42.0, "小初": 36.0,
    "一号": 26.0, "小一": 24.0,
    "二号": 22.0, "小二": 18.0,
    "三号": 16.0, "小三": 15.0,
    "四号": 14.0, "小四": 12.0,
    "五号": 10.5, "小五":  9.0,
    "六号":  7.5, "小六":  6.5,
    "七号":  5.5, "八号":  5.0,
}

# ── 中文对齐描述 → 标准值映射 ──────────────────────────────────
CN_ALIGN_TO_STD: dict[str, str] = {
    "居中": "center",
    "左对齐": "left",
    "右对齐": "right",
    "两端对齐": "justify",
    "分散对齐": "justify",
    "center": "center",
    "left": "left",
    "right": "right",
    "justify": "justify",
}


def normalize_pt(value) -> Optional[float]:
    """
    将 python-docx 的 Pt 对象或数值统一为 float 磅值。
    支持：Pt 对象、数值、None
    """
    if value is None:
        return None
    if hasattr(value, "pt"):          # Pt 对象
        v = value.pt
        return round(float(v), 2) if v is not None else None
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return None


def normalize_cm(value) -> Optional[float]:
    """
    将 python-docx 的 Emu 对象或数值统一为 float 厘米值。
    1 inch = 914400 EMU = 2.54 cm
    """
    if value is None:
        return None
    if hasattr(value, "cm"):          # Emu 对象（有 .cm 属性）
        v = value.cm
        return round(float(v), 2) if v is not None else None
    if hasattr(value, "pt"):          # Pt 对象 → 先转 pt → 再转 cm (1pt = 1/72 inch)
        pt_val = value.pt
        if pt_val is None:
            return None
        return round(float(pt_val) / 72 * 2.54, 2)
    try:
        # 假定已经是 cm
        return round(float(value), 2)
    except (TypeError, ValueError):
        return None


def normalize_align(value) -> Optional[str]:
    """
    将 python-docx 的 WD_ALIGN_PARAGRAPH 枚举转为标准字符串。
    返回："left" / "center" / "right" / "justify"
    """
    if value is None:
        return None
    # python-docx enum 有 .name 属性
    if hasattr(value, "name"):
        name = value.name.lower()
        return {"left": "left", "center": "center", "right": "right",
                "justify": "justify", "distribute": "justify"}.get(name, "left")
    # 已经是字符串
    if isinstance(value, str):
        return CN_ALIGN_TO_STD.get(value, value.lower())
    return None


def normalize_line_spacing(para_format) -> Tuple[Optional[str], Optional[float]]:
    """
    将 python-docx 段落格式的行距属性标准化。

    返回：(rule, value)
    - rule  : "fixed" | "multiple" | "at_least" | None
    - value : 磅值（fixed/at_least 时）或倍数（multiple 时）
    """
    try:
        from docx.enum.text import WD_LINE_SPACING
        ls  = para_format.line_spacing
        lsr = para_format.line_spacing_rule

        if ls is None:
            return None, None

        if lsr == WD_LINE_SPACING.EXACTLY:
            return "fixed", normalize_pt(ls)
        elif lsr == WD_LINE_SPACING.AT_LEAST:
            return "at_least", normalize_pt(ls)
        else:
            # MULTIPLE 或 None：ls 是一个无单位的倍数值
            try:
                return "multiple", round(float(ls), 2)
            except (TypeError, ValueError):
                return "multiple", None
    except Exception:
        return None, None


def normalize_font_size_name(size_name: str) -> Optional[float]:
    """
    将中文字号名称转换为磅值。
    "小四" → 12.0，"三号" → 16.0，未知返回 None
    """
    return CN_SIZE_TO_PT.get(size_name.strip())


def normalize_paper_size(width_cm: float, height_cm: float) -> str:
    """
    根据页面宽高（厘米）推断纸张规格名称。
    允许 ±0.5cm 的误差。
    """
    sizes = [
        ("A4",     21.0,  29.7),
        ("A3",     29.7,  42.0),
        ("B5",     17.6,  25.0),
        ("Letter", 21.6,  27.9),
    ]
    for name, w, h in sizes:
        if abs(width_cm - w) < 0.5 and abs(height_cm - h) < 0.5:
            return name
    return f"custom_{width_cm:.1f}x{height_cm:.1f}cm"


def normalize_first_line_indent_to_chars(
    indent_value,
    font_size_pt: Optional[float],
) -> Optional[float]:
    """
    将首行缩进的原始值（Pt/Emu 对象）转换为字符数。
    1字符 ≈ 1个字体点数宽度（近似，适用中文等宽字体）。
    """
    if indent_value is None or font_size_pt is None or font_size_pt == 0:
        return None
    pt_val = normalize_pt(indent_value)
    if pt_val is None:
        return None
    chars = pt_val / font_size_pt
    return round(chars, 1)


def normalize_align_from_str(raw: str) -> Optional[str]:
    """
    将自然语言对齐描述转为标准值（供 Word 规范文档解析使用，Sprint 4+）。
    "两端对齐" → "justify"，"居中" → "center"
    """
    return CN_ALIGN_TO_STD.get(raw.strip())
