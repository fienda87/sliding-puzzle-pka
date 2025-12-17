from __future__ import annotations

from typing import Iterable, Literal

Board = list[list[int]]
Move = Literal["UP", "DOWN", "LEFT", "RIGHT"]

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 100
PADDING = 10
FPS = 60
SOLVER_DELAY_MS = 400

COLOR_BACKGROUND = (240, 240, 240)
COLOR_TILE = (52, 152, 219)
COLOR_BLANK = (192, 192, 192)
COLOR_TEXT = (255, 255, 255)
COLOR_BUTTON = (46, 204, 113)
COLOR_BUTTON_HOVER = (39, 174, 96)
COLOR_BUTTON_DISABLED = (150, 150, 150)
COLOR_BUTTON_TEXT = (255, 255, 255)
COLOR_UI_TEXT = (50, 50, 50)
COLOR_TITLE = (41, 128, 185)

# Table styling
COLOR_TABLE_HEADER_BG = (52, 73, 94)
COLOR_TABLE_HEADER_TEXT = (255, 255, 255)
COLOR_TABLE_ROW_BG_1 = (255, 255, 255)
COLOR_TABLE_ROW_BG_2 = (245, 245, 245)
COLOR_TABLE_BORDER = (180, 180, 180)
COLOR_HIGHLIGHT_FASTEST_BG = (210, 255, 210)
COLOR_HIGHLIGHT_MOST_NODES_BG = (255, 210, 210)
COLOR_HIGHLIGHT_BOTH_BG = (255, 245, 200)

# Shuffle settings
SHUFFLE_MOVES_3x3 = 30
SHUFFLE_MOVES_4x4 = 60

FONT_NAME = "Arial"
FONT_SIZE_TILE = 28
FONT_SIZE_UI = 16
FONT_SIZE_TITLE = 48
FONT_SIZE_BUTTON = 20

GOAL_3x3: Board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
GOAL_4x4: Board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

TEST_EASY_3x3: Board = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
TEST_MEDIUM_3x3: Board = [[2, 0, 3], [1, 5, 6], [4, 7, 8]]
TEST_HARD_3x3: Board = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]


def apply_blank_moves(board: Board, moves: Iterable[Move]) -> Board:
    """Return a new board after moving the blank (0) following the given moves."""

    new_board = [row[:] for row in board]

    blank_row = blank_col = None
    for i, row in enumerate(new_board):
        for j, value in enumerate(row):
            if value == 0:
                blank_row, blank_col = i, j
                break
        if blank_row is not None:
            break

    if blank_row is None:
        raise ValueError("Board does not contain a blank tile (0)")

    deltas: dict[Move, tuple[int, int]] = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1),
    }

    n = len(new_board)
    m = len(new_board[0])

    for move in moves:
        dr, dc = deltas[move]
        nr, nc = blank_row + dr, blank_col + dc
        if not (0 <= nr < n and 0 <= nc < m):
            raise ValueError(f"Invalid move '{move}' from blank position {(blank_row, blank_col)}")

        new_board[blank_row][blank_col], new_board[nr][nc] = new_board[nr][nc], new_board[blank_row][blank_col]
        blank_row, blank_col = nr, nc

    return new_board


TEST_EASY_4x4: Board = apply_blank_moves(GOAL_4x4, ["LEFT", "UP"])
TEST_MEDIUM_4x4: Board = apply_blank_moves(
    GOAL_4x4,
    ["LEFT", "UP", "UP", "RIGHT", "DOWN", "LEFT", "DOWN", "RIGHT"],
)
TEST_HARD_4x4: Board = apply_blank_moves(
    GOAL_4x4,
    [
        "LEFT",
        "LEFT",
        "UP",
        "UP",
        "RIGHT",
        "DOWN",
        "RIGHT",
        "UP",
        "LEFT",
        "LEFT",
        "DOWN",
        "DOWN",
        "RIGHT",
        "RIGHT",
    ],
)

# Backwards-compatible alias used by some tests/scripts.
TEST_EXPERT_4x4: Board = TEST_HARD_4x4

DIFFICULTIES: tuple[str, ...] = ("easy", "medium", "hard")

LEVELS: dict[int, dict[str, dict[str, object]]] = {
    3: {
        "easy": {
            "board": TEST_EASY_3x3,
            "goal": GOAL_3x3,
            "grid_size": 3,
            "name": "Easy",
            "description": "~2 steps",
        },
        "medium": {
            "board": TEST_MEDIUM_3x3,
            "goal": GOAL_3x3,
            "grid_size": 3,
            "name": "Medium",
            "description": "~12 steps",
        },
        "hard": {
            "board": TEST_HARD_3x3,
            "goal": GOAL_3x3,
            "grid_size": 3,
            "name": "Hard",
            "description": "~30 steps",
        },
    },
    4: {
        "easy": {
            "board": TEST_EASY_4x4,
            "goal": GOAL_4x4,
            "grid_size": 4,
            "name": "Easy",
            "description": "~2 steps",
        },
        "medium": {
            "board": TEST_MEDIUM_4x4,
            "goal": GOAL_4x4,
            "grid_size": 4,
            "name": "Medium",
            "description": "~8 steps",
        },
        "hard": {
            "board": TEST_HARD_4x4,
            "goal": GOAL_4x4,
            "grid_size": 4,
            "name": "Hard",
            "description": "~14 steps",
        },
    },
}


def get_level(grid_size: int, difficulty: str) -> dict[str, object]:
    """Return the level preset for a given grid size and difficulty."""

    level = LEVELS.get(grid_size, {}).get(difficulty)
    if level is None:
        raise KeyError(f"Unknown level grid_size={grid_size} difficulty={difficulty}")
    return level
