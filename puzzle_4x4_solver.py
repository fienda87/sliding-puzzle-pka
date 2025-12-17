#!/usr/bin/env python3
"""Headless 4x4 sliding puzzle solver (Google Colab friendly).

This script prints output in 3 parts:
1) Initial & Goal state (ASCII table with box-drawing chars)
2) Algorithm steps (BFS, DFS, A*) showing first 5 + last 5 steps
3) Clean comparison table + winners

Usage (Colab / local):
    !python puzzle_4x4_solver.py

Optional arguments:
    !python puzzle_4x4_solver.py --difficulty hard --shuffle-moves 12 --seed 123

Notes:
- Pure Python (no pygame).
- Uses the existing solver implementations in sliding_puzzle/game.
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time
from dataclasses import dataclass


REPO_DIR = os.path.dirname(os.path.abspath(__file__))
SLIDING_PUZZLE_DIR = os.path.join(REPO_DIR, "sliding_puzzle")
if SLIDING_PUZZLE_DIR not in sys.path:
    sys.path.insert(0, SLIDING_PUZZLE_DIR)

from game.puzzle_state import PuzzleState  # noqa: E402
from game import puzzle_solver  # noqa: E402


Board = list[list[int]]

GOAL_4x4: Board = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0],
]

DIFFICULTY_TO_SHUFFLE_MOVES: dict[str, int] = {
    "easy": 4,
    "medium": 8,
    "hard": 12,
}

OPPOSITE_MOVE: dict[str, str] = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
}

ACTION_TO_DESCRIPTION: dict[str, str] = {
    "UP": "Move blank up",
    "DOWN": "Move blank down",
    "LEFT": "Move blank left",
    "RIGHT": "Move blank right",
}


def copy_board(board: Board) -> Board:
    return [row[:] for row in board]


def flatten_board(board: Board) -> list[int]:
    return [v for row in board for v in row]


def board_list_repr(board: Board) -> str:
    return "[" + ",".join(str(v) for v in flatten_board(board)) + "]"


def render_board_ascii_table(board: Board, *, show_blank_note: bool = False) -> str:
    size = len(board)

    max_num = max(max(row) for row in board)
    cell_width = max(len(str(max_num)), 2)

    def border(left: str, mid: str, right: str) -> str:
        return left + mid.join("─" * (cell_width + 2) for _ in range(size)) + right

    lines: list[str] = []
    lines.append(border("┌", "┬", "┐"))

    for i, row in enumerate(board):
        cells = [f" {str(v).ljust(cell_width)} " for v in row]
        line = "│" + "│".join(cells) + "│"
        if show_blank_note and i == size - 1:
            line += " (0 = blank)"
        lines.append(line)

        if i < size - 1:
            lines.append(border("├", "┼", "┤"))

    lines.append(border("└", "┴", "┘"))
    return "\n".join(lines)


def generate_solvable_puzzle_4x4(shuffle_moves: int, rng: random.Random) -> Board:
    if shuffle_moves <= 0:
        raise ValueError("shuffle_moves must be >= 1")

    while True:
        state = PuzzleState(GOAL_4x4)
        last_move: str | None = None
        seen = {state.get_board_tuple()}
        completed = True

        for _ in range(shuffle_moves):
            possible = state.get_possible_moves()

            if last_move is not None:
                possible = [
                    s for s in possible if s.action is None or s.action != OPPOSITE_MOVE[last_move]
                ]

            non_repeating = [s for s in possible if s.get_board_tuple() not in seen]
            if non_repeating:
                possible = non_repeating

            if not possible:
                completed = False
                break

            state = rng.choice(possible)
            last_move = state.action
            seen.add(state.get_board_tuple())

        if completed and state.board != GOAL_4x4:
            return copy_board(state.board)


@dataclass(frozen=True)
class AlgoResult:
    algorithm: str
    moves: int
    time_ms: float
    nodes_explored: int


def _format_result_without_time(
    solution_path: list[PuzzleState], nodes_explored: int
) -> dict[str, object]:
    moves = len(solution_path) - 1
    return {
        "path": solution_path,
        "moves": moves,
        "time_ms": 0.0,
        "nodes_explored": nodes_explored,
        "solution_path": solution_path,
        "steps": moves,
        "time_taken": 0.0,
    }


def solve_iddfs(initial_board: Board, goal_board: Board, max_depth: int) -> dict[str, object] | None:
    initial_state = PuzzleState(initial_board)

    if initial_state.is_goal(goal_board):
        return _format_result_without_time([initial_state], 1)

    nodes_explored = 0

    def dfs_limited(
        state: PuzzleState, remaining_depth: int, path_set: set[tuple[tuple[int, ...], ...]]
    ) -> PuzzleState | None:
        nonlocal nodes_explored
        nodes_explored += 1

        if state.is_goal(goal_board):
            return state
        if remaining_depth == 0:
            return None

        for next_state in state.get_possible_moves():
            t = next_state.get_board_tuple()
            if t in path_set:
                continue

            path_set.add(t)
            found = dfs_limited(next_state, remaining_depth - 1, path_set)
            if found is not None:
                return found
            path_set.remove(t)

        return None

    for limit in range(max_depth + 1):
        path_set = {initial_state.get_board_tuple()}
        found_goal_state = dfs_limited(initial_state, limit, path_set)
        if found_goal_state is not None:
            solution_path = puzzle_solver.build_solution_path(found_goal_state)
            return _format_result_without_time(solution_path, nodes_explored)

    return None


def run_solver_timed(func, *args, **kwargs) -> dict[str, object] | None:
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()

    if result is None:
        return None

    out = dict(result)
    out["time_ms"] = (end - start) * 1000
    out["time_taken"] = end - start
    return out


def solve_all_algorithms(
    initial_board: Board, goal_board: Board, *, max_depth_for_dfs: int
) -> dict[str, dict[str, object]]:
    bfs = run_solver_timed(puzzle_solver.solve_bfs, initial_board, goal_board)
    dfs = run_solver_timed(solve_iddfs, initial_board, goal_board, max_depth_for_dfs)
    astar = run_solver_timed(puzzle_solver.solve_astar, initial_board, goal_board)

    if bfs is None or dfs is None or astar is None:
        raise RuntimeError(
            "One of the solvers returned no solution (puzzle too hard / depth limit too low)."
        )

    bfs_moves = int(bfs["moves"])
    dfs_moves = int(dfs["moves"])
    astar_moves = int(astar["moves"])

    if not (bfs_moves == dfs_moves == astar_moves):
        raise RuntimeError(
            "Move counts differ (expected all optimal). "
            f"BFS={bfs_moves} DFS={dfs_moves} A*={astar_moves}."
        )

    return {"BFS": bfs, "DFS": dfs, "A*": astar}


def build_algo_results(solver_results: dict[str, dict[str, object]]) -> list[AlgoResult]:
    ordered = [
        ("BFS", solver_results["BFS"]),
        ("DFS", solver_results["DFS"]),
        ("A*", solver_results["A*"]),
    ]

    return [
        AlgoResult(
            algo,
            int(res["moves"]),
            float(res["time_ms"]),
            int(res["nodes_explored"]),
        )
        for algo, res in ordered
    ]


def render_algorithm_steps(algorithm: str, solution_path: list[PuzzleState]) -> str:
    total_moves = len(solution_path) - 1
    if total_moves < 0:
        total_moves = 0

    lines: list[str] = [f"{algorithm} Algorithm:"]

    if total_moves == 0:
        lines.append("[First 5 Steps]")
        lines.append(f"Step 0: {board_list_repr(solution_path[0].board)} → SOLVED! ✓")
        lines.append("[Last 5 Steps]")
        lines.append(f"Step 0: {board_list_repr(solution_path[0].board)} → SOLVED! ✓")
        return "\n".join(lines)

    first_end = min(5, total_moves)
    lines.append("[First 5 Steps]")
    for i in range(1, first_end + 1):
        step_state = solution_path[i]
        desc = ACTION_TO_DESCRIPTION.get(step_state.action or "", "")
        if i == total_moves:
            desc = "SOLVED! ✓"
        lines.append(f"Step {i}: {board_list_repr(step_state.board)} → {desc}")

    if total_moves > 10:
        lines.append(f"... [{total_moves - 10} more steps] ...")

    last_start = max(1, total_moves - 4)
    lines.append("[Last 5 Steps]")
    for i in range(last_start, total_moves + 1):
        step_state = solution_path[i]
        desc = ACTION_TO_DESCRIPTION.get(step_state.action or "", "")
        if i == total_moves:
            desc = "SOLVED! ✓"
        lines.append(f"Step {i}: {board_list_repr(step_state.board)} → {desc}")

    return "\n".join(lines)


def render_comparison_table(results: list[AlgoResult]) -> str:
    headers = ["Algoritma", "Moves", "Time (ms)", "Nodes Exp."]

    rows: list[list[str]] = []
    for r in results:
        rows.append([r.algorithm, str(r.moves), f"{int(round(r.time_ms))} ms", str(r.nodes_explored)])

    col_widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows)) for i in range(len(headers))
    ]

    def hline(left: str, mid: str, right: str, fill: str = "─") -> str:
        pieces = [fill * (w + 2) for w in col_widths]
        return left + mid.join(pieces) + right

    def format_row(values: list[str]) -> str:
        cells = []
        for i, v in enumerate(values):
            if i == 0:
                cells.append(f" {v.ljust(col_widths[i])} ")
            else:
                cells.append(f" {v.rjust(col_widths[i])} ")
        return "│" + "│".join(cells) + "│"

    out: list[str] = []
    out.append(hline("┌", "┬", "┐"))
    out.append(format_row(headers))
    out.append(hline("├", "┼", "┤"))
    for row in rows:
        out.append(format_row(row))
    out.append(hline("└", "┴", "┘"))
    return "\n".join(out)


def print_winners(results: list[AlgoResult]) -> None:
    fastest = min(results, key=lambda r: r.time_ms)
    least_nodes = min(results, key=lambda r: r.nodes_explored)

    print(f"Winner (Fastest): {fastest.algorithm} - {int(round(fastest.time_ms))} ms")
    print(
        f"Winner (Least Nodes Explored): {least_nodes.algorithm} - {least_nodes.nodes_explored} nodes"
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Puzzle 4x4 Solver (Headless, Colab-friendly)")

    parser.add_argument(
        "--difficulty",
        choices=sorted(DIFFICULTY_TO_SHUFFLE_MOVES.keys()),
        default="medium",
        help="Difficulty controls how many random blank moves are applied to the goal.",
    )
    parser.add_argument(
        "--shuffle-moves",
        type=int,
        default=None,
        help="Override the number of shuffle moves (kept low so BFS is feasible).",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility.")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    shuffle_moves = (
        int(args.shuffle_moves)
        if args.shuffle_moves is not None
        else DIFFICULTY_TO_SHUFFLE_MOVES[args.difficulty]
    )
    if shuffle_moves <= 0:
        raise SystemExit("shuffle_moves must be >= 1")

    rng = random.Random(args.seed)

    initial_board = generate_solvable_puzzle_4x4(shuffle_moves=shuffle_moves, rng=rng)

    print("Initial State:")
    print(render_board_ascii_table(initial_board, show_blank_note=True))
    print()

    print("Goal State:")
    print(render_board_ascii_table(GOAL_4x4))
    print()

    max_depth = max(shuffle_moves * 2, 20)
    solver_results = solve_all_algorithms(initial_board, GOAL_4x4, max_depth_for_dfs=max_depth)

    for algo in ("BFS", "DFS", "A*"):
        solution_path = solver_results[algo]["solution_path"]
        print(render_algorithm_steps(algo, solution_path))
        print()

    results = build_algo_results(solver_results)

    print(render_comparison_table(results))
    print()
    print_winners(results)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
