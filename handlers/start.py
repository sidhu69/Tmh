# Handles /start and registration flow using FSM
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.db import get_db
from utils import security
import datetime

# States for registration
class RegisterStates(StatesGroup):
    waiting_password = State()
    waiting_password_confirm = State()


async def start_cmd(message: types.Message, state: FSMContext):
    db = get_db()
    tg_id = message.from_user.id
    async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (tg_id,)) as cur:
        row = await cur.fetchone()
    if row:
        # Already registered
        await message.reply("Welcome back! Use the menu below.")
        return
    await message.reply(
        "Welcome! You are not registered yet.\nPlease send me a password to secure your account (do not share it)."
    )
    await state.set_state(RegisterStates.waiting_password.state)


async def receive_password(message: types.Message, state: FSMContext):
    pwd = message.text.strip()
    if len(pwd) < 6:
        await message.reply("Password must be at least 6 characters. Try again.")
        return
    await state.update_data(password=pwd)
    await message.reply("Please re-enter your password to confirm.")
    await state.set_state(RegisterStates.waiting_password_confirm.state)


async def confirm_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    pwd = data.get("password")
    if message.text.strip() != pwd:
        await message.reply("Passwords did not match. Please restart /start to try again.")
        await state.finish()
        return
    # Create user
    pwd_hash = security.hash_password(pwd)
    db = get_db()
    now = datetime.datetime.utcnow().isoformat()
    await db.execute(
        "INSERT INTO users (telegram_id, username, password_hash, balance, created_at) VALUES (?, ?, ?, ?, ?)",
        (message.from_user.id, message.from_user.username or "", pwd_hash, 0, now),
    )
    await db.commit()
    await message.reply("Registration complete! Use the menu to start playing.")
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=["start"], state="*")
    dp.register_message_handler(receive_password, state=RegisterStates.waiting_password)
    dp.register_message_handler(confirm_password, state=RegisterStates.waiting_password_confirm)