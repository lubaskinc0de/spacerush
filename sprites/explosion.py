from pygame.sprite import Sprite
from pygame import Surface

import pygame


class Explosion(Sprite):
    """Explosion sprite"""

    def __init__(
        self,
        center: tuple[int, int],
        size: str,
        explosion_images: dict[str, list[Surface]],
    ) -> None:
        super().__init__()

        self.size = size
        self.image = explosion_images[self.size][0]

        self.rect = self.image.get_rect()
        self.rect.center = center

        self._frame = 0
        self._last_frame = pygame.time.get_ticks()
        self._frame_rate = 50
        self.explosions_images = explosion_images

    def _is_last_frame(self):
        """Is explosion in the last frame"""

        return self._frame == len(self.explosions_images[self.size])

    def _next_frame(self):
        """Next explosion frame"""

        center = self.rect.center
        self.image = self.explosions_images[self.size][self._frame]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def _animate(self) -> None:
        """Animate frame"""

        now = pygame.time.get_ticks()

        if now - self._last_frame > self._frame_rate:
            self._last_frame = now
            self._frame += 1

            if self._is_last_frame():
                self.kill()
            else:
                self._next_frame()

    def update(self):
        self._animate()
