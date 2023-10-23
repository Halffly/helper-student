import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.routers import route

load_dotenv()

logging.basicConfig(level=logging.getLevelName(os.getenv("SYSTEM_LOG_LEVEL")))


bot = Bot(os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(route)

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
