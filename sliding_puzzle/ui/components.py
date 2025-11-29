import pygame
from utils.constants import *


class GameBoard:
    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.tile_size = TILE_SIZE
        self.padding = PADDING
    
    def render(self, screen, board):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                tile_value = board[i][j]
                
                tile_x = self.x + j * (self.tile_size + self.padding)
                tile_y = self.y + i * (self.tile_size + self.padding)
                
                if tile_value == 0:
                    pygame.draw.rect(screen, COLOR_BLANK, 
                                   (tile_x, tile_y, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(screen, COLOR_TILE, 
                                   (tile_x, tile_y, self.tile_size, self.tile_size))
                    
                    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TILE)
                    text = font.render(str(tile_value), True, COLOR_TEXT)
                    text_rect = text.get_rect(center=(tile_x + self.tile_size // 2, 
                                                       tile_y + self.tile_size // 2))
                    screen.blit(text, text_rect)
    
    def get_tile_at_pos(self, mouse_x, mouse_y):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                tile_x = self.x + j * (self.tile_size + self.padding)
                tile_y = self.y + i * (self.tile_size + self.padding)
                
                if (tile_x <= mouse_x <= tile_x + self.tile_size and 
                    tile_y <= mouse_y <= tile_y + self.tile_size):
                    return (i, j)
        return None


class UIButton:
    def __init__(self, x, y, width, height, text, font_size=FONT_SIZE_UI):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(FONT_NAME, font_size)
        self.is_hovered = False
        self.is_disabled = False
    
    def render(self, screen):
        if self.is_disabled:
            color = COLOR_BUTTON_DISABLED
        else:
            color = COLOR_BUTTON_HOVER if self.is_hovered else COLOR_BUTTON
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLOR_UI_TEXT, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, COLOR_BUTTON_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos):
        if self.is_disabled:
            return False
        return self.rect.collidepoint(mouse_pos)
    
    def update_hover(self, mouse_pos):
        if self.is_disabled:
            self.is_hovered = False
        else:
            self.is_hovered = self.rect.collidepoint(mouse_pos)


class GameUI:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.font_ui = pygame.font.SysFont(FONT_NAME, FONT_SIZE_UI)
        self.font_large = pygame.font.SysFont(FONT_NAME, 24)
    
    def draw_text(self, screen, text, x, y, font=None, color=COLOR_UI_TEXT):
        if font is None:
            font = self.font_ui
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
    
    def draw_metrics(self, screen, moves, elapsed_time):
        moves_text = f"Moves: {moves}"
        self.draw_text(screen, moves_text, 20, 20)
        
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        self.draw_text(screen, time_text, 20, 45)
    
    def draw_solver_info(self, screen, solver_result, solver_type):
        if solver_result:
            y_offset = 480
            self.draw_text(screen, f"{solver_type} Solution:", 20, y_offset)
            self.draw_text(screen, f"Steps: {solver_result['steps']}", 20, y_offset + 25)
            self.draw_text(screen, f"Time: {solver_result['time_taken']:.3f}s", 20, y_offset + 50)
            self.draw_text(screen, f"Nodes: {solver_result['nodes_explored']}", 20, y_offset + 75)
    
    def draw_win_message(self, screen):
        win_text = "SOLVED!"
        text_surface = self.font_large.render(win_text, True, (0, 200, 0))
        text_rect = text_surface.get_rect(center=(self.window_width // 2, 30))
        
        padding = 10
        bg_rect = text_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(screen, COLOR_BACKGROUND, bg_rect)
        pygame.draw.rect(screen, (0, 200, 0), bg_rect, 3)
        
        screen.blit(text_surface, text_rect)
    
    def draw_keyboard_legend(self, screen, controls):
        y_offset = self.window_height - 120
        small_font = pygame.font.SysFont(FONT_NAME, 12)
        
        for i, control in enumerate(controls):
            text_surface = small_font.render(control, True, COLOR_UI_TEXT)
            screen.blit(text_surface, (20, y_offset + i * 18))
