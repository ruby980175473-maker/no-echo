# ============================================================
# NO ECHO · 数据库模型（数据库字段 ↔ Python 对象映射）
# Supabase 返回 dict，通过此处的类进行类型化
# ============================================================

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Job:
    """对应 database/schema.sql 中的 jobs 表"""
    id:            str
    created_at:    datetime
    expires_at:    datetime
    status:        str
    file_name:     str
    file_path:     str
    error_message: Optional[str] = None


@dataclass
class Paragraph:
    """对应 paragraphs 表"""
    id:                 str
    job_id:             str
    index:              int
    text:               str
    heading_level:      Optional[int]   = None
    style_name:         Optional[str]   = None
    font_name:          Optional[str]   = None
    font_size_pt:       Optional[float] = None
    line_spacing:       Optional[float] = None
    first_line_indent:  Optional[float] = None
