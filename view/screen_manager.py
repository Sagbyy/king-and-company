import pygame
from typing import Callable, Dict, Any, Optional


class ScreenManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.current_screen: Optional[Callable] = None
        self.screen_data: Dict[str, Any] = {}
        self.running = True

    def register_screen(self, screen_name: str, screen_func: Callable) -> None:
        """Register a screen function with a name."""
        self.screen_data[screen_name] = screen_func

    def switch_screen(self, screen_name: str, *args, **kwargs) -> None:
        """Switch to a different screen."""
        if screen_name in self.screen_data:
            self.current_screen = self.screen_data[screen_name]
            self.current_screen_args = args
            self.current_screen_kwargs = kwargs

    def run(self) -> None:
        """Main game loop."""
        clock = pygame.time.Clock()

        while self.running:
            if self.current_screen:
                result = self.current_screen(
                    self.screen, *self.current_screen_args, **self.current_screen_kwargs
                )

                if isinstance(result, tuple):
                    screen_name, data = result
                    if screen_name == "quit":
                        self.running = False
                    else:
                        self.switch_screen(screen_name, data)
                elif result == "quit":
                    self.running = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
