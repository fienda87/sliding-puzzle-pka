from collections import deque
import time
import heapq
from .puzzle_state import PuzzleState


def build_solution_path(goal_state):
    path = []
    current = goal_state
    
    while current is not None:
        path.append(current)
        current = current.parent
    
    path.reverse()
    return path


def format_result(solution_path, nodes_explored, start_time):
    """Format the solver result in a consistent format."""
    time_ms = (time.time() - start_time) * 1000
    moves = len(solution_path) - 1
    
    return {
        'path': solution_path,
        'moves': moves,
        'time_ms': time_ms,
        'nodes_explored': nodes_explored,
        'solution_path': solution_path,
        'steps': moves,
        'time_taken': time.time() - start_time,
    }


def solve_bfs(initial_board, goal_board):
    start_time = time.time()
    
    initial_state = PuzzleState(initial_board)
    
    if initial_state.is_goal(goal_board):
        return format_result([initial_state], 1, start_time)
    
    queue = deque([initial_state])
    visited = {initial_state.get_board_tuple()}
    nodes_explored = 0
    
    while queue:
        current_state = queue.popleft()
        nodes_explored += 1
        
        if current_state.is_goal(goal_board):
            solution_path = build_solution_path(current_state)
            return format_result(solution_path, nodes_explored, start_time)
        
        for next_state in current_state.get_possible_moves():
            state_tuple = next_state.get_board_tuple()
            if state_tuple not in visited:
                visited.add(state_tuple)
                queue.append(next_state)
    
    return None


def solve_dfs(initial_board, goal_board, depth_limit=50):
    start_time = time.time()
    
    initial_state = PuzzleState(initial_board)
    
    if initial_state.is_goal(goal_board):
        return format_result([initial_state], 1, start_time)
    
    stack = [initial_state]
    visited = {initial_state.get_board_tuple()}
    nodes_explored = 0
    
    while stack:
        current_state = stack.pop()
        nodes_explored += 1
        
        if current_state.is_goal(goal_board):
            solution_path = build_solution_path(current_state)
            return format_result(solution_path, nodes_explored, start_time)
        
        if current_state.level >= depth_limit:
            continue
        
        for next_state in current_state.get_possible_moves():
            state_tuple = next_state.get_board_tuple()
            if state_tuple not in visited:
                visited.add(state_tuple)
                stack.append(next_state)
    
    return None


def precompute_goal_positions(goal_board):
    """Pre-compute goal positions for faster Manhattan distance calculation."""
    positions = {}
    n = len(goal_board)
    m = len(goal_board[0])
    
    for i in range(n):
        for j in range(m):
            value = goal_board[i][j]
            if value != 0:
                positions[value] = (i, j)
    
    return positions


def manhattan_distance(board, goal_positions):
    """Calculate Manhattan distance heuristic for A* algorithm.
    
    Args:
        board: Current puzzle board
        goal_positions: Pre-computed dictionary of {value: (row, col)} for goal state
    """
    distance = 0
    n = len(board)
    m = len(board[0])
    
    for i in range(n):
        for j in range(m):
            value = board[i][j]
            if value != 0:
                goal_i, goal_j = goal_positions[value]
                distance += abs(i - goal_i) + abs(j - goal_j)
    
    return distance


def solve_astar(initial_board, goal_board):
    """A* algorithm for solving sliding puzzle with Manhattan distance heuristic."""
    start_time = time.time()
    
    initial_state = PuzzleState(initial_board)
    
    if initial_state.is_goal(goal_board):
        return format_result([initial_state], 1, start_time)
    
    goal_positions = precompute_goal_positions(goal_board)
    
    open_set = []
    initial_h = manhattan_distance(initial_board, goal_positions)
    heapq.heappush(open_set, (initial_h, id(initial_state), initial_state))
    
    visited = set()
    nodes_explored = 0
    
    while open_set:
        f_score, _, current_state = heapq.heappop(open_set)
        
        state_tuple = current_state.get_board_tuple()
        if state_tuple in visited:
            continue
        
        visited.add(state_tuple)
        nodes_explored += 1
        
        if current_state.is_goal(goal_board):
            solution_path = build_solution_path(current_state)
            return format_result(solution_path, nodes_explored, start_time)
        
        for next_state in current_state.get_possible_moves():
            next_tuple = next_state.get_board_tuple()
            if next_tuple not in visited:
                h_score = manhattan_distance(next_state.board, goal_positions)
                g_score = next_state.level
                f_score = g_score + h_score
                heapq.heappush(open_set, (f_score, id(next_state), next_state))
    
    return None
