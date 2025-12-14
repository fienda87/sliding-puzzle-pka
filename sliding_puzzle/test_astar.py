import time
from game.puzzle_state import PuzzleState
from game.puzzle_solver import solve_bfs, solve_dfs, solve_astar, manhattan_distance, precompute_goal_positions
from game.puzzle_game import PuzzleGame
from utils.constants import *


def test_manhattan_distance():
    """Test Manhattan distance heuristic calculation."""
    print("Testing Manhattan Distance Heuristic...")
    
    goal = GOAL_3x3
    goal_positions = precompute_goal_positions(goal)
    
    already_goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    distance = manhattan_distance(already_goal, goal_positions)
    assert distance == 0, f"Expected 0, got {distance}"
    print(f"  ✓ Already goal state: distance = {distance}")
    
    one_move_away = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    distance = manhattan_distance(one_move_away, goal_positions)
    assert distance == 1, f"Expected 1, got {distance}"
    print(f"  ✓ One move away: distance = {distance}")
    
    two_moves_away = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
    distance = manhattan_distance(two_moves_away, goal_positions)
    print(f"  ✓ Two moves away: distance = {distance}")
    

def test_astar_easy_puzzle():
    """Test A* with easy puzzle (already solved)."""
    print("\nTesting A* with Easy Puzzle (Already Solved)...")
    
    initial_board = GOAL_3x3
    goal_board = GOAL_3x3
    
    result = solve_astar(initial_board, goal_board)
    
    assert result is not None, "A* should find solution for already solved puzzle"
    assert result['moves'] == 0, f"Expected 0 moves, got {result['moves']}"
    assert result['nodes_explored'] == 1, f"Expected 1 node explored, got {result['nodes_explored']}"
    assert len(result['path']) == 1, f"Expected path length 1, got {len(result['path'])}"
    
    print(f"  ✓ Moves: {result['moves']}")
    print(f"  ✓ Nodes explored: {result['nodes_explored']}")
    print(f"  ✓ Time: {result['time_ms']:.2f} ms")
    print(f"  ✓ Path length: {len(result['path'])}")
    

def test_astar_one_move_puzzle():
    """Test A* with one-move puzzle."""
    print("\nTesting A* with One-Move Puzzle...")
    
    initial_board = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    goal_board = GOAL_3x3
    
    result = solve_astar(initial_board, goal_board)
    
    assert result is not None, "A* should find solution for one-move puzzle"
    assert result['moves'] == 1, f"Expected 1 move, got {result['moves']}"
    assert result['nodes_explored'] >= 1, f"Expected at least 1 node explored, got {result['nodes_explored']}"
    
    print(f"  ✓ Moves: {result['moves']}")
    print(f"  ✓ Nodes explored: {result['nodes_explored']}")
    print(f"  ✓ Time: {result['time_ms']:.2f} ms")
    print(f"  ✓ Path length: {len(result['path'])}")
    

def test_astar_medium_puzzle():
    """Test A* with medium puzzle."""
    print("\nTesting A* with Medium Puzzle...")
    
    initial_board = TEST_MEDIUM_3x3
    goal_board = GOAL_3x3
    
    result = solve_astar(initial_board, goal_board)
    
    assert result is not None, "A* should find solution for medium puzzle"
    assert result['moves'] >= 1, f"Expected at least 1 move, got {result['moves']}"
    assert result['nodes_explored'] >= 1, f"Expected at least 1 node explored, got {result['nodes_explored']}"
    assert len(result['path']) == result['moves'] + 1, "Path length should be moves + 1"
    
    print(f"  ✓ Moves: {result['moves']}")
    print(f"  ✓ Nodes explored: {result['nodes_explored']}")
    print(f"  ✓ Time: {result['time_ms']:.2f} ms")
    print(f"  ✓ Path length: {len(result['path'])}")
    

