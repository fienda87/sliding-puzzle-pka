from collections import deque
import time
from .puzzle_state import PuzzleState


def build_solution_path(goal_state):
    path = []
    current = goal_state
    
    while current is not None:
        path.append(current)
        current = current.parent
    
    path.reverse()
    return path


def solve_bfs(initial_board, goal_board):
    start_time = time.time()
    
    initial_state = PuzzleState(initial_board)
    
    if initial_state.is_goal(goal_board):
        return {
            'solution_path': [initial_state],
            'moves': 0,
            'time_taken': time.time() - start_time,
            'nodes_explored': 1,
            'steps': 0
        }
    
    queue = deque([initial_state])
    visited = {initial_state.get_board_tuple()}
    nodes_explored = 0
    
    while queue:
        current_state = queue.popleft()
        nodes_explored += 1
        
        if current_state.is_goal(goal_board):
            solution_path = build_solution_path(current_state)
            time_taken = time.time() - start_time
            
            return {
                'solution_path': solution_path,
                'moves': len(solution_path) - 1,
                'time_taken': time_taken,
                'nodes_explored': nodes_explored,
                'steps': len(solution_path) - 1
            }
        
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
        return {
            'solution_path': [initial_state],
            'moves': 0,
            'time_taken': time.time() - start_time,
            'nodes_explored': 1,
            'steps': 0
        }
    
    stack = [initial_state]
    visited = {initial_state.get_board_tuple()}
    nodes_explored = 0
    
    while stack:
        current_state = stack.pop()
        nodes_explored += 1
        
        if current_state.is_goal(goal_board):
            solution_path = build_solution_path(current_state)
            time_taken = time.time() - start_time
            
            return {
                'solution_path': solution_path,
                'moves': len(solution_path) - 1,
                'time_taken': time_taken,
                'nodes_explored': nodes_explored,
                'steps': len(solution_path) - 1
            }
        
        if current_state.level >= depth_limit:
            continue
        
        for next_state in current_state.get_possible_moves():
            state_tuple = next_state.get_board_tuple()
            if state_tuple not in visited:
                visited.add(state_tuple)
                stack.append(next_state)
    
    return None
