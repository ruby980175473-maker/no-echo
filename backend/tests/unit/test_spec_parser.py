# ============================================================
# NO ECHO · Sprint 3A 单元测试：Specification Parser
# ============================================================

import sys
import json
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.modules.spec_parser.models import RuleSet, RuleField
from app.modules.spec_parser.spec_parser import parse_spec, UnsupportedSourceType
from app.modules.spec_parser.normalizer import (
    normalize_pt, normalize_cm, normalize_align,
    normalize_font_size_name, normalize_paper_size,
    normalize_line_spacing,
)

FIXTURES = Path(__file__).parent.parent / "fixtures"


# ─────────────────────────────────────────────────────────────
# Normalizer 单元测试
# ─────────────────────────────────────────────────────────────

class TestNormalizer:
    """Normalizer 层：各转换函数的正确性"""

    def test_normalize_pt_from_number(self):
        assert normalize_pt(16) == 16.0
        assert normalize_pt(12.5) == 12.5
        assert normalize_pt(None) is None

    def test_normalize_pt_from_pt_object(self):
        from docx.shared import Pt
        assert normalize_pt(Pt(16)) == 16.0
        assert normalize_pt(Pt(12)) == 12.0

    def test_normalize_cm_from_emu(self):
        from docx.shared import Cm
        result = normalize_cm(Cm(3.0))
        assert abs(result - 3.0) < 0.01

    def test_normalize_cm_from_number(self):
        assert normalize_cm(2.5) == 2.5
        assert normalize_cm(None) is None

    def test_normalize_align_enum(self):
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        assert normalize_align(WD_ALIGN_PARAGRAPH.CENTER)  == "center"
        assert normalize_align(WD_ALIGN_PARAGRAPH.JUSTIFY) == "justify"
        assert normalize_align(WD_ALIGN_PARAGRAPH.LEFT)    == "left"
        assert normalize_align(WD_ALIGN_PARAGRAPH.RIGHT)   == "right"

    def test_normalize_align_none(self):
        assert normalize_align(None) is None

    def test_normalize_font_size_name(self):
        assert normalize_font_size_name("小四")  == 12.0
        assert normalize_font_size_name("三号")  == 16.0
        assert normalize_font_size_name("小二")  == 18.0
        assert normalize_font_size_name("四号")  == 14.0
        assert normalize_font_size_name("未知")  is None

    def test_normalize_paper_size_a4(self):
        assert normalize_paper_size(21.0, 29.7) == "A4"

    def test_normalize_paper_size_tolerance(self):
        # A4 with slight floating point variance
        assert normalize_paper_size(21.01, 29.69) == "A4"

    def test_normalize_paper_size_custom(self):
        # 19x26 不属于任何标准纸张规格（A4=21x29.7, B5=17.6x25, Letter=21.6x27.9）
        result = normalize_paper_size(19.0, 26.0)
        assert "custom" in result


# ─────────────────────────────────────────────────────────────
# Word 模板提取测试（标准模板）
# ─────────────────────────────────────────────────────────────

