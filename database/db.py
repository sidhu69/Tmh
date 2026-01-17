# Async SQLite connection helper using aiosqlite
import aiosqlite
from typing import Optional
from config import DB_PATH

_db: Optional[aiosqlite.Connection] = None


async def init_db():
    global _db
    if _db is None:
        _db = await aiosqlite.connect(DB_PATH, check_same_thread=False)
        _db.row_factory = aiosqlite.Row
        # Enable foreign keys
        await _db.execute("PRAGMA foreign_keys = ON;")
        await _db.commit()


def get_db():
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db


async def shutdown_db():
    global _db
    if _db:
        await _db.close()
        _db = None