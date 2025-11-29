from game.puzzle_state import PuzzleState
from game.puzzle_solver import solve_bfs, solve_dfs
from game.puzzle_game import PuzzleGame
from utils.constants import *

print("Testing PuzzleState...")
state = PuzzleState([[1, 2, 3], [4, 5, 6], [7, 0, 8]])
print(f"  Blank position: {state.blank_pos}")
print(f"  Possible moves: {len(state.get_possible_moves())}")
print(f"  Is goal: {state.is_goal(GOAL_3x3)}")

print("\nTesting BFS solver on easy puzzle...")
result = solve_bfs(TEST_EASY_3x3, GOAL_3x3)
print(f"  Steps: {result['steps']}")
print(f"  Nodes explored: {result['nodes_explored']}")

print("\nTesting PuzzleGame...")
game = PuzzleGame(TEST_EASY_3x3, GOAL_3x3)
print(f"  Initial moves: {game.moves}")
print(f"  Blank at: {game.blank_pos}")
print(f"  Is solved: {game.is_solved()}")
game.handle_tile_click(2, 2)
print(f"  After click moves: {game.moves}")
print(f"  Is solved: {game.is_solved()}")

print("\nAll tests passed!")
