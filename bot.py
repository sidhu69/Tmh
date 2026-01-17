#!/usr/bin/env python3
# Entry point for the bot
import asyncio
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import db as db_module
from database import models
from handlers import start as start_h
from handlers import menu as menu_h
from handlers import wallet as wallet_h
from handlers import deposit as deposit_h
from handlers import withdraw as withdraw_h
from handlers import games as games_h

if not BOT_TOKEN:
    raise RuntimeError("Bot token not set. Set BOT_TOKEN environment variable.")

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(dp: Dispatcher):
    # Initialize database connection and create tables
    await db_module.init_db()
    await models.init_db()
    # register handlers
    start_h.register_handlers(dp)
    menu_h.register_handlers(dp)
    wallet_h.register_handlers(dp)
    deposit_h.register_handlers(dp)
    withdraw_h.register_handlers(dp)
    games_h.register_handlers(dp)
    print("Bot started. Connected to DB and registered handlers.")


async def on_shutdown(dp: Dispatcher):
    await bot.close()
    await db_module.shutdown_db()
    print("Shutting down.")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)