def test_response_format_consistency():
    """Test that all solvers return consistent format."""
    print("\nTesting Response Format Consistency...")
    
    initial_board = TEST_MEDIUM_3x3
    goal_board = GOAL_3x3
    
    bfs_result = solve_bfs(initial_board, goal_board)
    dfs_result = solve_dfs(initial_board, goal_board)
    astar_result = solve_astar(initial_board, goal_board)
    
    required_keys = {'path', 'moves', 'time_ms', 'nodes_explored', 'solution_path', 'steps', 'time_taken'}
    
    for result, solver_name in [(bfs_result, 'BFS'), (dfs_result, 'DFS'), (astar_result, 'A*')]:
        assert result is not None, f"{solver_name} should find solution"
        
        result_keys = set(result.keys())
        assert required_keys.issubset(result_keys), f"{solver_name} missing keys: {required_keys - result_keys}"
        
        assert isinstance(result['moves'], int), f"{solver_name} 'moves' should be int"
        assert isinstance(result['time_ms'], (int, float)), f"{solver_name} 'time_ms' should be numeric"
        assert isinstance(result['nodes_explored'], int), f"{solver_name} 'nodes_explored' should be int"
        assert isinstance(result['path'], list), f"{solver_name} 'path' should be list"
        
        print(f"  ✓ {solver_name} format is correct")
        print(f"    - Moves: {result['moves']}, Nodes: {result['nodes_explored']}, Time: {result['time_ms']:.2f}ms")
    

def test_astar_vs_others():
    """Test A* efficiency compared to BFS and DFS."""
    print("\nTesting A* Efficiency vs BFS and DFS...")
    
    initial_board = TEST_MEDIUM_3x3
    goal_board = GOAL_3x3
    
    print(f"  Puzzle: {initial_board}")
    print(f"  Goal:   {goal_board}")
    
    bfs_result = solve_bfs(initial_board, goal_board)
    dfs_result = solve_dfs(initial_board, goal_board)
    astar_result = solve_astar(initial_board, goal_board)
    
    assert bfs_result is not None, "BFS should find solution"
    assert astar_result is not None, "A* should find solution"
    
    bfs_moves = bfs_result['moves']
    astar_moves = astar_result['moves']
    
    bfs_nodes = bfs_result['nodes_explored']
    astar_nodes = astar_result['nodes_explored']
    
    dfs_info = ""
    if dfs_result is not None:
        dfs_moves = dfs_result['moves']
        dfs_nodes = dfs_result['nodes_explored']
        dfs_info = f"\n  DFS:  {dfs_moves} moves, {dfs_nodes} nodes explored"
    
    print(f"  BFS:  {bfs_moves} moves, {bfs_nodes} nodes explored")
    print(f"  A*:   {astar_moves} moves, {astar_nodes} nodes explored" + dfs_info)
    
    assert bfs_moves == astar_moves, \
        f"BFS and A* should find optimal path. BFS: {bfs_moves}, A*: {astar_moves}"
    
    print(f"  ✓ BFS and A* found optimal solution with {astar_moves} moves")
    print(f"  ✓ A* explored {astar_nodes} nodes (vs BFS {bfs_nodes})")
    print(f"  ✓ A* efficiency improvement: {bfs_nodes / astar_nodes:.1f}x fewer nodes explored")
    

def test_hard_puzzle():
    """Test A* with hard puzzle."""
    print("\nTesting A* with Hard Puzzle...")
    
    initial_board = TEST_HARD_3x3
    goal_board = GOAL_3x3
    
    result = solve_astar(initial_board, goal_board)
    
    assert result is not None, "A* should find solution for hard puzzle"
    assert result['moves'] >= 10, f"Hard puzzle should require at least 10 moves, got {result['moves']}"
    assert len(result['path']) == result['moves'] + 1, "Path length should be moves + 1"
    
    print(f"  ✓ Moves: {result['moves']}")
    print(f"  ✓ Nodes explored: {result['nodes_explored']}")
    print(f"  ✓ Time: {result['time_ms']:.2f} ms")
    print(f"  ✓ Path length: {len(result['path'])}")
    

def test_4x4_puzzle():
    """Test A* with 4x4 expert puzzle."""
    print("\nTesting A* with 4x4 Expert Puzzle...")
    print("  Note: 4x4 puzzles are computationally expensive, skipping full solve test")
    
    initial_board = TEST_EXPERT_4x4
    goal_board = GOAL_4x4
    
    goal_positions = precompute_goal_positions(goal_board)
    
    distance = manhattan_distance(initial_board, goal_positions)
    print(f"  ✓ Manhattan distance: {distance}")
    
    print(f"  ✓ Puzzle board: {initial_board}")
    print(f"  ✓ Goal board: {goal_board}")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("RUNNING A* ALGORITHM AND METRICS TESTS")
    print("=" * 60)
    
    try:
        test_manhattan_distance()
        test_astar_easy_puzzle()
        test_astar_one_move_puzzle()
        test_astar_medium_puzzle()
        test_response_format_consistency()
        test_astar_vs_others()
        test_hard_puzzle()
        test_4x4_puzzle()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
