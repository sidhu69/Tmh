# Common helpers for balance, formatting, and transactions
from database.db import get_db
import datetime

async def change_balance(telegram_id: int, delta_paise: int, reason: str = "adjust"):
    """
    Atomically change user balance and log transaction.
    delta_paise may be negative.
    """
    db = get_db()
    now = datetime.datetime.utcnow().isoformat()
    await db.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (delta_paise, telegram_id))
    await db.execute("INSERT INTO transactions (telegram_id, type, amount, status, created_at) VALUES (?, ?, ?, ?, ?)",
                     (telegram_id, reason, abs(delta_paise), "done" if delta_paise >= 0 else "pending", now))
    await db.commit()


def format_amount(paise: int) -> str:
    return f"₹{paise/100:.2f}"