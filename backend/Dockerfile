# ============================================================
# NO ECHO Backend · 多阶段 Dockerfile
# ============================================================

# ── Stage 1: 依赖安装（带编译环境）─────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: 开发环境（含 dev 依赖 + 源码挂载支持）────────────
FROM python:3.11-slim AS development
WORKDIR /app
COPY --from=builder /install /usr/local
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
EXPOSE 8000
# 源码通过 docker-compose volume 挂载，不需要 COPY

# ── Stage 3: 生产环境（最小镜像，非 root 用户）─────────────────
FROM python:3.11-slim AS production
WORKDIR /app
# 创建非 root 用户
RUN addgroup --system --gid 1001 appgroup \
    && adduser  --system --uid 1001 --ingroup appgroup appuser
COPY --from=builder /install /usr/local
COPY --chown=appuser:appgroup . .
USER appuser
EXPOSE 8000
# 生产环境不启用 --reload，通过多 worker 提升并发
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
