from game.puzzle_solver import (
    manhattan_distance,
    precompute_goal_positions,
    solve_astar,
    solve_bfs,
    solve_dfs,
)
from utils.constants import GOAL_3x3, GOAL_4x4, TEST_EXPERT_4x4, TEST_HARD_3x3, TEST_MEDIUM_3x3


def test_manhattan_distance() -> None:
    goal_positions = precompute_goal_positions(GOAL_3x3)

    assert manhattan_distance(GOAL_3x3, goal_positions) == 0
    assert manhattan_distance([[1, 2, 3], [4, 5, 6], [7, 0, 8]], goal_positions) == 1


def test_astar_easy_puzzle_already_solved() -> None:
    result = solve_astar(GOAL_3x3, GOAL_3x3)

    assert result is not None
    assert result["moves"] == 0
    assert result["nodes_explored"] == 1
    assert len(result["path"]) == 1


def test_astar_one_move_puzzle() -> None:
    result = solve_astar([[1, 2, 3], [4, 5, 6], [7, 0, 8]], GOAL_3x3)

    assert result is not None
    assert result["moves"] == 1


def test_astar_medium_puzzle() -> None:
    result = solve_astar(TEST_MEDIUM_3x3, GOAL_3x3)

    assert result is not None
    assert result["moves"] >= 1
    assert len(result["path"]) == result["moves"] + 1


def test_response_format_consistency() -> None:
    initial_board = TEST_MEDIUM_3x3
    goal_board = GOAL_3x3

    bfs_result = solve_bfs(initial_board, goal_board)
    dfs_result = solve_dfs(initial_board, goal_board)
    astar_result = solve_astar(initial_board, goal_board)

    required_keys = {"path", "moves", "time_ms", "nodes_explored", "solution_path", "steps", "time_taken"}

    for result in (bfs_result, dfs_result, astar_result):
        assert result is not None
        assert required_keys.issubset(result.keys())


def test_astar_vs_bfs_optimality() -> None:
    bfs_result = solve_bfs(TEST_MEDIUM_3x3, GOAL_3x3)
    astar_result = solve_astar(TEST_MEDIUM_3x3, GOAL_3x3)

    assert bfs_result is not None
    assert astar_result is not None
    assert bfs_result["moves"] == astar_result["moves"]


def test_hard_puzzle() -> None:
    result = solve_astar(TEST_HARD_3x3, GOAL_3x3)

    assert result is not None
    assert result["moves"] >= 10
    assert len(result["path"]) == result["moves"] + 1


def test_4x4_manhattan_distance_only() -> None:
    goal_positions = precompute_goal_positions(GOAL_4x4)
    assert manhattan_distance(TEST_EXPERT_4x4, goal_positions) >= 0
