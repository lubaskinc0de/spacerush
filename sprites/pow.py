from pygame.sprite import Sprite
from pygame import Surface


class Pow(Sprite):
    """Pow sprite"""

    def __init__(
        self, x: int, y: int, pow_img: Surface, window_height: int, type: str
    ) -> None:
        super().__init__()

        self.image = pow_img

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 2
        self.window_height = window_height
        self.type = type

    def update(self) -> None:
        self.rect.y += self.speed

        if self.rect.top > self.window_height:
            self.kill()
