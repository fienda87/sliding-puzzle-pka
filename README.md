# Sliding Block Puzzle Game

A complete implementation of the classic Sliding Block Puzzle (8-puzzle and 15-puzzle) with AI solvers using Python and Pygame.

## Features

- **Multiple Grid Sizes**: 3×3 (8-puzzle) and 4×4 (15-puzzle) support
- **Manual Gameplay**: Click tiles adjacent to the blank space to move them
- **BFS Solver**: Finds the optimal (shortest) solution
- **DFS Solver**: Finds a solution quickly (not necessarily optimal)
- **Animated Solutions**: Watch the AI solve the puzzle step-by-step
- **Move Counter**: Tracks the number of moves made
- **Real-Time Timer**: Shows elapsed time since game start
- **Clean UI**: Intuitive Pygame interface with colored tiles and buttons

## Installation

1. Ensure you have Python 3.7+ installed
2. Install Pygame:

```bash
pip install pygame
```

## Running the Game

```bash
cd sliding_puzzle
python main.py
```

## How to Play

1. **Manual Mode**: Click on any tile adjacent to the blank space to swap it
2. **BFS Solver**: Click "Solve BFS" to find and animate the optimal solution
3. **DFS Solver**: Click "Solve DFS" to find and animate a solution quickly
4. **Reset**: Click "Reset" to return to the initial board state

## Project Structure

```
sliding_puzzle/
├── main.py                 # Entry point and game loop
├── game/
│   ├── puzzle_state.py     # State representation
│   ├── puzzle_solver.py    # BFS and DFS algorithms
│   └── puzzle_game.py      # Game logic manager
├── ui/
│   ├── components.py       # UI components (board, buttons)
│   └── screens.py          # Screen management
├── utils/
│   └── constants.py        # Configuration and constants
└── assets/
    ├── fonts/
    └── images/
```

## Test Cases

The game includes several pre-configured test cases:

- **Easy (3×3)**: 1-2 moves to solve
- **Medium (3×3)**: 8-12 moves to solve
- **Hard (3×3)**: 20-30 moves to solve
- **Expert (4×4)**: 5+ moves to solve

To change the test case, modify the `initial_board` in `main.py`.

## Algorithm Details

### BFS (Breadth-First Search)
- Guarantees the shortest solution
- Uses a queue (FIFO) to explore states level-by-level
- More memory-intensive but optimal

### DFS (Depth-First Search)
- Finds a solution quickly
- Uses a stack (LIFO) with depth limit
- Less memory-intensive but not optimal

## Controls

- **Mouse**: Click tiles or buttons
- **Close Window**: Quit the game

## Requirements

- Python 3.7+
- Pygame 2.0+

## License

MIT License
