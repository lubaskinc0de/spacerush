import pygame.time

from pygame.sprite import Sprite
from pygame import Surface
from pygame import key as pygame_key

from pygame import K_LEFT, K_RIGHT


class Player(Sprite):
    """Player sprite"""

    def __init__(
        self, window_width: int, window_height: int, player_img: Surface
    ) -> None:
        super().__init__()

        self.image = player_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.centerx = window_width / 2
        self.rect.bottom = window_height - 10

        self.speed = 0

        self.window_height = window_height
        self.window_width = window_width

        self._shoot_delay = 250
        self._last_shoot = pygame.time.get_ticks()

    def _move(self) -> None:
        """Move player with speed"""

        self.rect.x += self.speed

    def is_reloaded(self) -> bool:
        """Is player ready for shoot"""

        now = pygame.time.get_ticks()
        return now - self._last_shoot > self._shoot_delay

    def shoot(self) -> None:
        """Reset last shoot"""

        self._last_shoot = pygame.time.get_ticks()

    def update(self):
        self.speed = 0

        keys_pressed = pygame_key.get_pressed()

        if keys_pressed[K_LEFT]:
            self.speed = -8
        if keys_pressed[K_RIGHT]:
            self.speed = 8

        self._move()

        if self.rect.right > self.window_width:
            self.rect.right = self.window_width
        if self.rect.left < 0:
            self.rect.left = 0
