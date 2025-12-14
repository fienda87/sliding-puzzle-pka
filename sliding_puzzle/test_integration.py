"""Integration tests for A* and metrics tracking."""

import time
from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_bfs, solve_dfs, solve_astar
from utils.constants import *


def test_integration_all_solvers():
    """Test that all solvers work together and return consistent formats."""
    print("Testing Integration: All Solvers with Metrics")
    print("=" * 60)
    
    test_cases = [
        ("Easy (1 move)", TEST_EASY_3x3, GOAL_3x3),
        ("Medium (5 moves)", TEST_MEDIUM_3x3, GOAL_3x3),
    ]
    
    for name, initial_board, goal_board in test_cases:
        print(f"\nTest Case: {name}")
        print(f"  Initial: {initial_board}")
        print(f"  Goal:    {goal_board}")
        
        bfs_result = solve_bfs(initial_board, goal_board)
        dfs_result = solve_dfs(initial_board, goal_board)
        astar_result = solve_astar(initial_board, goal_board)
        
        assert bfs_result is not None, "BFS should find solution"
        assert astar_result is not None, "A* should find solution"
        
        print(f"\n  BFS Results:")
        print(f"    - Moves: {bfs_result['moves']}")
        print(f"    - Time: {bfs_result['time_ms']:.2f} ms")
        print(f"    - Nodes explored: {bfs_result['nodes_explored']}")
        print(f"    - Has 'steps': {'steps' in bfs_result}")
        print(f"    - Has 'solution_path': {'solution_path' in bfs_result}")
        print(f"    - Has 'path': {'path' in bfs_result}")
        
        print(f"\n  A* Results:")
        print(f"    - Moves: {astar_result['moves']}")
        print(f"    - Time: {astar_result['time_ms']:.2f} ms")
        print(f"    - Nodes explored: {astar_result['nodes_explored']}")
        print(f"    - Has 'steps': {'steps' in astar_result}")
        print(f"    - Has 'solution_path': {'solution_path' in astar_result}")
        print(f"    - Has 'path': {'path' in astar_result}")
        
        if dfs_result is not None:
            print(f"\n  DFS Results:")
            print(f"    - Moves: {dfs_result['moves']}")
            print(f"    - Time: {dfs_result['time_ms']:.2f} ms")
            print(f"    - Nodes explored: {dfs_result['nodes_explored']}")
        
        assert bfs_result['moves'] == astar_result['moves'], \
            f"BFS and A* should find same optimal path. BFS: {bfs_result['moves']}, A*: {astar_result['moves']}"
        
        efficiency = bfs_result['nodes_explored'] / astar_result['nodes_explored']
        print(f"\n  ✓ A* is {efficiency:.1f}x more efficient than BFS")
        print(f"  ✓ Both found optimal solution with {astar_result['moves']} moves")


def test_game_integration():
    """Test PuzzleGame with solver results."""
    print("\n\nTesting Game Integration with Solver Results")
    print("=" * 60)
    
    game = PuzzleGame(TEST_EASY_3x3, GOAL_3x3)
    
    print(f"\nInitial Game State:")
    print(f"  Moves: {game.moves}")
    print(f"  Solved: {game.is_solved()}")
    print(f"  Can undo: {game.can_undo()}")
    
    result = solve_astar(game.current_board, game.goal_board)
    
    print(f"\nSolver Result:")
    print(f"  Moves in solution: {result['moves']}")
    print(f"  Nodes explored: {result['nodes_explored']}")
    print(f"  Time: {result['time_ms']:.2f} ms")
    
    print(f"\nApplying solution path to game...")
    for i, state in enumerate(result['solution_path']):
        game.apply_board_state(state.board)
        print(f"  Step {i}: Board updated, Solved: {game.is_solved()}")
    
    assert game.is_solved(), "Game should be solved after applying solution"
    print(f"\n  ✓ Game successfully solved with solution path")


def test_response_format():
    """Test that response format matches specification."""
    print("\n\nTesting Response Format Specification")
    print("=" * 60)
    
    initial_board = TEST_MEDIUM_3x3
    goal_board = GOAL_3x3
    
    result = solve_astar(initial_board, goal_board)
    
    print(f"\nResult Format Check:")
    
    required_keys = {
        'path': list,
        'moves': int,
        'time_ms': (int, float),
        'nodes_explored': int,
        'solution_path': list,
        'steps': int,
        'time_taken': float,
    }
    
    for key, expected_type in required_keys.items():
        assert key in result, f"Missing key: {key}"
        value = result[key]
        
        if isinstance(expected_type, tuple):
            assert isinstance(value, expected_type), \
                f"Key '{key}' should be {expected_type}, got {type(value)}"
        else:
            assert isinstance(value, expected_type), \
                f"Key '{key}' should be {expected_type}, got {type(value)}"
        
        print(f"  ✓ {key}: {expected_type.__name__ if not isinstance(expected_type, tuple) else '|'.join(t.__name__ for t in expected_type)}")
    
    print(f"\nResult Values:")
    print(f"  - path: list of {len(result['path'])} states")
    print(f"  - moves: {result['moves']}")
    print(f"  - time_ms: {result['time_ms']:.2f}")
    print(f"  - nodes_explored: {result['nodes_explored']}")
    print(f"  - solution_path: list of {len(result['solution_path'])} states")
    print(f"  - steps: {result['steps']}")
    print(f"  - time_taken: {result['time_taken']:.4f}")
    
    assert result['path'] == result['solution_path'], \
        "path and solution_path should be the same"
    assert result['moves'] == result['steps'], \
        "moves and steps should be the same"
    
    print(f"\n  ✓ Format specification fully satisfied")


def run_all_integration_tests():
    """Run all integration tests."""
    try:
        test_integration_all_solvers()
        test_game_integration()
        test_response_format()
        
        print("\n" + "=" * 60)
        print("✓ ALL INTEGRATION TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_integration_tests()
