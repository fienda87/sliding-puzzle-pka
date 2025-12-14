import pygame
from .components import GameBoard, UIButton, GameUI
from utils.constants import *


class MenuScreen:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        button_width = 300
        button_height = 50
        button_spacing = 20
        start_y = 200

        center_x = (window_width - button_width) // 2

        self.buttons = {
            'easy': UIButton(center_x, start_y, button_width, button_height,
                             "EASY - 3x3, ~2 steps", FONT_SIZE_BUTTON),
            'medium': UIButton(center_x, start_y + button_height + button_spacing,
                               button_width, button_height, "MEDIUM - 3x3, ~12 steps", FONT_SIZE_BUTTON),
            'hard': UIButton(center_x, start_y + 2 * (button_height + button_spacing),
                             button_width, button_height, "HARD - 3x3, ~30 steps", FONT_SIZE_BUTTON),
            'expert': UIButton(center_x, start_y + 3 * (button_height + button_spacing),
                               button_width, button_height, "EXPERT - 4x4, 5+ steps", FONT_SIZE_BUTTON)
        }

        self.title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TITLE, bold=True)
        self.subtitle_font = pygame.font.SysFont(FONT_NAME, 18)

    def render(self, screen):
        screen.fill(COLOR_BACKGROUND)

        title_text = self.title_font.render("SLIDING PUZZLE", True, COLOR_TITLE)
        title_rect = title_text.get_rect(center=(self.window_width // 2, 80))
        screen.blit(title_text, title_rect)

        subtitle_text = self.subtitle_font.render("Select Difficulty Level", True, COLOR_UI_TEXT)
        subtitle_rect = subtitle_text.get_rect(center=(self.window_width // 2, 140))
        screen.blit(subtitle_text, subtitle_rect)

        for button in self.buttons.values():
            button.render(screen)

        legend_y = self.window_height - 100
        legend_font = pygame.font.SysFont(FONT_NAME, 12)
        legend_text = legend_font.render(
            "Arrow keys (move), R (shuffle), U (undo), ESC (menu), Space (BFS), S (DFS), A (A*)",
            True,
            COLOR_UI_TEXT,
        )
        legend_rect = legend_text.get_rect(center=(self.window_width // 2, legend_y))
        screen.blit(legend_text, legend_rect)

    def handle_click(self, mouse_pos):
        for difficulty, button in self.buttons.items():
            if button.is_clicked(mouse_pos):
                return difficulty
        return None

    def update_hover(self, mouse_pos):
        for button in self.buttons.values():
            button.update_hover(mouse_pos)


class GameScreen:
    def __init__(self, window_width, window_height, grid_size):
        self.window_width = window_width
        self.window_height = window_height
        self.grid_size = grid_size

        board_size = grid_size * TILE_SIZE + (grid_size - 1) * PADDING

        panel_width = 220
        content_width = board_size + PADDING + panel_width

        board_x = (window_width - content_width) // 2
        board_y = 50

        self.board = GameBoard(board_x, board_y, grid_size)
        self.ui = GameUI(window_width, window_height)

        panel_x = board_x + board_size + PADDING
        panel_y = board_y

        button_width = panel_width
        button_height = 42
        button_spacing = 10

        self.button_solve_bfs = UIButton(panel_x, panel_y, button_width, button_height, "Solve with BFS")
        self.button_solve_dfs = UIButton(panel_x, panel_y + (button_height + button_spacing),
                                         button_width, button_height, "Solve with DFS")
        self.button_solve_astar = UIButton(panel_x, panel_y + 2 * (button_height + button_spacing),
                                           button_width, button_height, "Solve with A*")

        self.button_shuffle = UIButton(panel_x, panel_y + 3 * (button_height + button_spacing),
                                       button_width, button_height, "Shuffle")

        self.button_undo = UIButton(panel_x, panel_y + 4 * (button_height + button_spacing),
                                    button_width, button_height, "Undo")
        self.button_back = UIButton(panel_x, panel_y + 5 * (button_height + button_spacing),
                                    button_width, button_height, "Back to Menu")

        self.buttons = [
            self.button_solve_bfs,
            self.button_solve_dfs,
            self.button_solve_astar,
            self.button_shuffle,
            self.button_undo,
            self.button_back,
        ]

        self.table_x = board_x
        self.table_y = board_y + board_size + 18
        self.table_width = content_width
        self.table_height = max(60, window_height - self.table_y - 10)

        self.solver_result = None
        self.solver_type = None

        self.is_solving = False
        self.solving_algorithm = None

        self.comparison_results = []

    def render(self, screen, game):
        screen.fill(COLOR_BACKGROUND)

        self.board.render(screen, game.current_board)

        can_solve = game.can_solve() and not game.is_animating and not self.is_solving

        self.button_solve_bfs.is_disabled = not can_solve
        self.button_solve_dfs.is_disabled = not can_solve
        self.button_solve_astar.is_disabled = not can_solve

        busy = game.is_animating or self.is_solving
        self.button_shuffle.is_disabled = busy
        self.button_back.is_disabled = busy

        self.button_undo.is_disabled = busy or not game.can_undo()

        for button in self.buttons:
            button.render(screen)

        if self.is_solving:
            self.ui.draw_solving_status(screen, self.solving_algorithm, self.button_solve_bfs.rect.x, 20)

        self.ui.draw_comparison_table(
            screen,
            self.comparison_results,
            self.table_x,
            self.table_y,
            self.table_width,
            self.table_height,
        )

        if game.is_solved():
            self.ui.draw_win_message(screen)

    def handle_click(self, mouse_pos, game):
        tile = self.board.get_tile_at_pos(mouse_pos[0], mouse_pos[1])
        if tile:
            return ('tile_click', tile)

        if self.button_solve_bfs.is_clicked(mouse_pos):
            return ('solve_bfs', None)

        if self.button_solve_dfs.is_clicked(mouse_pos):
            return ('solve_dfs', None)

        if self.button_solve_astar.is_clicked(mouse_pos):
            return ('solve_astar', None)

        if self.button_shuffle.is_clicked(mouse_pos):
            return ('shuffle', None)

        if self.button_undo.is_clicked(mouse_pos):
            return ('undo', None)

        if self.button_back.is_clicked(mouse_pos):
            return ('back', None)

        return (None, None)

    def update_hover(self, mouse_pos):
        for button in self.buttons:
            button.update_hover(mouse_pos)

    def set_solver_result(self, result, solver_type):
        self.solver_result = result
        self.solver_type = solver_type

    def clear_solver_result(self):
        self.solver_result = None
        self.solver_type = None

    def set_solving(self, is_solving, algorithm=None):
        self.is_solving = is_solving
        self.solving_algorithm = algorithm if is_solving else None

    def add_comparison_result(self, algorithm, result):
        self.comparison_results.append(
            {
                'algorithm': algorithm,
                'moves': result['moves'],
                'time_ms': result['time_ms'],
                'nodes_explored': result['nodes_explored'],
            }
        )

    def clear_comparison_table(self):
        self.comparison_results = []
