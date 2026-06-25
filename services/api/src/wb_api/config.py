"""Application settings.

Loaded from environment (12-factor). Secrets (encryption keys, DB URL) are
never hard-coded; defaults are safe for local development only. ``app_env``
gates production-only behaviour such as hiding internal error detail.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_env: str = Field(default="development", validation_alias=AliasChoices("WB_APP_ENV", "APP_ENV"))
    service_version: str = Field(default="1.0.0", validation_alias=AliasChoices("WB_SERVICE_VERSION", "SERVICE_VERSION"))
    log_level: str = Field(default="INFO", validation_alias=AliasChoices("WB_LOG_LEVEL", "LOG_LEVEL"))

    database_url: str = Field(
        default="postgresql+psycopg://wb:wb@localhost:5432/wb",
        validation_alias=AliasChoices("DATABASE_URL", "WB_DATABASE_URL"),
    )
    db_pool_size: int = Field(default=5, validation_alias=AliasChoices("WB_DB_POOL_SIZE"))
    db_max_overflow: int = Field(default=10, validation_alias=AliasChoices("WB_DB_MAX_OVERFLOW"))
    db_statement_timeout_ms: int = Field(default=10_000, validation_alias=AliasChoices("WB_DB_STATEMENT_TIMEOUT_MS"))

    # Directory of verified, immutable rule bundles loaded by the engine.
    bundle_dir: str = Field(default="data/verified-rules", validation_alias=AliasChoices("WB_BUNDLE_DIR"))

    # Idempotency record retention.
    idempotency_ttl_seconds: int = Field(default=86_400, validation_alias=AliasChoices("WB_IDEMPOTENCY_TTL_SECONDS"))

    # Request limits.
    max_request_bytes: int = Field(default=256 * 1024, validation_alias=AliasChoices("WB_MAX_REQUEST_BYTES"))
    max_page_size: int = Field(default=100, validation_alias=AliasChoices("WB_MAX_PAGE_SIZE"))

    # ADR-011: critical stale content fails closed rather than guessing.
    fail_closed_on_stale: bool = Field(default=True, validation_alias=AliasChoices("WB_FAIL_CLOSED_ON_STALE"))

    # Curator OIDC (ADR-008). Empty issuer disables curator auth wiring in dev.
    curator_jwt_issuer: str = Field(default="", validation_alias=AliasChoices("WB_CURATOR_JWT_ISSUER"))
    curator_jwt_audience: str = Field(default="", validation_alias=AliasChoices("WB_CURATOR_JWT_AUDIENCE"))
    curator_jwks_url: str = Field(default="", validation_alias=AliasChoices("WB_CURATOR_JWKS_URL"))

    cors_allow_origins: str = Field(default="", validation_alias=AliasChoices("WB_CORS_ALLOW_ORIGINS"))

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in {"production", "prod"}

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
