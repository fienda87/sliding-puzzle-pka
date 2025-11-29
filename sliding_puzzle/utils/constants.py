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
COLOR_GRID_LINE = (200, 200, 200)
COLOR_TITLE = (41, 128, 185)

FONT_NAME = "Arial"
FONT_SIZE_TILE = 28
FONT_SIZE_UI = 16
FONT_SIZE_TITLE = 48
FONT_SIZE_BUTTON = 20

GOAL_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

TEST_EASY_3x3 = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
TEST_MEDIUM_3x3 = [[2, 0, 3], [1, 5, 6], [4, 7, 8]]
TEST_HARD_3x3 = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]

LEVELS = {
    'easy': {
        'board': [[1, 2, 3], [4, 5, 6], [7, 0, 8]],
        'goal': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        'grid_size': 3,
        'name': 'Easy',
        'description': '3x3, ~2 steps',
        'type': 'preset'
    },
    'medium': {
        'board': [[2, 0, 3], [1, 5, 6], [4, 7, 8]],
        'goal': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        'grid_size': 3,
        'name': 'Medium',
        'description': '3x3, ~12 steps',
        'type': 'preset'
    },
    'hard': {
        'board': [[6, 4, 7], [8, 5, 0], [3, 2, 1]],
        'goal': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        'grid_size': 3,
        'name': 'Hard',
        'description': '3x3, ~30 steps',
        'type': 'preset'
    },
    'random_3x3': {
        'goal': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        'grid_size': 3,
        'name': 'Random',
        'description': '3x3, Variable steps',
        'type': 'random'
    }
}

KEYBOARD_CONTROLS = [
    "Arrow Keys: Move blank tile",
    "U: Undo last move",
    "R: Reset puzzle",
    "ESC: Back to menu",
    "Space: Solve with BFS",
    "S: Solve with DFS"
]
