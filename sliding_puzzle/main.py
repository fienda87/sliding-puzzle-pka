import sys

import pygame

from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_astar, solve_bfs, solve_dfs
from ui.screens import GameScreen, MenuScreen, MetricsScreen
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
) -> dict[str, object] | None:
    """Run a solver, record its metrics, and animate its solution path."""

    if game.is_animating or game_screen.is_solving:
        return None

    starting_board = [row[:] for row in game.current_board]

    game_screen.set_solving(True, algorithm_label)

    screen.fill(COLOR_BACKGROUND)
    game_screen.render(screen, game)
    pygame.display.flip()
    pygame.event.pump()

    result = solver_func(game.current_board, game.goal_board)

    game_screen.set_solving(False)

    if not result:
        return None

    game_screen.add_comparison_result(algorithm_label, result)
    animate_solution(game, screen, game_screen, result["solution_path"])
    game.apply_board_state(starting_board)

    return result


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sliding Puzzle Game")

    clock = pygame.time.Clock()

    game_state = "MENU"

    menu_screen = MenuScreen(WINDOW_WIDTH, WINDOW_HEIGHT)
    game: PuzzleGame | None = None
    game_screen: GameScreen | None = None
    metrics_screen: MetricsScreen | None = None

    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        if game_state == "MENU":
            menu_screen.update_hover(mouse_pos)
        elif game_state == "GAME" and game_screen:
            game_screen.update_hover(mouse_pos)
        elif game_state == "METRICS" and metrics_screen:
            metrics_screen.update_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "MENU":
                    level_data = menu_screen.handle_click(mouse_pos)
                    if level_data:
                        game = PuzzleGame(level_data["board"], level_data["goal"])
                        game_screen = GameScreen(WINDOW_WIDTH, WINDOW_HEIGHT, level_data["grid_size"])
                        metrics_screen = MetricsScreen(WINDOW_WIDTH, WINDOW_HEIGHT, game_screen.comparison_results)
                        game_state = "GAME"
                        pygame.display.set_caption("Sliding Puzzle Game")

                elif game_state == "GAME" and game and game_screen:
                    action, data = game_screen.handle_click(mouse_pos, game)

                    if action == "tile_click" and not game.is_animating and not game_screen.is_solving:
                        row, col = data
                        game.handle_tile_click(row, col)

                    elif action == "solve_bfs":
                        result = solve_and_animate(game, screen, game_screen, solve_bfs, "BFS")
                        if result and metrics_screen:
                            metrics_screen.focus_last_page()
                            game_state = "METRICS"
                            pygame.display.set_caption("Algorithm Comparison Metrics")

                    elif action == "solve_dfs":
                        result = solve_and_animate(game, screen, game_screen, solve_dfs, "DFS")
                        if result and metrics_screen:
                            metrics_screen.focus_last_page()
                            game_state = "METRICS"
                            pygame.display.set_caption("Algorithm Comparison Metrics")

                    elif action == "solve_astar":
                        result = solve_and_animate(game, screen, game_screen, solve_astar, "A*")
                        if result and metrics_screen:
                            metrics_screen.focus_last_page()
                            game_state = "METRICS"
                            pygame.display.set_caption("Algorithm Comparison Metrics")

                    elif action == "shuffle" and not game.is_animating and not game_screen.is_solving:
                        game.shuffle()
                        game_screen.clear_comparison_table()
                        if metrics_screen:
                            metrics_screen.page_index = 0

                    elif action == "undo" and not game.is_animating and not game_screen.is_solving:
                        game.undo()

                    elif action == "back" and not game.is_animating and not game_screen.is_solving:
                        menu_screen.reset()
                        game = None
                        game_screen = None
                        metrics_screen = None
                        game_state = "MENU"
                        pygame.display.set_caption("Sliding Puzzle Game")

                elif game_state == "METRICS" and metrics_screen:
                    action = metrics_screen.handle_click(mouse_pos)

                    if action == "prev":
                        metrics_screen.previous_page()
                    elif action == "next":
                        metrics_screen.next_page()
                    elif action == "reset":
                        metrics_screen.results.clear()
                        metrics_screen.page_index = 0
                    elif action == "back":
                        game_state = "GAME"
                        pygame.display.set_caption("Sliding Puzzle Game")

            elif event.type == pygame.KEYDOWN:
                if game_state == "MENU" and event.key == pygame.K_ESCAPE:
                    menu_screen.go_back()
                    continue

                if game_state == "METRICS" and metrics_screen:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "GAME"
                        pygame.display.set_caption("Sliding Puzzle Game")
                    elif event.key in (pygame.K_LEFT, pygame.K_PAGEUP):
                        metrics_screen.previous_page()
                    elif event.key in (pygame.K_RIGHT, pygame.K_PAGEDOWN):
                        metrics_screen.next_page()
                    elif event.key == pygame.K_r:
                        metrics_screen.results.clear()
                        metrics_screen.page_index = 0
                    continue

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
                    if metrics_screen:
                        metrics_screen.page_index = 0
                elif event.key == pygame.K_ESCAPE:
                    menu_screen.reset()
                    game = None
                    game_screen = None
                    metrics_screen = None
                    game_state = "MENU"
                    pygame.display.set_caption("Sliding Puzzle Game")
                elif event.key == pygame.K_SPACE:
                    result = solve_and_animate(game, screen, game_screen, solve_bfs, "BFS")
                    if result and metrics_screen:
                        metrics_screen.focus_last_page()
                        game_state = "METRICS"
                        pygame.display.set_caption("Algorithm Comparison Metrics")
                elif event.key == pygame.K_s:
                    result = solve_and_animate(game, screen, game_screen, solve_dfs, "DFS")
                    if result and metrics_screen:
                        metrics_screen.focus_last_page()
                        game_state = "METRICS"
                        pygame.display.set_caption("Algorithm Comparison Metrics")
                elif event.key == pygame.K_a:
                    result = solve_and_animate(game, screen, game_screen, solve_astar, "A*")
                    if result and metrics_screen:
                        metrics_screen.focus_last_page()
                        game_state = "METRICS"
                        pygame.display.set_caption("Algorithm Comparison Metrics")

        if game_state == "MENU":
            menu_screen.render(screen)
        elif game_state == "GAME" and game and game_screen:
            game_screen.render(screen, game)
        elif game_state == "METRICS" and metrics_screen:
            metrics_screen.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
