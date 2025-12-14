"""
Test that all difficulty presets can be properly loaded and initialized
"""
import pygame
from game.puzzle_game import PuzzleGame
from ui.screens import GameScreen
from utils.constants import LEVELS, WINDOW_WIDTH, WINDOW_HEIGHT

pygame.init()


def test_all_difficulty_presets():
    """Test that all difficulty presets can be initialized"""
    print("Testing all difficulty presets...\n")
    
    for difficulty_key, level_data in LEVELS.items():
        print(f"Testing {difficulty_key}: {level_data['name']}")
        
        assert 'board' in level_data, f"Missing 'board' in {difficulty_key}"
        assert 'goal' in level_data, f"Missing 'goal' in {difficulty_key}"
        assert 'grid_size' in level_data, f"Missing 'grid_size' in {difficulty_key}"
        assert 'name' in level_data, f"Missing 'name' in {difficulty_key}"
        assert 'description' in level_data, f"Missing 'description' in {difficulty_key}"
        assert 'shuffles' in level_data, f"Missing 'shuffles' in {difficulty_key}"
        
        grid_size = level_data['grid_size']
        assert grid_size in [3, 4], f"Invalid grid size {grid_size} for {difficulty_key}"
        
        assert len(level_data['board']) == grid_size, f"Board size mismatch for {difficulty_key}"
        assert len(level_data['goal']) == grid_size, f"Goal size mismatch for {difficulty_key}"
        
        for row in level_data['board']:
            assert len(row) == grid_size, f"Board row size mismatch for {difficulty_key}"
        
        for row in level_data['goal']:
            assert len(row) == grid_size, f"Goal row size mismatch for {difficulty_key}"
        
        game = PuzzleGame(level_data['board'], level_data['goal'])
        assert game is not None, f"Failed to create game for {difficulty_key}"
        print(f"  ✓ PuzzleGame created successfully")
        
        game_screen = GameScreen(WINDOW_WIDTH, WINDOW_HEIGHT, level_data['grid_size'])
        assert game_screen is not None, f"Failed to create game screen for {difficulty_key}"
        print(f"  ✓ GameScreen created successfully")
        
        assert game_screen.grid_size == grid_size, f"Grid size mismatch in GameScreen for {difficulty_key}"
        print(f"  ✓ Grid size: {grid_size}x{grid_size}")
        
        print(f"  ✓ Shuffles: {level_data['shuffles']}")
        print(f"  ✓ {difficulty_key} passed!\n")
    
    print(f"✓ All {len(LEVELS)} difficulty presets tested successfully!")


def test_3x3_and_4x4_coverage():
    """Test that we have both 3x3 and 4x4 difficulties"""
    print("\nTesting 3x3 and 4x4 coverage...")
    
    grid_3x3_count = sum(1 for level in LEVELS.values() if level['grid_size'] == 3)
    grid_4x4_count = sum(1 for level in LEVELS.values() if level['grid_size'] == 4)
    
    print(f"  3x3 difficulties: {grid_3x3_count}")
    print(f"  4x4 difficulties: {grid_4x4_count}")
    
    assert grid_3x3_count > 0, "Should have at least one 3x3 difficulty"
    assert grid_4x4_count > 0, "Should have at least one 4x4 difficulty"
    
    print("  ✓ Both 3x3 and 4x4 difficulties are available!")


def test_tile_scaling():
    """Test that tiles scale correctly for different grid sizes"""
    print("\nTesting tile scaling...")
    
    from ui.components import GameBoard
    
    board_3x3 = GameBoard(0, 0, 3)
    board_4x4 = GameBoard(0, 0, 4)
    
    print(f"  3x3 tile size: {board_3x3.tile_size}px")
    print(f"  4x4 tile size: {board_4x4.tile_size}px")
    print(f"  3x3 font size: {board_3x3.font_size}")
    print(f"  4x4 font size: {board_4x4.font_size}")
    
    assert board_4x4.tile_size < board_3x3.tile_size, "4x4 tiles should be smaller than 3x3"
    assert board_4x4.font_size < board_3x3.font_size, "4x4 font should be smaller than 3x3"
    
    print("  ✓ Tile scaling works correctly!")


def run_all_tests():
    print("="*60)
    print("Testing Difficulty Presets and Grid Support")
    print("="*60 + "\n")
    
    try:
        test_all_difficulty_presets()
        test_3x3_and_4x4_coverage()
        test_tile_scaling()
        
        print("\n" + "="*60)
        print("✓ ALL DIFFICULTY PRESET TESTS PASSED!")
        print("="*60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
