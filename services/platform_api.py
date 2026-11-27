from __future__ import annotations

from typing import Any

import aiohttp

from data.config import load_config


class PlatformAPIError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


async def _post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    env = load_config()
    base_url = env.str("IELTS_API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    internal_secret = env.str("IELTS_BOT_INTERNAL_SECRET", "").strip()

    if not internal_secret:
        raise PlatformAPIError(
            "IELTS_BOT_INTERNAL_SECRET is not configured for the bot."
        )

    timeout = aiohttp.ClientTimeout(total=35)
    headers = {"X-IELTS-Bot-Secret": internal_secret}

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{base_url}/api/ai-services/telegram/bot/{path}/",
                json=payload,
                headers=headers,
            ) as response:
                try:
                    data = await response.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError):
                    data = {}

                if response.status >= 400:
                    detail = data.get("detail", "Platform API request failed.")
                    raise PlatformAPIError(str(detail), response.status)

                if not isinstance(data, dict):
                    raise PlatformAPIError("Platform API returned an invalid response.")

                return data
    except aiohttp.ClientError as exc:
        raise PlatformAPIError(
            "Could not connect to the IELTS Prep AI backend."
        ) from exc
    except TimeoutError as exc:
        raise PlatformAPIError(
            "The IELTS Prep AI backend request timed out."
        ) from exc


async def verify_telegram_link(telegram_id: int, token: str) -> dict[str, Any]:
    return await _post(
        "verify",
        {"telegram_id": telegram_id, "token": token},
    )


async def get_platform_profile(telegram_id: int) -> dict[str, Any]:
    return await _post("profile", {"telegram_id": telegram_id})


async def ask_verix(telegram_id: int, message: str) -> str:
    result = await _post(
        "chat",
        {"telegram_id": telegram_id, "message": message},
    )
    answer = result.get("message")
    if not isinstance(answer, str) or not answer.strip():
        raise PlatformAPIError("VERIX returned an empty response.")
    return answer.strip()
