from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from data.config import (
    get_admin_ids,
    get_bot_token,
    get_log_level,
    load_config,
    should_drop_pending_updates,
)
from handlers import setup_routers
from services.user_preferences import initialize_preferences


COMMANDS = {
    "uz": [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="menu", description="Asosiy menyu"),
        BotCommand(command="settings", description="Sozlamalar"),
        BotCommand(command="language", description="Tilni o‘zgartirish"),
        BotCommand(command="referral", description="Taklif havolasi"),
        BotCommand(command="help", description="Yordam"),
        BotCommand(command="ping", description="Bot holatini tekshirish"),
        BotCommand(command="link", description="IELTS Prep AI hisobini bog‘lash"),
        BotCommand(command="profile", description="IELTS profilingiz va natijalar"),
        BotCommand(command="verix", description="VERIX AI bilan suhbat"),
    ],
    "en": [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="menu", description="Open main menu"),
        BotCommand(command="settings", description="User settings"),
        BotCommand(command="language", description="Change language"),
        BotCommand(command="referral", description="Referral link and stats"),
        BotCommand(command="help", description="Show help"),
        BotCommand(command="ping", description="Check bot status"),
        BotCommand(command="link", description="Link your IELTS Prep AI account"),
        BotCommand(command="profile", description="View your IELTS profile and scores"),
        BotCommand(command="verix", description="Chat with VERIX AI"),
    ],
    "ru": [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="menu", description="Главное меню"),
        BotCommand(command="settings", description="Настройки"),
        BotCommand(command="language", description="Изменить язык"),
        BotCommand(command="referral", description="Реферальная ссылка"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="ping", description="Проверить работу бота"),
        BotCommand(command="link", description="Связать аккаунт IELTS Prep AI"),
        BotCommand(command="profile", description="Ваш IELTS-профиль и результаты"),
        BotCommand(command="verix", description="Чат с VERIX AI"),
    ],
}


async def configure_bot_commands(bot: Bot) -> None:
    for language_code, commands in COMMANDS.items():
        await bot.set_my_commands(commands, language_code=language_code)
    await bot.set_my_commands(COMMANDS["en"])


async def on_startup(bot: Bot, admin_ids: set[int]) -> None:
    logger = logging.getLogger(__name__)
    await configure_bot_commands(bot)
    logger.info("Bot started")
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, "Bot started successfully.")
        except Exception:
            logger.exception("Could not send startup notification to admin_id=%s", admin_id)


async def main() -> None:
    env = load_config()
    logging.basicConfig(
        level=get_log_level(env),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    await initialize_preferences()

    bot = Bot(
        token=get_bot_token(env),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(setup_routers())

    admin_ids = get_admin_ids(env)

    async def startup_handler(dispatcher: Dispatcher) -> None:
        await on_startup(bot=bot, admin_ids=admin_ids)

    dispatcher.startup.register(startup_handler)

    try:
        await bot.delete_webhook(drop_pending_updates=should_drop_pending_updates(env))
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.getLogger(__name__).info("Bot stopped")
