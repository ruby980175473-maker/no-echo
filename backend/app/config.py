# ============================================================
# NO ECHO · 配置管理
# Sprint 1: Supabase / 第三方 API Key 均设为可选（空字符串）
#            只有 max_file_size_mb 等基础参数是必要的
# ============================================================

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        protected_namespaces=("settings_",),
        env_file=".env",
        extra="ignore",       # 忽略 .env 中多余的字段，不报错
    )

    # ── Supabase（Sprint 2+ 启用，Sprint 1 留空即可）─────────
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    # ── 第三方检测 API（Sprint 3/4 启用）─────────────────────
    bing_search_api_key: str = ""
    gptzero_api_key: str = ""

    # ── 应用参数（Sprint 1 就用到）───────────────────────────
    max_file_size_mb: int = 20
    file_expiry_hours: int = 24
    rate_limit_per_hour: int = 10

    # ── 模型（Sprint 3+ 启用）────────────────────────────────
    model_cache_dir: str = "./models_cache"
    embedding_model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"

    # ── 环境标识 ──────────────────────────────────────────────
    environment: str = "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
