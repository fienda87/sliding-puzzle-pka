# Sliding Puzzle Game

A sliding puzzle game with multiple grid sizes (3x3 and 4x4) and intelligent solvers (BFS, DFS, A*).

## Features

- **Multiple Grid Sizes**: Play with 3x3 or 4x4 grids
- **6 Difficulty Levels**: 3 levels for each grid size (Easy, Medium, Hard)
- **Smart Solvers**: BFS, DFS, and A* algorithms with performance metrics
- **Interactive UI**: Mouse and keyboard controls
- **Dynamic Rendering**: Tiles automatically scale for different grid sizes

## Installation

1. Download / clone this repository
2. Open in VS Code and cd to the project folder

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install pygame

# Run the game
cd sliding_puzzle
python main.py
```

## Controls

- **Arrow Keys**: Move tiles
- **Mouse Click**: Click adjacent tile to swap with blank
- **R**: Shuffle puzzle
- **U**: Undo last move
- **ESC**: Return to menu
- **Space**: Solve with BFS
- **S**: Solve with DFS
- **A**: Solve with A*

## Difficulty Levels

### 3x3 Grid
- **Easy**: 5 shuffles (~2-5 steps)
- **Medium**: 15 shuffles (~10-15 steps)
- **Hard**: 30 shuffles (~25-35 steps)

### 4x4 Grid
- **Easy**: 8 shuffles (~5-10 steps)
- **Medium**: 20 shuffles (~15-25 steps)
- **Hard**: 40 shuffles (~30-50 steps)

## Testing

```bash
# Quick smoke test
python test_quick.py

# Test 4x4 functionality
python test_4x4.py

# Test difficulty presets
python test_difficulty_presets.py

# Test A* algorithm
python test_astar.py
```

## Documentation

- `GRID_SUPPORT.md`: Details on 4x4 grid implementation
- `A_STAR_IMPLEMENTATION.md`: A* algorithm documentation
- `IMPLEMENTATION_SUMMARY.md`: Overall project summary
