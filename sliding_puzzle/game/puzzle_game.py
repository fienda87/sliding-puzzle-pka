import time
import random

from utils.constants import SHUFFLE_MOVES_3x3, SHUFFLE_MOVES_4x4


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
        self.has_scrambled = self.current_board != self.goal_board
    
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
        self.has_scrambled = self.current_board != self.goal_board

    def shuffle(self, move_count=None):
        n = len(self.goal_board)
        if move_count is None:
            move_count = SHUFFLE_MOVES_4x4 if n == 4 else SHUFFLE_MOVES_3x3

        board = [row[:] for row in self.goal_board]

        blank_row, blank_col = None, None
        for i in range(n):
            for j in range(n):
                if board[i][j] == 0:
                    blank_row, blank_col = i, j
                    break
            if blank_row is not None:
                break

        if blank_row is None:
            blank_row, blank_col = n - 1, n - 1

        last_action = None
        opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        directions = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]

        for _ in range(move_count):
            possible = []
            for dr, dc, action in directions:
                if last_action and opposite[last_action] == action:
                    continue

                nr = blank_row + dr
                nc = blank_col + dc
                if 0 <= nr < n and 0 <= nc < n:
                    possible.append((nr, nc, action))

            if not possible:
                continue

            nr, nc, action = random.choice(possible)
            board[blank_row][blank_col], board[nr][nc] = board[nr][nc], board[blank_row][blank_col]
            blank_row, blank_col = nr, nc
            last_action = action

        if board == self.goal_board:
            possible = []
            for dr, dc, action in directions:
                nr = blank_row + dr
                nc = blank_col + dc
                if 0 <= nr < n and 0 <= nc < n:
                    possible.append((nr, nc, action))

            if possible:
                nr, nc, _ = random.choice(possible)
                board[blank_row][blank_col], board[nr][nc] = board[nr][nc], board[blank_row][blank_col]

        self.reset(board=board)
        self.has_scrambled = True
        return board

    def can_solve(self):
        return self.has_scrambled and not self.is_solved()
    
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
            self.has_scrambled = True
            return True
        
        return False
    
    def is_solved(self):
        return self.current_board == self.goal_board
    
    def get_time_elapsed(self):
        return time.time() - self.start_time
    
    def apply_board_state(self, board):
        self.current_board = [row[:] for row in board]
        self.blank_pos = self.find_blank()
        self.has_scrambled = self.current_board != self.goal_board
    
    def undo(self):
        if self.move_history:
            previous_board = self.move_history.pop()
            self.current_board = [row[:] for row in previous_board]
            self.blank_pos = self.find_blank()
            self.moves = max(0, self.moves - 1)
            self.has_scrambled = self.current_board != self.goal_board
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
            self.has_scrambled = True
            return True
        
        return False
