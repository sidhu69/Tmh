# Main menu handler and keyboard
from aiogram import types, Dispatcher
from utils.keyboards import main_menu_keyboard

async def menu_cmd(message: types.Message):
    await message.reply("Main Menu:", reply_markup=main_menu_keyboard())


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(menu_cmd, commands=["menu"])
    # Option-based handlers can be routed in other modules (e.g. games, wallet)