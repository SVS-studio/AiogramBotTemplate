from __future__ import annotations

import logging

from environs import Env


class ConfigError(RuntimeError):
    """Raised when required application configuration is invalid."""


def load_config() -> Env:
    env = Env()
    env.read_env()

    if not env.str("BOT_TOKEN", "").strip():
        raise ConfigError(
            "BOT_TOKEN is missing or empty. Set it in your .env file."
        )

    return env


def get_bot_token(env: Env) -> str:
    return env.str("BOT_TOKEN").strip()


def get_platform_api_base_url(env: Env) -> str:
    return env.str("IELTS_API_BASE_URL", "http://127.0.0.1:8000").strip().rstrip("/")


def get_platform_api_secret(env: Env) -> str:
    return env.str("IELTS_BOT_INTERNAL_SECRET", "").strip()


def get_admin_ids(env: Env) -> set[int]:
    raw_admins = env.list("ADMINS", subcast=str, default=[])
    try:
        return {int(admin.strip()) for admin in raw_admins if admin.strip()}
    except ValueError as exc:
        raise ConfigError("ADMINS must contain comma-separated integer user IDs.") from exc


def get_log_level(env: Env) -> int:
    level_name = env.str("LOG_LEVEL", "INFO").upper()
    level = logging.getLevelName(level_name)
    if not isinstance(level, int):
        raise ConfigError(
            "LOG_LEVEL must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL."
        )
    return level


def should_drop_pending_updates(env: Env) -> bool:
    return env.bool("DROP_PENDING_UPDATES", True)
