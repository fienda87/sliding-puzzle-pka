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

GOAL_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
GOAL_4x4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

TEST_EASY_3x3 = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
TEST_MEDIUM_3x3 = [[2, 0, 3], [1, 5, 6], [4, 7, 8]]
TEST_HARD_3x3 = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]
TEST_EXPERT_4x4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 15, 14, 0]]

DIFFICULTY_PRESETS_3X3 = {
    'easy': {'shuffles': 5, 'name': 'Easy', 'description': '5 shuffles'},
    'medium': {'shuffles': 15, 'name': 'Medium', 'description': '15 shuffles'},
    'hard': {'shuffles': 30, 'name': 'Hard', 'description': '30 shuffles'}
}

DIFFICULTY_PRESETS_4X4 = {
    'easy': {'shuffles': 8, 'name': 'Easy', 'description': '5-10 shuffles'},
    'medium': {'shuffles': 20, 'name': 'Medium', 'description': '15-25 shuffles'},
    'hard': {'shuffles': 40, 'name': 'Hard', 'description': '30-50 shuffles'}
}

LEVELS = {
    'easy_3x3': {
        'board': [[1, 2, 3], [4, 5, 6], [7, 0, 8]],
        'goal': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        'grid_size': 3,
        'name': 'Easy (3x3)',
        'description': '3x3 Grid, ~2 steps',
        'shuffles': 5
    },
    'medium_3x3': {
        'board': [[2, 0, 3], [1, 5, 6], [4, 7, 8]],
        'goal': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        'grid_size': 3,
        'name': 'Medium (3x3)',
        'description': '3x3 Grid, ~12 steps',
        'shuffles': 15
    },
    'hard_3x3': {
        'board': [[8, 7, 6], [5, 4, 3], [2, 1, 0]],
        'goal': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        'grid_size': 3,
        'name': 'Hard (3x3)',
        'description': '3x3 Grid, ~30 steps',
        'shuffles': 30
    },
    'easy_4x4': {
        'board': GOAL_4x4,
        'goal': GOAL_4x4,
        'grid_size': 4,
        'name': 'Easy (4x4)',
        'description': '4x4 Grid, 5-10 shuffles',
        'shuffles': 8
    },
    'medium_4x4': {
        'board': GOAL_4x4,
        'goal': GOAL_4x4,
        'grid_size': 4,
        'name': 'Medium (4x4)',
        'description': '4x4 Grid, 15-25 shuffles',
        'shuffles': 20
    },
    'hard_4x4': {
        'board': GOAL_4x4,
        'goal': GOAL_4x4,
        'grid_size': 4,
        'name': 'Hard (4x4)',
        'description': '4x4 Grid, 30-50 shuffles',
        'shuffles': 40
    }
}

KEYBOARD_CONTROLS = [
    "Arrow Keys: Move blank tile",
    "U: Undo last move",
    "R: Shuffle puzzle",
    "ESC: Back to menu",
    "Space: Solve with BFS",
    "S: Solve with DFS",
    "A: Solve with A*"
]
