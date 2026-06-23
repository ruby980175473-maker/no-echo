# NO ECHO · 系统架构图说明

```
用户浏览器（Next.js · Vercel）
        │
        │ HTTPS
        ▼
   Nginx 反向代理
   /api/* → 后端
   /*     → 前端
        │
   ┌────┴─────┐
   ▼           ▼
前端           后端（FastAPI · Railway）
(Next.js)      │
               ├── 文件解析（python-docx）
               ├── 格式检查（规则引擎）
               ├── 重复风险（SimHash + sentence-transformers）
               │         + Bing Search API
               │         + Semantic Scholar API
               ├── AIGC 风险（GPTZero API）
               └── 结果聚合
                        │
                        ▼
                   Supabase
                   ├── PostgreSQL（任务 + 结果存储）
                   └── Storage（临时文件，24h 清理）
```

## 数据流说明

1. 用户上传 DOCX → Nginx → FastAPI → Supabase Storage
2. FastAPI 创建 job 记录（status=pending）
3. 后台串行执行：解析 → 格式检查 → 重复风险 → AIGC 风险
4. 检测结果写入 PostgreSQL
5. 前端轮询 /api/status/{job_id}，status=completed 后跳转结果页
6. 前端请求 /api/results/{job_id}/detail，渲染段落高亮报告
