# In-memory session manager with persistence into DB table gamesessions
import json
import datetime
from typing import Dict, Any, Optional
from database.db import get_db
from .engine import generate_mines, compute_multiplier
from .ui import grid_keyboard

class MinesSession:
    def __init__(self, telegram_id: int, session_id: int, grid_size: int = 5, mines_count: int = 5):
        self.telegram_id = telegram_id
        self.session_id = session_id
        self.grid_size = grid_size
        self.mines_count = mines_count
        self.mines = generate_mines(grid_size, mines_count)
        # 2D revealed map
        self.revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        self.opened_safe = 0
        self.bet_amount = 0  # paise
        self.state = "active"

    def open_tile(self, r: int, c: int) -> dict:
        if self.state != "active":
            return {"error": "session not active"}
        if (r, c) in self.mines:
            self.revealed[r][c] = True
            self.state = "lost"
            return {"result": "mine"}
        else:
            if not self.revealed[r][c]:
                self.revealed[r][c] = True
                self.opened_safe += 1
            multiplier = compute_multiplier(self.opened_safe, self.grid_size, self.mines_count)
            return {"result": "safe", "opened": self.opened_safe, "multiplier": multiplier}

    def cashout(self) -> dict:
        if self.state != "active":
            return {"error": "session not active"}
        self.state = "cashed_out"
        multiplier = compute_multiplier(self.opened_safe, self.grid_size, self.mines_count)
        winnings = int(self.bet_amount * multiplier)
        return {"winnings": winnings, "multiplier": multiplier}

    def render_keyboard(self):
        return grid_keyboard(self.grid_size, tuple(tuple(row) for row in self.revealed))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "telegram_id": self.telegram_id,
            "session_id": self.session_id,
            "grid_size": self.grid_size,
            "mines_count": self.mines_count,
            "mines": list(self.mines),
            "revealed": self.revealed,
            "opened_safe": self.opened_safe,
            "bet_amount": self.bet_amount,
            "state": self.state,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        obj = cls(d["telegram_id"], d["session_id"], d["grid_size"], d["mines_count"])
        obj.mines = set(tuple(x) for x in d.get("mines", []))
        obj.revealed = d.get("revealed", obj.revealed)
        obj.opened_safe = d.get("opened_safe", 0)
        obj.bet_amount = d.get("bet_amount", 0)
        obj.state = d.get("state", "active")
        return obj


class MinesSessionManager:
    _in_memory: Dict[int, MinesSession] = {}
    _id_counter = 1

    async def create_session(self, telegram_id: int, grid_size: int = 5, mines_count: int = 5) -> MinesSession:
        session_id = MinesSessionManager._id_counter
        MinesSessionManager._id_counter += 1
        session = MinesSession(telegram_id, session_id, grid_size, mines_count)
        MinesSessionManager._in_memory[session_id] = session
        # persist
        db = get_db()
        now = datetime.datetime.utcnow().isoformat()
        payload = json.dumps(session.to_dict())
        await db.execute("INSERT INTO gamesessions (telegram_id, game_name, state, payload, created_at) VALUES (?, ?, ?, ?, ?)",
                         (telegram_id, "mines", "active", payload, now))
        await db.commit()
        return session

    async def get_session(self, session_id: int) -> Optional[MinesSession]:
        return MinesSessionManager._in_memory.get(session_id)

    async def persist_session(self, session: MinesSession):
        db = get_db()
        payload = json.dumps(session.to_dict())
        await db.execute("UPDATE gamesessions SET state = ?, payload = ? WHERE id = ?", (session.state, payload, session.session_id))
        await db.commit()