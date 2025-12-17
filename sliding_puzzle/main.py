import sys

import pygame

from game.puzzle_game import PuzzleGame
from game.puzzle_solver import solve_astar, solve_bfs, solve_dfs
from ui.metrics_window import MetricsWindow
from ui.screens import GameScreen, MenuScreen
from utils.constants import COLOR_BACKGROUND, FPS, SOLVER_DELAY_MS, WINDOW_HEIGHT, WINDOW_WIDTH


def animate_solution(
    game: PuzzleGame,
    screen: pygame.Surface,
    game_screen: GameScreen,
    solution_path,
    *,
    metrics_window: MetricsWindow | None = None,
) -> None:
    """Animate a solver's solution path by stepping through board states."""

    game.is_animating = True

    for state in solution_path:
        game.apply_board_state(state.board)

        screen.fill(COLOR_BACKGROUND)
        game_screen.render(screen, game)
        pygame.display.flip()

        pygame.time.delay(SOLVER_DELAY_MS)

        for event in pygame.event.get():
            if metrics_window is not None:
                metrics_window.handle_event(event)

            if event.type == pygame.QUIT:
                if metrics_window is not None:
                    metrics_window.close()
                pygame.quit()
                sys.exit()

    game.is_animating = False


def solve_and_animate(
    game: PuzzleGame,
    screen: pygame.Surface,
    game_screen: GameScreen,
    solver_func,
    algorithm_label: str,
    *,
    metrics_window: MetricsWindow | None = None,
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
    animate_solution(
        game,
        screen,
        game_screen,
        result["solution_path"],
        metrics_window=metrics_window,
    )
    game.apply_board_state(starting_board)

    return result


def main() -> None:
    pygame.init()

    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    pygame.display.set_caption("Sliding Puzzle Game")

    clock = pygame.time.Clock()

    game_state = "MENU"

    menu_screen = MenuScreen(*window_size)
    game: PuzzleGame | None = None
    game_screen: GameScreen | None = None

    metrics_window = MetricsWindow()

    running = True
    game_mouse_pos = (0, 0)

    while running:
        if game_state == "MENU":
            menu_screen.update_hover(game_mouse_pos)
        elif game_state == "GAME" and game_screen:
            game_screen.update_hover(game_mouse_pos)

        for event in pygame.event.get():
            if metrics_window.handle_event(event):
                continue

            if event.type == pygame.QUIT:
                running = False
                continue

            new_window_size = None
            if event.type == pygame.VIDEORESIZE:
                new_window_size = event.size
            elif event.type in (pygame.WINDOWRESIZED, pygame.WINDOWSIZECHANGED) and hasattr(event, "x") and hasattr(
                event, "y"
            ):
                new_window_size = (event.x, event.y)

            if new_window_size is not None:
                window_size = new_window_size
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
                menu_screen = MenuScreen(*window_size)
                if game is not None and game_screen is not None:
                    game_screen = GameScreen(
                        *window_size,
                        game_screen.grid_size,
                        game.metrics_results,
                    )
                continue

            if event.type == pygame.MOUSEMOTION:
                game_mouse_pos = event.pos
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "MENU":
                    level_data = menu_screen.handle_click(event.pos)
                    if level_data:
                        game = PuzzleGame(level_data["board"], level_data["goal"])
                        game_screen = GameScreen(
                            *window_size,
                            level_data["grid_size"],
                            game.metrics_results,
                        )
                        game_state = "GAME"
                        pygame.display.set_caption("Sliding Puzzle Game")

                elif game_state == "GAME" and game and game_screen:
                    action, data = game_screen.handle_click(event.pos, game)

                    if action == "tile_click" and not game.is_animating and not game_screen.is_solving:
                        row, col = data
                        game.handle_tile_click(row, col)

                    elif action == "solve_bfs":
                        solve_and_animate(
                            game,
                            screen,
                            game_screen,
                            solve_bfs,
                            "BFS",
                            metrics_window=metrics_window,
                        )

                    elif action == "solve_dfs":
                        solve_and_animate(
                            game,
                            screen,
                            game_screen,
                            solve_dfs,
                            "DFS",
                            metrics_window=metrics_window,
                        )

                    elif action == "solve_astar":
                        solve_and_animate(
                            game,
                            screen,
                            game_screen,
                            solve_astar,
                            "A*",
                            metrics_window=metrics_window,
                        )

                    elif action == "shuffle" and not game.is_animating and not game_screen.is_solving:
                        game.shuffle()

                    elif action == "undo" and not game.is_animating and not game_screen.is_solving:
                        game.undo()

                    elif action == "metrics":
                        metrics_window.open(game.metrics_results)

                    elif action == "back" and not game.is_animating and not game_screen.is_solving:
                        menu_screen.reset()
                        game = None
                        game_screen = None
                        metrics_window.close()
                        game_state = "MENU"
                        pygame.display.set_caption("Sliding Puzzle Game")

            elif event.type == pygame.KEYDOWN:
                if game_state == "MENU" and event.key == pygame.K_ESCAPE:
                    menu_screen.go_back()
                    continue

                if game_state != "GAME" or not game or not game_screen:
                    continue

                if event.key == pygame.K_m:
                    metrics_window.open(game.metrics_results)
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
                elif event.key == pygame.K_ESCAPE:
                    menu_screen.reset()
                    game = None
                    game_screen = None
                    metrics_window.close()
                    game_state = "MENU"
                    pygame.display.set_caption("Sliding Puzzle Game")
                elif event.key == pygame.K_SPACE:
                    solve_and_animate(
                        game,
                        screen,
                        game_screen,
                        solve_bfs,
                        "BFS",
                        metrics_window=metrics_window,
                    )
                elif event.key == pygame.K_s:
                    solve_and_animate(
                        game,
                        screen,
                        game_screen,
                        solve_dfs,
                        "DFS",
                        metrics_window=metrics_window,
                    )
                elif event.key == pygame.K_a:
                    solve_and_animate(
                        game,
                        screen,
                        game_screen,
                        solve_astar,
                        "A*",
                        metrics_window=metrics_window,
                    )

        if game_state == "MENU":
            menu_screen.render(screen)
        elif game_state == "GAME" and game and game_screen:
            game_screen.render(screen, game)

        pygame.display.flip()

        metrics_window.render()
        clock.tick(FPS)

    metrics_window.close()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
