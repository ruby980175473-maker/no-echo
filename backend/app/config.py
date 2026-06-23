# ============================================================
# NO ECHO · 配置管理
# 使用 pydantic-settings 从环境变量读取配置
# ============================================================

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ── Supabase ──────────────────────────────────────────────
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    # ── 第三方 API ────────────────────────────────────────────
    bing_search_api_key: str
    gptzero_api_key: str

    # ── 应用参数 ──────────────────────────────────────────────
    max_file_size_mb: int = 20
    file_expiry_hours: int = 24
    rate_limit_per_hour: int = 10

    # ── 模型 ──────────────────────────────────────────────────
    model_cache_dir: str = "./models_cache"
    embedding_model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"

    # ── 环境 ──────────────────────────────────────────────────
    environment: str = "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


# 单例：整个应用通过 from app.config import settings 使用
settings = Settings()
