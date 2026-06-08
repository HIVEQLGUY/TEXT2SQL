from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _parse_int(value: str | None, default: int) -> int:
    if value is None or value == "":
        return default
    return int(value)


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _merged_env() -> dict[str, str]:
    env_file = Path(os.environ.get("TEXT2SQL_ENV_FILE", ROOT_DIR / ".env"))
    values = load_env_file(env_file)
    values.update(os.environ)
    return values


@dataclass(frozen=True)
class DatabaseSettings:
    host: str
    port: int
    user: str
    password: str
    database: str
    connect_timeout: int = 10
    read_timeout: int = 30
    write_timeout: int = 30
    mysql_get_server_public_key: bool = False

    def safe_info(self) -> dict[str, object]:
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "database": self.database,
            "mysql_get_server_public_key": self.mysql_get_server_public_key,
        }

    def missing_values(self, prefix: str) -> list[str]:
        missing = []
        for name, value in {
            "HOST": self.host,
            "USER": self.user,
            "PASSWORD": self.password,
            "NAME": self.database,
        }.items():
            if not value:
                missing.append(f"{prefix}_{name}")
        return missing


@dataclass(frozen=True)
class Settings:
    app_name: str
    environment: str
    log_level: str
    metadata_db: DatabaseSettings
    warehouse_db: DatabaseSettings
    llm: LLMSettings

    def missing_required_values(self) -> list[str]:
        missing = [
            *self.metadata_db.missing_values("META_DB"),
            *self.warehouse_db.missing_values("DW_DB"),
        ]
        if self.llm.enabled:
            missing.extend(self.llm.missing_values())
        return missing


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    base_url: str
    api_key: str
    model: str
    timeout_seconds: int = 60

    @property
    def enabled(self) -> bool:
        return bool(self.provider or self.base_url or self.api_key or self.model)

    def safe_info(self) -> dict[str, object]:
        return {
            "provider": self.provider,
            "base_url": self.base_url,
            "model": self.model,
            "timeout_seconds": self.timeout_seconds,
            "api_key_configured": bool(self.api_key),
        }

    def missing_values(self) -> list[str]:
        missing = []
        for name, value in {
            "LLM_BASE_URL": self.base_url,
            "LLM_API_KEY": self.api_key,
            "LLM_MODEL": self.model,
        }.items():
            if not value:
                missing.append(name)
        return missing


def _load_database_settings(values: dict[str, str], prefix: str) -> DatabaseSettings:
    legacy_prefix = "DB" if prefix == "DW_DB" else prefix
    return DatabaseSettings(
        host=values.get(f"{prefix}_HOST") or values.get(f"{legacy_prefix}_HOST", ""),
        port=_parse_int(values.get(f"{prefix}_PORT") or values.get(f"{legacy_prefix}_PORT"), 3306),
        user=values.get(f"{prefix}_USER") or values.get(f"{legacy_prefix}_USER", ""),
        password=values.get(f"{prefix}_PASSWORD") or values.get(f"{legacy_prefix}_PASSWORD", ""),
        database=values.get(f"{prefix}_NAME") or values.get(f"{legacy_prefix}_NAME", ""),
        connect_timeout=_parse_int(
            values.get(f"{prefix}_CONNECT_TIMEOUT") or values.get(f"{legacy_prefix}_CONNECT_TIMEOUT"),
            10,
        ),
        read_timeout=_parse_int(
            values.get(f"{prefix}_READ_TIMEOUT") or values.get(f"{legacy_prefix}_READ_TIMEOUT"),
            30,
        ),
        write_timeout=_parse_int(
            values.get(f"{prefix}_WRITE_TIMEOUT") or values.get(f"{legacy_prefix}_WRITE_TIMEOUT"),
            30,
        ),
        mysql_get_server_public_key=_parse_bool(
            values.get(f"{prefix}_MYSQL_GET_SERVER_PUBLIC_KEY")
            or values.get(f"{legacy_prefix}_MYSQL_GET_SERVER_PUBLIC_KEY"),
            default=False,
        ),
    )


def _load_llm_settings(values: dict[str, str]) -> LLMSettings:
    return LLMSettings(
        provider=values.get("LLM_PROVIDER", ""),
        base_url=values.get("LLM_BASE_URL", ""),
        api_key=values.get("LLM_API_KEY", ""),
        model=values.get("LLM_MODEL", ""),
        timeout_seconds=_parse_int(values.get("LLM_TIMEOUT_SECONDS"), 60),
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    values = _merged_env()
    return Settings(
        app_name=values.get("APP_NAME", "TEXT2SQL"),
        environment=values.get("APP_ENV", "local"),
        log_level=values.get("APP_LOG_LEVEL", "INFO"),
        metadata_db=_load_database_settings(values, "META_DB"),
        warehouse_db=_load_database_settings(values, "DW_DB"),
        llm=_load_llm_settings(values),
    )


def reload_settings_for_tests() -> None:
    get_settings.cache_clear()
