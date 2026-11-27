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
        "help": "📖 <b>Yordam</b>\n/start — botni ishga tushirish\n/menu — asosiy menyu\n/settings — sozlamalar\n/language — tilni o‘zgartirish\n/referral — taklif havolasi va statistika\n/help — yordam\n/ping — bot holatini tekshirish\n/link — platforma hisobini bog‘lash\n/profile — IELTS profilingiz\n/verix — VERIX AI",
        "menu_title": "🏠 <b>Asosiy menyu</b>\nKerakli bo‘limni tanlang:",
        "features_title": "🧩 <b>Imkoniyatlar</b>\n\n• Reply Keyboard orqali tezkor navigatsiya\n• Inline Keyboard orqali bo‘limlarni boshqarish\n• O‘zbek, ingliz va rus tillari\n• Referral tracking va statistika\n• Foydalanuvchi sozlamalarini SQLite'da saqlash",
        "settings_title": "⚙️ <b>Sozlamalar</b>\nTil: {language}\nBildirishnomalar: {notification_status}\n\nTugmalar orqali sozlamalarni o‘zgartiring.",
        "choose_language": "🌐 <b>Tilni tanlang</b>",
        "language_saved": "✅ Til O‘zbekcha qilib o‘rnatildi.",
        "about": "ℹ️ <b>Aiogram Bot Template</b>\nSVS tomonidan tayyorlangan, aiogram 3.17 asosidagi ko‘p tilli starter loyiha.",
        "profile": "👤 <b>Profil</b>\nIsm: {name}\nTelegram ID: <code>{user_id}</code>\nUsername: {username}\nTil: {language}\nTaklif qilganlaringiz: {referral_count}",
        "ping": "🏓 Pong! Bot ishlayapti.",
        "back": "⬅️ Orqaga",
        "home": "🏠 Bosh menyu",
        "btn_features": "🧩 Imkoniyatlar",
        "btn_settings": "⚙️ Sozlamalar",
        "btn_profile": "👤 Profil",
        "btn_referrals": "👥 Referallar",
        "btn_about": "ℹ️ Loyiha haqida",
        "btn_language": "🌐 Tilni o‘zgartirish",
        "notifications_on": "🔔 Bildirishnomalar: YONIQ",
        "notifications_off": "🔕 Bildirishnomalar: O‘CHIQ",
        "status_on": "Yoniq",
        "status_off": "O‘chiq",
        "notifications_enabled": "Bildirishnomalar yoqildi.",
        "notifications_disabled": "Bildirishnomalar o‘chirildi.",
        "referral_info": "👥 <b>Referral dasturi</b>\n\nDo‘stlaringizni botga taklif qiling. Ular sizning havolangiz orqali birinchi marta /start qilganda hisobingizga qo‘shiladi.\n\n👤 Taklif qilgan foydalanuvchilar: <b>{count}</b>\n\n🔗 Sizning havolangiz:\n<code>{link}</code>",
        "share_referral": "📤 Havolani ulashish",
        "share_referral_text": "Ushbu Telegram botni sinab ko‘ring!",
        "referral_welcome": "🎉 Siz taklif havolasi orqali keldingiz. Taklif muvaffaqiyatli qayd etildi!",
        "link_help": "🔗 <b>IELTS Prep AI hisobini bog‘lash</b>\nPlatformada profilingizni oching → Connect Telegram tugmasini bosing → hosil bo‘lgan havolani oching.\n\nHisob bog‘langandan keyin bu botda VERIX va profilingiz ishlaydi.",
        "link_success": "✅ Telegram hisobingiz IELTS Prep AI profilingizga muvaffaqiyatli bog‘landi. Endi VERIX va /profile dan foydalanishingiz mumkin.",
        "link_failed": "❌ Bog‘lash havolasi yaroqsiz, muddati tugagan yoki allaqachon ishlatilgan. Platformadan yangi havola yarating.",
        "account_not_linked": "🔒 Telegram hisobingiz IELTS Prep AI bilan bog‘lanmagan. Platformadagi Profile → Connect Telegram orqali hisobingizni ulang.",
        "platform_error": "⚠️ IELTS Prep AI serveriga ulanib bo‘lmadi. Birozdan keyin qayta urinib ko‘ring.",
        "profile_summary": "👤 <b>IELTS Prep AI profilingiz</b>\nIsm: {first_name}\nEmail: {email}\nReja: {plan}\nDaraja: {level}\nMaqsad: {target}\nOverall: {overall}\nListening: {listening}\nReading: {reading}\nWriting: {writing}\nSpeaking: {speaking}\nStreak: {streak}\nTugallangan testlar: {tests}",
        "verix_prompt": "VERIXga savolingizni yuboring: /verix How can I improve my IELTS Writing Task 2?",
        "verix_too_long": "Xabar juda uzun. Iltimos, 4000 belgidan qisqa xabar yuboring.",
        "unknown": "Bu buyruqni tushunmadim. Menyudan foydalaning yoki /help yuboring.",
    },
    "en": {
        "welcome": "Hello, {name}! 👋\n\nThe bot is ready. Use the menu below to navigate.",
        "help": "📖 <b>Help</b>\n/start — start the bot\n/menu — open the main menu\n/settings — open settings\n/language — change language\n/referral — referral link and stats\n/help — show help\n/ping — check bot status\n/link — link your platform account\n/profile — view your IELTS profile\n/verix — chat with VERIX AI",
        "menu_title": "🏠 <b>Main menu</b>\nChoose a section:",
        "features_title": "🧩 <b>Features</b>\n\n• Reply Keyboard navigation\n• Inline Keyboard controls\n• Uzbek, English, and Russian languages\n• Referral tracking and statistics\n• User preferences stored in SQLite",
        "settings_title": "⚙️ <b>Settings</b>\nLanguage: {language}\nNotifications: {notification_status}\n\nUse the buttons to update your preferences.",
        "choose_language": "🌐 <b>Choose a language</b>",
        "language_saved": "✅ Language set to English.",
        "about": "ℹ️ <b>Aiogram Bot Template</b>\nA multilingual starter project built with aiogram 3.17 by SVS.",
        "profile": "👤 <b>Profile</b>\nName: {name}\nTelegram ID: <code>{user_id}</code>\nUsername: {username}\nLanguage: {language}\nInvited users: {referral_count}",
        "ping": "🏓 Pong! The bot is running.",
        "back": "⬅️ Back",
        "home": "🏠 Main menu",
        "btn_features": "🧩 Features",
        "btn_settings": "⚙️ Settings",
        "btn_profile": "👤 Profile",
        "btn_referrals": "👥 Referrals",
        "btn_about": "ℹ️ About",
        "btn_language": "🌐 Change language",
        "notifications_on": "🔔 Notifications: ON",
        "notifications_off": "🔕 Notifications: OFF",
        "status_on": "On",
        "status_off": "Off",
        "notifications_enabled": "Notifications enabled.",
        "notifications_disabled": "Notifications disabled.",
        "referral_info": "👥 <b>Referral program</b>\n\nInvite friends to this bot. They are counted once when they open your link and start the bot for the first time.\n\n👤 Invited users: <b>{count}</b>\n\n🔗 Your referral link:\n<code>{link}</code>",
        "share_referral": "📤 Share referral link",
        "share_referral_text": "Try this Telegram bot!",
        "referral_welcome": "🎉 You joined through a referral link. The referral has been recorded!",
        "link_help": "🔗 <b>Link your IELTS Prep AI account</b>\nOpen your profile on the platform → choose Connect Telegram → open the generated link.\n\nAfter linking, VERIX and your platform profile will be available here.",
        "link_success": "✅ Your Telegram account is now linked to your IELTS Prep AI profile. Use VERIX or /profile.",
        "link_failed": "❌ This link is invalid, expired, or already used. Generate a new link from the platform.",
        "account_not_linked": "🔒 Your Telegram account is not linked to IELTS Prep AI. Open Profile → Connect Telegram on the platform first.",
        "platform_error": "⚠️ Could not reach the IELTS Prep AI server. Please try again shortly.",
        "profile_summary": "👤 <b>Your IELTS Prep AI profile</b>\nName: {first_name}\nEmail: {email}\nPlan: {plan}\nLevel: {level}\nTarget: {target}\nOverall: {overall}\nListening: {listening}\nReading: {reading}\nWriting: {writing}\nSpeaking: {speaking}\nStreak: {streak}\nCompleted tests: {tests}",
        "verix_prompt": "Send a question to VERIX: /verix How can I improve my IELTS Writing Task 2?",
        "verix_too_long": "Your message is too long. Please keep it under 4000 characters.",
        "unknown": "I didn't understand that. Use the menu or send /help.",
    },
    "ru": {
        "welcome": "Здравствуйте, {name}! 👋\n\nБот готов к работе. Используйте меню ниже.",
        "help": "📖 <b>Помощь</b>\n/start — запустить бота\n/menu — главное меню\n/settings — настройки\n/language — изменить язык\n/referral — реферальная ссылка и статистика\n/help — помощь\n/ping — проверить работу бота\n/link — связать аккаунт платформы\n/profile — IELTS-профиль\n/verix — чат с VERIX AI",
        "menu_title": "🏠 <b>Главное меню</b>\nВыберите раздел:",
        "features_title": "🧩 <b>Возможности</b>\n\n• Навигация через Reply Keyboard\n• Управление через Inline Keyboard\n• Узбекский, английский и русский языки\n• Реферальная система и статистика\n• Сохранение настроек в SQLite",
        "settings_title": "⚙️ <b>Настройки</b>\nЯзык: {language}\nУведомления: {notification_status}\n\nИзмените настройки с помощью кнопок.",
        "choose_language": "🌐 <b>Выберите язык</b>",
        "language_saved": "✅ Язык установлен: Русский.",
        "about": "ℹ️ <b>Aiogram Bot Template</b>\nМногоязычный стартовый проект на aiogram 3.17 от SVS.",
        "profile": "👤 <b>Профиль</b>\nИмя: {name}\nTelegram ID: <code>{user_id}</code>\nUsername: {username}\nЯзык: {language}\nПриглашённые пользователи: {referral_count}",
        "ping": "🏓 Pong! Бот работает.",
        "back": "⬅️ Назад",
        "home": "🏠 Главное меню",
        "btn_features": "🧩 Возможности",
        "btn_settings": "⚙️ Настройки",
        "btn_profile": "👤 Профиль",
        "btn_referrals": "👥 Рефералы",
        "btn_about": "ℹ️ О проекте",
        "btn_language": "🌐 Изменить язык",
        "notifications_on": "🔔 Уведомления: ВКЛ",
        "notifications_off": "🔕 Уведомления: ВЫКЛ",
        "status_on": "Включены",
        "status_off": "Выключены",
        "notifications_enabled": "Уведомления включены.",
        "notifications_disabled": "Уведомления выключены.",
        "referral_info": "👥 <b>Реферальная программа</b>\n\nПриглашайте друзей в бота. Они будут засчитаны один раз, когда впервые запустят бота по вашей ссылке.\n\n👤 Приглашено пользователей: <b>{count}</b>\n\n🔗 Ваша ссылка:\n<code>{link}</code>",
        "share_referral": "📤 Поделиться ссылкой",
        "share_referral_text": "Попробуйте этого Telegram-бота!",
        "referral_welcome": "🎉 Вы перешли по реферальной ссылке. Приглашение засчитано!",
        "link_help": "🔗 <b>Связать аккаунт IELTS Prep AI</b>\nОткройте профиль на платформе → нажмите Connect Telegram → перейдите по созданной ссылке.\n\nПосле привязки здесь будут доступны VERIX и ваш профиль.",
        "link_success": "✅ Ваш Telegram успешно связан с профилем IELTS Prep AI. Используйте VERIX или /profile.",
        "link_failed": "❌ Ссылка недействительна, истекла или уже использована. Создайте новую ссылку на платформе.",
        "account_not_linked": "🔒 Telegram не связан с IELTS Prep AI. Сначала откройте Profile → Connect Telegram на платформе.",
        "platform_error": "⚠️ Не удалось подключиться к серверу IELTS Prep AI. Попробуйте позже.",
        "profile_summary": "👤 <b>Ваш профиль IELTS Prep AI</b>\nИмя: {first_name}\nEmail: {email}\nПлан: {plan}\nУровень: {level}\nЦель: {target}\nOverall: {overall}\nListening: {listening}\nReading: {reading}\nWriting: {writing}\nSpeaking: {speaking}\nStreak: {streak}\nЗавершённые тесты: {tests}",
        "verix_prompt": "Отправьте вопрос VERIX: /verix How can I improve my IELTS Writing Task 2?",
        "verix_too_long": "Сообщение слишком длинное. Ограничьте его 4000 символами.",
        "unknown": "Не удалось распознать команду. Используйте меню или отправьте /help.",
    },
}


def get_text(locale: str, key: str, **kwargs) -> str:
    """
    Return translated text with formatted placeholders.

    `locale` is the selected translation language.
    `language` and `language_name` are supported as translation placeholders.
    """

    if "language_name" in kwargs:
        kwargs.setdefault("language", kwargs["language_name"])

    if locale not in TEXTS:
        locale = "en"

    if key not in TEXTS[locale]:
        raise KeyError(
            f"Translation key '{key}' not found for language '{locale}'"
        )

    template = TEXTS[locale][key]

    try:
        return template.format(**kwargs) if kwargs else template
    except KeyError as error:
        raise KeyError(
            f"Missing placeholder {error} in translation "
            f"'{key}' for language '{locale}'"
        ) from error
