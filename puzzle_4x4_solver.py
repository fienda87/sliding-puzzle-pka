#!/usr/bin/env python3
"""Headless 4x4 sliding puzzle solver script (Google Colab friendly).

Usage (Colab / local):
    !python puzzle_4x4_solver.py

Optional with arguments:
    !python puzzle_4x4_solver.py --difficulty hard --shuffle-moves 15

Notes:
- No pygame dependency.
- Imports the existing solver modules from this repository.
- Displays detailed output with ASCII tables and progress indicators.
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
    """Create a deep copy of a board."""
    return [row[:] for row in board]


def render_board_ascii_table(board: Board, title: str = "") -> str:
    """Render a board as an ASCII table with box-drawing characters.
    
    Example output:
    ┌────┬────┬────┬────┐
    │ 1  │ 2  │ 3  │ 4  │
    ├────┼────┼────┼────┤
    │ 5  │ 6  │ 7  │ 8  │
    ├────┼────┼────┼────┤
    │ 9  │ 10 │ 11 │ 12 │
    ├────┼────┼────┼────┤
    │ 13 │ 14 │ 15 │ 0  │
    └────┴────┴────┴────┘
    """
    size = len(board)
    
    # Determine cell width based on largest number
    max_num = max(max(row) for row in board)
    cell_width = max(len(str(max_num)), 2)
    
    lines: list[str] = []
    
    # Title
    if title:
        lines.append(title)
    
    # Top border
    lines.append("┌" + "┬".join("─" * (cell_width + 2) for _ in range(size)) + "┐")
    
    # Rows with data
    for i, row in enumerate(board):
        cells = []
        for value in row:
            if value == 0:
                display = "0"
            else:
                display = str(value)
            cells.append(f" {display.ljust(cell_width)} ")
        lines.append("│" + "│".join(cells) + "│")
        
        # Add middle border between rows
        if i < size - 1:
            lines.append("├" + "┼".join("─" * (cell_width + 2) for _ in range(size)) + "┤")
    
    # Bottom border
    lines.append("└" + "┴".join("─" * (cell_width + 2) for _ in range(size)) + "┘")
    
    # Add note about blank tile
    if title:
        lines.append("(0 = blank)")
    
    return "\n".join(lines)


def generate_solvable_puzzle_4x4(shuffle_moves: int, rng: random.Random) -> Board:
    """Generate a random solvable 4x4 board by shuffling from the goal.
    
    Args:
        shuffle_moves: Number of random moves to apply to goal state
        rng: Random number generator for reproducibility
        
    Returns:
        A solvable 4x4 puzzle board
    """
    if shuffle_moves <= 0:
        raise ValueError("shuffle_moves must be >= 1")

    while True:
        state = PuzzleState(GOAL_4x4)
        last_move: str | None = None

        for _ in range(shuffle_moves):
            possible = state.get_possible_moves()

            # Avoid immediate reversal of last move for more interesting puzzles
            if last_move is not None:
                possible = [
                    s for s in possible if s.action is None or s.action != OPPOSITE_MOVE[last_move]
                ]

            if not possible:
                possible = state.get_possible_moves()

            state = rng.choice(possible)
            last_move = state.action

        # Ensure we got a different board from the goal
        if state.board != GOAL_4x4:
            return copy_board(state.board)


@dataclass(frozen=True)
class AlgoResult:
    """Result of running a single algorithm."""
    algorithm: str
    moves: int
    time_ms: float
    nodes_explored: int


def solve_iddfs(initial_board: Board, goal_board: Board, max_depth: int) -> dict[str, object] | None:
    """Solve with Iterative Deepening DFS (optimal for unit-cost moves).
    
    This provides an optimal solution like BFS but with better memory usage.
    """
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
    """Render comparison table with box-drawing characters.
    
    Example output:
    ┌─────────────┬───────────┬──────────┬─────────────┐
    │ Algoritma   │ Moves     │ Time (ms)│ Nodes Exp.  │
    ├─────────────┼───────────┼──────────┼─────────────┤
    │ BFS         │ 52        │ 2450 ms  │ 45820       │
    │ DFS         │ 52        │ 1890 ms  │ 38420       │
    │ A*          │ 52        │ 280 ms   │ 892         │
    └─────────────┴───────────┴──────────┴─────────────┘
    """
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

    # Calculate column widths
    col_widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]

    def hline(left: str, mid: str, right: str, fill: str = "─") -> str:
        """Generate horizontal line for table borders."""
        pieces = [fill * (w + 2) for w in col_widths]
        return left + mid.join(pieces) + right

    def format_row(values: list[str]) -> str:
        """Format a row with proper alignment."""
        cells = []
        for i, v in enumerate(values):
            if i == 0:
                # Left-align algorithm name
                cells.append(f" {v.ljust(col_widths[i])} ")
            else:
                # Right-align numbers
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
    """Run all three algorithms on a single puzzle and return results.
    
    Displays progress indicators while running.
    """
    results = []
    
    # Run BFS
    print("Running BFS... ⏳", end="", flush=True)
    bfs = puzzle_solver.solve_bfs(initial_board, goal_board)
    print("\rRunning BFS... ✓ ")
    
    # Run DFS
    print("Running DFS... ⏳", end="", flush=True)
    dfs = solve_iddfs(initial_board, goal_board, max_depth=max_depth_for_dfs)
    print("\rRunning DFS... ✓ ")
    
    # Run A*
    print("Running A*... ⏳", end="", flush=True)
    astar = puzzle_solver.solve_astar(initial_board, goal_board)
    print("\rRunning A*... ✓  ")
    print()

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


def print_winners(results: list[AlgoResult]) -> None:
    """Print winner highlights for fastest and least nodes explored."""
    fastest = min(results, key=lambda r: r.time_ms)
    least_nodes = min(results, key=lambda r: r.nodes_explored)
    
    print(f"Winner (Fastest): {fastest.algorithm} - {int(round(fastest.time_ms))} ms")
    print(f"Winner (Least Nodes Explored): {least_nodes.algorithm} - {least_nodes.nodes_explored} nodes")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
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
    """Main entry point for the script."""
    args = parse_args(sys.argv[1:] if argv is None else argv)

    shuffle_moves = (
        int(args.shuffle_moves)
        if args.shuffle_moves is not None
        else DIFFICULTY_TO_SHUFFLE_MOVES[args.difficulty]
    )

    if shuffle_moves <= 0:
        raise SystemExit("shuffle_moves must be >= 1")

    rng = random.Random(args.seed)

    # Header
    title = "Puzzle 4x4 Solver - Detailed Output"
    print()
    print("=" * 50)
    print(title)
    print("=" * 50)
    print()

    # Part 1: Generate and display puzzle
    print("PART 1: Generate Random Puzzle 4x4")
    print("-" * 50)
    print()
    
    initial_board = generate_solvable_puzzle_4x4(shuffle_moves=shuffle_moves, rng=rng)
    
    print(render_board_ascii_table(initial_board, "Initial State:"))
    print()
    print(render_board_ascii_table(GOAL_4x4, "Goal State:"))
    print()

    # Part 2: Run algorithms with progress indicators
    print("PART 2: Run Algorithms (BFS, DFS, A*)")
    print("-" * 50)
    print()
    
    # For IDDFS, we set max depth to a reasonable value
    # Using shuffle_moves * 2 to ensure solvability even with non-optimal shuffles
    max_depth = max(shuffle_moves * 2, 20)
    results = run_single_puzzle(initial_board, GOAL_4x4, max_depth_for_dfs=max_depth)

    # Part 3: Display results
    print("PART 3: Algorithm Comparison Results")
    print("-" * 50)
    print()
    print(render_comparison_table(results))
    print()
    
    # Display winners
    print_winners(results)
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
