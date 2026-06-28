# ============================================================
# NO ECHO · Sprint 2 单元测试：DOCX 解析器
# ============================================================

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.modules.parser.docx_parser import (
    parse_document,
    parse_title,
    parse_headings,
    parse_abstract_cn,
    parse_abstract_en,
    parse_keywords_cn,
    parse_keywords_en,
    parse_references,
    parse_paragraphs,
)
from app.modules.parser.models import DocumentModel

FIXTURES = Path(__file__).parent.parent / "fixtures"


# ─────────────────────────────────────────────────────────────
# Fixture 1: 完整正常论文
# ─────────────────────────────────────────────────────────────

class TestNormalThesis:
    """完整论文：所有字段均应被正确解析"""

    @pytest.fixture(scope="class")
    def doc(self):
        return parse_document(FIXTURES / "normal_thesis.docx")

    def test_returns_document_model(self, doc):
        assert isinstance(doc, DocumentModel)

    def test_title_extracted(self, doc):
        assert doc.title is not None
        assert "AIGC" in doc.title or "论文" in doc.title or "大语言" in doc.title

    def test_abstract_cn_extracted(self, doc):
        assert doc.abstract_cn is not None
        assert len(doc.abstract_cn) > 20
        assert "AIGC" in doc.abstract_cn or "检测" in doc.abstract_cn

    def test_abstract_en_extracted(self, doc):
        assert doc.abstract_en is not None
        assert len(doc.abstract_en) > 20

    def test_keywords_cn_extracted(self, doc):
        assert len(doc.keywords_cn) >= 3
        assert any("AIGC" in k or "模型" in k or "检测" in k for k in doc.keywords_cn)

    def test_keywords_en_extracted(self, doc):
        assert len(doc.keywords_en) >= 2
        assert any("model" in k.lower() or "AIGC" in k or "detection" in k.lower()
                   for k in doc.keywords_en)

    def test_headings_extracted(self, doc):
        assert len(doc.headings) >= 5
        levels = [h.level for h in doc.headings]
        assert 1 in levels
        assert 2 in levels
        assert 3 in levels

    def test_headings_level1_count(self, doc):
        h1 = [h for h in doc.headings if h.level == 1]
        assert len(h1) >= 5  # 绪论、相关工作、方法、实验、结论、参考文献

    def test_references_extracted(self, doc):
        assert len(doc.references) == 3
        assert doc.references[0].startswith("[1]")
        assert doc.references[1].startswith("[2]")

    def test_paragraphs_not_empty(self, doc):
        assert len(doc.paragraphs) >= 5

    def test_metadata_complete(self, doc):
        m = doc.metadata
        assert m.file_size_bytes > 0
        assert m.word_count > 100
        assert m.heading_count >= 5
        assert m.reference_count == 3
        assert m.has_abstract_cn is True
        assert m.has_abstract_en is True
        assert m.has_keywords_cn is True
        assert m.has_keywords_en is True

    def test_output_is_valid_json(self, doc):
        """DocumentModel 必须能序列化为 JSON"""
        json_str = doc.model_dump_json()
        assert len(json_str) > 100
        import json
        data = json.loads(json_str)
        assert "title" in data
        assert "metadata" in data


# ─────────────────────────────────────────────────────────────
# Fixture 2: 无摘要论文
# ─────────────────────────────────────────────────────────────

class TestNoAbstract:
    """无摘要：abstract 字段应为 None，其他字段正常"""

    @pytest.fixture(scope="class")
    def doc(self):
        return parse_document(FIXTURES / "no_abstract.docx")

    def test_abstract_cn_is_none(self, doc):
        assert doc.abstract_cn is None

    def test_abstract_en_is_none(self, doc):
        assert doc.abstract_en is None

    def test_title_still_extracted(self, doc):
        assert doc.title is not None

    def test_headings_still_extracted(self, doc):
        assert len(doc.headings) >= 2

    def test_references_still_extracted(self, doc):
        assert len(doc.references) >= 1

    def test_metadata_has_abstract_false(self, doc):
        assert doc.metadata.has_abstract_cn is False
        assert doc.metadata.has_abstract_en is False

    def test_parser_does_not_crash(self, doc):
        """无摘要时解析器不应崩溃"""
        assert isinstance(doc, DocumentModel)


# ─────────────────────────────────────────────────────────────
# Fixture 3: 无参考文献
# ─────────────────────────────────────────────────────────────

