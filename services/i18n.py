from __future__ import annotations

from typing import Final

DEFAULT_LANGUAGE: Final = "uz"
SUPPORTED_LANGUAGES: Final = ("uz", "en", "ru")

LANGUAGE_NAMES: Final = {
    "uz": "🇺🇿 O‘zbekcha",
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
}

TEXTS: Final[dict[str, dict[str, str]]] = {
    "uz": {
        "welcome": "Assalomu alaykum, {name}! 👋\n\nBot ishga tayyor. Quyidagi menyudan foydalaning.",
        "help": "📖 <b>Yordam</b>\n/start — botni ishga tushirish\n/menu — asosiy menyu\n/language — tilni o‘zgartirish\n/help — yordam\n/ping — bot holatini tekshirish",
        "menu_title": "🏠 <b>Asosiy menyu</b>\nKerakli bo‘limni tanlang:",
        "features_title": "🧩 <b>Imkoniyatlar</b>\n\n• Reply Keyboard orqali tezkor navigatsiya\n• Inline Keyboard orqali bo‘limlarni boshqarish\n• Uch tilli interfeys\n• Til tanlovini SQLite'da saqlash\n• /ping demo komandasi",
        "settings_title": "⚙️ <b>Sozlamalar</b>\nInterfeys tilini o‘zgartirishingiz mumkin.",
        "choose_language": "🌐 <b>Tilni tanlang</b>",
        "language_saved": "✅ Til O‘zbekcha qilib o‘rnatildi.",
        "about": "ℹ️ <b>Aiogram Bot Template</b>\nSVS tomonidan tayyorlangan, aiogram 3.17 asosidagi ko‘p tilli starter loyiha.",
        "profile": "👤 <b>Profil</b>\nIsm: {name}\nTelegram ID: <code>{user_id}</code>\nUsername: {username}\nTil: {language}",
        "ping": "🏓 Pong! Bot ishlayapti.",
        "back": "⬅️ Orqaga",
        "home": "🏠 Bosh menyu",
        "btn_features": "🧩 Imkoniyatlar",
        "btn_settings": "⚙️ Sozlamalar",
        "btn_profile": "👤 Profil",
        "btn_about": "ℹ️ Loyiha haqida",
        "btn_language": "🌐 Tilni o‘zgartirish",
        "unknown": "Bu buyruqni tushunmadim. Menyudan foydalaning yoki /help yuboring.",
    },
    "en": {
        "welcome": "Hello, {name}! 👋\n\nThe bot is ready. Use the menu below to navigate.",
        "help": "📖 <b>Help</b>\n/start — start the bot\n/menu — open the main menu\n/language — change language\n/help — show help\n/ping — check bot status",
        "menu_title": "🏠 <b>Main menu</b>\nChoose a section:",
        "features_title": "🧩 <b>Features</b>\n\n• Quick navigation with Reply Keyboard\n• Section controls with Inline Keyboard\n• Three interface languages\n• Language preference persisted in SQLite\n• /ping demo command",
        "settings_title": "⚙️ <b>Settings</b>\nYou can change the interface language here.",
        "choose_language": "🌐 <b>Choose a language</b>",
        "language_saved": "✅ Language set to English.",
        "about": "ℹ️ <b>Aiogram Bot Template</b>\nA multilingual starter project built with aiogram 3.17 by SVS.",
        "profile": "👤 <b>Profile</b>\nName: {name}\nTelegram ID: <code>{user_id}</code>\nUsername: {username}\nLanguage: {language}",
        "ping": "🏓 Pong! The bot is running.",
        "back": "⬅️ Back",
        "home": "🏠 Main menu",
        "btn_features": "🧩 Features",
        "btn_settings": "⚙️ Settings",
        "btn_profile": "👤 Profile",
        "btn_about": "ℹ️ About",
        "btn_language": "🌐 Change language",
        "unknown": "I didn't understand that. Use the menu or send /help.",
    },
    "ru": {
        "welcome": "Здравствуйте, {name}! 👋\n\nБот готов к работе. Используйте меню ниже.",
        "help": "📖 <b>Помощь</b>\n/start — запустить бота\n/menu — главное меню\n/language — изменить язык\n/help — помощь\n/ping — проверить работу бота",
        "menu_title": "🏠 <b>Главное меню</b>\nВыберите раздел:",
        "features_title": "🧩 <b>Возможности</b>\n\n• Быстрая навигация через Reply Keyboard\n• Управление разделами через Inline Keyboard\n• Три языка интерфейса\n• Сохранение языка в SQLite\n• Демокоманда /ping",
        "settings_title": "⚙️ <b>Настройки</b>\nЗдесь можно изменить язык интерфейса.",
        "choose_language": "🌐 <b>Выберите язык</b>",
        "language_saved": "✅ Язык установлен: Русский.",
        "about": "ℹ️ <b>Aiogram Bot Template</b>\nМногоязычный стартовый проект на aiogram 3.17 от SVS.",
        "profile": "👤 <b>Профиль</b>\nИмя: {name}\nTelegram ID: <code>{user_id}</code>\nUsername: {username}\nЯзык: {language}",
        "ping": "🏓 Pong! Бот работает.",
        "back": "⬅️ Назад",
        "home": "🏠 Главное меню",
        "btn_features": "🧩 Возможности",
        "btn_settings": "⚙️ Настройки",
        "btn_profile": "👤 Профиль",
        "btn_about": "ℹ️ О проекте",
        "btn_language": "🌐 Изменить язык",
        "unknown": "Не удалось распознать команду. Используйте меню или отправьте /help.",
    },
}


def get_text(language: str, key: str, **kwargs: str) -> str:
    """Return a translated string, falling back to Uzbek for unknown locales."""
    locale = language if language in TEXTS else DEFAULT_LANGUAGE
    return TEXTS[locale][key].format(**kwargs) if kwargs else TEXTS[locale][key]
