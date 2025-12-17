# Puzzle 4x4 Solver - Detailed Output Guide

## Overview

`puzzle_4x4_solver.py` adalah script standalone untuk menyelesaikan puzzle sliding 4x4 menggunakan tiga algoritma pencarian: **BFS**, **DFS**, dan **A***. Script ini dirancang khusus untuk Google Colab dan environment headless (tanpa GUI).

## Features

1. **Generate Random Solvable 4x4 Puzzle** - Menghasilkan puzzle acak yang dijamin solvable
2. **ASCII Table Display** - Menampilkan Initial State dan Goal State dengan format tabel ASCII yang rapi
3. **Progress Indicators** - Menampilkan progress saat algoritma berjalan (⏳ dan ✓)
4. **Algorithm Comparison** - Membandingkan performa ketiga algoritma
5. **Winner Highlights** - Menampilkan algoritma tercepat dan paling efisien
6. **No Dependencies** - Tidak memerlukan pygame atau library GUI lainnya

## Usage

### Basic Usage (Default Medium Difficulty)

```bash
python puzzle_4x4_solver.py
```

### Custom Difficulty

```bash
# Easy (4 shuffle moves)
python puzzle_4x4_solver.py --difficulty easy

# Medium (8 shuffle moves)
python puzzle_4x4_solver.py --difficulty medium

# Hard (12 shuffle moves)
python puzzle_4x4_solver.py --difficulty hard
```

### Custom Shuffle Moves

```bash
# Specify exact number of shuffle moves
python puzzle_4x4_solver.py --shuffle-moves 10
```

### Reproducible Results

```bash
# Use seed for reproducible random generation
python puzzle_4x4_solver.py --seed 42
```

## Google Colab Usage

### Step 1: Clone Repository

```python
!git clone https://github.com/[USERNAME]/sliding-puzzle-pka.git
%cd sliding-puzzle-pka
```

### Step 2: Run Solver

```python
# Default run
!python puzzle_4x4_solver.py

# With custom settings
!python puzzle_4x4_solver.py --difficulty hard --seed 123
```

## Output Format

### Part 1: Generate Random Puzzle 4x4

Displays Initial State and Goal State in ASCII table format:

```
Initial State:
┌────┬────┬────┬────┐
│ 1  │ 2  │ 3  │ 4  │
├────┼────┼────┼────┤
│ 5  │ 6  │ 7  │ 8  │
├────┼────┼────┼────┤
│ 9  │ 10 │ 11 │ 12 │
├────┼────┼────┼────┤
│ 13 │ 14 │ 0  │ 15 │
└────┴────┴────┴────┘
(0 = blank)

Goal State:
┌────┬────┬────┬────┐
│ 1  │ 2  │ 3  │ 4  │
├────┼────┼────┼────┤
│ 5  │ 6  │ 7  │ 8  │
├────┼────┼────┼────┤
│ 9  │ 10 │ 11 │ 12 │
├────┼────┼────┼────┤
│ 13 │ 14 │ 15 │ 0  │
└────┴────┴────┴────┘
(0 = blank)
```

### Part 2: Run Algorithms

Shows progress indicators for each algorithm:

```
Running BFS... ✓ 
Running DFS... ✓ 
Running A*... ✓  
```

### Part 3: Algorithm Comparison Results

Displays comparison table with metrics:

```
┌───────────┬───────┬───────────┬────────────┐
│ Algoritma │ Moves │ Time (ms) │ Nodes Exp. │
├───────────┼───────┼───────────┼────────────┤
│ BFS       │     8 │     10 ms │        681 │
│ DFS       │     8 │      6 ms │       1304 │
│ A*        │     8 │      0 ms │         12 │
└───────────┴───────┴───────────┴────────────┘

Winner (Fastest): A* - 0 ms
Winner (Least Nodes Explored): A* - 12 nodes
```

## Metrics Explained

### Moves
- Jumlah langkah yang dibutuhkan untuk menyelesaikan puzzle
- Semua algoritma menghasilkan solusi optimal (jumlah moves sama)

