from __future__ import annotations

from html import escape
from urllib.parse import quote

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, User

from keyboards.menus import (
    back_home_inline_keyboard,
    language_inline_keyboard,
    main_inline_keyboard,
    main_reply_keyboard,
    referral_inline_keyboard,
    settings_inline_keyboard,
)
from services.i18n import LANGUAGE_NAMES, SUPPORTED_LANGUAGES, get_text
from services.user_preferences import (
    get_settings,
    register_user,
    set_language,
    toggle_notifications,
)

router = Router(name="common")

_BUTTON_TO_ACTION = {
    get_text(language, key): action
    for language in SUPPORTED_LANGUAGES
    for key, action in (
        ("btn_features", "features"),
        ("btn_settings", "settings"),
        ("btn_profile", "profile"),
        ("btn_referrals", "referrals"),
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


async def _referral_data(user_id: int, bot_username: str) -> tuple[str, int]:
    settings = await get_settings(user_id)
    referral_url = f"https://t.me/{bot_username}?start=ref_{user_id}"
    return referral_url, settings["referral_count"]


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
        settings = await get_settings(user.id if user else message.from_user.id)
        text = get_text(
            language,
            "settings_title",
            language=LANGUAGE_NAMES[language],
            notification_status=get_text(
                language,
                "status_on" if settings["notifications_enabled"] else "status_off",
            ),
        )
        keyboard = settings_inline_keyboard(language, settings["notifications_enabled"])
    elif section == "about":
        text = get_text(language, "about")
        keyboard = back_home_inline_keyboard(language)
    elif section == "profile":
        profile_user = user or message.from_user
        if profile_user is None:
            return
        settings = await get_settings(profile_user.id)
        text = get_text(
            language,
            "profile",
            name=escape(profile_user.full_name),
            user_id=str(profile_user.id),
            username=escape(f"@{profile_user.username}" if profile_user.username else "—"),
            language=LANGUAGE_NAMES[language],
            referral_count=str(settings["referral_count"]),
        )
        keyboard = back_home_inline_keyboard(language)
    elif section == "referrals":
        referral_user = user or message.from_user
        if referral_user is None:
            return
        referral_url, count = await _referral_data(
            referral_user.id,
            (await message.bot.get_me()).username or "",
        )
        text = get_text(
            language,
            "referral_info",
            count=str(count),
            link=escape(referral_url),
        )
        keyboard = referral_inline_keyboard(language, quote(referral_url, safe=""))
    else:
        return

    await message.answer(text, reply_markup=keyboard)


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    if message.from_user is None:
        return

    referrer_id = None
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) == 2 and parts[1].startswith("ref_"):
        raw_referrer = parts[1][4:]
        if raw_referrer.isdigit():
            referrer_id = int(raw_referrer)

    is_new_user, referral_credited = await register_user(
        message.from_user.id,
        referrer_id,
    )
    settings = await get_settings(message.from_user.id)
    language = settings["language"]
    greeting = get_text(
        language,
        "welcome",
        name=escape(message.from_user.first_name or "there"),
    )
    if referral_credited:
        greeting += "\n\n" + get_text(language, "referral_welcome")
    await message.answer(greeting, reply_markup=main_reply_keyboard(language))
    await message.answer(
        get_text(language, "menu_title"),
        reply_markup=main_inline_keyboard(language),
    )


@router.message(Command("menu"))
async def menu_handler(message: Message) -> None:
    if message.from_user is None:
        return
    await _show_menu(message, (await get_settings(message.from_user.id))["language"])


@router.message(Command("language"))
async def language_handler(message: Message) -> None:
    if message.from_user is None:
        return
    language = (await get_settings(message.from_user.id))["language"]
    await message.answer(
        get_text(language, "choose_language"),
        reply_markup=language_inline_keyboard(),
    )


@router.message(Command("referral"))
async def referral_handler(message: Message) -> None:
    if message.from_user is None:
        return
    language = (await get_settings(message.from_user.id))["language"]
    await _show_section(message, language, "referrals")


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    if message.from_user is None:
        return
    language = (await get_settings(message.from_user.id))["language"]
    await message.answer(
        get_text(language, "help"),
        reply_markup=main_reply_keyboard(language),
    )


@router.message(F.text.in_(set(_BUTTON_TO_ACTION)))
async def reply_menu_handler(message: Message) -> None:
    if message.from_user is None or message.text is None:
        return
    settings = await get_settings(message.from_user.id)
    await _show_section(message, settings["language"], _BUTTON_TO_ACTION[message.text])


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


@router.callback_query(F.data == "settings:toggle_notifications")
async def toggle_notifications_handler(callback: CallbackQuery) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return

    enabled = await toggle_notifications(callback.from_user.id)
    settings = await get_settings(callback.from_user.id)
    language = settings["language"]
    await callback.answer(
        get_text(language, "notifications_enabled" if enabled else "notifications_disabled")
    )
    await callback.message.edit_text(
        get_text(
            language,
            "settings_title",
            language=LANGUAGE_NAMES[language],
            notification_status=get_text(
                language,
                "status_on" if enabled else "status_off",
            ),
        ),
        reply_markup=settings_inline_keyboard(language, enabled),
    )


@router.callback_query(F.data.startswith("menu:"))
async def inline_menu_handler(callback: CallbackQuery) -> None:
    if not isinstance(callback.message, Message):
        await callback.answer()
        return

    language = (await get_settings(callback.from_user.id))["language"]
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
