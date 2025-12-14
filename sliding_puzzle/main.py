import pygame
import sys
from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_bfs, solve_dfs, solve_astar
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


def solve_and_animate(game, screen, game_screen, solver_func, algorithm_label):
    if game.is_animating or game_screen.is_solving:
        return

    starting_board = [row[:] for row in game.current_board]

    game_screen.set_solving(True, algorithm_label)

    screen.fill(COLOR_BACKGROUND)
    game_screen.render(screen, game)
    pygame.display.flip()
    pygame.event.pump()

    print(f"[SOLVER] Running {algorithm_label} solver...")
    result = solver_func(game.current_board, game.goal_board)

    game_screen.set_solving(False)

    if result:
        print(f"[SOLVER] {algorithm_label} Solution Found!")
        print(f"[SOLVER] Steps: {result['steps']}")
        print(f"[SOLVER] Time: {result['time_taken']:.3f}s")
        print(f"[SOLVER] Nodes Explored: {result['nodes_explored']}")

        game_screen.set_solver_result(result, algorithm_label)
        game_screen.add_comparison_result(algorithm_label, result)

        animate_solution(game, screen, game_screen, result['solution_path'], algorithm_label)
        game.apply_board_state(starting_board)
    else:
        print("[SOLVER] No solution found!")


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
                        
                        if action == 'tile_click' and not game.is_animating and not game_screen.is_solving:
                            row, col = data
                            game.handle_tile_click(row, col)
                            game_screen.clear_solver_result()

                        elif action == 'solve_bfs':
                            solve_and_animate(game, screen, game_screen, solve_bfs, "BFS")

                        elif action == 'solve_dfs':
                            solve_and_animate(game, screen, game_screen, solve_dfs, "DFS")

                        elif action == 'solve_astar':
                            solve_and_animate(game, screen, game_screen, solve_astar, "A*")

                        elif action == 'shuffle' and not game.is_animating and not game_screen.is_solving:
                            game.shuffle()
                            game_screen.clear_solver_result()
                            game_screen.clear_comparison_table()
                            print("[GAME] Puzzle shuffled")

                        elif action == 'undo' and not game.is_animating and not game_screen.is_solving:
                            if game.undo():
                                game_screen.clear_solver_result()
                                print("[GAME] Undo last move")

                        elif action == 'back' and not game.is_animating and not game_screen.is_solving:
                            game_state = "MENU"
                            print("[GAME] Returning to menu")
            
            elif event.type == pygame.KEYDOWN:
                if game_state == "GAME" and game and game_screen and not game.is_animating and not game_screen.is_solving:
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
                        game.shuffle()
                        game_screen.clear_solver_result()
                        game_screen.clear_comparison_table()
                        print("[GAME] Puzzle shuffled")
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "MENU"
                        print("[GAME] Returning to menu")
                    elif event.key == pygame.K_SPACE:
                        solve_and_animate(game, screen, game_screen, solve_bfs, "BFS")
                    elif event.key == pygame.K_s:
                        solve_and_animate(game, screen, game_screen, solve_dfs, "DFS")
                    elif event.key == pygame.K_a:
                        solve_and_animate(game, screen, game_screen, solve_astar, "A*")
        
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
