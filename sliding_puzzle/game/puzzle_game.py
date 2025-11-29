import time


class PuzzleGame:
    def __init__(self, initial_board, goal_board):
        self.initial_board = [row[:] for row in initial_board]
        self.goal_board = goal_board
        self.current_board = [row[:] for row in initial_board]
        self.moves = 0
        self.start_time = time.time()
        self.blank_pos = self.find_blank()
        self.is_animating = False
        self.move_history = []
    
    def find_blank(self):
        for i in range(len(self.current_board)):
            for j in range(len(self.current_board[i])):
                if self.current_board[i][j] == 0:
                    return (i, j)
        return None
    
    def reset(self, board=None):
        if board is None:
            board = self.initial_board
        else:
            self.initial_board = [row[:] for row in board]
        
        self.current_board = [row[:] for row in self.initial_board]
        self.moves = 0
        self.start_time = time.time()
        self.blank_pos = self.find_blank()
        self.is_animating = False
        self.move_history = []
    
    def handle_tile_click(self, row, col):
        if self.is_animating:
            return False
        
        blank_row, blank_col = self.blank_pos
        
        is_adjacent = (
            (abs(row - blank_row) == 1 and col == blank_col) or
            (abs(col - blank_col) == 1 and row == blank_row)
        )
        
        if is_adjacent:
            self.move_history.append([row[:] for row in self.current_board])
            
            self.current_board[blank_row][blank_col], self.current_board[row][col] = \
                self.current_board[row][col], self.current_board[blank_row][blank_col]
            
            self.blank_pos = (row, col)
            self.moves += 1
            return True
        
        return False
    
    def is_solved(self):
        return self.current_board == self.goal_board
    
    def get_time_elapsed(self):
        return time.time() - self.start_time
    
    def apply_board_state(self, board):
        self.current_board = [row[:] for row in board]
        self.blank_pos = self.find_blank()
    
    def undo(self):
        if self.move_history:
            previous_board = self.move_history.pop()
            self.current_board = [row[:] for row in previous_board]
            self.blank_pos = self.find_blank()
            self.moves = max(0, self.moves - 1)
            return True
        return False
    
    def can_undo(self):
        return len(self.move_history) > 0
    
    def move_blank_direction(self, direction):
        if self.is_animating:
            return False
        
        blank_row, blank_col = self.blank_pos
        n = len(self.current_board)
        m = len(self.current_board[0])
        
        new_row, new_col = blank_row, blank_col
        
        if direction == 'UP':
            new_row = blank_row - 1
        elif direction == 'DOWN':
            new_row = blank_row + 1
        elif direction == 'LEFT':
            new_col = blank_col - 1
        elif direction == 'RIGHT':
            new_col = blank_col + 1
        
        if 0 <= new_row < n and 0 <= new_col < m:
            self.move_history.append([row[:] for row in self.current_board])
            
            self.current_board[blank_row][blank_col], self.current_board[new_row][new_col] = \
                self.current_board[new_row][new_col], self.current_board[blank_row][blank_col]
            
            self.blank_pos = (new_row, new_col)
            self.moves += 1
            return True
        
        return False
