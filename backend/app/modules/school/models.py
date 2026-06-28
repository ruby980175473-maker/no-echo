# ============================================================
# NO ECHO · School Profile 数据模型
#
# 实体层级：
# School（学校）
#   └── College（学院，可选）
#   └── SpecVersion（规范版本）
#         ├── degree_level（本科/硕士/博士/全部）
#         ├── year（2025/2026/...）
#         └── rule_set_id → RuleSet
#
# 设计原则：
# - 一所学校可以有多个规范版本（按年份区分）
# - 同一学校可以同时维护不同学院、不同学历层次的版本
# - RuleSet 通过 POST /api/spec/upload 独立上传，再绑定到 SpecVersion
# ============================================================

from __future__ import annotations
from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ── 枚举 ───────────────────────────────────────────────────────

class DegreeLevel(str, Enum):
    undergraduate = "undergraduate"   # 本科
    master        = "master"          # 硕士
    doctoral      = "doctoral"        # 博士
    all           = "all"             # 通用，不区分层次


class SpecStatus(str, Enum):
    draft    = "draft"      # 草稿：已创建，Rule Set 尚未上传或尚未激活
    active   = "active"     # 有效：当前使用的版本（同条件下只能有一个）
    archived = "archived"   # 归档：历史版本，不再使用


# ── School ─────────────────────────────────────────────────────

class SchoolCreate(BaseModel):
    """创建学校的请求体"""
    name:       str                  # 浙江工业大学之江学院
    short_name: Optional[str] = None # 之江学院
    city:       Optional[str] = None
    province:   Optional[str] = None


class SchoolUpdate(BaseModel):
    """更新学校的请求体（所有字段可选）"""
    name:       Optional[str] = None
    short_name: Optional[str] = None
    city:       Optional[str] = None
    province:   Optional[str] = None
    is_active:  Optional[bool] = None


class SchoolResponse(BaseModel):
    """学校完整信息响应"""
    id:          str
    name:        str
    short_name:  Optional[str]
    city:        Optional[str]
    province:    Optional[str]
    is_active:   bool
    created_at:  datetime
    updated_at:  datetime


class SchoolListItem(BaseModel):
    """学校列表条目（精简）"""
    id:                  str
    name:                str
    short_name:          Optional[str]
    city:                Optional[str]
    is_active:           bool
    spec_version_count:  int = 0   # 该校下的规范版本总数
    active_spec_count:   int = 0   # 其中状态为 active 的数量


# ── College ─────────────────────────────────────────────────────

class CollegeCreate(BaseModel):
    name:       str                  # 广告传媒学院
    short_name: Optional[str] = None # 广传院


class CollegeResponse(BaseModel):
    id:         str
    school_id:  str
    name:       str
    short_name: Optional[str]
    is_active:  bool
    created_at: datetime


# ── SpecVersion ─────────────────────────────────────────────────

class SpecVersionCreate(BaseModel):
    """
    创建规范版本的请求体。
    创建后状态为 draft；需通过 attach_ruleset 绑定 Rule Set 后才能 activate。
    """
    college_id:   Optional[str]  = None
    # None = 适用该校所有学院；填写则限定到具体学院

    degree_level: DegreeLevel    = DegreeLevel.all
    year:         int            = Field(ge=2000, le=2100)
    label:        Optional[str]  = None
    # 人类可读标签，如 "2025届本科毕业论文格式规范"

    description:  Optional[str]  = None


class SpecVersionResponse(BaseModel):
    """规范版本完整信息响应"""
    id:           str
    school_id:    str
    college_id:   Optional[str]
    college_name: Optional[str]  # join 显示，来自 colleges.name
    degree_level: DegreeLevel
    year:         int
    label:        Optional[str]
    description:  Optional[str]
    status:       SpecStatus
    is_current:   bool
    rule_set_id:  Optional[str]  # None = 尚未绑定 Rule Set
    has_rule_set: bool           # 便于前端判断
    created_at:   datetime
    updated_at:   datetime


class SpecVersionListItem(BaseModel):
    """规范版本列表条目（精简）"""
    id:           str
    degree_level: DegreeLevel
    year:         int
    label:        Optional[str]
    status:       SpecStatus
    is_current:   bool
    has_rule_set: bool
    college_name: Optional[str] = None


# ── Match Query ──────────────────────────────────────────────────

class SpecMatchResult(BaseModel):
    """
    学校规范版本匹配结果。

    匹配优先级（从高到低）：
    1. 精确匹配：school + college + degree_level + year
    2. 学院通用：school + college + degree_all + year
    3. 全校通用：school + college=NULL + degree_level + year
    4. 全校全层：school + college=NULL + degree_all + year
    """
    spec_version: SpecVersionResponse
    match_level:  str   # "exact" | "degree_all" | "college_null" | "college_null_degree_all"
    match_reason: str   # "精确匹配：广告学院 · 本科 · 2026年"


# ── Attach RuleSet Request ───────────────────────────────────────

class AttachRuleSetRequest(BaseModel):
    """将 Rule Set 绑定到规范版本"""
    rule_set_id: str
    # 来自 POST /api/spec/upload 返回的 spec_id
    # 注：此处 spec_id 指的是 rule_sets 表中的 UUID，
    # 不是 spec_versions 表中的 UUID（两个不同概念）
