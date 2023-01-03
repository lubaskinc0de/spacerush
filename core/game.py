import pygame

from sprites.player import Player
from sprites.mob import Mob

from .window import Window

class Game:
    '''Main game class'''

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    def __init__(
        self, width: int, height: int,
        caption: str, fps: int) -> None:

        self._sprites = pygame.sprite.Group()
        self._mobs = pygame.sprite.Group()

        self._clock = pygame.time.Clock()

        self._initialize_pygame()
        self._initialize_window(width, height, caption)

        self._player = Player(50, 40, self._window.width, self._window.height)
        self._player.set_color(self.GREEN)
        
        self._add_sprite(self._player)
        self._add_mobs()

        self._fps = fps
    

    def _initialize_pygame(self) -> None:
        '''Initialize pygame'''

        pygame.init()
        pygame.mixer.init()
    
    
    def _initialize_window(
        self, window_w: int,
        window_h: int, window_caption: str) -> None:
        '''Initialize window'''

        self._window = Window(
            window_w, window_h, window_caption
            )
        
        self._screen: pygame.Surface = self._window.get_screen()

        self._window.set_caption()

   
    def _add_sprite(self, sprite: pygame.sprite.Sprite) -> None:
        '''Add sprite to the game'''

        self._sprites.add(sprite)
    
    def _add_mob(self, mob: Mob):
        '''Add mob to the mobs'''

        self._mobs.add(mob)
    
    def _add_mobs(self) -> None:
        '''Add mobs to the game'''

        for _ in range(8):
            m = Mob(30, 40, self._window.width, self._window.height)
            m.set_color(self.RED)
            
            self._add_sprite(m)
            self._add_mob(m)
    
    def _stop(self):
        '''Stop the game'''

        self._is_game_running = False

    def start(self) -> None:
        '''Start the game'''

        self._is_game_running = True

        self._main_loop()
    
    def _dispatch_events(self, events: list[pygame.event.Event]):
        '''Dispatch game events'''

        for event in events:
            if event.type == pygame.QUIT:
                self._stop()
    
    def _update_sprites(self) -> None:
        '''Update game sprites'''

        self._sprites.update()
    
    def _draw_sprites(self) -> None:
        '''Render all sprites'''

        self._sprites.draw(self._screen)
    
    def _fill_screen(self, color: tuple[int, int, int]) -> None:
        '''Fill the screen with color'''

        self._screen.fill(color)

    def _flip_screen(self) -> None:
        '''Flip the screen'''

        pygame.display.flip()
    
    def _render(self):
        '''Render the game'''

        self._fill_screen(self.BLACK)
        self._draw_sprites()
        self._flip_screen()

    def _update(self):
        self._update_sprites()

    def _quit_game(self) -> None:
        '''Quit the game'''

        pygame.quit()
    
    def _main_loop(self) -> None:
        '''The main game loop'''

        while self._is_game_running:
            events: list[pygame.event.Event] = pygame.event.get()

            self._dispatch_events(events)
            self._update()

            if pygame.sprite.spritecollide(self._player, self._mobs, False):
                self._stop()

            self._render()

            self._clock.tick(self._fps)
        
        self._quit_game()

