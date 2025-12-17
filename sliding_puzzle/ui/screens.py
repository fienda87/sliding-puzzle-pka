import pygame

from ui.components import GameBoard, UIButton, GameUI
from utils.constants import (
    COLOR_BACKGROUND,
    COLOR_TABLE_BORDER,
    COLOR_TABLE_HEADER_BG,
    COLOR_TABLE_HEADER_TEXT,
    COLOR_TABLE_ROW_BG_1,
    COLOR_TABLE_ROW_BG_2,
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
    """Main gameplay screen, including solver controls."""

    def __init__(
        self,
        window_width: int,
        window_height: int,
        grid_size: int,
        metrics_results: list[dict[str, object]] | None = None,
    ):
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
        self.button_metrics = UIButton(
            panel_x,
            panel_y + 5 * (button_height + button_spacing),
            button_width,
            button_height,
            "Metrics",
        )
        self.button_back = UIButton(
            panel_x,
            panel_y + 6 * (button_height + button_spacing),
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
            self.button_metrics,
            self.button_back,
        ]

        self.table_x = board_x
        self.table_y = board_y + board_size + 18
        self.table_width = content_width
        self.table_height = max(60, window_height - self.table_y - 10)

        self.is_solving = False
        self.solving_algorithm: str | None = None

        self.comparison_results = metrics_results if metrics_results is not None else []

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

        if self.button_metrics.is_clicked(mouse_pos):
            return ("metrics", None)

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
        self.comparison_results.clear()


class MetricsScreen:
    """Standalone metrics table view used inside the separate metrics window."""

    def __init__(
        self,
        window_width: int,
        window_height: int,
        results: list[dict[str, object]],
        *,
        sort_by_time: bool = False,
    ):
        self.window_width = window_width
        self.window_height = window_height
        self.results = results
        self.sort_by_time = sort_by_time

        self.page_index = 0
        self.rows_per_page = 10

        self.title_font = pygame.font.SysFont(FONT_NAME, 28, bold=True)
        self.header_font = pygame.font.SysFont(FONT_NAME, 16, bold=True)
        self.row_font = pygame.font.SysFont(FONT_NAME, 16)
        self.page_font = pygame.font.SysFont(FONT_NAME, 16)

        self.header_height = 30
        self.row_height = 26

        self._create_layout()

    def resize(self, window_width: int, window_height: int) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self._create_layout()

    def _create_layout(self) -> None:
        margin = 18
        panel_width = max(460, self.window_width - margin * 2)
        panel_height = max(360, self.window_height - margin * 2)

        panel_x = (self.window_width - panel_width) // 2
        panel_y = (self.window_height - panel_height) // 2
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        content_padding = 18
        title_row_height = 36
        title_row_y = self.panel_rect.y + content_padding

        close_size = 30
        self.button_close_x = UIButton(
            self.panel_rect.right - content_padding - close_size,
            title_row_y,
            close_size,
            close_size,
            "X",
            16,
        )

        self.title_center_y = title_row_y + title_row_height // 2

        divider_y = title_row_y + title_row_height + 12
        self.divider_y = divider_y

        table_top = divider_y + 12

        close_button_height = 44
        close_button_width = min(360, self.panel_rect.width - content_padding * 2)
        close_button_y = self.panel_rect.bottom - content_padding - close_button_height
        self.button_close = UIButton(
            self.panel_rect.centerx - close_button_width // 2,
            close_button_y,
            close_button_width,
            close_button_height,
            "Close Window",
        )

        pagination_button_height = 36
        pagination_button_width = 140
        pagination_y = self.button_close.rect.y - 16 - pagination_button_height

        self.button_prev = UIButton(
            self.panel_rect.x + content_padding,
            pagination_y,
            pagination_button_width,
            pagination_button_height,
            "Previous",
        )
        self.button_next = UIButton(
            self.panel_rect.right - content_padding - pagination_button_width,
            pagination_y,
            pagination_button_width,
            pagination_button_height,
            "Next",
        )

        table_bottom = pagination_y - 12
        available_table_height = max(60, table_bottom - table_top)

        self.rows_per_page = max(
            1,
            int((available_table_height - self.header_height) // self.row_height),
        )
        table_height = self.header_height + self.rows_per_page * self.row_height

        self.table_rect = pygame.Rect(
            self.panel_rect.x + content_padding,
            table_top,
            self.panel_rect.width - content_padding * 2,
            table_height,
        )

        self.buttons = [self.button_close_x, self.button_prev, self.button_next, self.button_close]

    def get_total_pages(self) -> int:
        results = self._get_sorted_results()
        if not results:
            return 1
        return max(1, (len(results) + self.rows_per_page - 1) // self.rows_per_page)

    def _clamp_page(self) -> None:
        total_pages = self.get_total_pages()
        self.page_index = max(0, min(self.page_index, total_pages - 1))

    def focus_last_page(self) -> None:
        self.page_index = self.get_total_pages() - 1

    def next_page(self) -> None:
        self.page_index += 1
        self._clamp_page()

    def previous_page(self) -> None:
        self.page_index -= 1
        self._clamp_page()

    def _get_sorted_results(self) -> list[dict[str, object]]:
        if not self.sort_by_time:
            return list(self.results)

        def key_fn(r: dict[str, object]) -> tuple[float, str]:
            value = r.get("time_ms")
            try:
                time_ms = float(value) if value is not None else float("inf")
            except (TypeError, ValueError):
                time_ms = float("inf")
            return (time_ms, str(r.get("algorithm") or ""))

        return sorted(self.results, key=key_fn)

    def get_page_results(self) -> list[dict[str, object]]:
        self._clamp_page()
        results = self._get_sorted_results()
        start = self.page_index * self.rows_per_page
        end = start + self.rows_per_page
        return results[start:end]

    def render(self, screen: pygame.Surface) -> None:
        self._clamp_page()
        screen.fill(COLOR_BACKGROUND)

        pygame.draw.rect(screen, COLOR_TABLE_ROW_BG_1, self.panel_rect)
        pygame.draw.rect(screen, COLOR_TABLE_BORDER, self.panel_rect, 2)

        title_surface = self.title_font.render("Algorithm Comparison Metrics", True, COLOR_TITLE)
        title_rect = title_surface.get_rect(center=(self.panel_rect.centerx, self.title_center_y))
        screen.blit(title_surface, title_rect)

        pygame.draw.line(
            screen,
            COLOR_TABLE_BORDER,
            (self.panel_rect.left, self.divider_y),
            (self.panel_rect.right, self.divider_y),
            2,
        )

        results = self._get_sorted_results()
        if not results:
            pygame.draw.rect(screen, COLOR_TABLE_BORDER, self.table_rect, 1)
            empty_text = self.row_font.render("No metrics yet. Run a solver to see results.", True, COLOR_UI_TEXT)
            empty_rect = empty_text.get_rect(center=self.table_rect.center)
            screen.blit(empty_text, empty_rect)
        else:
            self._draw_table(screen, self.get_page_results())

        total_pages = self.get_total_pages()
        self.button_prev.is_disabled = self.page_index <= 0
        self.button_next.is_disabled = self.page_index >= total_pages - 1
        self.button_close.is_disabled = False  # Always allow close
        self.button_close_x.is_disabled = False  # Always allow close

        for button in self.buttons:
            button.render(screen)

        page_label = f"Page {self.page_index + 1} of {total_pages}"
        page_surface = self.page_font.render(page_label, True, COLOR_UI_TEXT)
        page_rect = page_surface.get_rect(center=(self.panel_rect.centerx, self.button_prev.rect.centery))
        screen.blit(page_surface, page_rect)

    def _draw_table(self, screen: pygame.Surface, page_results: list[dict[str, object]]) -> None:
        pygame.draw.rect(screen, COLOR_TABLE_BORDER, self.table_rect, 1)

        header_rect = pygame.Rect(self.table_rect.x, self.table_rect.y, self.table_rect.width, self.header_height)
        pygame.draw.rect(screen, COLOR_TABLE_HEADER_BG, header_rect)
        pygame.draw.rect(screen, COLOR_TABLE_BORDER, header_rect, 1)

        columns = [
            ("Algoritma", "algorithm", 0.28),
            ("Moves", "moves", 0.16),
            ("Time (ms)", "time_ms", 0.22),
            ("Nodes Exp", "nodes_explored", 0.34),
        ]

        col_rects: list[pygame.Rect] = []
        current_x = self.table_rect.x
        for i, (_, _, fraction) in enumerate(columns):
            col_width = (
                self.table_rect.width - (current_x - self.table_rect.x)
                if i == len(columns) - 1
                else int(self.table_rect.width * fraction)
            )
            col_rect = pygame.Rect(current_x, self.table_rect.y, col_width, self.header_height)
            col_rects.append(col_rect)
            current_x += col_width

        for col_rect, (title, _, _) in zip(col_rects, columns):
            text_surface = self.header_font.render(title, True, COLOR_TABLE_HEADER_TEXT)
            text_rect = text_surface.get_rect(center=col_rect.center)
            screen.blit(text_surface, text_rect)

        for col_rect in col_rects[1:]:
            pygame.draw.line(
                screen,
                COLOR_TABLE_BORDER,
                (col_rect.left, self.table_rect.y),
                (col_rect.left, self.table_rect.y + self.table_rect.height),
            )

        for i, r in enumerate(page_results):
            row_y = self.table_rect.y + self.header_height + i * self.row_height
            row_rect = pygame.Rect(self.table_rect.x, row_y, self.table_rect.width, self.row_height)

            bg_color = COLOR_TABLE_ROW_BG_1 if i % 2 == 0 else COLOR_TABLE_ROW_BG_2
            pygame.draw.rect(screen, bg_color, row_rect)
            pygame.draw.rect(screen, COLOR_TABLE_BORDER, row_rect, 1)

            for col_rect, (_, key, _) in zip(col_rects, columns):
                value = r.get(key)
                if key == "time_ms" and value is not None:
                    try:
                        display = str(int(round(float(value))))
                    except (TypeError, ValueError):
                        display = ""
                else:
                    display = "" if value is None else str(value)

                cell_rect = pygame.Rect(col_rect.x, row_y, col_rect.width, self.row_height)
                text_surface = self.row_font.render(display, True, COLOR_UI_TEXT)
                text_rect = text_surface.get_rect(center=cell_rect.center)
                screen.blit(text_surface, text_rect)

    def handle_click(self, mouse_pos: tuple[int, int]) -> str | None:
        if self.button_close_x.is_clicked(mouse_pos) or self.button_close.is_clicked(mouse_pos):
            return "close"

        if self.button_prev.is_clicked(mouse_pos) and not self.button_prev.is_disabled:
            return "prev"

        if self.button_next.is_clicked(mouse_pos) and not self.button_next.is_disabled:
            return "next"

        return None

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        for button in self.buttons:
            button.update_hover(mouse_pos)
