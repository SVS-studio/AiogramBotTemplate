from __future__ import annotations

import asyncio
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import TypedDict

from services.i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "bot.sqlite3"


class UserSettings(TypedDict):
    language: str
    notifications_enabled: bool
    referral_count: int


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def _initialize_sync() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(_connect()) as connection:
        connection.execute("PRAGMA journal_mode=WAL")
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id INTEGER PRIMARY KEY,
                    language TEXT NOT NULL DEFAULT 'uz',
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(user_preferences)")
            }
            if "notifications_enabled" not in columns:
                connection.execute(
                    "ALTER TABLE user_preferences ADD COLUMN notifications_enabled INTEGER NOT NULL DEFAULT 1"
                )
            if "referred_by" not in columns:
                connection.execute(
                    "ALTER TABLE user_preferences ADD COLUMN referred_by INTEGER"
                )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_user_preferences_referred_by
                ON user_preferences(referred_by)
                """
            )


def _register_user_sync(user_id: int, referrer_id: int | None = None) -> tuple[bool, bool]:
    credited_referral = None
    with closing(_connect()) as connection:
        with connection:
            existing = connection.execute(
                "SELECT user_id FROM user_preferences WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            if existing:
                return False, False

            if referrer_id and referrer_id != user_id:
                referrer = connection.execute(
                    "SELECT user_id FROM user_preferences WHERE user_id = ?",
                    (referrer_id,),
                ).fetchone()
                if referrer:
                    credited_referral = referrer_id

            connection.execute(
                """
                INSERT INTO user_preferences (user_id, language, notifications_enabled, referred_by)
                VALUES (?, ?, 1, ?)
                """,
                (user_id, DEFAULT_LANGUAGE, credited_referral),
            )
    return True, credited_referral is not None


def _get_settings_sync(user_id: int) -> UserSettings:
    with closing(_connect()) as connection:
        with connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO user_preferences (user_id, language)
                VALUES (?, ?)
                """,
                (user_id, DEFAULT_LANGUAGE),
            )
        row = connection.execute(
            """
            SELECT language, notifications_enabled,
                   (SELECT COUNT(*) FROM user_preferences AS invited
                    WHERE invited.referred_by = user_preferences.user_id) AS referral_count
            FROM user_preferences
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

    language = row["language"] if row and row["language"] in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    return {
        "language": language,
        "notifications_enabled": bool(row["notifications_enabled"]) if row else True,
        "referral_count": int(row["referral_count"]) if row else 0,
    }


def _set_language_sync(user_id: int, language: str) -> None:
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    with closing(_connect()) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO user_preferences (user_id, language)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    language = excluded.language,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (user_id, language),
            )


def _toggle_notifications_sync(user_id: int) -> bool:
    with closing(_connect()) as connection:
        with connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO user_preferences (user_id, language)
                VALUES (?, ?)
                """,
                (user_id, DEFAULT_LANGUAGE),
            )
            connection.execute(
                """
                UPDATE user_preferences
                SET notifications_enabled = CASE
                    WHEN notifications_enabled = 1 THEN 0 ELSE 1
                END,
                updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                """,
                (user_id,),
            )
        row = connection.execute(
            "SELECT notifications_enabled FROM user_preferences WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    return bool(row["notifications_enabled"])


async def initialize_preferences() -> None:
    await asyncio.to_thread(_initialize_sync)


async def register_user(user_id: int, referrer_id: int | None = None) -> tuple[bool, bool]:
    return await asyncio.to_thread(_register_user_sync, user_id, referrer_id)


async def get_settings(user_id: int) -> UserSettings:
    return await asyncio.to_thread(_get_settings_sync, user_id)


async def get_language(user_id: int) -> str:
    settings = await get_settings(user_id)
    return settings["language"]


async def set_language(user_id: int, language: str) -> None:
    await asyncio.to_thread(_set_language_sync, user_id, language)


async def toggle_notifications(user_id: int) -> bool:
    return await asyncio.to_thread(_toggle_notifications_sync, user_id)
