-- ============================================================
-- Seed 001 · 开发测试数据
-- 用于本地开发和 CI 集成测试
-- ============================================================

-- 插入一条已完成的测试任务
INSERT INTO jobs (id, status, file_name, file_path) VALUES
    ('00000000-0000-0000-0000-000000000001', 'completed', 'sample_thesis.docx', 'dev/sample_thesis.docx');

-- 插入测试段落
INSERT INTO paragraphs (job_id, index, text, heading_level, style_name) VALUES
    ('00000000-0000-0000-0000-000000000001', 0, '摘要', 1, 'Heading 1'),
    ('00000000-0000-0000-0000-000000000001', 1, '人工智能的发展推动了教育数字化转型。本研究通过问卷调查法...', null, 'Normal');
