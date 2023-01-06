from pygame.sprite import Sprite
from pygame import Surface


class Bullet(Sprite):
    """Bullet sprite"""

    def __init__(self, x: int, y: int, bullet_img: Surface) -> None:
        super().__init__()

        self.image = bullet_img
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self) -> None:
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()
