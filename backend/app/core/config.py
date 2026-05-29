from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Energy TradeOps Platform"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./energy_tradeops.db"
    seed_on_startup: bool = True
    risk_monitor_enabled: bool = True
    risk_monitor_interval_seconds: int = 300
    negative_margin_alert_threshold: float = -50_000
    high_volatility_threshold_percent: float = 7.5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
