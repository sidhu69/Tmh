# Reply and Inline keyboards used across the bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🎮 Games"))
    kb.add(KeyboardButton("💰 Wallet"))
    kb.add(KeyboardButton("➕ Deposit"))
    kb.add(KeyboardButton("➖ Withdrawal"))
    kb.add(KeyboardButton("👥 Refer"))
    return kb

def games_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Mines"))
    kb.add(KeyboardButton("Back"))
    return kb