### Time (ms)
- Waktu eksekusi algoritma dalam milliseconds
- **A*** biasanya paling cepat karena menggunakan heuristic (Manhattan distance)
- **BFS** dan **DFS** biasanya lebih lambat untuk puzzle yang kompleks

### Nodes Explored
- Jumlah state/node yang di-explore oleh algoritma
- **A*** mengexplore paling sedikit nodes karena guided search
- **BFS** mengexplore banyak nodes tapi garantee optimal solution
- **DFS** (IDDFS) mengexplore nodes berulang di setiap iterasi depth

## Algorithm Details

### BFS (Breadth-First Search)
- **Guarantee**: Optimal solution
- **Strategy**: Explore all nodes at current depth before moving deeper
- **Memory**: High (stores all nodes at current level)
- **Use Case**: When optimal solution is critical

### DFS (Iterative Deepening DFS)
- **Guarantee**: Optimal solution (with IDDFS)
- **Strategy**: Depth-first with increasing depth limit
- **Memory**: Low (only stores current path)
- **Use Case**: When memory is limited

### A* (A-star)
- **Guarantee**: Optimal solution (with admissible heuristic)
- **Strategy**: Best-first search using Manhattan distance heuristic
- **Memory**: Moderate
- **Use Case**: When speed is critical (usually fastest)

## Technical Details

### Puzzle Generation
- Generates solvable puzzles by shuffling from goal state
- Avoids immediate move reversal for more interesting puzzles
- Guarantees solvability

### Solvability
- All generated puzzles are guaranteed solvable
- Maximum depth is set to ensure algorithms can find solution
- For medium difficulty: max_depth = 16 (shuffle_moves * 2)

### Dependencies
- **Python 3.7+** (uses type annotations)
- **No external libraries** required (uses standard library only)
- **Colab compatible** (no pygame or GUI dependencies)

## Troubleshooting

### Script Fails to Run
- Check Python version: `python --version` (need 3.7+)
- Check you're in the correct directory
- Try with explicit path: `python /path/to/puzzle_4x4_solver.py`

### Solver Takes Too Long
- Reduce difficulty: use `--difficulty easy`
- Reduce shuffle moves: use `--shuffle-moves 4`
- For hard puzzles, DFS may take longer

### Unicode Characters Not Displaying
- Ensure terminal/Colab supports UTF-8
- Box-drawing characters (┌─┐) require UTF-8 encoding
- Most modern terminals support this by default

## Examples

### Example 1: Quick Test (Easy Puzzle)
```bash
python puzzle_4x4_solver.py --difficulty easy --seed 1
```

### Example 2: Reproducible Results
```bash
# Same seed always produces same puzzle
python puzzle_4x4_solver.py --seed 42
python puzzle_4x4_solver.py --seed 42  # Same output
```

### Example 3: Hard Challenge
```bash
python puzzle_4x4_solver.py --difficulty hard --seed 999
```

### Example 4: Custom Configuration
```bash
python puzzle_4x4_solver.py --shuffle-moves 15 --seed 123
```

## Performance Notes

- **Easy puzzles (4 moves)**: All algorithms solve in < 10ms
- **Medium puzzles (8 moves)**: A* typically < 1ms, BFS/DFS < 50ms
- **Hard puzzles (12 moves)**: A* typically < 5ms, BFS/DFS may take 100-1000ms
- **Very hard puzzles (15+ moves)**: BFS may take several seconds

## Best Practices for Colab

1. **Use seeds for reproducibility**: `--seed 42`
2. **Start with easy difficulty** to verify setup: `--difficulty easy`
3. **Increase difficulty gradually**: easy → medium → hard
4. **Monitor execution time** for very hard puzzles
5. **Capture output** if needed: `!python puzzle_4x4_solver.py > output.txt`

## Credits

- **BFS/DFS/A* Implementation**: `sliding_puzzle/game/puzzle_solver.py`
- **Puzzle State Management**: `sliding_puzzle/game/puzzle_state.py`
- **Script Author**: Created for Google Colab compatibility

## License

Same as the main repository.
