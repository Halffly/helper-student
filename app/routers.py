from aiogram import Router, F
from aiogram.filters import CommandStart

from app.commands import start
from app.text_answer import mathematica, all_text

route = Router(name=__name__)


def register_message(f, *flt, state=None):
    return route.message(*flt)(f)


register_message(start, CommandStart())
register_message(mathematica, F.text == 'Математика')
register_message(all_text)
