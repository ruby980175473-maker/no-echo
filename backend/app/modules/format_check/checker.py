# ============================================================
# NO ECHO · 格式规范检查模块
# 职责：将段落格式属性与规范对比，输出格式问题列表
# 技术：规则引擎（rules.py 定义规范）
# 参考：docs/TDD/NO_ECHO_TDD_V1.0.md § 5.2
# ============================================================

from __future__ import annotations
from app.modules.parser.docx_parser import ParseResult
from app.models.schemas import FormatIssue
from app.modules.format_check.rules import DEFAULT_FORMAT_RULES


def run_format_check(
    parse_result: ParseResult,
    template_rules: dict | None = None,
) -> list[FormatIssue]:
    """
    对解析后的段落列表执行格式规范检查。

    Args:
        parse_result: DOCX 解析结果
        template_rules: 用户上传的模板提取出的规范（优先于内置规范）
                        若为 None，使用 DEFAULT_FORMAT_RULES

    Returns:
        list[FormatIssue]: 所有发现的格式问题，无问题时返回空列表
    """
    # TODO: 实现
    # rules = template_rules or DEFAULT_FORMAT_RULES
    # 检查项：标题字体字号、正文字体字号、行距、首行缩进、参考文献格式 ...
    raise NotImplementedError
