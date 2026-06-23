# ============================================================
# NO ECHO · 集成测试：完整上传检测流程
# 覆盖：上传 → 进度轮询 → 结果查询
# ============================================================

import pytest


class TestUploadFlow:
    def test_health_check(self, client):
        """验证健康检查接口正常"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_upload_invalid_format(self, client):
        """上传非 DOCX 文件应返回 415"""
        # TODO: 实现
        pass

    def test_upload_oversized_file(self, client):
        """上传超过限制大小的文件应返回 413"""
        # TODO: 实现
        pass

    def test_full_detection_flow(self, client, sample_docx_path):
        """完整流程：上传 → 等待完成 → 查询结果"""
        # TODO: 实现（需要 mock 第三方 API）
        pass
