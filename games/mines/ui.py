# UI helper for mines: inline keyboards and tile labels
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Tuple

def tile_button(row: int, col: int, label: str, callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=label, callback_data=callback_data)


def grid_keyboard(grid_size: int = 5, revealed: Tuple[Tuple[bool]] = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for r in range(grid_size):
        row_buttons = []
        for c in range(grid_size):
            label = "■"
            if revealed and revealed[r][c]:
                label = "▫"  # revealed safe tile
            cb = f"mines:open:{r}:{c}"
            row_buttons.append(tile_button(r, c, label, cb))
        kb.row(*row_buttons)
    # Add cashout button
    kb.add(InlineKeyboardButton(text="Cashout", callback_data="mines:cashout"))
    return kb