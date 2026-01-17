# Withdrawal flow: amount -> UPI -> create pending withdrawal and lock balance
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.db import get_db
from config import MIN_WITHDRAWAL
import datetime

class WithdrawStates(StatesGroup):
    waiting_amount = State()
    waiting_upi = State()

async def withdraw_cmd(message: types.Message):
    await message.reply(f"Enter withdrawal amount in rupees (minimum ₹{MIN_WITHDRAWAL}).")
    await WithdrawStates.waiting_amount.set()

async def receive_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(float(message.text.strip()) * 100)
    except Exception:
        await message.reply("Invalid amount. Enter a numeric value.")
        return
    if amount < MIN_WITHDRAWAL * 100:
        await message.reply(f"Minimum withdrawal is ₹{MIN_WITHDRAWAL}.")
        return
    db = get_db()
    async with db.execute("SELECT balance FROM users WHERE telegram_id = ?", (message.from_user.id,)) as cur:
        row = await cur.fetchone()
    if not row:
        await message.reply("You are not registered. Use /start.")
        await state.finish()
        return
    balance = row["balance"]
    if amount > balance:
        await message.reply("Insufficient balance.")
        await state.finish()
        return
    # Check pending withdrawals
    async with db.execute("SELECT COUNT(*) as cnt FROM withdrawals WHERE telegram_id = ? AND status = 'pending'", (message.from_user.id,)) as cur:
        r = await cur.fetchone()
    if r["cnt"] > 0:
        await message.reply("You already have a pending withdrawal. Wait until it is processed.")
        await state.finish()
        return
    await state.update_data(amount=amount)
    await message.reply("Enter your UPI ID to receive the funds.")
    await WithdrawStates.waiting_upi.set()

async def receive_upi(message: types.Message, state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount")
    upi = message.text.strip()
    db = get_db()
    now = datetime.datetime.utcnow().isoformat()
    # Create withdrawal and deduct (lock) balance by updating users.balance
    await db.execute("INSERT INTO withdrawals (telegram_id, amount, upi_id, status, created_at) VALUES (?, ?, ?, ?, ?)",
                     (message.from_user.id, amount, upi, "pending", now))
    # Deduct balance (locked)
    await db.execute("UPDATE users SET balance = balance - ? WHERE telegram_id = ?", (amount, message.from_user.id))
    await db.execute("INSERT INTO transactions (telegram_id, type, amount, status, created_at) VALUES (?, ?, ?, ?, ?)",
                     (message.from_user.id, "withdraw", amount, "pending", now))
    await db.commit()
    await message.reply("Withdrawal requested and balance deducted (locked). An admin will process this request.")
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(withdraw_cmd, commands=["withdraw"])
    dp.register_message_handler(receive_amount, state=WithdrawStates.waiting_amount)
    dp.register_message_handler(receive_upi, state=WithdrawStates.waiting_upi)