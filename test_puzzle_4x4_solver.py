#!/usr/bin/env python3

import os
import random
import sys
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from puzzle_4x4_solver import (  # noqa: E402
    ACTION_TO_DESCRIPTION,
    AlgoResult,
    GOAL_4x4,
    PuzzleState,
    board_list_repr,
    generate_solvable_puzzle_4x4,
    main,
    render_algorithm_steps,
    render_board_ascii_table,
    render_comparison_table,
    run_solver_timed,
    solve_all_algorithms,
    build_algo_results,
)


def _blank_pos(board: list[list[int]]) -> tuple[int, int]:
    for r, row in enumerate(board):
        for c, v in enumerate(row):
            if v == 0:
                return (r, c)
    raise AssertionError("No blank (0) found")


def _expected_action(prev: list[list[int]], curr: list[list[int]]) -> str:
    pr, pc = _blank_pos(prev)
    cr, cc = _blank_pos(curr)

    dr, dc = cr - pr, cc - pc
    if (dr, dc) == (-1, 0):
        return "UP"
    if (dr, dc) == (1, 0):
        return "DOWN"
    if (dr, dc) == (0, -1):
        return "LEFT"
    if (dr, dc) == (0, 1):
        return "RIGHT"
    raise AssertionError("Boards are not one blank move apart")


def _assert_one_blank_swap(prev: list[list[int]], curr: list[list[int]]) -> None:
    flat_prev = [v for row in prev for v in row]
    flat_curr = [v for row in curr for v in row]

    diffs = [i for i, (a, b) in enumerate(zip(flat_prev, flat_curr)) if a != b]
    assert len(diffs) == 2
    a1, a2 = flat_prev[diffs[0]], flat_prev[diffs[1]]
    b1, b2 = flat_curr[diffs[0]], flat_curr[diffs[1]]
    assert {a1, a2} == {0, b1, b2}  # includes blank and the swapped tile


def test_render_board_ascii_table():
    board = GOAL_4x4
    result = render_board_ascii_table(board)

    for ch in ("┌", "┐", "└", "┘", "├", "┤", "┬", "┴", "┼", "│", "─"):
        assert ch in result

    # Blank note should only appear when requested
    assert "(0 = blank)" not in result
    assert "(0 = blank)" in render_board_ascii_table(board, show_blank_note=True)


def test_generate_solvable_puzzle():
    rng = random.Random(42)
    puzzle = generate_solvable_puzzle_4x4(shuffle_moves=4, rng=rng)

    assert len(puzzle) == 4
    assert len(puzzle[0]) == 4
    assert puzzle != GOAL_4x4

    all_nums = {v for row in puzzle for v in row}
    assert all_nums == set(range(16))


def test_run_solver_timed_uses_perf_counter():
    def dummy_solver():
        s = PuzzleState(GOAL_4x4)
        return {
            "path": [s],
            "moves": 0,
            "time_ms": 0.0,
            "nodes_explored": 1,
            "solution_path": [s],
            "steps": 0,
            "time_taken": 0.0,
        }

    with patch("puzzle_4x4_solver.time.perf_counter", side_effect=[1.0, 1.25]):
        out = run_solver_timed(dummy_solver)

    assert out is not None
    assert abs(float(out["time_ms"]) - 250.0) < 1e-9
    assert abs(float(out["time_taken"]) - 0.25) < 1e-9


def test_solvers_and_steps_output():
    rng = random.Random(123)
    initial_board = generate_solvable_puzzle_4x4(shuffle_moves=8, rng=rng)

    solver_results = solve_all_algorithms(initial_board, GOAL_4x4, max_depth_for_dfs=30)

    for algo in ("BFS", "DFS", "A*"):
        res = solver_results[algo]
        path = res["solution_path"]

        assert path[0].board == initial_board
        assert path[-1].board == GOAL_4x4

        # Verify transitions are logical and action matches blank movement
        for i in range(1, len(path)):
            prev = path[i - 1]
            curr = path[i]
            _assert_one_blank_swap(prev.board, curr.board)
            assert curr.action == _expected_action(prev.board, curr.board)

        out = render_algorithm_steps(algo, path)
        assert f"{algo} Algorithm:" in out
        assert "[First 5 Steps]" in out
        assert "[Last 5 Steps]" in out

        moves = len(path) - 1
        step1_expected = f"Step 1: {board_list_repr(path[1].board)}"
        assert step1_expected in out

        last_expected = f"Step {moves}: {board_list_repr(GOAL_4x4)} → SOLVED! ✓"
        assert last_expected in out

        # Ensure non-final step includes a move description
        if moves > 1:
            first_action_desc = ACTION_TO_DESCRIPTION[path[1].action]
            assert f"Step 1: {board_list_repr(path[1].board)} → {first_action_desc}" in out


def test_steps_ellipsis_formatting_for_long_solutions():
    # We only validate the formatting rule here (not the correctness of the states)
    states = [PuzzleState(GOAL_4x4)]
    for i in range(12):
        states.append(PuzzleState(GOAL_4x4, parent=states[-1], action="UP", level=i + 1))

    out = render_algorithm_steps("BFS", states)
    assert "... [2 more steps] ..." in out
    assert "[First 5 Steps]" in out
    assert "[Last 5 Steps]" in out


def test_render_comparison_table():
    results = [
        AlgoResult("BFS", 8, 37.2, 1222),
        AlgoResult("DFS", 8, 18.9, 2380),
        AlgoResult("A*", 8, 0.4, 14),
    ]

    table = render_comparison_table(results)
    assert "┌" in table
    assert "Algoritma" in table
    assert "Moves" in table
    assert "Time (ms)" in table
    assert "Nodes Exp." in table
    assert "BFS" in table
    assert "DFS" in table
    assert "A*" in table


def test_main_output_structure_is_clean():
    buf = StringIO()
    with redirect_stdout(buf):
        main(["--seed", "1", "--shuffle-moves", "4"])

    out = buf.getvalue()

    assert "Initial State:" in out
    assert "Goal State:" in out
    assert "BFS Algorithm:" in out
    assert "DFS Algorithm:" in out
    assert "A* Algorithm:" in out

    # Clean comparison table should exist
    assert "│ Algoritma" in out

    # No progress indicator clutter
    assert "Running BFS" not in out


def test_build_algo_results_metrics_consistent():
    rng = random.Random(999)
    initial_board = generate_solvable_puzzle_4x4(shuffle_moves=4, rng=rng)
    solver_results = solve_all_algorithms(initial_board, GOAL_4x4, max_depth_for_dfs=20)

    algo_results = build_algo_results(solver_results)
    assert [r.algorithm for r in algo_results] == ["BFS", "DFS", "A*"]

    for r in algo_results:
        assert r.moves == int(solver_results[r.algorithm]["moves"])
        assert r.nodes_explored == int(solver_results[r.algorithm]["nodes_explored"])
        assert r.time_ms == float(solver_results[r.algorithm]["time_ms"])
