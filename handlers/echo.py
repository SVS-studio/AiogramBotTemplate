from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from services.i18n import get_text
from services.user_preferences import get_language

router = Router(name="echo")


@router.message(Command("ping"))
async def ping_handler(message: Message) -> None:
    if message.from_user is None:
        return
    language = await get_language(message.from_user.id)
    await message.answer(get_text(language, "ping"))


@router.message(F.text)
async def echo_handler(message: Message) -> None:
    """Fallback example: echo text that was not handled by another router."""
    if message.text:
        await message.answer(message.text)
