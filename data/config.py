from __future__ import annotations

import logging

from environs import Env


class ConfigError(RuntimeError):
    """Raised when required application configuration is invalid."""


def load_config() -> Env:
    env = Env()
    env.read_env()

    try:
        env.str("BOT_TOKEN")
    except Exception as exc:
        raise ConfigError(
            "BOT_TOKEN is missing. Create a .env file based on .env.example."
        ) from exc

    return env


def get_bot_token(env: Env) -> str:
    token = env.str("BOT_TOKEN").strip()
    if not token:
        raise ConfigError("BOT_TOKEN cannot be empty.")
    return token


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
