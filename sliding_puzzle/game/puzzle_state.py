class PuzzleState:
    def __init__(self, board, parent=None, action=None, level=0):
        self.board = [row[:] for row in board]
        self.parent = parent
        self.action = action
        self.level = level
        self.blank_pos = self.find_blank()
    
    def find_blank(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def get_possible_moves(self):
        moves = []
        row, col = self.blank_pos
        n = len(self.board)
        m = len(self.board[0])
        
        directions = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]
        
        for dr, dc, action_name in directions:
            new_row, new_col = row + dr, col + dc
            
            if 0 <= new_row < n and 0 <= new_col < m:
                new_board = [row[:] for row in self.board]
                new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]
                
                new_state = PuzzleState(new_board, parent=self, action=action_name, level=self.level + 1)
                moves.append(new_state)
        
        return moves
    
    def is_goal(self, goal_board):
        return self.board == goal_board
    
    def get_board_tuple(self):
        return tuple(tuple(row) for row in self.board)
    
    def __eq__(self, other):
        if not isinstance(other, PuzzleState):
            return False
        return self.get_board_tuple() == other.get_board_tuple()
    
    def __hash__(self):
        return hash(self.get_board_tuple())
    
    def __repr__(self):
        return f"PuzzleState(level={self.level}, action={self.action})"
