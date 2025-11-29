# Getting Started with Sliding Puzzle Game

## Quick Start Guide

### Step 1: Install Dependencies

Make sure you have Python 3.7 or higher installed. Then install pygame:

```bash
pip install pygame
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Run the Game

Navigate to the sliding_puzzle directory and run main.py:

```bash
cd sliding_puzzle
python main.py
```

Alternatively, use the convenience script from the project root:

```bash
./run_game.sh
```

### Step 3: Play!

The game window will open with a 3×3 puzzle grid.

---

## Game Controls

### Manual Play Mode

- **Click a tile** adjacent to the blank space to move it
- The blank space is shown in gray
- Only tiles directly above, below, left, or right of the blank can move
- No diagonal moves allowed

### Solver Buttons

- **Solve BFS**: Click to watch the optimal solution (shortest path)
  - Guaranteed to find the shortest solution
  - May take a few seconds for complex puzzles
  
- **Solve DFS**: Click for a quick solution
  - Finds a solution fast
  - May not be the shortest path
  
- **Reset**: Click to return to the initial puzzle state
  - Resets move counter to 0
  - Restarts the timer

### Display Information

- **Top Left Corner**:
  - Move counter: Shows how many moves you've made
  - Timer: Shows elapsed time in MM:SS format
  
- **Bottom Left Corner** (after solving):
  - Solver type (BFS or DFS)
  - Number of steps in solution
  - Time taken to find solution
  - Number of nodes explored

---

## Understanding the Display

### Tile Colors
- **Blue tiles**: Numbered puzzle pieces (1-8 for 3×3, 1-15 for 4×4)
- **Gray tile**: Empty space (blank)

### Win Condition
- All numbers in order from left to right, top to bottom
- Blank space in the bottom-right corner
- A "SOLVED!" message appears at the top

### Example Goal State (3×3):
```
1  2  3
4  5  6
7  8  [blank]
```

---

## Changing Puzzle Difficulty

To change the puzzle difficulty, edit `main.py` around line 62:

### Easy Puzzle (1-2 moves)
```python
initial_board = TEST_EASY_3x3
goal_board = GOAL_3x3
grid_size = 3
```

### Medium Puzzle (5-10 moves)
```python
initial_board = TEST_MEDIUM_3x3
goal_board = GOAL_3x3
grid_size = 3
```

### Hard Puzzle (20-30 moves)
```python
initial_board = TEST_HARD_3x3
goal_board = GOAL_3x3
grid_size = 3
```

### Expert Puzzle (4×4 grid)
```python
initial_board = TEST_EXPERT_4x4
goal_board = GOAL_4x4
grid_size = 4
```

---

## Tips and Tricks

### For Manual Play
1. Start by getting the top row correct
2. Then work on the left column
3. Solve the remaining 2×2 square last

### Understanding Solvers
- **BFS** explores all possibilities level by level
  - Best for: Finding the absolute shortest solution
  - Trade-off: Slower and uses more memory
  
- **DFS** dives deep into one path before backtracking
  - Best for: Quick solutions
  - Trade-off: May find longer paths

### Performance Notes
- 3×3 puzzles solve almost instantly
- 4×4 puzzles may take several seconds with BFS
- DFS is generally faster but gives longer solutions

---

## Troubleshooting

### Issue: "No module named 'pygame'"
**Solution**: Install pygame with `pip install pygame`

### Issue: Game window doesn't open
**Solution**: Make sure you have a display/GUI environment. The game requires a graphical interface.

### Issue: "No module named 'game'"
**Solution**: Make sure you're running the game from the `sliding_puzzle` directory:
```bash
cd sliding_puzzle
python main.py
```

### Issue: Solver takes too long
**Solution**: 
- For 4×4 puzzles, DFS is recommended for faster results
- Complex 3×3 puzzles can take 10-30 seconds with BFS
- This is normal for exploring large state spaces

---

## Console Output

When you run solvers, you'll see output like this:

```
[SOLVER] Running BFS solver...
[SOLVER] BFS Solution Found!
[SOLVER] Steps: 5
[SOLVER] Time: 0.0004s
[SOLVER] Nodes Explored: 47
```

This shows:
- **Steps**: Number of moves in the solution
- **Time**: How long it took to find the solution
- **Nodes Explored**: How many states were examined

---

## Customization

### Change Animation Speed

Edit `utils/constants.py`:
```python
SOLVER_DELAY_MS = 400  # Lower = faster animation
```

Recommended values:
- 200 = Fast
- 400 = Medium (default)
- 600 = Slow

### Change Colors

Edit `utils/constants.py`:
```python
COLOR_TILE = (52, 152, 219)      # Blue tiles
COLOR_BLANK = (192, 192, 192)     # Gray blank
COLOR_BUTTON = (46, 204, 113)     # Green buttons
```

Colors are in RGB format (Red, Green, Blue), values 0-255.

### Create Custom Puzzles

Add your own puzzle to `utils/constants.py`:
```python
MY_CUSTOM_PUZZLE = [[2, 1, 3], [4, 5, 6], [7, 8, 0]]
```

Then use it in `main.py`:
```python
initial_board = MY_CUSTOM_PUZZLE
```

---

## Testing Your Installation

Run the validation script to ensure everything works:

```bash
python validate_implementation.py
```

You should see:
```
✅ ALL TESTS PASSED! Implementation is complete.
```

---

## System Requirements

- **Python**: 3.7 or higher
- **Pygame**: 2.0 or higher
- **Operating System**: Windows, macOS, or Linux with GUI
- **Display**: Any resolution (window is 800×600)

---

## Need Help?

1. Check the README.md for project overview
2. Review TESTING.md for test results
3. See IMPLEMENTATION_SUMMARY.md for technical details

---

## Fun Facts

- The 8-puzzle has 9!/2 = 181,440 possible configurations
- The 15-puzzle has 16!/2 ≈ 10.4 trillion configurations!
- Not all random configurations are solvable
- The puzzles in this game are guaranteed to be solvable

Enjoy playing!
