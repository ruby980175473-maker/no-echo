#!/usr/bin/env bash
# ============================================================
# NO ECHO · 开发环境初始化脚本（首次使用）
# ============================================================
set -e

echo "======================================================"
echo "  NO ECHO · 开发环境初始化"
echo "======================================================"

# 检查依赖工具
check_command() {
  if ! command -v "$1" &>/dev/null; then
    echo "✗ 缺少依赖：$1 未安装"
    exit 1
  fi
}
check_command node
check_command python3
check_command docker

# 环境变量配置
if [ ! -f .env ]; then
  cp .env.example .env
  echo "→ 已创建 .env，请填写 API Keys 后重新运行"
  exit 0
fi

# 前端依赖
echo "→ 安装前端依赖..."
cd frontend
cp -n .env.local.example .env.local 2>/dev/null || true
npm install
cd ..

# 后端 venv
echo "→ 创建 Python 虚拟环境..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements-dev.txt -q
cp -n .env.example .env 2>/dev/null || true
cd ..

echo ""
echo "======================================================"
echo "  ✓ 初始化完成！"
echo "  运行 make dev 启动开发环境"
echo "======================================================"
