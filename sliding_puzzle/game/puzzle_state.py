from __future__ import annotations


class PuzzleState:
    """Immutable-ish representation of a puzzle board for search algorithms.

    Each state keeps a parent link so solvers can reconstruct the solution path.
    """

    def __init__(
        self,
        board: list[list[int]],
        parent: PuzzleState | None = None,
        action: str | None = None,
        level: int = 0,
    ):
        self.board = [row[:] for row in board]
        self.parent = parent
        self.action = action
        self.level = level
        self.blank_pos = self.find_blank()

    def find_blank(self) -> tuple[int, int] | None:
        for i, row in enumerate(self.board):
            for j, value in enumerate(row):
                if value == 0:
                    return (i, j)
        return None

    def get_possible_moves(self) -> list[PuzzleState]:
        """Return a list of next states reachable with one blank move."""

        moves: list[PuzzleState] = []
        if self.blank_pos is None:
            return moves

        row, col = self.blank_pos
        n = len(self.board)
        m = len(self.board[0])

        directions = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]

        for dr, dc, action_name in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < n and 0 <= new_col < m:
                new_board = [r[:] for r in self.board]
                new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]

                moves.append(PuzzleState(new_board, parent=self, action=action_name, level=self.level + 1))

        return moves

    def is_goal(self, goal_board: list[list[int]]) -> bool:
        return self.board == goal_board

    def get_board_tuple(self) -> tuple[tuple[int, ...], ...]:
        return tuple(tuple(row) for row in self.board)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PuzzleState):
            return False
        return self.get_board_tuple() == other.get_board_tuple()

    def __hash__(self) -> int:
        return hash(self.get_board_tuple())

    def __repr__(self) -> str:
        return f"PuzzleState(level={self.level}, action={self.action})"
