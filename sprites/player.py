from pygame.sprite import Sprite
from pygame import Surface
from pygame import key as pygame_key

from pygame import K_LEFT, K_RIGHT, K_UP

class Player(Sprite):
    '''Player sprite'''

    def __init__(
        self, width: int, height: int,
        window_width: int, window_height: int,
        ) -> None:
        super().__init__()

        self.image = Surface((width, height))
        self.rect = self.image.get_rect()

        self.rect.centerx = window_width / 2
        self.rect.bottom = window_height - 10

        self.speed = 0

        self.window_height = window_height
        self.window_width = window_width
    
    def set_color(self, color: tuple[int, int, int]) -> None:
        '''Set player color'''

        self.image.fill(color)
    
    def _move(self) -> None:
        '''Move player with speed'''

        self.rect.x += self.speed

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