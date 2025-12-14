"""
Test that the application can start without errors (no GUI)
"""
import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from game.puzzle_game import PuzzleGame
        print("  ✓ game.puzzle_game imported")
        
        from game.puzzle_solver import solve_bfs, solve_dfs, solve_astar
        print("  ✓ game.puzzle_solver imported")
        
        from game.puzzle_state import PuzzleState
        print("  ✓ game.puzzle_state imported")
        
        from utils.constants import LEVELS, GOAL_3x3, GOAL_4x4
        print("  ✓ utils.constants imported")
        
        print("\n✓ All imports successful!")
        return True
    except Exception as e:
        print(f"\n✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_level_loading():
    """Test that all levels can be loaded"""
    print("\nTesting level loading...")
    
    try:
        from game.puzzle_game import PuzzleGame
        from utils.constants import LEVELS
        
        for level_key, level_data in LEVELS.items():
            game = PuzzleGame(level_data['board'], level_data['goal'])
            print(f"  ✓ {level_key}: {level_data['name']}")
        
        print(f"\n✓ All {len(LEVELS)} levels loaded successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Level loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_game_initialization():
    """Test that games can be initialized for both grid sizes"""
    print("\nTesting game initialization...")
    
    try:
        from game.puzzle_game import PuzzleGame
        from utils.constants import GOAL_3x3, GOAL_4x4
        
        # Test 3x3
        game_3x3 = PuzzleGame(GOAL_3x3, GOAL_3x3)
        assert len(game_3x3.current_board) == 3
        print("  ✓ 3x3 game initialized")
        
        # Test 4x4
        game_4x4 = PuzzleGame(GOAL_4x4, GOAL_4x4)
        assert len(game_4x4.current_board) == 4
        print("  ✓ 4x4 game initialized")
        
        print("\n✓ Game initialization successful for both sizes!")
        return True
    except Exception as e:
        print(f"\n✗ Game initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("="*60)
    print("STARTUP TEST - NO GUI")
    print("="*60 + "\n")
    
    tests = [
        test_imports,
        test_level_loading,
        test_game_initialization
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "="*60)
    if all(results):
        print("✅ ALL STARTUP TESTS PASSED!")
        print("="*60)
        return 0
    else:
        print("❌ SOME STARTUP TESTS FAILED")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
