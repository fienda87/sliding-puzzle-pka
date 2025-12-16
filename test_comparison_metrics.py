#!/usr/bin/env python3
"""Test that algorithm comparison metrics are tracked and rendered without crashes."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "sliding_puzzle"))

import pygame

from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_astar, solve_bfs, solve_dfs
from ui.screens import GameScreen
from utils.constants import LEVELS, WINDOW_HEIGHT, WINDOW_WIDTH


def test_algorithm_comparison_metrics() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    level_data = LEVELS[3]["medium"]
    game = PuzzleGame(level_data["board"], level_data["goal"])
    game_screen = GameScreen(WINDOW_WIDTH, WINDOW_HEIGHT, level_data["grid_size"])

    algorithms = [("BFS", solve_bfs), ("DFS", solve_dfs), ("A*", solve_astar)]

    for algo_name, solver_func in algorithms:
        result = solver_func(game.current_board, game.goal_board)

        assert "moves" in result
        assert "time_ms" in result
        assert "nodes_explored" in result

        game_screen.add_comparison_result(algo_name, result)

    assert len(game_screen.comparison_results) == 3

    game_screen.render(screen, game)

    initial_moves = game.moves
    initial_time = game.get_time_elapsed()

    if game.move_blank_direction("LEFT"):
        assert game.moves == initial_moves + 1

    current_time = game.get_time_elapsed()
    assert current_time >= initial_time

    game_screen.clear_comparison_table()
    assert len(game_screen.comparison_results) == 0

    pygame.quit()


if __name__ == "__main__":
    test_algorithm_comparison_metrics()
