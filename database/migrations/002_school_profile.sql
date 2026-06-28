-- ============================================================
-- Migration 002 · School Profile 系统
-- 新增：schools / colleges / spec_versions 三张表
-- 修改：jobs 表新增 spec_version_id 外键
-- ============================================================

-- ── 1. 学校表 ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS schools (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(200) NOT NULL,
    short_name  VARCHAR(50),
    city        VARCHAR(100),
    province    VARCHAR(50),
    country     VARCHAR(50)  NOT NULL DEFAULT '中国',
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- 全文搜索索引（支持中文学校名称搜索）
CREATE INDEX IF NOT EXISTS idx_schools_name_gin
    ON schools USING gin(to_tsvector('simple', name));

CREATE INDEX IF NOT EXISTS idx_schools_active
    ON schools (is_active);


-- ── 2. 学院表 ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS colleges (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id   UUID        NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name        VARCHAR(200) NOT NULL,
    short_name  VARCHAR(50),
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    -- 同一学校下，学院名称唯一
    UNIQUE (school_id, name)
);

CREATE INDEX IF NOT EXISTS idx_colleges_school_id
    ON colleges (school_id);


-- ── 3. 规范版本表（核心关联表）────────────────────────────────
CREATE TABLE IF NOT EXISTS spec_versions (
    id           UUID         PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 学校关联（必填）
    school_id    UUID         NOT NULL REFERENCES schools(id) ON DELETE CASCADE,

    -- 学院关联（可选；NULL 表示适用该校所有学院）
    college_id   UUID         REFERENCES colleges(id) ON DELETE SET NULL,

    -- 学历层次
    degree_level VARCHAR(20)  NOT NULL DEFAULT 'all'
                 CHECK (degree_level IN ('undergraduate', 'master', 'doctoral', 'all')),

    -- 年份（如 2025、2026）
    year         SMALLINT     NOT NULL
                 CHECK (year BETWEEN 2000 AND 2100),

    -- 人类可读标签
    label        VARCHAR(200),
    description  TEXT,

    -- 状态
    status       VARCHAR(20)  NOT NULL DEFAULT 'draft'
                 CHECK (status IN ('draft', 'active', 'archived')),
    is_current   BOOLEAN      NOT NULL DEFAULT FALSE,

    -- 关联已解析的 Rule Set
    -- NULL 表示尚未绑定（版本处于草稿状态）
    rule_set_id  UUID         REFERENCES rule_sets(id) ON DELETE SET NULL,

    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    -- 唯一性约束：同一条件下只能有一个版本记录
    -- （业务逻辑层额外保证同条件下只能有一个 active 版本）
    UNIQUE (school_id, college_id, degree_level, year)
);

-- 唯一局部索引：同一 school + college + degree_level 条件下，
-- 只允许一个 is_current=TRUE 且 status='active' 的版本
CREATE UNIQUE INDEX IF NOT EXISTS idx_spec_versions_single_current
    ON spec_versions (school_id, COALESCE(college_id, '00000000-0000-0000-0000-000000000000'), degree_level)
    WHERE is_current = TRUE AND status = 'active';

-- 查询优化索引
CREATE INDEX IF NOT EXISTS idx_spec_versions_school_id
    ON spec_versions (school_id);

CREATE INDEX IF NOT EXISTS idx_spec_versions_lookup
    ON spec_versions (school_id, college_id, degree_level, year, status);

CREATE INDEX IF NOT EXISTS idx_spec_versions_active
    ON spec_versions (school_id, status)
    WHERE status = 'active';


-- ── 4. 更新 jobs 表：新增 spec_version_id 关联 ───────────────
-- 用户提交论文检测时，需要指定使用哪个规范版本做格式比对
ALTER TABLE jobs
    ADD COLUMN IF NOT EXISTS spec_version_id UUID REFERENCES spec_versions(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_jobs_spec_version_id
    ON jobs (spec_version_id);


-- ── 5. 自动更新 updated_at 的触发器函数 ──────────────────────
-- （Supabase 支持 PostgreSQL 触发器）
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_schools_updated_at
    BEFORE UPDATE ON schools
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

CREATE TRIGGER set_spec_versions_updated_at
    BEFORE UPDATE ON spec_versions
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
