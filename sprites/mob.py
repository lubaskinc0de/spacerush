from pygame.sprite import Sprite
from pygame import Surface
from pygame import key as pygame_key

import random

class Mob(Sprite):
    '''Mob sprite'''

    def __init__(
        self, width: int, height: int,
        window_w: int, window_h: int) -> None:

        super().__init__()

        self.window_w = window_w
        self.window_h = window_h

        self.image = Surface((width, height))
        self.rect = self.image.get_rect()

        self.speedy = self._get_random_speed(1, 8)
        self.speedx = self._get_random_speed(-3, 3)

        self._set_coords(*self._get_random_coords())

    def set_color(self, color: tuple[int, int, int]) -> None:
        '''Set mob color'''

        self.image.fill(color)

    def _get_random_coords(self) -> tuple[int, int]:
        '''Get random coords'''

        random_x: int = random.randrange(self.window_w - self.rect.width)
        random_y: int = random.randrange(-100, -40)

        return (random_x, random_y)
    
    def _get_random_speed(self, *range) -> int:
        '''Get random speed between range'''

        return random.randrange(*range)

    def _set_coords(self, x: int, y: int) -> None:
        '''Set mob coords'''

        self.rect.x = x
        self.rect.y = y

    def update(self) -> None:
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > self.window_h + 10 or self.rect.left < -25 or self.rect.right > self.window_w + 20:
            self._set_coords(*self._get_random_coords())
            self.speedy = self._get_random_speed(1, 8)
            self.speedx = self._get_random_speed(-3, 3)

