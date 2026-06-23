# ============================================================
# NO ECHO · 格式规范内置规则
# 基于 GB/T 常见本科论文格式要求
# ============================================================

DEFAULT_FORMAT_RULES: dict = {
    "heading_1": {
        "font_name": ["黑体", "SimHei"],
        "font_size_pt": 16,
        "bold": True,
    },
    "heading_2": {
        "font_name": ["黑体", "SimHei"],
        "font_size_pt": 14,
        "bold": True,
    },
    "heading_3": {
        "font_name": ["黑体", "SimHei"],
        "font_size_pt": 12,
        "bold": True,
    },
    "body": {
        "font_name": ["宋体", "SimSun"],
        "font_size_pt": 12,
        "line_spacing_min": 1.4,
        "line_spacing_max": 1.6,
        "first_line_indent_cm": 0.74,  # 两字符缩进
    },
    "reference_pattern": r"^\[\d+\]\s.+",  # GB/T 7714 基础正则
}
