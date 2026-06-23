<div align="center">
  <h1>NO ECHO</h1>
  <p>本科论文预检平台 · 重复风险 × AIGC风险 × 格式检查</p>

  ![License](https://img.shields.io/badge/license-MIT-blue.svg)
  ![Frontend](https://img.shields.io/badge/frontend-Next.js%2014-black)
  ![Backend](https://img.shields.io/badge/backend-FastAPI-009688)
  ![Database](https://img.shields.io/badge/database-Supabase-3ECF8E)
  ![Status](https://img.shields.io/badge/status-WIP-yellow)
</div>

---

## 简介

NO ECHO 是一个面向中国本科毕业生的**论文预检平台**。
在正式提交知网查重前，帮助学生低成本定位「重复风险段落」「AIGC 高风险段落」和「格式规范问题」，提供段落级标注与可执行修改建议。

> ⚠️ NO ECHO 不等于知网查重。重复风险评级基于公开资源，仅供参考。

### 核心功能

| 功能 | 说明 |
|------|------|
| 🔁 重复风险预检 | 基于 Bing Search API + Semantic Scholar 的段落级公开资源相似度检测 |
| 🤖 AIGC 风险预检 | 调用 GPTZero API，输出段落级 AI 生成概率 |
| 📐 格式规范检查 | 对照学校模板或 GB/T 内置规范，检测字体 / 行距 / 参考文献等格式问题 |
| 📊 可视化报告 | 段落高亮渲染 + 内联修改建议 + PDF 导出 |

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Next.js 14 · TypeScript · Tailwind CSS |
| 后端 | Python 3.11 · FastAPI · Uvicorn |
| 数据库 | Supabase (PostgreSQL) |
| 文件存储 | Supabase Storage |
| DOCX 解析 | python-docx · Mammoth |
| 相似度检测 | SimHash · sentence-transformers |
| 网页搜索 | Bing Search API (Azure) |
| 学术搜索 | Semantic Scholar API（免费） |
| AIGC 检测 | GPTZero API |
| 部署 | Vercel (前端) · Railway (后端) |

---

## 快速开始

### 环境要求

- Node.js >= 18.17.0
- Python >= 3.11
- Docker & Docker Compose（可选，推荐）

### 方式一：Docker 一键启动（推荐）

```bash
git clone https://github.com/your-username/no-echo.git
cd no-echo

# 复制并填写环境变量
cp .env.example .env

# 启动开发环境
make dev
```

访问 http://localhost:3000

### 方式二：手动启动

```bash
git clone https://github.com/your-username/no-echo.git
cd no-echo

# 1. 安装依赖并启动后端
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # 填写 API Keys
uvicorn app.main:app --reload --port 8000

# 2. 另开终端，启动前端
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

前端 http://localhost:3000 · 后端 http://localhost:8000 · API 文档 http://localhost:8000/docs

---

## 项目结构

```
no-echo/
├── .github/                     # GitHub Actions CI/CD + Issue 模板
│   ├── workflows/
│   │   ├── ci-frontend.yml      # 前端 lint + typecheck + build
│   │   ├── ci-backend.yml       # 后端 lint + typecheck + pytest
│   │   └── deploy.yml           # 自动部署到 Vercel + Railway
│   └── ISSUE_TEMPLATE/
│
├── frontend/                    # Next.js 14 前端（Vercel 部署）
│   ├── app/                     # App Router 页面
│   │   ├── upload/              # 文件上传页
│   │   ├── processing/[job_id]/ # 检测进度页
│   │   └── results/[job_id]/    # 结果页（总览 + 详细报告）
│   ├── components/              # React 组件
│   │   ├── ui/                  # 通用 UI 原子组件（Button, Card, Badge）
│   │   ├── upload/              # 上传相关组件
│   │   ├── results/             # 结果展示组件
│   │   └── layout/              # Header, Footer
│   └── lib/                     # 工具库
│       ├── api/                 # 后端 API 调用封装
│       ├── hooks/               # 自定义 React Hooks
│       └── types/               # TypeScript 类型定义
│
├── backend/                     # FastAPI 后端（Railway 部署）
│   ├── app/
│   │   ├── main.py              # FastAPI 入口 + 生命周期管理
│   │   ├── config.py            # 配置管理（pydantic-settings）
│   │   ├── routers/             # API 路由层
│   │   ├── modules/             # 核心检测模块（不含业务逻辑入口）
│   │   │   ├── parser/          # DOCX 解析
│   │   │   ├── format_check/    # 格式规范检查
│   │   │   ├── similarity/      # 重复风险检测
│   │   │   └── aigc/            # AIGC 风险检测
│   │   ├── services/            # 第三方 API 封装
│   │   ├── models/              # Pydantic schemas + DB models
│   │   └── utils/               # 工具函数
│   └── tests/                   # 后端测试（pytest）
│       ├── unit/
│       └── integration/
│
├── database/                    # 数据库相关
│   ├── migrations/              # SQL 迁移文件（按顺序执行）
│   ├── seeds/                   # 测试数据
│   └── schema.sql               # 完整 schema 参考文档
│
├── docs/                        # 项目文档
│   ├── PRD/                     # 产品需求文档
│   ├── ADR/                     # 架构决策记录
│   ├── TDD/                     # 技术设计文档
│   ├── api/                     # OpenAPI 规范
│   └── diagrams/                # 架构图
│
├── scripts/                     # 运维脚本
│   ├── setup.sh                 # 一键初始化开发环境
│   ├── migrate.sh               # 执行数据库迁移
│   └── clean.sh                 # 清理临时文件
│
├── tests/                       # 端到端测试（Playwright）
│   └── e2e/
│
├── docker/                      # Docker 配置
│   ├── nginx/                   # Nginx 反向代理配置
│   └── (frontend & backend Dockerfile 在各自目录下)
│
├── .gitignore
├── .env.example                 # 根目录环境变量模板
├── docker-compose.yml           # 生产环境编排
├── docker-compose.dev.yml       # 开发环境编排（含热重载）
├── Makefile                     # 常用命令快捷入口
├── README.md
└── LICENSE
```

---

## 常用命令

```bash
make help        # 查看所有可用命令
make dev         # 启动开发环境（Docker）
make test        # 运行所有测试
make lint        # 运行 lint 检查
make build       # 构建生产镜像
make migrate     # 执行数据库迁移
make clean       # 清理构建产物
```

---

## 开发指南

- 分支策略：`main`（生产）→ `dev`（集成）→ `feature/xxx`（功能）
- 提交格式：遵循 [Conventional Commits](https://www.conventionalcommits.org/)
- 每个 PR 必须通过 CI 检查后才能合并
- API 变更需同步更新 `docs/api/openapi.yaml`

详见 [docs/TDD/NO_ECHO_TDD_V1.0.md](docs/TDD/NO_ECHO_TDD_V1.0.md)

---

## 文档

| 文档 | 路径 |
|------|------|
| 产品需求文档 (PRD) | [docs/PRD/NO_ECHO_PRD_V1.0.md](docs/PRD/NO_ECHO_PRD_V1.0.md) |
| 架构决策记录 (ADR) | [docs/ADR/NO_ECHO_ADR_V1.0.md](docs/ADR/NO_ECHO_ADR_V1.0.md) |
| 技术设计文档 (TDD) | [docs/TDD/NO_ECHO_TDD_V1.0.md](docs/TDD/NO_ECHO_TDD_V1.0.md) |
| API 规范 | [docs/api/openapi.yaml](docs/api/openapi.yaml) |

---

## License

[MIT](LICENSE) © 2026 NO ECHO Contributors
