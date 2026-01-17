# Games menu and entry points
from aiogram import types, Dispatcher
from utils.keyboards import games_menu_keyboard
from games.mines.session import MinesSessionManager

async def games_cmd(message: types.Message):
    await message.reply("Games menu:", reply_markup=games_menu_keyboard())

async def start_mines(message: types.Message):
    # Start a Mines session and show UI
    manager = MinesSessionManager()
    session = await manager.create_session(message.from_user.id)
    await message.reply("Mines game started! Use in-chat buttons to open tiles.", reply_markup=session.render_keyboard())

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(games_cmd, commands=["games"])
    # text trigger example
    dp.register_message_handler(start_mines, lambda m: m.text and m.text.strip().lower() == "🎮 games")