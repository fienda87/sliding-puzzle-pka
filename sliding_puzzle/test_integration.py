"""Integration tests for solvers + metrics tracking."""

from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_astar, solve_bfs, solve_dfs
from utils.constants import GOAL_3x3, TEST_EASY_3x3, TEST_MEDIUM_3x3


def test_integration_all_solvers() -> None:
    test_cases = [("Easy (1 move)", TEST_EASY_3x3, GOAL_3x3), ("Medium", TEST_MEDIUM_3x3, GOAL_3x3)]

    for _, initial_board, goal_board in test_cases:
        bfs_result = solve_bfs(initial_board, goal_board)
        dfs_result = solve_dfs(initial_board, goal_board)
        astar_result = solve_astar(initial_board, goal_board)

        assert bfs_result is not None
        assert astar_result is not None

        assert bfs_result["moves"] == astar_result["moves"]

        if dfs_result is not None:
            assert "nodes_explored" in dfs_result


def test_game_integration() -> None:
    game = PuzzleGame(TEST_EASY_3x3, GOAL_3x3)

    result = solve_astar(game.current_board, game.goal_board)
    assert result is not None

    for state in result["solution_path"]:
        game.apply_board_state(state.board)

    assert game.is_solved()


def test_response_format() -> None:
    result = solve_astar(TEST_MEDIUM_3x3, GOAL_3x3)
    assert result is not None

    required_keys = {
        "path",
        "moves",
        "time_ms",
        "nodes_explored",
        "solution_path",
        "steps",
        "time_taken",
    }

    assert required_keys.issubset(result.keys())
    assert result["path"] == result["solution_path"]
    assert result["moves"] == result["steps"]
