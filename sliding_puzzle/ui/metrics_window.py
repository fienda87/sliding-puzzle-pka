from __future__ import annotations

from dataclasses import dataclass

import pygame

from ui.screens import MetricsScreen

try:
    from pygame._sdl2 import Renderer, Texture, Window
except Exception:  # pragma: no cover
    Renderer = None  # type: ignore[assignment]
    Texture = None  # type: ignore[assignment]
    Window = None  # type: ignore[assignment]


@dataclass
class MetricsWindowConfig:
    width: int = 560
    height: int = 480
    sort_by_time: bool = False


class MetricsWindow:
    def __init__(self, config: MetricsWindowConfig | None = None):
        self.config = config or MetricsWindowConfig()

        self._window: Window | None = None
        self._renderer: Renderer | None = None
        self._texture: Texture | None = None
        self._surface: pygame.Surface | None = None

        self._screen: MetricsScreen | None = None
        self._results: list[dict[str, object]] | None = None

        self._mouse_pos = (0, 0)

    @property
    def window_id(self) -> int | None:
        return None if self._window is None else self._window.id

    def is_open(self) -> bool:
        return self._window is not None

    def open(self, results: list[dict[str, object]]) -> bool:
        if self._window is not None:
            return True

        if Window is None or Renderer is None or Texture is None:
            return False

        self._results = results

        self._window = Window(
            "Algorithm Comparison Metrics",
            size=(self.config.width, self.config.height),
            resizable=True,
        )
        self._renderer = Renderer(self._window)
        self._resize_surfaces(self.config.width, self.config.height)

        self._screen = MetricsScreen(
            self.config.width,
            self.config.height,
            results,
            sort_by_time=self.config.sort_by_time,
        )
        self._mouse_pos = (0, 0)
        return True

    def close(self) -> None:
        if self._window is not None:
            self._window.destroy()

        self._window = None
        self._renderer = None
        self._texture = None
        self._surface = None
        self._screen = None
        self._results = None

    def _resize_surfaces(self, width: int, height: int) -> None:
        if self._renderer is None or Texture is None:
            return

        self._surface = pygame.Surface((width, height))
        self._texture = Texture(self._renderer, size=(width, height))

    def _is_event_for_this_window(self, event: pygame.event.Event) -> bool:
        return self._window is not None and hasattr(event, "window") and event.window == self._window.id

    def handle_event(self, event: pygame.event.Event) -> bool:
        if self._window is None or self._screen is None:
            return False

        if event.type == pygame.WINDOWCLOSE and self._is_event_for_this_window(event):
            self.close()
            return True

        if event.type in (pygame.WINDOWRESIZED, pygame.WINDOWSIZECHANGED) and self._is_event_for_this_window(event):
            new_w = getattr(event, "x", None) or getattr(event, "w", None)
            new_h = getattr(event, "y", None) or getattr(event, "h", None)
            if isinstance(new_w, int) and isinstance(new_h, int) and new_w > 0 and new_h > 0:
                self._resize_surfaces(new_w, new_h)
                self._screen.resize(new_w, new_h)
            return True

        if event.type == pygame.MOUSEMOTION and self._is_event_for_this_window(event):
            self._mouse_pos = event.pos
            self._screen.update_hover(self._mouse_pos)
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._is_event_for_this_window(event):
            action = self._screen.handle_click(event.pos)
            self._apply_action(action)
            return True

        if event.type == pygame.KEYDOWN and self._is_event_for_this_window(event):
            if event.key == pygame.K_ESCAPE:
                self.close()
            elif event.key in (pygame.K_LEFT, pygame.K_PAGEUP):
                self._screen.previous_page()
            elif event.key in (pygame.K_RIGHT, pygame.K_PAGEDOWN):
                self._screen.next_page()
            return True

        return False

    def _apply_action(self, action: str | None) -> None:
        if self._screen is None:
            return

        if action == "prev":
            self._screen.previous_page()
            # Ensure window is still active after pagination
            if self._window is None:
                return
        elif action == "next":
            self._screen.next_page()
            # Ensure window is still active after pagination
            if self._window is None:
                return
        elif action == "close":
            self.close()

    def render(self) -> None:
        if self._window is None or self._renderer is None or self._texture is None or self._surface is None or self._screen is None:
            return

        size = self._window.size
        if tuple(size) != self._surface.get_size():
            self._resize_surfaces(size[0], size[1])
            self._screen.resize(size[0], size[1])

        self._screen.render(self._surface)

        self._texture.update(self._surface)
        self._renderer.clear()
        self._renderer.blit(self._texture)
        self._renderer.present()
