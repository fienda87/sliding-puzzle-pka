# Changes: Remove Move Counter & Timer Display

## Summary
Removed the visual display of move counter and timer from gameplay UI while preserving internal tracking for algorithm comparison metrics.

## Changes Made

### 1. UI Display Removal
**File: `sliding_puzzle/ui/screens.py`**
- **Line 147**: Removed the call to `self.ui.draw_metrics(screen, game.moves, game.get_time_elapsed())`
- **Effect**: Move counter and timer are no longer visible during gameplay

### 2. Internal Tracking Preserved
**File: `sliding_puzzle/game/puzzle_game.py`**
- **No changes made**: All internal tracking remains intact
- `game.moves` continues to track the number of moves
- `game.start_time` and `game.get_time_elapsed()` continue to track elapsed time
- **Purpose**: These internal metrics are still needed for algorithm comparison

### 3. Algorithm Metrics Unaffected
**Files: `sliding_puzzle/ui/screens.py`, `sliding_puzzle/ui/components.py`**
- **No changes made**: Algorithm comparison table functionality remains intact
- The comparison table still displays:
  - Algorithm name (BFS, DFS, A*)
  - Moves (from solver result, not game.moves)
  - Time in ms (from solver result, not game time)
  - Nodes explored
- **Important**: These metrics come from solver results, not from game state

## Testing Performed

### 1. Unit Tests
- ✅ `test_quick.py` - All core functionality tests pass
- ✅ `test_integration.py` - All integration tests pass
- ✅ `test_astar.py` - All A* algorithm tests pass

### 2. Custom Tests Created
- ✅ `test_ui_no_crash.py` - Verifies UI initializes and renders without crashes
  - Tests all difficulty levels
  - Confirms internal move/time tracking still works
  - Confirms rendering works after moves
  
- ✅ `test_comparison_metrics.py` - Verifies algorithm comparison functionality
  - Tests all three solvers (BFS, DFS, A*)
  - Confirms comparison table receives and stores results
  - Confirms internal game tracking persists
  - Confirms UI renders correctly with comparison table

## Acceptance Criteria Status

✅ **Move counter tidak visible saat bermain**
   - The `draw_metrics()` call has been removed from the render method
   
✅ **Timer tidak visible saat bermain**
   - Same change removes both counter and timer display
   
✅ **Gameplay lancar tanpa counter/timer**
   - All tests pass, no crashes or errors
   
✅ **Algorithm metrics (untuk comparison table) masih working**
   - Comparison table functionality fully preserved
   - All solver results properly displayed
   
✅ **Clean, minimal UI**
   - UI now shows only: puzzle board, control buttons, comparison table, and win message
   - No redundant move/time display cluttering the interface

## Visual Changes

### Before:
```
Top-left corner displayed:
- Moves: X
- Time: MM:SS
```

### After:
```
Top-left corner: Clean (no text)
```

### Preserved:
- Puzzle board
- Control buttons (Solve with BFS/DFS/A*, Shuffle, Undo, Back to Menu)
- Algorithm comparison table (when solvers are run)
- Win message (when puzzle is solved)
- Solving status indicator (during solver execution)

## Migration Notes

- The `draw_metrics()` method in `ui/components.py` is still available but unused
- Can be removed in future cleanup if confirmed not needed
- Internal tracking variables remain for potential future features
- No breaking changes to existing functionality
