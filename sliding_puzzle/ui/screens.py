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
        legend_text = legend_font.render("Use arrow keys, R (reset), U (undo), ESC (menu), Space (BFS), S (DFS)", 
                                        True, COLOR_UI_TEXT)
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
        
        board_width = grid_size * TILE_SIZE + (grid_size - 1) * PADDING
        board_x = (window_width - board_width) // 2
        board_y = 100
        
        self.board = GameBoard(board_x, board_y, grid_size)
        self.ui = GameUI(window_width, window_height)
        
        button_y = board_y + grid_size * (TILE_SIZE + PADDING) + 30
        button_width = 120
        button_height = 40
        button_spacing = 15
        
        total_button_width = 3 * button_width + 2 * button_spacing
        start_x = (window_width - total_button_width) // 2
        
        self.button_solve_bfs = UIButton(start_x, button_y, button_width, button_height, "Solve BFS")
        self.button_solve_dfs = UIButton(start_x + button_width + button_spacing, button_y, 
                                         button_width, button_height, "Solve DFS")
        self.button_reset = UIButton(start_x + 2 * (button_width + button_spacing), button_y, 
                                     button_width, button_height, "Reset")
        
        button_y2 = button_y + button_height + button_spacing
        self.button_undo = UIButton(start_x, button_y2, button_width, button_height, "Undo")
        self.button_back = UIButton(start_x + button_width + button_spacing, button_y2, 
                                    button_width, button_height, "Back to Menu")
        
        self.buttons = [self.button_solve_bfs, self.button_solve_dfs, self.button_reset, 
                       self.button_undo, self.button_back]
        
        self.solver_result = None
        self.solver_type = None
    
    def render(self, screen, game):
        screen.fill(COLOR_BACKGROUND)
        
        self.board.render(screen, game.current_board)
        
        self.button_undo.is_disabled = not game.can_undo()
        
        for button in self.buttons:
            button.render(screen)
        
        self.ui.draw_metrics(screen, game.moves, game.get_time_elapsed())
        
        if self.solver_result:
            self.ui.draw_solver_info(screen, self.solver_result, self.solver_type)
        
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
        
        if self.button_reset.is_clicked(mouse_pos):
            return ('reset', None)
        
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
