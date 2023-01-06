from dataclasses import dataclass

import pygame


@dataclass
class Window:
    width: int
    height: int
    caption: str

    def get_screen(self) -> pygame.Surface:
        screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))

        return screen

    def set_caption(self) -> None:
        pygame.display.set_caption(self.caption)