class TestNoReferences:
    """无参考文献：references 应为空列表"""

    @pytest.fixture(scope="class")
    def doc(self):
        return parse_document(FIXTURES / "no_references.docx")

    def test_references_is_empty(self, doc):
        assert doc.references == []

    def test_reference_count_is_zero(self, doc):
        assert doc.metadata.reference_count == 0

    def test_abstract_cn_still_extracted(self, doc):
        assert doc.abstract_cn is not None

    def test_abstract_en_still_extracted(self, doc):
        assert doc.abstract_en is not None

    def test_keywords_cn_extracted(self, doc):
        assert len(doc.keywords_cn) >= 2

    def test_parser_does_not_crash(self, doc):
        assert isinstance(doc, DocumentModel)


# ─────────────────────────────────────────────────────────────
# Fixture 4: 无英文摘要
# ─────────────────────────────────────────────────────────────

class TestNoAbstractEn:
    """无英文摘要：abstract_en 为 None，abstract_cn 正常"""

    @pytest.fixture(scope="class")
    def doc(self):
        return parse_document(FIXTURES / "no_abstract_en.docx")

    def test_abstract_en_is_none(self, doc):
        assert doc.abstract_en is None

    def test_abstract_cn_extracted(self, doc):
        assert doc.abstract_cn is not None
        assert len(doc.abstract_cn) > 10

    def test_keywords_en_empty(self, doc):
        assert doc.keywords_en == []

    def test_keywords_cn_extracted(self, doc):
        assert len(doc.keywords_cn) >= 2

    def test_metadata_flags_correct(self, doc):
        assert doc.metadata.has_abstract_cn is True
        assert doc.metadata.has_abstract_en is False
        assert doc.metadata.has_keywords_en is False


# ─────────────────────────────────────────────────────────────
# Fixture 5: 标题层级异常
# ─────────────────────────────────────────────────────────────

class TestAbnormalHeadings:
    """标题层级异常：H3 直接出现在 H1 后，解析器不应崩溃"""

    @pytest.fixture(scope="class")
    def doc(self):
        return parse_document(FIXTURES / "abnormal_headings.docx")

    def test_parser_does_not_crash(self, doc):
        assert isinstance(doc, DocumentModel)

    def test_headings_all_captured(self, doc):
        """所有标题都应被捕获，无论层级是否连续"""
        assert len(doc.headings) >= 4

    def test_level3_headings_captured(self, doc):
        """H3 即使跳过 H2 也应被正确识别"""
        h3_list = [h for h in doc.headings if h.level == 3]
        assert len(h3_list) >= 1

    def test_level1_and_level2_coexist(self, doc):
        """H1 和 H2 都存在"""
        levels = {h.level for h in doc.headings}
        assert 1 in levels
        assert 2 in levels

    def test_abstract_extracted_despite_abnormal_structure(self, doc):
        """即使结构异常，摘要仍能正常提取"""
        assert doc.abstract_cn is not None

    def test_references_extracted(self, doc):
        assert len(doc.references) >= 1


# ─────────────────────────────────────────────────────────────
# 通用测试：DocumentModel JSON 结构一致性
# ─────────────────────────────────────────────────────────────

class TestDocumentModelStructure:
    """所有 fixture 的 DocumentModel 必须有一致的 JSON 结构"""

    @pytest.mark.parametrize("fixture_name", [
        "normal_thesis.docx",
        "no_abstract.docx",
        "no_references.docx",
        "no_abstract_en.docx",
        "abnormal_headings.docx",
    ])
    def test_all_fixtures_have_required_fields(self, fixture_name):
        import json
        doc = parse_document(FIXTURES / fixture_name)
        data = json.loads(doc.model_dump_json())

        required_fields = [
            "title", "abstract_cn", "abstract_en",
            "keywords_cn", "keywords_en",
            "headings", "paragraphs",
            "images", "tables", "references",
            "metadata",
        ]
        for field in required_fields:
            assert field in data, f"{fixture_name} 缺少字段: {field}"

    @pytest.mark.parametrize("fixture_name", [
        "normal_thesis.docx",
        "no_abstract.docx",
        "no_references.docx",
        "no_abstract_en.docx",
        "abnormal_headings.docx",
    ])
    def test_metadata_always_present(self, fixture_name):
        import json
        doc = parse_document(FIXTURES / fixture_name)
        data = json.loads(doc.model_dump_json())
        metadata_fields = [
            "file_name", "file_size_bytes", "word_count", "char_count",
            "paragraph_count", "heading_count", "reference_count",
            "has_abstract_cn", "has_abstract_en",
        ]
        for field in metadata_fields:
            assert field in data["metadata"], f"{fixture_name} metadata 缺少字段: {field}"
