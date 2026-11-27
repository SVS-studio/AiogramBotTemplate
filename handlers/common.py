from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

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


async def _show_menu(message: Message, language: str, *, greeting: str | None = None) -> None:
    await message.answer(
        greeting or get_text(language, "menu_title"),
        reply_markup=main_reply_keyboard(language),
    )
    await message.answer(
        get_text(language, "menu_title"),
        reply_markup=main_inline_keyboard(language),
    )


async def _show_section(message: Message, language: str, section: str) -> None:
    if section == "features":
        text = get_text(language, "features_title")
        keyboard = back_home_inline_keyboard(language)
    elif section == "settings":
        text = get_text(language, "settings_title")
        keyboard = settings_inline_keyboard(language)
    elif section == "about":
        text = get_text(language, "about")
        keyboard = back_home_inline_keyboard(language)
    else:
        user = message.from_user
        if user is None:
            return
        text = get_text(
            language,
            "profile",
            name=user.full_name,
            user_id=str(user.id),
            username=f"@{user.username}" if user.username else "—",
            language=LANGUAGE_NAMES[language],
        )
        keyboard = back_home_inline_keyboard(language)
    await message.answer(text, reply_markup=keyboard)


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    if message.from_user is None:
        return
    language = await get_language(message.from_user.id)
    greeting = get_text(
        language,
        "welcome",
        name=message.from_user.first_name or "there",
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
    language = await get_language(message.from_user.id)
    await _show_menu(message, language)


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
    action = _BUTTON_TO_ACTION[message.text]
    await _show_section(message, language, action)


@router.callback_query(F.data.startswith("language:"))
async def language_callback_handler(callback: CallbackQuery) -> None:
    if callback.from_user is None or callback.message is None:
        await callback.answer()
        return

    language = callback.data.split(":", maxsplit=1)[1]
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
    if callback.from_user is None or callback.message is None:
        await callback.answer()
        return

    language = await get_language(callback.from_user.id)
    action = callback.data.split(":", maxsplit=1)[1]
    await callback.answer()

    if action == "language":
        await callback.message.answer(
            get_text(language, "choose_language"),
            reply_markup=language_inline_keyboard(),
        )
        return

    if action == "home":
        await callback.message.answer(
            get_text(language, "menu_title"),
            reply_markup=main_reply_keyboard(language),
        )
        await callback.message.answer(
            get_text(language, "menu_title"),
            reply_markup=main_inline_keyboard(language),
        )
        return

    if action in {"features", "settings", "profile", "about"}:
        await _show_section(callback.message, language, action)
