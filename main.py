from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import (
    get_admin_ids,
    get_bot_token,
    get_log_level,
    load_config,
    should_drop_pending_updates,
)
from handlers import setup_routers


async def on_startup(bot: Bot, admin_ids: set[int]) -> None:
    logging.getLogger(__name__).info("Bot started")
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, "Bot ishga tushdi.")
        except Exception:
            logging.getLogger(__name__).exception(
                "Could not send startup notification to admin_id=%s", admin_id
            )


async def main() -> None:
    env = load_config()
    logging.basicConfig(
        level=get_log_level(env),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    bot = Bot(
        token=get_bot_token(env),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(setup_routers())

    admin_ids = get_admin_ids(env)
    dispatcher.startup.register(
        lambda: on_startup(bot=bot, admin_ids=admin_ids)
    )

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
