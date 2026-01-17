```markdown
# mines-games-bot (TMH) — Telegram Mines Multi-Game Betting Bot

This repository is a modular, production-style scaffold for a Telegram-based multi-game betting bot designed to run on Termux (Android).

Goals:
- Python 3.10+ (Termux supported)
- aiogram Telegram bot
- SQLite (initial DB)
- Modular code structure (handlers, games, utils, database)
- Mines game implemented as the first game
- Secure password hashing and server-side money logic

Setup (Termux)
1. pkg update -y
2. pkg install python git -y
3. git clone <this-repo>
4. cd mines-games-bot
5. python3 -m pip install -r requirements.txt

Environment
- Set your bot token in Termux (do NOT commit to git):
  export BOT_TOKEN="8476511730:AAFGq0RHAptiPjRGWX8qG0zz5CriWrwZ4zQ"
- Optionally set UPI id:
  export UPI_ID="your-upi@bank"

Run
- python3 bot.py

Notes / Security
- Passwords are hashed using PBKDF2 (no plain text storage).
- All balance changes are performed server-side and logged in the transactions table.
- Deposit flows mark deposits as PENDING for manual admin approval.
- Withdrawals lock (deduct) the user's balance and mark request PENDING for admin processing.
- Do not expose the BOT_TOKEN in public repos. Use environment variables.
- This scaffold is intended to be extended (admin panel, more games, stronger RNG, audits).

Project Structure
See the repository tree in the prompt. Start by exploring `handlers/` and `games/mines/`.

Extending
- Add admin commands to approve deposits/withdrawals.
- Improve Mines engine with a provably fair RNG and better payout curve.
- Add persistent session storage and recovery logic.
```