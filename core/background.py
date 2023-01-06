import pygame


class Background:
    """Game bg"""

    def __init__(self, path: str) -> None:
        self._image = pygame.image.load(path).convert()
        self._rect = self._image.get_rect()

    def blit(self, screen: pygame.Surface) -> None:
        """Blit screen"""

        screen.blit(self._image, self._rect)
