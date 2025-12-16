import sys

import pygame

from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_astar, solve_bfs, solve_dfs
from ui.screens import GameScreen, MenuScreen
from utils.constants import COLOR_BACKGROUND, FPS, SOLVER_DELAY_MS, WINDOW_HEIGHT, WINDOW_WIDTH


def animate_solution(game: PuzzleGame, screen: pygame.Surface, game_screen: GameScreen, solution_path) -> None:
    """Animate a solver's solution path by stepping through board states."""

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


def solve_and_animate(
    game: PuzzleGame,
    screen: pygame.Surface,
    game_screen: GameScreen,
    solver_func,
    algorithm_label: str,
) -> None:
    """Run a solver, add metrics to the comparison table, and animate its path."""

    if game.is_animating or game_screen.is_solving:
        return

    starting_board = [row[:] for row in game.current_board]

    game_screen.set_solving(True, algorithm_label)

    screen.fill(COLOR_BACKGROUND)
    game_screen.render(screen, game)
    pygame.display.flip()
    pygame.event.pump()

    result = solver_func(game.current_board, game.goal_board)

    game_screen.set_solving(False)

    if not result:
        return

    game_screen.add_comparison_result(algorithm_label, result)
    animate_solution(game, screen, game_screen, result["solution_path"])
    game.apply_board_state(starting_board)


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sliding Puzzle Game")

    clock = pygame.time.Clock()

    game_state = "MENU"

    menu_screen = MenuScreen(WINDOW_WIDTH, WINDOW_HEIGHT)
    game: PuzzleGame | None = None
    game_screen: GameScreen | None = None

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

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "MENU":
                    level_data = menu_screen.handle_click(mouse_pos)
                    if level_data:
                        game = PuzzleGame(level_data["board"], level_data["goal"])
                        game_screen = GameScreen(WINDOW_WIDTH, WINDOW_HEIGHT, level_data["grid_size"])
                        game_state = "GAME"

                elif game_state == "GAME" and game and game_screen:
                    action, data = game_screen.handle_click(mouse_pos, game)

                    if action == "tile_click" and not game.is_animating and not game_screen.is_solving:
                        row, col = data
                        game.handle_tile_click(row, col)

                    elif action == "solve_bfs":
                        solve_and_animate(game, screen, game_screen, solve_bfs, "BFS")

                    elif action == "solve_dfs":
                        solve_and_animate(game, screen, game_screen, solve_dfs, "DFS")

                    elif action == "solve_astar":
                        solve_and_animate(game, screen, game_screen, solve_astar, "A*")

                    elif action == "shuffle" and not game.is_animating and not game_screen.is_solving:
                        game.shuffle()
                        game_screen.clear_comparison_table()

                    elif action == "undo" and not game.is_animating and not game_screen.is_solving:
                        game.undo()

                    elif action == "back" and not game.is_animating and not game_screen.is_solving:
                        menu_screen.reset()
                        game_state = "MENU"

            elif event.type == pygame.KEYDOWN:
                if game_state == "MENU" and event.key == pygame.K_ESCAPE:
                    menu_screen.go_back()

                if game_state != "GAME" or not game or not game_screen:
                    continue

                if game.is_animating or game_screen.is_solving:
                    continue

                if event.key == pygame.K_UP:
                    game.move_blank_direction("UP")
                elif event.key == pygame.K_DOWN:
                    game.move_blank_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    game.move_blank_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    game.move_blank_direction("RIGHT")
                elif event.key == pygame.K_u:
                    game.undo()
                elif event.key == pygame.K_r:
                    game.shuffle()
                    game_screen.clear_comparison_table()
                elif event.key == pygame.K_ESCAPE:
                    menu_screen.reset()
                    game_state = "MENU"
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
