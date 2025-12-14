from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_bfs
from game.puzzle_state import PuzzleState
from utils.constants import GOAL_3x3, TEST_EASY_3x3


def test_puzzle_state_basics() -> None:
    state = PuzzleState(TEST_EASY_3x3)
    assert state.blank_pos == (2, 1)
    assert state.is_goal(GOAL_3x3) is False
    assert len(state.get_possible_moves()) > 0


def test_bfs_solver_smoke() -> None:
    result = solve_bfs(TEST_EASY_3x3, GOAL_3x3)
    assert result is not None
    assert result["moves"] == 1


def test_puzzle_game_smoke() -> None:
    game = PuzzleGame(TEST_EASY_3x3, GOAL_3x3)
    assert game.moves == 0
    assert game.is_solved() is False

    assert game.handle_tile_click(2, 2) is True
    assert game.moves == 1
    assert game.is_solved() is True
