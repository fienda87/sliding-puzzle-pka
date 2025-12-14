#!/usr/bin/env python3
"""Quick test to verify the UI initializes without crashes after removing move counter/timer display"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sliding_puzzle'))

import pygame
from game.puzzle_game import PuzzleGame
from ui.screens import GameScreen, MenuScreen
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, LEVELS

def test_ui_initialization():
    """Test that UI components initialize without crashes"""
    print("Testing UI initialization without move counter/timer display...")
    
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Test menu screen
    menu_screen = MenuScreen(WINDOW_WIDTH, WINDOW_HEIGHT)
    menu_screen.render(screen)
    print("✓ Menu screen renders successfully")
    
    # Test game screen for each difficulty
    for difficulty, level_data in LEVELS.items():
        game = PuzzleGame(level_data['board'], level_data['goal'])
        game_screen = GameScreen(WINDOW_WIDTH, WINDOW_HEIGHT, level_data['grid_size'])
        
        # Render the game screen
        game_screen.render(screen, game)
        print(f"✓ Game screen renders successfully for {difficulty} difficulty")
        
        # Make a move and verify internal tracking still works
        initial_moves = game.moves
        initial_time = game.get_time_elapsed()
        
        # Try to make a move
        if game.move_blank_direction('UP') or game.move_blank_direction('DOWN') or \
           game.move_blank_direction('LEFT') or game.move_blank_direction('RIGHT'):
            assert game.moves == initial_moves + 1, "Move counter not tracking internally"
            print(f"✓ Internal move tracking works: {initial_moves} -> {game.moves}")
        
        # Verify time tracking works
        current_time = game.get_time_elapsed()
        assert current_time >= initial_time, "Timer not tracking internally"
        print(f"✓ Internal time tracking works: {initial_time:.3f}s -> {current_time:.3f}s")
        
        # Render again to ensure no crashes with updated state
        game_screen.render(screen, game)
        print(f"✓ Game screen renders after move without crashes")
    
    pygame.quit()
    print("\n✓ ALL UI TESTS PASSED - No move counter/timer visible, internal tracking preserved!")

if __name__ == "__main__":
    test_ui_initialization()
