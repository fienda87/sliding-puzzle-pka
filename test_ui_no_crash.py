#!/usr/bin/env python3
"""Quick test to verify the UI initializes without crashes."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "sliding_puzzle"))

import pygame

from game.puzzle_game import PuzzleGame
from ui.screens import GameScreen, MenuScreen
from utils.constants import LEVELS, WINDOW_HEIGHT, WINDOW_WIDTH


def test_ui_initialization() -> None:
    """Test that UI components initialize without crashes."""

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    menu_screen = MenuScreen(WINDOW_WIDTH, WINDOW_HEIGHT)
    menu_screen.render(screen)

    for grid_size, difficulties in LEVELS.items():
        for difficulty, level_data in difficulties.items():
            game = PuzzleGame(level_data["board"], level_data["goal"])
            game_screen = GameScreen(WINDOW_WIDTH, WINDOW_HEIGHT, level_data["grid_size"])

            game_screen.render(screen, game)

            initial_moves = game.moves
            initial_time = game.get_time_elapsed()

            if (
                game.move_blank_direction("UP")
                or game.move_blank_direction("DOWN")
                or game.move_blank_direction("LEFT")
                or game.move_blank_direction("RIGHT")
            ):
                assert game.moves == initial_moves + 1

            current_time = game.get_time_elapsed()
            assert current_time >= initial_time

            game_screen.render(screen, game)
            print(f"✓ UI renders for {grid_size}x{grid_size} {difficulty}")

    pygame.quit()


if __name__ == "__main__":
    test_ui_initialization()
