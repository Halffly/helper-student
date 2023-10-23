import logging

from aiogram.types import Message

from app.keyboards import get_menu

log = logging.getLogger("app.commands")


async def start(msg: Message):

    await msg.reply(
        "Добро пожаловать😊\nЯ буду помогать вам в рутиных задачах.\n\nАвтор бота @bit_founder",
        reply_markup=get_menu()
    )