class TestWordTemplateStandard:
    """标准模板：验证所有主要格式规则均被正确提取"""

    @pytest.fixture(scope="class")
    def rule_set(self):
        return parse_spec(FIXTURES / "word_template_standard.docx")

    def test_returns_rule_set(self, rule_set):
        assert isinstance(rule_set, RuleSet)

    def test_meta_source_type(self, rule_set):
        assert rule_set.meta.source_type == "word_template"

    def test_meta_source_files(self, rule_set):
        assert "word_template_standard.docx" in rule_set.meta.source_files

    # ── 页面布局 ───────────────────────────────────────────────
    def test_page_size_is_a4(self, rule_set):
        assert rule_set.page_layout is not None
        ps = rule_set.page_layout.paper_size
        assert ps is not None
        assert ps.value == "A4"

    def test_margin_top_correct(self, rule_set):
        mt = rule_set.page_layout.margin_top_cm
        assert mt is not None
        assert abs(float(mt.value) - 3.0) < 0.1

    def test_margin_left_correct(self, rule_set):
        ml = rule_set.page_layout.margin_left_cm
        assert ml is not None
        assert abs(float(ml.value) - 2.5) < 0.1

    # ── 标题格式 ───────────────────────────────────────────────
    def test_heading1_exists(self, rule_set):
        assert rule_set.headings is not None
        assert rule_set.headings.heading1 is not None

    def test_heading1_font_name_is_heiti(self, rule_set):
        h1 = rule_set.headings.heading1
        assert h1.font_name is not None
        assert h1.font_name.value == "黑体"

    def test_heading1_font_size_is_16pt(self, rule_set):
        h1 = rule_set.headings.heading1
        assert h1.font_size_pt is not None
        assert abs(float(h1.font_size_pt.value) - 16.0) < 0.1

    def test_heading1_is_bold(self, rule_set):
        h1 = rule_set.headings.heading1
        assert h1.bold is not None
        assert h1.bold.value is True

    def test_heading1_align_is_center(self, rule_set):
        h1 = rule_set.headings.heading1
        assert h1.align is not None
        assert h1.align.value == "center"

    def test_heading2_font_size_is_14pt(self, rule_set):
        h2 = rule_set.headings.heading2
        assert h2 is not None
        assert h2.font_size_pt is not None
        assert abs(float(h2.font_size_pt.value) - 14.0) < 0.1

    def test_heading2_align_is_left(self, rule_set):
        h2 = rule_set.headings.heading2
        assert h2.align is not None
        assert h2.align.value == "left"

    def test_heading3_exists(self, rule_set):
        assert rule_set.headings.heading3 is not None

    # ── 正文格式 ───────────────────────────────────────────────
    def test_body_exists(self, rule_set):
        assert rule_set.body is not None

    def test_body_font_name_is_songti(self, rule_set):
        assert rule_set.body.font_name is not None
        assert rule_set.body.font_name.value == "宋体"

    def test_body_font_size_is_12pt(self, rule_set):
        assert rule_set.body.font_size_pt is not None
        assert abs(float(rule_set.body.font_size_pt.value) - 12.0) < 0.1

    def test_body_align_is_justify(self, rule_set):
        assert rule_set.body.align is not None
        assert rule_set.body.align.value == "justify"

    def test_body_line_spacing_is_fixed(self, rule_set):
        assert rule_set.body.line_spacing_rule is not None
        assert rule_set.body.line_spacing_rule.value == "fixed"

    def test_body_line_spacing_is_22pt(self, rule_set):
        assert rule_set.body.line_spacing_pt is not None
        assert abs(float(rule_set.body.line_spacing_pt.value) - 22.0) < 0.5

    # ── RuleField 结构完整性 ───────────────────────────────────
    def test_every_rule_has_source(self, rule_set):
        data = rule_set.model_dump()
        def check(obj):
            if isinstance(obj, dict):
                if {"value", "source", "confidence"}.issubset(obj.keys()):
                    assert isinstance(obj["source"], str) and len(obj["source"]) > 0
                else:
                    for v in obj.values():
                        check(v)
        check(data)

    def test_every_rule_has_confidence(self, rule_set):
        data = rule_set.model_dump()
        def check(obj):
            if isinstance(obj, dict):
                if {"value", "source", "confidence"}.issubset(obj.keys()):
                    assert 0.0 <= obj["confidence"] <= 1.0
                else:
                    for v in obj.values():
                        check(v)
        check(data)

    def test_all_values_are_python_primitives(self, rule_set):
        """value 字段应该是 str/float/int/bool，不是 Pt 对象"""
        data = rule_set.model_dump()
        def check(obj):
            if isinstance(obj, dict):
                if {"value", "source", "confidence"}.issubset(obj.keys()):
                    v = obj["value"]
                    assert isinstance(v, (str, float, int, bool, type(None))), \
                        f"value 不是 Python 原生类型：{type(v)} = {v}"
                else:
                    for val in obj.values():
                        check(val)
        check(data)

    def test_json_serializable(self, rule_set):
        """Rule Set 必须可以序列化为 JSON"""
        json_str = rule_set.model_dump_json()
        assert len(json_str) > 100
        data = json.loads(json_str)
        assert "meta" in data
        assert "page_layout" in data
        assert "headings" in data

    def test_template_confidence_is_high(self, rule_set):
        """Word 模板读取的置信度应该在 0.9 以上"""
        data = rule_set.model_dump()
        def check(obj):
            if isinstance(obj, dict):
                if {"value", "source", "confidence"}.issubset(obj.keys()):
                    assert obj["confidence"] >= 0.9, \
                        f"置信度过低：{obj['confidence']} for {obj['source']}"
                else:
                    for v in obj.values():
                        check(v)
        check(data)


# ─────────────────────────────────────────────────────────────
# 极简模板（无自定义样式）鲁棒性测试
# ─────────────────────────────────────────────────────────────

class TestWordTemplateMinimal:
    """极简模板：没有自定义样式时，解析器不应崩溃"""

    @pytest.fixture(scope="class")
    def rule_set(self):
        return parse_spec(FIXTURES / "word_template_minimal.docx")

    def test_does_not_crash(self, rule_set):
        assert isinstance(rule_set, RuleSet)

    def test_page_layout_extracted(self, rule_set):
        """即使无自定义样式，页面布局仍然可以提取"""
        assert rule_set.page_layout is not None
        assert rule_set.page_layout.paper_size is not None

    def test_json_serializable(self, rule_set):
        json_str = rule_set.model_dump_json()
        data = json.loads(json_str)
        assert "meta" in data


# ─────────────────────────────────────────────────────────────
# 不支持的文件类型
# ─────────────────────────────────────────────────────────────

class TestUnsupportedTypes:

    def test_pdf_raises_error(self, tmp_path):
        fake_pdf = tmp_path / "spec.pdf"
        fake_pdf.write_bytes(b"%PDF-1.4 fake")
        with pytest.raises(UnsupportedSourceType):
            parse_spec(fake_pdf)

    def test_txt_raises_error(self, tmp_path):
        fake_txt = tmp_path / "spec.txt"
        fake_txt.write_text("some text")
        with pytest.raises(UnsupportedSourceType):
            parse_spec(fake_txt)

    def test_missing_file_raises_error(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            parse_spec(tmp_path / "nonexistent.docx")
