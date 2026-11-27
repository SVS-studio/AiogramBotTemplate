from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from services.i18n import LANGUAGE_NAMES, SUPPORTED_LANGUAGES, get_text


def main_reply_keyboard(language: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for key in ("btn_features", "btn_settings", "btn_profile", "btn_about"):
        builder.button(text=get_text(language, key))
    builder.adjust(2, 2)
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder=get_text(language, "menu_title").replace("<b>", "").replace("</b>", ""),
    )


def main_inline_keyboard(language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, callback in (
        ("btn_features", "menu:features"),
        ("btn_settings", "menu:settings"),
        ("btn_profile", "menu:profile"),
        ("btn_about", "menu:about"),
        ("btn_language", "menu:language"),
    ):
        builder.button(text=get_text(language, key), callback_data=callback)
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def language_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for language in SUPPORTED_LANGUAGES:
        builder.button(
            text=LANGUAGE_NAMES[language],
            callback_data=f"language:{language}",
        )
    builder.adjust(1)
    return builder.as_markup()


def back_home_inline_keyboard(language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(language, "back"), callback_data="menu:home")
    builder.adjust(1)
    return builder.as_markup()


def settings_inline_keyboard(language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=get_text(language, "btn_language"),
        callback_data="menu:language",
    )
    builder.button(text=get_text(language, "home"), callback_data="menu:home")
    builder.adjust(1)
    return builder.as_markup()
