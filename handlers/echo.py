from aiogram import F, Router
from aiogram.types import Message

router = Router(name="echo")


@router.message(F.text)
async def echo_handler(message: Message) -> None:
    """Example handler. Replace or remove it when building your bot."""
    if message.text:
        await message.answer(message.text)
