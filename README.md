# Sliding Puzzle Solver

## Cara Menjalankan (Local)

Pertama download / clone repo ini
buka di vs code pastiin cd path ke folder 

### Buat virtual environment
```bash
python -m venv venv
```

### Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Install dependencies
```bash
pip install pygame
```

### Run project
```bash
# (venv) harus ada di terminal
python main.py
```

## Cara Menjalankan di Google Colab (Headless Mode)

Untuk menjalankan puzzle solver 4x4 di Google Colab tanpa GUI:

```python
# Clone repository
!git clone https://github.com/[USERNAME]/sliding-puzzle-pka.git
%cd sliding-puzzle-pka

# Run solver dengan default settings (medium difficulty)
!python puzzle_4x4_solver.py

# Atau dengan custom settings
!python puzzle_4x4_solver.py --difficulty hard
!python puzzle_4x4_solver.py --shuffle-moves 10 --seed 42
```

### Output yang dihasilkan:
- Initial State & Goal State dalam format ASCII table
- Progress indicator untuk BFS, DFS, dan A*
- Comparison table dengan metrics (Moves, Time, Nodes Explored)
- Winner highlights (Fastest & Least Nodes Explored)

