#!/usr/bin/env bash
# ============================================================
# NO ECHO · 清理构建产物和缓存
# ============================================================
set -e

echo "→ 清理前端构建产物..."
rm -rf frontend/.next frontend/out frontend/dist

echo "→ 清理 Python 缓存..."
find backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find backend -name "*.pyc" -delete 2>/dev/null || true
rm -rf backend/.pytest_cache backend/.mypy_cache backend/.ruff_cache

echo "→ 清理测试报告..."
rm -rf playwright-report test-results tests/e2e/results

echo "✓ 清理完成"
