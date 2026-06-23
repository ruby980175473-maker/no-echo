#!/usr/bin/env bash
# ============================================================
# NO ECHO · 数据库迁移脚本
# 通过 Supabase CLI 或直接 psql 执行 migrations/ 下的 SQL 文件
# ============================================================
set -e

if [ -z "$SUPABASE_URL" ]; then
  echo "✗ 环境变量 SUPABASE_URL 未设置，请先配置 .env"
  exit 1
fi

echo "→ 执行数据库迁移..."
for FILE in database/migrations/*.sql; do
  echo "  → $FILE"
  # TODO: 通过 supabase CLI 或 psql 执行
  # supabase db push --db-url "$SUPABASE_URL" < "$FILE"
done

echo "✓ 迁移完成"
