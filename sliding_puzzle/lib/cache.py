from collections import OrderedDict


class SolverCache:
    def __init__(self, max_entries=50):
        self.cache = OrderedDict()
        self.max_entries = max_entries
        self.hits = 0
        self.misses = 0
    
    def get(self, board, solver_type):
        key = (tuple(tuple(row) for row in board), solver_type)
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            return self.cache[key]
        self.misses += 1
        return None
    
    def set(self, board, solver_type, result):
        if len(self.cache) >= self.max_entries:
            self.cache.popitem(last=False)
        key = (tuple(tuple(row) for row in board), solver_type)
        self.cache[key] = result
    
    def clear(self):
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.cache)
        }
