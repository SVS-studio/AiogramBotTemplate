
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
    referral_inline_keyboard,
    settings_inline_keyboard,
)
from services.i18n import (
    LANGUAGE_NAMES,
    SUPPORTED_LANGUAGES,
    get_text,
)
from services.platform_api import PlatformAPIError, get_platform_profile, verify_telegram_link
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

VALID_SECTIONS = {
    "features",
    "settings",
    "profile",
    "referrals",
    "about",
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


async def _referral_data(
    user_id: int,
    bot_username: str,
) -> tuple[str, int]:
    settings = await get_settings(user_id)

    referral_url = (
        f"https://t.me/{bot_username}?start=ref_{user_id}"
    )

    return referral_url, settings["referral_count"]


async def _show_section(
    message: Message,
    language: str,
    section: str,
    *,
    user: User | None = None,
) -> None:

    if section not in VALID_SECTIONS:
        return

    current_user = user or message.from_user

    if current_user is None:
        return

    if section == "features":
        text = get_text(language, "features_title")
        keyboard = back_home_inline_keyboard(language)

    elif section == "settings":
        settings = await get_settings(current_user.id)

        notification_status = get_text(
            language,
            (
                "status_on"
                if settings["notifications_enabled"]
                else "status_off"
            ),
        )

        text = get_text(
            language,
            "settings_title",
            language_name=LANGUAGE_NAMES[language],
            notification_status=notification_status,
        )

        keyboard = settings_inline_keyboard(
            language,
            settings["notifications_enabled"],
        )

    elif section == "about":
        text = get_text(language, "about")
        keyboard = back_home_inline_keyboard(language)

    elif section == "profile":
        try:
            platform_profile = await get_platform_profile(current_user.id)
            text = get_text(
                language,
                "profile_summary",
                first_name=escape(str(platform_profile.get("first_name") or "—")),
                email=escape(str(platform_profile.get("email") or "—")),
                plan=escape(str(platform_profile.get("plan") or "—")),
                level=escape(str(platform_profile.get("english_level") or "—")),
                target=f"{platform_profile.get('target_band_score', 0):g}",
                overall=f"{platform_profile.get('overall_band_score', 0):g}",
                listening=f"{platform_profile.get('listening_score', 0):g}",
                reading=f"{platform_profile.get('reading_score', 0):g}",
                writing=f"{platform_profile.get('writing_score', 0):g}",
                speaking=f"{platform_profile.get('speaking_score', 0):g}",
                streak=str(platform_profile.get("user_streak", 0)),
                tests=str(platform_profile.get("test_completed", 0)),
            )
        except PlatformAPIError as exc:
            key = "account_not_linked" if exc.status_code == 404 else "platform_error"
            text = get_text(language, key)

        keyboard = back_home_inline_keyboard(language)

    elif section == "referrals":
        bot_info = await message.bot.get_me()

        if not bot_info.username:
            return

        referral_url, count = await _referral_data(
            current_user.id,
            bot_info.username,
        )

        text = get_text(
            language,
            "referral_info",
            count=str(count),
            link=escape(referral_url),
        )

        keyboard = referral_inline_keyboard(
            language,
            referral_url,
        )

    else:
        return

    await message.answer(
        text,
        reply_markup=keyboard,
    )


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    current_user = message.from_user
    if current_user is None:
        return

    parts = (message.text or "").split(maxsplit=1)
    payload = parts[1].strip() if len(parts) == 2 else ""
    referrer_id = None
    link_result = None
    link_error = False

    if payload.startswith("ref_"):
        raw_referrer = payload[4:]
        if raw_referrer.isdigit():
            referrer_id = int(raw_referrer)
    elif payload:
        try:
            link_result = await verify_telegram_link(current_user.id, payload)
        except PlatformAPIError:
            link_error = True

    _, referral_credited = await register_user(current_user.id, referrer_id)
    settings = await get_settings(current_user.id)
    language = settings["language"]

    if link_result and link_result.get("success"):
        greeting = get_text(language, "link_success")
    elif link_error:
        greeting = get_text(language, "link_failed")
    else:
        greeting = get_text(
            language,
            "welcome",
            name=escape(current_user.first_name or "there"),
        )

    if referral_credited:
        greeting += "\n\n" + get_text(language, "referral_welcome")

    await message.answer(
        greeting,
        reply_markup=main_reply_keyboard(language),
    )
    await message.answer(
        get_text(language, "menu_title"),
        reply_markup=main_inline_keyboard(language),
    )


@router.message(Command("menu"))
async def menu_handler(message: Message) -> None:
    if message.from_user is None:
        return

    settings = await get_settings(message.from_user.id)

    await _show_menu(
        message,
        settings["language"],
    )


@router.message(Command("settings"))
async def settings_handler(message: Message) -> None:
    if message.from_user is None:
        return

    settings = await get_settings(message.from_user.id)

    await _show_section(
        message,
        settings["language"],
        "settings",
    )


@router.message(Command("language"))
async def language_handler(message: Message) -> None:
    if message.from_user is None:
        return

    settings = await get_settings(message.from_user.id)
    language = settings["language"]

    await message.answer(
        get_text(language, "choose_language"),
        reply_markup=language_inline_keyboard(),
    )


@router.message(Command("referral"))
async def referral_handler(message: Message) -> None:
    if message.from_user is None:
        return

    settings = await get_settings(message.from_user.id)

    await _show_section(
        message,
        settings["language"],
        "referrals",
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    if message.from_user is None:
        return

    settings = await get_settings(message.from_user.id)
    language = settings["language"]

    await message.answer(
        get_text(language, "help"),
        reply_markup=main_reply_keyboard(language),
    )


@router.message(F.text.in_(set(_BUTTON_TO_ACTION)))
async def reply_menu_handler(message: Message) -> None:
    if message.from_user is None or message.text is None:
        return

    settings = await get_settings(message.from_user.id)

    action = _BUTTON_TO_ACTION[message.text]

    await _show_section(
        message,
        settings["language"],
        action,
    )


@router.callback_query(F.data.startswith("language:"))
async def language_callback_handler(
    callback: CallbackQuery,
) -> None:

    if not isinstance(callback.message, Message):
        await callback.answer()
        return

    language = (callback.data or "").partition(":")[2]

    if language not in SUPPORTED_LANGUAGES:
        await callback.answer(
            "Unsupported language",
            show_alert=True,
        )
        return

    await set_language(
        callback.from_user.id,
        language,
    )

    await callback.answer(
        get_text(language, "language_saved")
    )

    await _show_menu(
        callback.message,
        language,
    )


@router.callback_query(
    F.data == "settings:toggle_notifications"
)
async def toggle_notifications_handler(
    callback: CallbackQuery,
) -> None:

    if not isinstance(callback.message, Message):
        await callback.answer()
        return

    enabled = await toggle_notifications(
        callback.from_user.id
    )

    settings = await get_settings(
        callback.from_user.id
    )

    language = settings["language"]

    notification_status = get_text(
        language,
        "status_on" if enabled else "status_off",
    )

    await callback.answer(
        get_text(
            language,
            "notifications_enabled"
            if enabled
            else "notifications_disabled",
        )
    )

    await callback.message.edit_text(
        get_text(
            language,
            "settings_title",
            language_name=LANGUAGE_NAMES[language],
            notification_status=notification_status,
        ),
        reply_markup=settings_inline_keyboard(
            language,
            enabled,
        ),
    )


@router.callback_query(F.data.startswith("menu:"))
async def inline_menu_handler(
    callback: CallbackQuery,
) -> None:

    if not isinstance(callback.message, Message):
        await callback.answer()
        return

    settings = await get_settings(
        callback.from_user.id
    )

    language = settings["language"]

    action = (
        callback.data or ""
    ).partition(":")[2]

    await callback.answer()

    if action == "language":
        await callback.message.answer(
            get_text(language, "choose_language"),
            reply_markup=language_inline_keyboard(),
        )
        return

    if action == "home":
        await _show_menu(
            callback.message,
            language,
        )
        return

    if action not in VALID_SECTIONS:
        return

    await _show_section(
        callback.message,
        language,
        action,
        user=callback.from_user,
    )
