# Bot and app configuration.
# IMPORTANT: Do not commit secrets. Use environment variables on Termux:
#   export BOT_TOKEN="your_token_here"
#   export UPI_ID="your_upi@bank"
import os
from typing import Final

BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN")  # Set in environment on Termux
UPI_ID: Final[str] = os.getenv("UPI_ID", "example@upi")  # Replace or set env var

# App limits
MIN_WITHDRAWAL = 110  # ₹
MAX_GRID_SIZE = 5

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "tmh.sqlite3")