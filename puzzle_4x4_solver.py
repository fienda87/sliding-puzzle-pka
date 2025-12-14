#!/usr/bin/env python3
"""Headless 4x4 sliding puzzle solver script (Google Colab friendly).

Usage (Colab / local):
    !python puzzle_4x4_solver.py

Optional:
    !python puzzle_4x4_solver.py --difficulty hard --runs 3 --verbose

Notes:
- No pygame dependency.
- Imports the existing solver modules from this repository.
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


def copy_board(board: Board) -> Board:
    return [row[:] for row in board]


def format_board(board: Board) -> str:
    width = len(str(max(max(row) for row in board)))
    lines: list[str] = []
    for row in board:
        parts = []
        for v in row:
            parts.append(".".rjust(width) if v == 0 else str(v).rjust(width))
        lines.append(" ".join(parts))
    return "\n".join(lines)


def generate_solvable_puzzle_4x4(shuffle_moves: int, rng: random.Random) -> Board:
    """Generate a random solvable 4x4 board by shuffling from the goal."""

    if shuffle_moves <= 0:
        raise ValueError("shuffle_moves must be >= 1")

    while True:
        state = PuzzleState(GOAL_4x4)
        last_move: str | None = None

        for _ in range(shuffle_moves):
            possible = state.get_possible_moves()

            if last_move is not None:
                possible = [
                    s for s in possible if s.action is None or s.action != OPPOSITE_MOVE[last_move]
                ]

            if not possible:
                possible = state.get_possible_moves()

            state = rng.choice(possible)
            last_move = state.action

        if state.board != GOAL_4x4:
            return copy_board(state.board)


@dataclass(frozen=True)
class AlgoResult:
    algorithm: str
    moves: int
    time_ms: float
    nodes_explored: int


def solve_iddfs(initial_board: Board, goal_board: Board, max_depth: int) -> dict[str, object] | None:
    """Solve with Iterative Deepening DFS (optimal for unit-cost moves)."""

    start_time = time.time()
    initial_state = PuzzleState(initial_board)

    if initial_state.is_goal(goal_board):
        return puzzle_solver.format_result([initial_state], 1, start_time)

    nodes_explored = 0

    def dfs_limited(state: PuzzleState, remaining_depth: int, path_set: set[tuple[tuple[int, ...], ...]]):
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
            return puzzle_solver.format_result(solution_path, nodes_explored, start_time)

    return None


def render_comparison_table(results: list[AlgoResult]) -> str:
    headers = ["Algoritma", "Moves", "Time (ms)", "Nodes Exp."]

    rows = []
    for r in results:
        rows.append(
            [
                r.algorithm,
                str(r.moves),
                f"{int(round(r.time_ms))} ms",
                str(r.nodes_explored),
            ]
        )

    col_widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows))
        for i in range(len(headers))
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


def run_single_puzzle(initial_board: Board, goal_board: Board, max_depth_for_dfs: int) -> list[AlgoResult]:
    bfs = puzzle_solver.solve_bfs(initial_board, goal_board)
    dfs = solve_iddfs(initial_board, goal_board, max_depth=max_depth_for_dfs)
    astar = puzzle_solver.solve_astar(initial_board, goal_board)

    if bfs is None or dfs is None or astar is None:
        raise RuntimeError("One of the solvers returned no solution (puzzle too hard / depth limit too low).")

    bfs_moves = int(bfs["moves"])
    dfs_moves = int(dfs["moves"])
    astar_moves = int(astar["moves"])

    if not (bfs_moves == dfs_moves == astar_moves):
        raise RuntimeError(
            "Move counts differ (expected all optimal). "
            f"BFS={bfs_moves} DFS={dfs_moves} A*={astar_moves}."
        )

    return [
        AlgoResult("BFS", bfs_moves, float(bfs["time_ms"]), int(bfs["nodes_explored"])),
        AlgoResult("DFS", dfs_moves, float(dfs["time_ms"]), int(dfs["nodes_explored"])),
        AlgoResult("A*", astar_moves, float(astar["time_ms"]), int(astar["nodes_explored"])),
    ]


def aggregate_results(all_runs: list[list[AlgoResult]]) -> list[AlgoResult]:
    by_algo: dict[str, list[AlgoResult]] = {}
    for run in all_runs:
        for r in run:
            by_algo.setdefault(r.algorithm, []).append(r)

    aggregated: list[AlgoResult] = []
    for algo in ["BFS", "DFS", "A*"]:
        items = by_algo[algo]
        moves = int(round(sum(i.moves for i in items) / len(items)))
        time_ms = sum(i.time_ms for i in items) / len(items)
        nodes_explored = int(round(sum(i.nodes_explored for i in items) / len(items)))
        aggregated.append(AlgoResult(algo, moves, time_ms, nodes_explored))

    return aggregated


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
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of random puzzles to run (results are averaged).",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each generated puzzle board.",
    )

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
    if int(args.runs) <= 0:
        raise SystemExit("runs must be >= 1")

    rng = random.Random(args.seed)

    title = "Puzzle 4x4 Solver - Headless Mode"
    print(title)
    print("━" * len(title))
    print()

    all_runs: list[list[AlgoResult]] = []

    for run_idx in range(1, int(args.runs) + 1):
        initial_board = generate_solvable_puzzle_4x4(shuffle_moves=shuffle_moves, rng=rng)

        if args.verbose:
            print(f"Run {run_idx}/{args.runs} - difficulty={args.difficulty}, shuffle_moves={shuffle_moves}")
            print(format_board(initial_board))
            print()

        # For IDDFS, we cap the depth to the shuffle length (a solution of that length is guaranteed).
        run_results = run_single_puzzle(initial_board, GOAL_4x4, max_depth_for_dfs=shuffle_moves)
        all_runs.append(run_results)

    results = aggregate_results(all_runs)
    print(render_comparison_table(results))
    print()

    fastest = min(results, key=lambda r: r.time_ms)
    print(f"Winner (Fastest): {fastest.algorithm} - {int(round(fastest.time_ms))} ms")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
