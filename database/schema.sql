-- ============================================================
-- NO ECHO · 完整数据库 Schema 参考文档
-- 数据库：Supabase (PostgreSQL 15)
-- 说明：此文件为参考文档，实际迁移通过 migrations/ 目录执行
-- ============================================================

-- ── 检测任务表 ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at      TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '24 hours',
    status          VARCHAR(20) NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','parsing','checking','completed','failed')),
    file_name       VARCHAR(255) NOT NULL,
    file_path       VARCHAR(500) NOT NULL,
    error_message   TEXT
);

-- ── 段落表（DOCX 解析结果）────────────────────────────────────
CREATE TABLE IF NOT EXISTS paragraphs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id              UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    index               INTEGER NOT NULL,
    text                TEXT NOT NULL,
    heading_level       INTEGER CHECK (heading_level IN (1, 2, 3)),
    style_name          VARCHAR(100),
    font_name           VARCHAR(100),
    font_size_pt        NUMERIC(5,2),
    line_spacing        NUMERIC(5,2),
    first_line_indent   NUMERIC(5,2),
    UNIQUE (job_id, index)
);

-- ── 重复风险标注表 ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS similarity_risks (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paragraph_id     UUID NOT NULL REFERENCES paragraphs(id) ON DELETE CASCADE,
    risk_level       VARCHAR(10) NOT NULL CHECK (risk_level IN ('high','medium','low','none')),
    risk_type        VARCHAR(30) NOT NULL CHECK (risk_type IN ('web','academic','internal','paraphrase')),
    matched_text     TEXT,
    source_url       TEXT,
    source_title     TEXT,
    similarity_score NUMERIC(4,3) CHECK (similarity_score BETWEEN 0 AND 1)
);

-- ── AIGC 风险标注表 ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS aigc_risks (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paragraph_id     UUID NOT NULL REFERENCES paragraphs(id) ON DELETE CASCADE,
    risk_level       VARCHAR(10) NOT NULL CHECK (risk_level IN ('high','medium','low','none')),
    ai_probability   NUMERIC(4,3) NOT NULL CHECK (ai_probability BETWEEN 0 AND 1),
    sentence_details JSONB,
    api_source       VARCHAR(30) NOT NULL DEFAULT 'gptzero'
);

-- ── 格式问题表 ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS format_issues (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id          UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    section         VARCHAR(50) NOT NULL,
    issue_type      VARCHAR(80) NOT NULL,
    description     TEXT NOT NULL,
    expected        VARCHAR(200),
    actual          VARCHAR(200),
    paragraph_index INTEGER
);

-- ── 索引 ──────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_paragraphs_job_id         ON paragraphs(job_id);
CREATE INDEX IF NOT EXISTS idx_similarity_paragraph_id   ON similarity_risks(paragraph_id);
CREATE INDEX IF NOT EXISTS idx_aigc_paragraph_id         ON aigc_risks(paragraph_id);
CREATE INDEX IF NOT EXISTS idx_format_issues_job_id      ON format_issues(job_id);
CREATE INDEX IF NOT EXISTS idx_jobs_expires_at           ON jobs(expires_at);  -- 清理任务用
CREATE INDEX IF NOT EXISTS idx_jobs_status               ON jobs(status);

-- ── Row Level Security (Supabase) ─────────────────────────────
-- V1.0：通过 job_id UUID 隔离访问（无需登录）
-- V1.1：启用 RLS + user_id 关联
ALTER TABLE jobs             ENABLE ROW LEVEL SECURITY;
ALTER TABLE paragraphs       ENABLE ROW LEVEL SECURITY;
ALTER TABLE similarity_risks ENABLE ROW LEVEL SECURITY;
ALTER TABLE aigc_risks       ENABLE ROW LEVEL SECURITY;
ALTER TABLE format_issues    ENABLE ROW LEVEL SECURITY;

-- V1.0 临时策略：允许匿名访问（通过 job_id 隔离）
-- TODO V1.1：替换为基于 auth.uid() 的精细策略
CREATE POLICY "anon_access_jobs" ON jobs FOR ALL USING (true);
CREATE POLICY "anon_access_paragraphs" ON paragraphs FOR ALL USING (true);
CREATE POLICY "anon_access_similarity" ON similarity_risks FOR ALL USING (true);
CREATE POLICY "anon_access_aigc" ON aigc_risks FOR ALL USING (true);
CREATE POLICY "anon_access_format" ON format_issues FOR ALL USING (true);
