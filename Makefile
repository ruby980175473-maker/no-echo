# ============================================================
# NO ECHO · Makefile
# 用法：make <command>
# ============================================================

.PHONY: help dev build test lint migrate clean logs

# 默认显示帮助
help:
	@echo ""
	@echo "  NO ECHO · 可用命令"
	@echo "  ─────────────────────────────────────────────"
	@echo "  make dev         启动开发环境（Docker Compose）"
	@echo "  make dev-local   不使用 Docker，分别启动前后端"
	@echo "  make build       构建生产 Docker 镜像"
	@echo "  make test        运行所有测试（前端 + 后端 + e2e）"
	@echo "  make test-fe     仅运行前端测试"
	@echo "  make test-be     仅运行后端测试"
	@echo "  make test-e2e    仅运行端到端测试"
	@echo "  make lint        运行所有 lint 检查"
	@echo "  make lint-fe     仅 ESLint + TypeScript 检查"
	@echo "  make lint-be     仅 ruff + mypy 检查"
	@echo "  make migrate     执行数据库迁移"
	@echo "  make logs        查看所有服务日志"
	@echo "  make clean       清理构建产物和缓存"
	@echo "  make setup       初始化开发环境（首次使用）"
	@echo "  ─────────────────────────────────────────────"
	@echo ""

# ── 开发 ─────────────────────────────────────────────────────
dev:
	docker compose -f docker-compose.dev.yml up --build

build:
	docker compose build

logs:
	docker compose -f docker-compose.dev.yml logs -f

# ── 本地开发（不用 Docker）────────────────────────────────────
dev-local:
	@echo "→ 启动后端..."
	cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000 &
	@echo "→ 启动前端..."
	cd frontend && npm run dev

# ── 测试 ─────────────────────────────────────────────────────
test: test-be test-fe test-e2e

test-be:
	cd backend && source venv/bin/activate && pytest tests/ -v --cov=app --cov-report=term-missing

test-fe:
	cd frontend && npm run test

test-e2e:
	cd tests/e2e && npx playwright test

# ── Lint ─────────────────────────────────────────────────────
lint: lint-be lint-fe

lint-be:
	cd backend && source venv/bin/activate && ruff check app/ && mypy app/

lint-fe:
	cd frontend && npm run lint && npm run typecheck

# ── 数据库 ───────────────────────────────────────────────────
migrate:
	bash scripts/migrate.sh

# ── 清理 ─────────────────────────────────────────────────────
clean:
	bash scripts/clean.sh

# ── 初始化（首次使用）────────────────────────────────────────
setup:
	bash scripts/setup.sh
