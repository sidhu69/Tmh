# Mines game engine: generate mines, compute payouts
import random
from typing import List, Set, Tuple

GridPos = Tuple[int, int]  # (row, col) 0-based


def generate_mines(grid_size: int = 5, mines_count: int = 5) -> Set[GridPos]:
    """
    Server-side random mine placement.
    """
    coords = [(r, c) for r in range(grid_size) for c in range(grid_size)]
    chosen = set(random.sample(coords, mines_count))
    return chosen


def compute_multiplier(opened_safe: int, grid_size: int = 5, mines_count: int = 5) -> float:
    """
    Example multiplier progression. This is deterministic calculation but can be updated.
    Returns multiplier for current cashout if player has opened `opened_safe` safe tiles.
    We store amounts in paise (integers) in DB; multiplier is float.
    """
    total_tiles = grid_size * grid_size
    safe_tiles = total_tiles - mines_count
    # Naive risk-based multiplier curve:
    # base odds = safe_tiles / total_tiles
    # increase multiplier with each safe opened
    if opened_safe <= 0:
        return 1.0
    # simple curve: 1 + (opened_safe * factor)
    factor = 0.25 + (safe_tiles / total_tiles) * 0.75
    multiplier = 1.0 + opened_safe * factor
    return round(multiplier, 2)