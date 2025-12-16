# Google Colab Quick Start Guide

## Copy-Paste Ready Commands for Google Colab

### Step 1: Clone Repository

```python
# Clone the repository
!git clone https://github.com/[YOUR-USERNAME]/sliding-puzzle-pka.git

# Change to project directory
%cd sliding-puzzle-pka
```

### Step 2: Run Solver (Choose One)

```python
# ===== Option 1: Default Run (Medium Difficulty) =====
!python puzzle_4x4_solver.py

# ===== Option 2: Easy Puzzle =====
!python puzzle_4x4_solver.py --difficulty easy

# ===== Option 3: Hard Puzzle =====
!python puzzle_4x4_solver.py --difficulty hard

# ===== Option 4: Custom Configuration =====
!python puzzle_4x4_solver.py --shuffle-moves 10 --seed 42

# ===== Option 5: Reproducible Results =====
!python puzzle_4x4_solver.py --seed 123
```

## Expected Output

You will see three parts in the output:

### ✅ Part 1: Puzzle States
- **Initial State**: The randomly generated puzzle
- **Goal State**: The target configuration
- Both displayed as ASCII tables with box-drawing characters

### ✅ Part 2: Algorithm Progress
- **Running BFS... ✓** 
- **Running DFS... ✓** 
- **Running A*... ✓**

### ✅ Part 3: Results
- **Comparison Table**: Shows Moves, Time (ms), and Nodes Explored for each algorithm
- **Winner Highlights**: Shows fastest algorithm and most efficient algorithm

## Example Output

```
==================================================
Puzzle 4x4 Solver - Detailed Output
==================================================

PART 1: Generate Random Puzzle 4x4
--------------------------------------------------

Initial State:
┌────┬────┬────┬────┐
│ 1  │ 2  │ 3  │ 4  │
├────┼────┼────┼────┤
│ 5  │ 6  │ 7  │ 8  │
├────┼────┼────┼────┤
│ 9  │ 10 │ 0  │ 12 │
├────┼────┼────┼────┤
│ 13 │ 14 │ 11 │ 15 │
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

PART 2: Run Algorithms (BFS, DFS, A*)
--------------------------------------------------

Running BFS... ✓ 
Running DFS... ✓ 
Running A*... ✓  

PART 3: Algorithm Comparison Results
--------------------------------------------------

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

## Understanding the Metrics

| Metric | Description |
|--------|-------------|
| **Moves** | Number of steps to solve the puzzle (all algorithms produce optimal solutions) |
| **Time (ms)** | Execution time in milliseconds (A* is usually fastest) |
| **Nodes Exp.** | Number of states explored (A* explores fewest nodes) |

## Algorithm Comparison

### BFS (Breadth-First Search)
- ✅ Guarantees optimal solution
- ✅ Complete (always finds solution if exists)
- ❌ High memory usage
- ❌ Slower for complex puzzles

### DFS (Iterative Deepening)
- ✅ Guarantees optimal solution
- ✅ Low memory usage
- ❌ May explore many nodes repeatedly
- ❌ Slower than A* but faster than standard DFS

### A* (A-star with Manhattan Distance)
- ✅ Guarantees optimal solution
- ✅ Fastest execution time
- ✅ Fewest nodes explored
- ✅ Best overall performance

## Troubleshooting

### Problem: Characters display incorrectly
**Solution**: Colab supports UTF-8 by default. If you see issues, try restarting the runtime.

### Problem: Script takes too long
**Solution**: Use easier difficulty or fewer shuffle moves:
```python
!python puzzle_4x4_solver.py --difficulty easy
```

### Problem: Cannot clone repository
**Solution**: Check the repository URL is correct. Replace `[YOUR-USERNAME]` with actual username.

### Problem: Module not found error
**Solution**: Make sure you're in the correct directory:
```python
%cd sliding-puzzle-pka
!ls  # Should see puzzle_4x4_solver.py
```

## Tips for Best Results

1. **Start with easy**: Test with `--difficulty easy` first
2. **Use seeds for reproducibility**: Add `--seed 42` to get same puzzle every time
3. **Compare difficulties**: Run easy, medium, and hard to see performance differences
4. **Observe A* efficiency**: Notice how A* explores significantly fewer nodes

## Advanced Usage

### Run Multiple Tests
```python
# Test all difficulties
!python puzzle_4x4_solver.py --difficulty easy --seed 1
!python puzzle_4x4_solver.py --difficulty medium --seed 1
!python puzzle_4x4_solver.py --difficulty hard --seed 1
```

### Save Output to File
```python
# Save results to text file
!python puzzle_4x4_solver.py > results.txt

# View saved results
!cat results.txt
```

### Custom Experiments
```python
# Test with specific number of moves
for moves in [4, 6, 8, 10, 12]:
    print(f"\n{'='*50}")
    print(f"Testing with {moves} shuffle moves")
    print('='*50)
    !python puzzle_4x4_solver.py --shuffle-moves {moves} --seed 42
```

## Need Help?

- Check the full guide: [PUZZLE_4X4_SOLVER_GUIDE.md](PUZZLE_4X4_SOLVER_GUIDE.md)
- Review the main README: [README.md](README.md)
- Check the source code: [puzzle_4x4_solver.py](puzzle_4x4_solver.py)

## Key Takeaways

1. **A* is the winner** for most cases (fastest + fewest nodes)
2. **BFS guarantees optimal** but uses more memory
3. **DFS (IDDFS) is memory efficient** but may be slower
4. **All algorithms produce optimal solutions** (same number of moves)
5. **Perfect for learning** algorithm comparison in practice

Happy solving! 🧩✨
