from __future__ import annotations

from html import escape

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, User

from keyboards.menus import (
    back_home_inline_keyboard,
    language_inline_keyboard,
    main_inline_keyboard,
    main_reply_keyboard,
    settings_inline_keyboard,
)
from services.i18n import LANGUAGE_NAMES, SUPPORTED_LANGUAGES, get_text
from services.user_preferences import get_language, set_language

router = Router(name="common")

_BUTTON_TO_ACTION = {
    get_text(language, key): action
    for language in SUPPORTED_LANGUAGES
    for key, action in (
        ("btn_features", "features"),
        ("btn_settings", "settings"),
        ("btn_profile", "profile"),
        ("btn_about", "about"),
    )
}


async def _show_menu(message: Message, language: str) -> None:
    await message.answer(
        get_text(language, "menu_title"),
        reply_markup=main_reply_keyboard(language),
    )
    await message.answer(
        get_text(language, "menu_title"),
        reply_markup=main_inline_keyboard(language),
    )


async def _show_section(
    message: Message,
    language: str,
    section: str,
    *,
    user: User | None = None,
) -> None:
    if section == "features":
        text = get_text(language, "features_title")
        keyboard = back_home_inline_keyboard(language)
    elif section == "settings":
        text = get_text(language, "settings_title")
        keyboard = settings_inline_keyboard(language)
    elif section == "about":
        text = get_text(language, "about")
        keyboard = back_home_inline_keyboard(language)
    elif section == "profile":
        profile_user = user or message.from_user
        if profile_user is None:
            return
        text = get_text(
            language,
            "profile",
            name=escape(profile_user.full_name),
            user_id=str(profile_user.id),
            username=escape(f"@{profile_user.username}" if profile_user.username else "—"),
            language=LANGUAGE_NAMES[language],
        )
        keyboard = back_home_inline_keyboard(language)
    else:
        return

    await message.answer(text, reply_markup=keyboard)


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    if message.from_user is None:
        return

    language = await get_language(message.from_user.id)
    greeting = get_text(
        language,
        "welcome",
        name=escape(message.from_user.first_name or "there"),
    )
    await message.answer(greeting, reply_markup=main_reply_keyboard(language))
    await message.answer(
        get_text(language, "menu_title"),
        reply_markup=main_inline_keyboard(language),
    )


@router.message(Command("menu"))
async def menu_handler(message: Message) -> None:
    if message.from_user is None:
        return
    await _show_menu(message, await get_language(message.from_user.id))


@router.message(Command("language"))
async def language_handler(message: Message) -> None:
    if message.from_user is None:
        return

    language = await get_language(message.from_user.id)
    await message.answer(
        get_text(language, "choose_language"),
        reply_markup=language_inline_keyboard(),
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    if message.from_user is None:
        return

    language = await get_language(message.from_user.id)
    await message.answer(
        get_text(language, "help"),
        reply_markup=main_reply_keyboard(language),
    )


@router.message(F.text.in_(set(_BUTTON_TO_ACTION)))
async def reply_menu_handler(message: Message) -> None:
    if message.from_user is None or message.text is None:
        return

    language = await get_language(message.from_user.id)
    await _show_section(message, language, _BUTTON_TO_ACTION[message.text])


@router.callback_query(F.data.startswith("language:"))
async def language_callback_handler(callback: CallbackQuery) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return

    language = (callback.data or "").partition(":")[2]
    if language not in SUPPORTED_LANGUAGES:
        await callback.answer("Unsupported language", show_alert=True)
        return

    await set_language(callback.from_user.id, language)
    await callback.answer(get_text(language, "language_saved"))
    await callback.message.answer(
        get_text(language, "menu_title"),
        reply_markup=main_reply_keyboard(language),
    )
    await callback.message.answer(
        get_text(language, "menu_title"),
        reply_markup=main_inline_keyboard(language),
    )


@router.callback_query(F.data.startswith("menu:"))
async def inline_menu_handler(callback: CallbackQuery) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return

    language = await get_language(callback.from_user.id)
    action = (callback.data or "").partition(":")[2]
    await callback.answer()

    if action == "language":
        await callback.message.answer(
            get_text(language, "choose_language"),
            reply_markup=language_inline_keyboard(),
        )
        return

    if action == "home":
        await _show_menu(callback.message, language)
        return

    await _show_section(
        callback.message,
        language,
        action,
        user=callback.from_user,
    )
