# ============================================================
# NO ECHO · School Profile API 路由
# 业务逻辑待实现（所有路由当前返回 501 Not Implemented）
#
# 管理员操作流程：
#   1. POST /api/schools                      → 创建学校
#   2. POST /api/schools/{id}/colleges         → 添加学院（可选）
#   3. POST /api/schools/{id}/specs            → 创建规范版本（草稿）
#   4. POST /api/spec/upload                   → 上传规范文件 → 获得 rule_set_id
#   5. POST /api/schools/{id}/specs/{sid}/ruleset → 绑定 Rule Set
#   6. POST /api/schools/{id}/specs/{sid}/activate → 激活版本
#
# 用户使用流程：
#   1. GET /api/schools?search=浙工            → 搜索学校
#   2. GET /api/schools/{id}/specs/match       → 按学院+层次+年份匹配规范
#   3. → 获得 spec_version_id，传给论文检测接口
# ============================================================

from typing import Optional
from fastapi import APIRouter, HTTPException, Path, Query

from app.modules.school.models import (
    AttachRuleSetRequest,
    CollegeCreate,
    CollegeResponse,
    DegreeLevel,
    SchoolCreate,
    SchoolListItem,
    SchoolResponse,
    SchoolUpdate,
    SpecMatchResult,
    SpecVersionCreate,
    SpecVersionListItem,
    SpecVersionResponse,
)

router = APIRouter()

_NOT_IMPL = HTTPException(status_code=501, detail="业务逻辑待实现（Sprint 4+）")


# ── Schools ───────────────────────────────────────────────────────

@router.post(
    "/schools",
    response_model=SchoolResponse,
    status_code=201,
    summary="创建学校",
)
async def create_school(body: SchoolCreate):
    """
    创建一所学校记录。
    TODO: 写入 schools 表，检查 name 唯一性。
    """
    raise _NOT_IMPL


@router.get(
    "/schools",
    response_model=list[SchoolListItem],
    summary="搜索/列出学校",
)
async def list_schools(
    search:   Optional[str] = Query(None, description="按学校名称模糊搜索"),
    city:     Optional[str] = Query(None, description="按城市过滤"),
    province: Optional[str] = Query(None),
    limit:    int = Query(20, ge=1, le=100),
    offset:   int = Query(0, ge=0),
):
    """
    列出学校列表，支持名称搜索和地区过滤。
    TODO: 查询 schools 表，left join spec_versions 统计版本数。
    """
    raise _NOT_IMPL


@router.get(
    "/schools/{school_id}",
    response_model=SchoolResponse,
    summary="获取学校详情",
)
async def get_school(school_id: str = Path(...)):
    """
    获取指定学校的详细信息。
    TODO: 查询 schools 表，404 处理。
    """
    raise _NOT_IMPL


@router.put(
    "/schools/{school_id}",
    response_model=SchoolResponse,
    summary="更新学校信息",
)
async def update_school(school_id: str, body: SchoolUpdate):
    """
    更新学校的基本信息（名称、城市等）。
    TODO: 更新 schools 表，updated_at 自动刷新。
    """
    raise _NOT_IMPL


# ── Colleges ──────────────────────────────────────────────────────

@router.post(
    "/schools/{school_id}/colleges",
    response_model=CollegeResponse,
    status_code=201,
    summary="为学校添加学院",
)
async def create_college(school_id: str, body: CollegeCreate):
    """
    在指定学校下创建学院记录。
    TODO: 校验 school_id 存在，写入 colleges 表。
    """
    raise _NOT_IMPL


@router.get(
    "/schools/{school_id}/colleges",
    response_model=list[CollegeResponse],
    summary="列出学校下所有学院",
)
async def list_colleges(school_id: str):
    """
    TODO: 查询 colleges 表，按 school_id 过滤。
    """
    raise _NOT_IMPL


# ── SpecVersions ──────────────────────────────────────────────────

@router.post(
    "/schools/{school_id}/specs",
    response_model=SpecVersionResponse,
    status_code=201,
    summary="创建规范版本（草稿）",
)
async def create_spec_version(school_id: str, body: SpecVersionCreate):
    """
    为学校创建一个新的规范版本，初始状态为 draft。

    唯一性约束：同一 school + college + degree_level + year 组合只能有一条记录。
    Rule Set 需要在创建后通过 POST .../ruleset 单独绑定。

    TODO: 校验 school_id 和 college_id 存在，写入 spec_versions 表，
          检查唯一约束冲突（409 Conflict）。
    """
    raise _NOT_IMPL


