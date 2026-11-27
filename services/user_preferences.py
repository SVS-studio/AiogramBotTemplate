from __future__ import annotations

import asyncio
import sqlite3
from contextlib import closing
from pathlib import Path

from services.i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "bot.sqlite3"


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_PATH, timeout=10)


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


def _get_language_sync(user_id: int) -> str:
    with closing(_connect()) as connection:
        row = connection.execute(
            "SELECT language FROM user_preferences WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    if row and row[0] in SUPPORTED_LANGUAGES:
        return row[0]
    return DEFAULT_LANGUAGE


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


async def initialize_preferences() -> None:
    await asyncio.to_thread(_initialize_sync)


async def get_language(user_id: int) -> str:
    return await asyncio.to_thread(_get_language_sync, user_id)


async def set_language(user_id: int, language: str) -> None:
    await asyncio.to_thread(_set_language_sync, user_id, language)
