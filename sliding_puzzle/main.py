import pygame
import sys
from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_bfs, solve_dfs
from ui.screens import GameScreen, MenuScreen
from utils.constants import *


def animate_solution(game, screen, game_screen, solution_path, solver_type):
    game.is_animating = True
    
    for state in solution_path:
        game.apply_board_state(state.board)
        
        screen.fill(COLOR_BACKGROUND)
        game_screen.render(screen, game)
        pygame.display.flip()
        
        pygame.time.delay(SOLVER_DELAY_MS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    game.is_animating = False


def main():
    pygame.init()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sliding Puzzle Game")
    
    clock = pygame.time.Clock()
    
    game_state = "MENU"
    current_difficulty = None
    
    menu_screen = MenuScreen(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = None
    game_screen = None
    
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        if game_state == "MENU":
            menu_screen.update_hover(mouse_pos)
        elif game_state == "GAME" and game_screen:
            game_screen.update_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game_state == "MENU":
                        difficulty = menu_screen.handle_click(mouse_pos)
                        if difficulty:
                            current_difficulty = difficulty
                            level_data = LEVELS[difficulty]
                            
                            game = PuzzleGame(level_data['board'], level_data['goal'])
                            game_screen = GameScreen(WINDOW_WIDTH, WINDOW_HEIGHT, level_data['grid_size'])
                            
                            game_state = "GAME"
                            print(f"[GAME] Starting {level_data['name']} difficulty")
                    
                    elif game_state == "GAME" and game and game_screen:
                        action, data = game_screen.handle_click(mouse_pos, game)
                        
                        if action == 'tile_click' and not game.is_animating:
                            row, col = data
                            game.handle_tile_click(row, col)
                            game_screen.clear_solver_result()
                        
                        elif action == 'solve_bfs' and not game.is_animating:
                            print("[SOLVER] Running BFS solver...")
                            result = solve_bfs(game.current_board, game.goal_board)
                            
                            if result:
                                print(f"[SOLVER] BFS Solution Found!")
                                print(f"[SOLVER] Steps: {result['steps']}")
                                print(f"[SOLVER] Time: {result['time_taken']:.3f}s")
                                print(f"[SOLVER] Nodes Explored: {result['nodes_explored']}")
                                
                                game_screen.set_solver_result(result, "BFS")
                                animate_solution(game, screen, game_screen, result['solution_path'], "BFS")
                            else:
                                print("[SOLVER] No solution found!")
                        
                        elif action == 'solve_dfs' and not game.is_animating:
                            print("[SOLVER] Running DFS solver...")
                            result = solve_dfs(game.current_board, game.goal_board)
                            
                            if result:
                                print(f"[SOLVER] DFS Solution Found!")
                                print(f"[SOLVER] Steps: {result['steps']}")
                                print(f"[SOLVER] Time: {result['time_taken']:.3f}s")
                                print(f"[SOLVER] Nodes Explored: {result['nodes_explored']}")
                                
                                game_screen.set_solver_result(result, "DFS")
                                animate_solution(game, screen, game_screen, result['solution_path'], "DFS")
                            else:
                                print("[SOLVER] No solution found!")
                        
                        elif action == 'reset':
                            game.reset()
                            game_screen.clear_solver_result()
                            print("[GAME] Board reset to initial state")
                        
                        elif action == 'undo':
                            if game.undo():
                                game_screen.clear_solver_result()
                                print("[GAME] Undo last move")
                        
                        elif action == 'back':
                            game_state = "MENU"
                            print("[GAME] Returning to menu")
            
            elif event.type == pygame.KEYDOWN:
                if game_state == "GAME" and game and not game.is_animating:
                    if event.key == pygame.K_UP:
                        game.move_blank_direction('UP')
                        game_screen.clear_solver_result()
                    elif event.key == pygame.K_DOWN:
                        game.move_blank_direction('DOWN')
                        game_screen.clear_solver_result()
                    elif event.key == pygame.K_LEFT:
                        game.move_blank_direction('LEFT')
                        game_screen.clear_solver_result()
                    elif event.key == pygame.K_RIGHT:
                        game.move_blank_direction('RIGHT')
                        game_screen.clear_solver_result()
                    elif event.key == pygame.K_u:
                        if game.undo():
                            game_screen.clear_solver_result()
                            print("[GAME] Undo last move")
                    elif event.key == pygame.K_r:
                        game.reset()
                        game_screen.clear_solver_result()
                        print("[GAME] Board reset to initial state")
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "MENU"
                        print("[GAME] Returning to menu")
                    elif event.key == pygame.K_SPACE:
                        print("[SOLVER] Running BFS solver...")
                        result = solve_bfs(game.current_board, game.goal_board)
                        
                        if result:
                            print(f"[SOLVER] BFS Solution Found!")
                            print(f"[SOLVER] Steps: {result['steps']}")
                            print(f"[SOLVER] Time: {result['time_taken']:.3f}s")
                            print(f"[SOLVER] Nodes Explored: {result['nodes_explored']}")
                            
                            game_screen.set_solver_result(result, "BFS")
                            animate_solution(game, screen, game_screen, result['solution_path'], "BFS")
                        else:
                            print("[SOLVER] No solution found!")
                    elif event.key == pygame.K_s:
                        print("[SOLVER] Running DFS solver...")
                        result = solve_dfs(game.current_board, game.goal_board)
                        
                        if result:
                            print(f"[SOLVER] DFS Solution Found!")
                            print(f"[SOLVER] Steps: {result['steps']}")
                            print(f"[SOLVER] Time: {result['time_taken']:.3f}s")
                            print(f"[SOLVER] Nodes Explored: {result['nodes_explored']}")
                            
                            game_screen.set_solver_result(result, "DFS")
                            animate_solution(game, screen, game_screen, result['solution_path'], "DFS")
                        else:
                            print("[SOLVER] No solution found!")
        
        if game_state == "MENU":
            menu_screen.render(screen)
        elif game_state == "GAME" and game and game_screen:
            game_screen.render(screen, game)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
