# Deposit flow: ask amount -> send UPI info -> collect tx id and screenshot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.db import get_db
from config import UPI_ID
import datetime

class DepositStates(StatesGroup):
    waiting_amount = State()
    waiting_tx_and_screenshot = State()

async def deposit_cmd(message: types.Message):
    await message.reply("Enter deposit amount in rupees (e.g. 150).")
    await DepositStates.waiting_amount.set()

async def receive_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(float(message.text.strip()) * 100)  # store paise
    except Exception:
        await message.reply("Invalid amount. Enter a numeric value.")
        return
    if amount <= 0:
        await message.reply("Amount must be greater than 0.")
        return
    await state.update_data(amount=amount)
    await message.reply(
        f"Send the payment to UPI ID: {UPI_ID}\nAmount: ₹{amount/100:.2f}\nAfter payment, reply with transaction ID and upload the screenshot (as a photo)."
    )
    await DepositStates.waiting_tx_and_screenshot.set()

async def receive_tx_and_screenshot(message: types.Message, state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount")
    if not amount:
        await message.reply("Flow expired. Start again with /deposit")
        await state.finish()
        return
    tx_id = None
    file_id = None
    if message.text:
        tx_id = message.text.strip()
    if message.photo:
        # save the largest photo file_id
        file_id = message.photo[-1].file_id
    db = get_db()
    now = datetime.datetime.utcnow().isoformat()
    await db.execute(
        "INSERT INTO deposits (telegram_id, amount, transaction_id, screenshot_file_id, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (message.from_user.id, amount, tx_id or "", file_id or "", "pending", now),
    )
    await db.commit()
    await message.reply("Deposit submitted and marked PENDING. An admin will approve it shortly.")
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(deposit_cmd, commands=["deposit"])
    dp.register_message_handler(receive_amount, state=DepositStates.waiting_amount)
    dp.register_message_handler(receive_tx_and_screenshot, state=DepositStates.waiting_tx_and_screenshot, content_types=['text','photo'])