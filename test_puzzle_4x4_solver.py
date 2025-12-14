#!/usr/bin/env python3
"""Test script for puzzle_4x4_solver.py to ensure it works correctly."""

import sys
import os
import random

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from puzzle_4x4_solver import (
    render_board_ascii_table,
    generate_solvable_puzzle_4x4,
    run_single_puzzle,
    render_comparison_table,
    print_winners,
    GOAL_4x4,
    AlgoResult,
)


def test_render_board_ascii_table():
    """Test that the ASCII table rendering works correctly."""
    print("Testing render_board_ascii_table...")
    
    board = GOAL_4x4
    result = render_board_ascii_table(board, "Test Board:")
    
    # Check that box-drawing characters are present
    assert "┌" in result
    assert "┐" in result
    assert "└" in result
    assert "┘" in result
    assert "├" in result
    assert "┤" in result
    assert "┬" in result
    assert "┴" in result
    assert "┼" in result
    assert "│" in result
    assert "─" in result
    assert "(0 = blank)" in result
    assert "Test Board:" in result
    
    print("✓ render_board_ascii_table test passed")


def test_generate_solvable_puzzle():
    """Test that puzzle generation works."""
    print("Testing generate_solvable_puzzle_4x4...")
    
    rng = random.Random(42)
    
    # Test easy difficulty
    puzzle = generate_solvable_puzzle_4x4(shuffle_moves=4, rng=rng)
    assert len(puzzle) == 4
    assert len(puzzle[0]) == 4
    assert puzzle != GOAL_4x4  # Should be different from goal
    
    # Check that all numbers 0-15 are present
    all_nums = set()
    for row in puzzle:
        all_nums.update(row)
    assert all_nums == set(range(16))
    
    print("✓ generate_solvable_puzzle_4x4 test passed")


def test_render_comparison_table():
    """Test that the comparison table renders correctly."""
    print("Testing render_comparison_table...")
    
    results = [
        AlgoResult("BFS", 52, 2450.5, 45820),
        AlgoResult("DFS", 52, 1890.3, 38420),
        AlgoResult("A*", 52, 280.1, 892),
    ]
    
    table = render_comparison_table(results)
    
    # Check for table structure
    assert "┌" in table
    assert "Algoritma" in table
    assert "Moves" in table
    assert "Time (ms)" in table
    assert "Nodes Exp." in table
    assert "BFS" in table
    assert "DFS" in table
    assert "A*" in table
    assert "52" in table
    
    print("✓ render_comparison_table test passed")


def test_print_winners():
    """Test that winner printing works."""
    print("Testing print_winners...")
    
    results = [
        AlgoResult("BFS", 52, 2450.5, 45820),
        AlgoResult("DFS", 52, 1890.3, 38420),
        AlgoResult("A*", 52, 280.1, 892),
    ]
    
    # Capture output (just make sure it doesn't crash)
    print_winners(results)
    
    print("✓ print_winners test passed")


def test_full_solver_run():
    """Test a full solver run with a simple puzzle."""
    print("Testing full solver run...")
    
    rng = random.Random(123)
    
    # Generate a simple puzzle
    initial_board = generate_solvable_puzzle_4x4(shuffle_moves=4, rng=rng)
    
    # Run solvers
    results = run_single_puzzle(initial_board, GOAL_4x4, max_depth_for_dfs=10)
    
    # Check that we got results for all three algorithms
    assert len(results) == 3
    assert results[0].algorithm == "BFS"
    assert results[1].algorithm == "DFS"
    assert results[2].algorithm == "A*"
    
    # Check that all have the same number of moves (optimal)
    assert results[0].moves == results[1].moves == results[2].moves
    
    # Check that A* explored fewer nodes (it should be the most efficient)
    astar_nodes = results[2].nodes_explored
    bfs_nodes = results[0].nodes_explored
    assert astar_nodes <= bfs_nodes
    
    print("✓ full solver run test passed")


def main():
    """Run all tests."""
    print("=" * 50)
    print("Testing puzzle_4x4_solver.py")
    print("=" * 50)
    print()
    
    try:
        test_render_board_ascii_table()
        test_generate_solvable_puzzle()
        test_render_comparison_table()
        test_print_winners()
        test_full_solver_run()
        
        print()
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
        return 0
        
    except Exception as e:
        print()
        print("=" * 50)
        print(f"Test failed: {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
