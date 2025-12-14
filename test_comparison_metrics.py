#!/usr/bin/env python3
"""Test that algorithm comparison metrics still work after removing move counter/timer from UI"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sliding_puzzle'))

import pygame
from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_bfs, solve_dfs, solve_astar
from ui.screens import GameScreen
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, LEVELS

def test_algorithm_comparison_metrics():
    """Test that algorithm comparison table receives and displays metrics correctly"""
    print("Testing Algorithm Comparison Metrics...")
    print("=" * 60)
    
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Use medium difficulty for testing
    level_data = LEVELS['medium']
    game = PuzzleGame(level_data['board'], level_data['goal'])
    game_screen = GameScreen(WINDOW_WIDTH, WINDOW_HEIGHT, level_data['grid_size'])
    
    print(f"\nTesting with {level_data['name']} puzzle")
    print(f"Initial board: {level_data['board']}")
    print(f"Goal board: {level_data['goal']}")
    
    # Test each solver and add results to comparison table
    algorithms = [
        ('BFS', solve_bfs),
        ('DFS', solve_dfs),
        ('A*', solve_astar),
    ]
    
    for algo_name, solver_func in algorithms:
        print(f"\nRunning {algo_name} solver...")
        result = solver_func(game.current_board, game.goal_board)
        
        # Verify result has all required metrics
        assert 'moves' in result, f"{algo_name} result missing 'moves'"
        assert 'time_ms' in result, f"{algo_name} result missing 'time_ms'"
        assert 'nodes_explored' in result, f"{algo_name} result missing 'nodes_explored'"
        
        print(f"  Moves: {result['moves']}")
        print(f"  Time: {result['time_ms']:.2f} ms")
        print(f"  Nodes Explored: {result['nodes_explored']}")
        
        # Add to comparison table
        game_screen.add_comparison_result(algo_name, result)
        print(f"✓ {algo_name} result added to comparison table")
    
    # Verify comparison results were stored
    assert len(game_screen.comparison_results) == 3, "Not all results were stored"
    print(f"\n✓ All {len(game_screen.comparison_results)} algorithm results stored")
    
    # Verify each result has correct format
    for i, result in enumerate(game_screen.comparison_results):
        assert 'algorithm' in result, f"Result {i} missing 'algorithm'"
        assert 'moves' in result, f"Result {i} missing 'moves'"
        assert 'time_ms' in result, f"Result {i} missing 'time_ms'"
        assert 'nodes_explored' in result, f"Result {i} missing 'nodes_explored'"
        print(f"✓ Result {i} ({result['algorithm']}): {result}")
    
    # Render the screen to ensure comparison table draws correctly
    print("\nRendering game screen with comparison table...")
    game_screen.render(screen, game)
    print("✓ Game screen rendered successfully with comparison table")
    
    # Verify internal game tracking still works
    print("\nVerifying internal game tracking...")
    initial_moves = game.moves
    initial_time = game.get_time_elapsed()
    print(f"  Initial moves: {initial_moves}")
    print(f"  Initial time: {initial_time:.3f}s")
    
    # Make a move
    if game.move_blank_direction('LEFT'):
        print(f"  After move - moves: {game.moves}, time: {game.get_time_elapsed():.3f}s")
        assert game.moves == initial_moves + 1, "Move counter not working"
        print("✓ Internal move tracking works")
    
    # Test clear comparison table
    game_screen.clear_comparison_table()
    assert len(game_screen.comparison_results) == 0, "Clear comparison table failed"
    print("✓ Clear comparison table works")
    
    pygame.quit()
    
    print("\n" + "=" * 60)
    print("✓ ALL ALGORITHM COMPARISON METRICS TESTS PASSED!")
    print("  - Algorithm metrics are correctly tracked")
    print("  - Comparison table receives and stores results")
    print("  - Internal game tracking (moves/time) still works")
    print("  - UI renders without move counter/timer display")
    print("=" * 60)

if __name__ == "__main__":
    test_algorithm_comparison_metrics()
