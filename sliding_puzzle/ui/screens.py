import pygame

from ui.components import GameBoard, UIButton, GameUI
from utils.constants import (
    COLOR_BACKGROUND,
    COLOR_TITLE,
    COLOR_UI_TEXT,
    DIFFICULTIES,
    FONT_NAME,
    FONT_SIZE_BUTTON,
    FONT_SIZE_TITLE,
    PADDING,
    TILE_SIZE,
    get_level,
)


class MenuScreen:
    """Two-step menu flow: grid selection (3x3/4x4) then difficulty selection."""

    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height

        self.title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TITLE, bold=True)
        self.subtitle_font = pygame.font.SysFont(FONT_NAME, 18)

        self.view: str = "grid"
        self.selected_grid_size: int | None = None

        self._create_buttons()

    def _create_buttons(self) -> None:
        button_width = 300
        button_height = 50
        button_spacing = 18

        center_x = (self.window_width - button_width) // 2

        grid_start_y = 240
        self.grid_buttons: dict[int, UIButton] = {
            3: UIButton(center_x, grid_start_y, button_width, button_height, "3x3 Grid", FONT_SIZE_BUTTON),
            4: UIButton(
                center_x,
                grid_start_y + button_height + button_spacing,
                button_width,
                button_height,
                "4x4 Grid",
                FONT_SIZE_BUTTON,
            ),
        }

        diff_start_y = 210
        self.difficulty_buttons: dict[str, UIButton] = {}
        for i, difficulty in enumerate(DIFFICULTIES):
            y = diff_start_y + i * (button_height + button_spacing)
            label = difficulty.capitalize()
            self.difficulty_buttons[difficulty] = UIButton(center_x, y, button_width, button_height, label, FONT_SIZE_BUTTON)

        self.back_button = UIButton(center_x, diff_start_y + 3 * (button_height + button_spacing) + 10, button_width, 44, "Back")

    def reset(self) -> None:
        self.view = "grid"
        self.selected_grid_size = None

    def can_go_back(self) -> bool:
        return self.view == "difficulty"

    def go_back(self) -> None:
        if self.can_go_back():
            self.reset()

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(COLOR_BACKGROUND)

        title_text = self.title_font.render("SLIDING PUZZLE", True, COLOR_TITLE)
        title_rect = title_text.get_rect(center=(self.window_width // 2, 80))
        screen.blit(title_text, title_rect)

        if self.view == "grid":
            subtitle = "Select Grid Size"
            subtitle_y = 150
        else:
            grid = self.selected_grid_size or 3
            subtitle = f"Select Difficulty ({grid}x{grid})"
            subtitle_y = 140

        subtitle_text = self.subtitle_font.render(subtitle, True, COLOR_UI_TEXT)
        subtitle_rect = subtitle_text.get_rect(center=(self.window_width // 2, subtitle_y))
        screen.blit(subtitle_text, subtitle_rect)

        if self.view == "grid":
            for button in self.grid_buttons.values():
                button.render(screen)
        else:
            for button in self.difficulty_buttons.values():
                button.render(screen)
            self.back_button.render(screen)

    def handle_click(self, mouse_pos: tuple[int, int]) -> dict[str, object] | None:
        if self.view == "grid":
            for grid_size, button in self.grid_buttons.items():
                if button.is_clicked(mouse_pos):
                    self.view = "difficulty"
                    self.selected_grid_size = grid_size
                    return None
            return None

        if self.back_button.is_clicked(mouse_pos):
            self.reset()
            return None

        for difficulty, button in self.difficulty_buttons.items():
            if button.is_clicked(mouse_pos):
                return get_level(self.selected_grid_size or 3, difficulty)

        return None

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        if self.view == "grid":
            for button in self.grid_buttons.values():
                button.update_hover(mouse_pos)
            return

        for button in self.difficulty_buttons.values():
            button.update_hover(mouse_pos)
        self.back_button.update_hover(mouse_pos)


class GameScreen:
    """Main gameplay screen, including solver controls and comparison table."""

    def __init__(self, window_width: int, window_height: int, grid_size: int):
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
        self.button_solve_dfs = UIButton(
            panel_x,
            panel_y + (button_height + button_spacing),
            button_width,
            button_height,
            "Solve with DFS",
        )
        self.button_solve_astar = UIButton(
            panel_x,
            panel_y + 2 * (button_height + button_spacing),
            button_width,
            button_height,
            "Solve with A*",
        )

        self.button_shuffle = UIButton(
            panel_x,
            panel_y + 3 * (button_height + button_spacing),
            button_width,
            button_height,
            "Shuffle",
        )

        self.button_undo = UIButton(
            panel_x,
            panel_y + 4 * (button_height + button_spacing),
            button_width,
            button_height,
            "Undo",
        )
        self.button_back = UIButton(
            panel_x,
            panel_y + 5 * (button_height + button_spacing),
            button_width,
            button_height,
            "Back to Menu",
        )

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

        self.is_solving = False
        self.solving_algorithm: str | None = None

        self.comparison_results: list[dict[str, object]] = []

    def render(self, screen: pygame.Surface, game) -> None:
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

    def handle_click(self, mouse_pos: tuple[int, int], _game) -> tuple[str | None, object | None]:
        tile = self.board.get_tile_at_pos(mouse_pos[0], mouse_pos[1])
        if tile:
            return ("tile_click", tile)

        if self.button_solve_bfs.is_clicked(mouse_pos):
            return ("solve_bfs", None)

        if self.button_solve_dfs.is_clicked(mouse_pos):
            return ("solve_dfs", None)

        if self.button_solve_astar.is_clicked(mouse_pos):
            return ("solve_astar", None)

        if self.button_shuffle.is_clicked(mouse_pos):
            return ("shuffle", None)

        if self.button_undo.is_clicked(mouse_pos):
            return ("undo", None)

        if self.button_back.is_clicked(mouse_pos):
            return ("back", None)

        return (None, None)

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        for button in self.buttons:
            button.update_hover(mouse_pos)

    def set_solving(self, is_solving: bool, algorithm: str | None = None) -> None:
        self.is_solving = is_solving
        self.solving_algorithm = algorithm if is_solving else None

    def add_comparison_result(self, algorithm: str, result: dict[str, object]) -> None:
        self.comparison_results.append(
            {
                "algorithm": algorithm,
                "moves": result["moves"],
                "time_ms": result["time_ms"],
                "nodes_explored": result["nodes_explored"],
            }
        )

    def clear_comparison_table(self) -> None:
        self.comparison_results = []
