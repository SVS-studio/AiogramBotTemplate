from __future__ import annotations

from html import escape

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from services.i18n import get_text
from services.platform_api import (
    PlatformAPIError,
    ask_verix,
    get_platform_profile,
)
from services.user_preferences import get_language

router = Router(name="ielts_companion")


def _profile_text(language: str, profile: dict) -> str:
    return get_text(
        language,
        "profile_summary",
        first_name=escape(str(profile.get("first_name") or "—")),
        email=escape(str(profile.get("email") or "—")),
        plan=escape(str(profile.get("plan") or "—")),
        level=escape(str(profile.get("english_level") or "—")),
        target=f"{profile.get('target_band_score', 0):g}",
        overall=f"{profile.get('overall_band_score', 0):g}",
        listening=f"{profile.get('listening_score', 0):g}",
        reading=f"{profile.get('reading_score', 0):g}",
        writing=f"{profile.get('writing_score', 0):g}",
        speaking=f"{profile.get('speaking_score', 0):g}",
        streak=str(profile.get("user_streak", 0)),
        tests=str(profile.get("test_completed", 0)),
    )


@router.message(Command("link"))
async def link_help_handler(message: Message) -> None:
    if message.from_user is None:
        return
    language = await get_language(message.from_user.id)
    await message.answer(get_text(language, "link_help"))


@router.message(Command("profile"))
async def platform_profile_handler(message: Message) -> None:
    if message.from_user is None:
        return
    language = await get_language(message.from_user.id)
    try:
        profile = await get_platform_profile(message.from_user.id)
    except PlatformAPIError as exc:
        key = "account_not_linked" if exc.status_code == 404 else "platform_error"
        await message.answer(get_text(language, key))
        return
    await message.answer(_profile_text(language, profile))


async def _send_verix_answer(message: Message, prompt: str) -> None:
    if message.from_user is None:
        return
    language = await get_language(message.from_user.id)
    if not prompt.strip():
        await message.answer(get_text(language, "verix_prompt"))
        return
    if len(prompt) > 4000:
        await message.answer(get_text(language, "verix_too_long"))
        return

    await message.chat.do("typing")
    try:
        answer = await ask_verix(message.from_user.id, prompt)
    except PlatformAPIError as exc:
        key = "account_not_linked" if exc.status_code == 404 else "platform_error"
        await message.answer(get_text(language, key))
        return

    # Disable the bot's default HTML parse mode: VERIX may return Markdown/plain text.
    await message.answer(answer[:3900], parse_mode=None)


@router.message(Command("verix"))
async def verix_command_handler(message: Message) -> None:
    prompt = (message.text or "").partition(" ")[2].strip()
    await _send_verix_answer(message, prompt)


@router.message(F.text & ~F.text.startswith("/"))
async def verix_text_handler(message: Message) -> None:
    if message.text:
        await _send_verix_answer(message, message.text.strip())
