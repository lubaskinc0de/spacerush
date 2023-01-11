from pygame.sprite import Sprite
from pygame import Surface
from typing import Tuple
import random
import pygame


class Mob(Sprite):
    """Mob sprite"""

    def __init__(self, window_w: int, window_h: int, mob_img: Surface) -> None:
        super().__init__()

        self.window_w = window_w
        self.window_h = window_h

        self.image_orig = mob_img

        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()

        self.speedy = self._get_random_speed(4, 8)
        self.speedx = self._get_random_speed(-3, 3)

        self._set_coords(*self._get_random_coords())

        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

        self.radius = int(self.rect.width * 0.85 / 2)

    def _get_random_coords(self) -> Tuple[int, int]:
        """Get random coords"""

        random_x: int = random.randrange(self.window_w - self.rect.width)
        random_y: int = random.randrange(-100, -40)

        return (random_x, random_y)

    def _get_random_speed(self, *range) -> int:
        """Get random speed between range"""

        return random.randrange(*range)

    def _set_coords(self, x: int, y: int) -> None:
        """Set mob coords"""

        self.rect.x = x
        self.rect.y = y

    def rotate(self):
        """Rotate mob"""

        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360

            new_image = pygame.transform.rotate(self.image_orig, self.rot)

            old_center = self.rect.center

            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self) -> None:
        self.rotate()

        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if (
            self.rect.top > self.window_h + 10
            or self.rect.left < -25
            or self.rect.right > self.window_w + 20
        ):
            self._set_coords(*self._get_random_coords())
            self.speedy = self._get_random_speed(1, 8)
            self.speedx = self._get_random_speed(-3, 3)