@router.get(
    "/schools/{school_id}/specs",
    response_model=list[SpecVersionListItem],
    summary="列出学校下所有规范版本",
)
async def list_spec_versions(
    school_id:    str,
    degree_level: Optional[DegreeLevel] = Query(None),
    year:         Optional[int]         = Query(None),
    status:       Optional[str]         = Query(None, description="draft | active | archived"),
):
    """
    列出指定学校下的所有规范版本，支持按层次/年份/状态过滤。
    TODO: 查询 spec_versions 表，left join colleges 获取 college_name。
    """
    raise _NOT_IMPL


@router.get(
    "/schools/{school_id}/specs/match",
    response_model=SpecMatchResult,
    summary="按学院+层次+年份匹配规范版本",
)
async def match_spec_version(
    school_id:    str,
    degree_level: DegreeLevel   = Query(..., description="本科/硕士/博士"),
    college_id:   Optional[str] = Query(None, description="学院 ID，不填则匹配全校通用版本"),
    year:         Optional[int] = Query(None, description="年份，不填则使用当前年份"),
):
    """
    按优先级从高到低匹配最合适的有效规范版本：
    1. 精确匹配：school + college + degree_level + year（status=active）
    2. 学院通用：school + college + degree=all + year
    3. 全校版本：school + college=NULL + degree_level + year
    4. 全校全层：school + college=NULL + degree=all + year

    任何一级匹配成功则返回，全部失败则 404。

    TODO: 实现四级查询逻辑，rule_set 必须已绑定（has_rule_set=True）才算匹配成功。
    """
    raise _NOT_IMPL


@router.get(
    "/schools/{school_id}/specs/{spec_id}",
    response_model=SpecVersionResponse,
    summary="获取规范版本详情",
)
async def get_spec_version(school_id: str, spec_id: str):
    """
    TODO: 查询 spec_versions 表，验证 school_id 匹配，404 处理。
    """
    raise _NOT_IMPL


@router.post(
    "/schools/{school_id}/specs/{spec_id}/ruleset",
    status_code=200,
    summary="绑定 Rule Set 到规范版本",
)
async def attach_ruleset(school_id: str, spec_id: str, body: AttachRuleSetRequest):
    """
    将已上传解析完成的 Rule Set（来自 POST /api/spec/upload）
    绑定到指定规范版本。

    操作顺序：
    1. POST /api/spec/upload → 获得 rule_set_id
    2. POST /api/schools/{id}/specs/{sid}/ruleset（本接口）→ 完成绑定

    绑定后版本 has_rule_set=True，可以执行 activate。

    TODO: 校验 rule_set_id 存在于 rule_sets 表，
          更新 spec_versions.rule_set_id，has_rule_set=True。
    """
    raise _NOT_IMPL


@router.post(
    "/schools/{school_id}/specs/{spec_id}/activate",
    status_code=200,
    summary="激活规范版本",
)
async def activate_spec_version(school_id: str, spec_id: str):
    """
    将指定版本设为 active（当前有效版本）。

    激活条件：版本必须已绑定 Rule Set（has_rule_set=True）。
    激活后：将同一 school + college + degree_level 条件下
    其他 active 版本自动设为 archived。

    TODO: 事务操作：UPDATE spec_versions SET status='archived'
          WHERE school_id=... AND college_id=... AND degree_level=...
                AND status='active';
          然后 UPDATE spec_versions SET status='active', is_current=TRUE
          WHERE id=spec_id;
    """
    raise _NOT_IMPL


@router.post(
    "/schools/{school_id}/specs/{spec_id}/archive",
    status_code=200,
    summary="归档规范版本",
)
async def archive_spec_version(school_id: str, spec_id: str):
    """
    将版本标记为 archived（历史版本）。
    如果该版本是 is_current=True，同时清除 is_current 标记。

    TODO: UPDATE spec_versions SET status='archived', is_current=FALSE
          WHERE id=spec_id AND school_id=school_id;
    """
    raise _NOT_IMPL


@router.get(
    "/schools/{school_id}/specs/{spec_id}/ruleset",
    summary="获取规范版本对应的 Rule Set JSON",
)
async def get_spec_ruleset(school_id: str, spec_id: str):
    """
    TODO: 从 spec_versions 拿到 rule_set_id，
          再从 rule_sets 表查 rule_json 字段返回。
    """
    raise _NOT_IMPL
