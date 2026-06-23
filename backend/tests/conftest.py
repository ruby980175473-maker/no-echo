# ============================================================
# NO ECHO · pytest 测试全局配置
# ============================================================

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client():
    """同步 TestClient，用于集成测试"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_docx_path(tmp_path) -> str:
    """
    生成最简测试用 DOCX 文件路径。
    TODO: 用 python-docx 创建包含各类风险的标准测试文件
    """
    # TODO: 创建测试 DOCX
    return str(tmp_path / "test_thesis.docx")
