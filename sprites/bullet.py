from pygame.sprite import Sprite
from pygame import Surface

class Bullet(Sprite):
    '''Bullet sprite'''
    
    def __init__(self, width: int, height: int, x: int, y: int) -> None:
        super().__init__()

        self.image = Surface((width, height))

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
    
    def set_color(self, color: tuple[int, int, int]):
        self.image.fill(color)

    def update(self) -> None:
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()