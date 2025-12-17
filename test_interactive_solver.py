#!/usr/bin/env python3
"""Test script for interactive puzzle solver functionality."""

import os
import sys
import subprocess
from io import StringIO
from unittest.mock import patch

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_interactive_mode_simulation():
    """Simulate interactive user inputs to test the menu system."""
    # Test inputs: BFS, DFS, A*, New Puzzle, Quit
    test_inputs = "1\n2\n3\n4\n5\n"
    
    # Capture output and simulate input
    with patch('builtins.input', side_effect=test_inputs.strip().split('\n')):
        with patch('sys.stdin.isatty', return_value=True):
            try:
                from puzzle_4x4_solver import main
                result = main([])
                print("✓ Interactive mode executed successfully")
                return True
            except Exception as e:
                print(f"✗ Interactive mode failed: {e}")
                return False

def test_menu_rendering():
    """Test that the menu renders correctly."""
    from puzzle_4x4_solver import render_menu, validate_menu_input
    
    menu = render_menu()
    required_elements = [
        "╔", "║", "╚", "BFS", "DFS", "A*", 
        "New Puzzle", "Quit", "Enter choice"
    ]
    
    for element in required_elements:
        if element not in menu:
            print(f"✗ Menu missing required element: {element}")
            return False
    
    # Test input validation
    valid_inputs = ["1", "2", "3", "4", "5"]
    invalid_inputs = ["0", "6", "abc", "", " "]
    
    for inp in valid_inputs:
        if validate_menu_input(inp) is None:
            print(f"✗ Valid input {inp} not accepted")
            return False
    
    for inp in invalid_inputs:
        if validate_menu_input(inp) is not None:
            print(f"✗ Invalid input {inp} was accepted")
            return False
    
    print("✓ Menu rendering and validation tests passed")
    return True

def test_backward_compatibility():
    """Test that headless mode still works with command line arguments."""
    try:
        result = subprocess.run([
            sys.executable, "puzzle_4x4_solver.py", 
            "--difficulty", "easy", "--seed", "1"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Check for expected output elements (headless mode doesn't have "Cumulative Comparison:")
            expected_elements = [
                "Initial State:", "Goal State:", 
                "BFS Algorithm:", "DFS Algorithm:", "A* Algorithm:",
                "Algoritma"
            ]
            
            # Additional elements that should be in the comparison table
            expected_table_elements = ["BFS", "DFS", "A*", "Moves", "Time (ms)", "Nodes Exp."]
            
            missing_elements = []
            for element in expected_elements:
                if element not in result.stdout:
                    missing_elements.append(element)
            
            # Also check table elements
            missing_table_elements = []
            for element in expected_table_elements:
                if element not in result.stdout:
                    missing_table_elements.append(element)
            
            if missing_elements:
                print(f"✗ Headless mode missing elements: {missing_elements}")
                return False
            
            if missing_table_elements:
                print(f"✗ Headless mode missing table elements: {missing_table_elements}")
                return False
            
            print("✓ Backward compatibility test passed")
            return True
        else:
            print(f"✗ Headless mode failed with return code {result.returncode}")
            print(f"stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Headless mode timed out")
        return False
    except Exception as e:
        print(f"✗ Headless mode test error: {e}")
        return False

def test_fair_comparison_logic():
    """Test that puzzle state management ensures fair comparison."""
    # This test verifies that the core puzzle management logic is correct
    # We can't easily test the full interactive loop without user simulation
    
    from puzzle_4x4_solver import (
        generate_solvable_puzzle_4x4, 
        copy_board,
        execute_algorithm,
        GOAL_4x4
    )
    
    # Generate a test puzzle
    import random
    rng = random.Random(42)
    initial_board = generate_solvable_puzzle_4x4(shuffle_moves=4, rng=rng)
    current_board = copy_board(initial_board)
    
    # Test that BFS works
    bfs_result = execute_algorithm("BFS", current_board, max_depth=20)
    if bfs_result is None:
        print("✗ BFS algorithm failed")
        return False
    
    # Test that puzzle state is preserved after algorithm execution
    # (since we copy the board before each algorithm)
    if current_board != initial_board:
        print("✗ Puzzle state was modified during algorithm execution")
        return False
    
    print("✓ Fair comparison logic test passed")
    return True

def main():
    """Run all tests."""
    print("Testing Interactive 4x4 Puzzle Solver...")
    print("=" * 50)
    
    tests = [
        ("Menu Rendering", test_menu_rendering),
        ("Backward Compatibility", test_backward_compatibility), 
        ("Fair Comparison Logic", test_fair_comparison_logic),
        ("Interactive Mode Simulation", test_interactive_mode_simulation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"  FAILED: {test_name}")
        except Exception as e:
            print(f"  ERROR: {test_name} - {e}")
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())