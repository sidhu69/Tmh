# Table creation for users, transactions, deposits, withdrawals, gamesessions
from database.db import get_db
import aiosqlite
import datetime

CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    username TEXT,
    password_hash TEXT NOT NULL,
    balance INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);
"""

CREATE_TRANSACTIONS = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    type TEXT NOT NULL, -- deposit / withdraw / bet / win
    amount INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TEXT NOT NULL
);
"""

CREATE_DEPOSITS = """
CREATE TABLE IF NOT EXISTS deposits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    transaction_id TEXT,
    screenshot_file_id TEXT,
    status TEXT DEFAULT 'pending',
    created_at TEXT NOT NULL
);
"""

CREATE_WITHDRAWALS = """
CREATE TABLE IF NOT EXISTS withdrawals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    upi_id TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TEXT NOT NULL
);
"""

CREATE_GAMESESSIONS = """
CREATE TABLE IF NOT EXISTS gamesessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    game_name TEXT NOT NULL,
    state TEXT NOT NULL,
    payload TEXT,
    created_at TEXT NOT NULL
);
"""


async def init_db():
    db = get_db()  # raises if not initialized
    async with db.execute("BEGIN"):
        await db.execute(CREATE_USERS)
        await db.execute(CREATE_TRANSACTIONS)
        await db.execute(CREATE_DEPOSITS)
        await db.execute(CREATE_WITHDRAWALS)
        await db.execute(CREATE_GAMESESSIONS)
        await db.commit()