import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game.puzzle_state import PuzzleState


def count_inversions(board_flat):
    inversions = 0
    for i in range(len(board_flat)):
        for j in range(i + 1, len(board_flat)):
            if board_flat[i] != 0 and board_flat[j] != 0:
                if board_flat[i] > board_flat[j]:
                    inversions += 1
    return inversions


def is_solvable(board, goal_board):
    board_flat = [tile for row in board for tile in row]
    goal_flat = [tile for row in goal_board for tile in row]
    
    initial_inv = count_inversions(board_flat)
    goal_inv = count_inversions(goal_flat)
    
    return (initial_inv % 2) == (goal_inv % 2)


def generate_random_solvable_puzzle(grid_size=3):
    if grid_size == 3:
        goal_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    else:
        raise ValueError("Only 3x3 puzzles supported")
    
    current_board = [row[:] for row in goal_board]
    current_state = PuzzleState(current_board)
    
    num_moves = random.randint(100, 200)
    previous_state = None
    
    for _ in range(num_moves):
        possible_moves = current_state.get_possible_moves()
        
        if previous_state:
            possible_moves = [
                move for move in possible_moves
                if move.board != previous_state.board
            ]
        
        if possible_moves:
            previous_state = current_state
            current_state = random.choice(possible_moves)
    
    return current_state.board
