from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router(name="common")


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "Hello! The bot is running.\n\nSend any text message to see the example echo handler."
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "Available commands:\n"
        "/start — start the bot\n"
        "/help — show this message"
    )
