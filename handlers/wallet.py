# Shows wallet balance and transaction summary
from aiogram import types, Dispatcher
from database.db import get_db

async def wallet_handler(message: types.Message):
    tg_id = message.from_user.id
    db = get_db()
    async with db.execute("SELECT balance FROM users WHERE telegram_id = ?", (tg_id,)) as cur:
        row = await cur.fetchone()
    if not row:
        await message.reply("You are not registered. Send /start to register.")
        return
    balance = row["balance"]
    await message.reply(f"Your balance: ₹{balance/100:.2f}\nBalances are managed server-side.")


def register_handlers(dp: Dispatcher):
    # Simple keyword trigger
    dp.register_message_handler(wallet_handler, lambda m: m.text and m.text.strip().lower() == "💰 wallet")
    # also register a command
    dp.register_message_handler(wallet_handler, commands=["wallet"])