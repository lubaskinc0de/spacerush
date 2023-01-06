import os
import pygame

from random import randrange
from time import sleep
from typing import Optional

from sprites.player import Player
from sprites.mob import Mob
from sprites.bullet import Bullet

from .window import Window
from .background import Background


class Game:
    """Main game class"""

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    def __init__(
        self,
        width: int,
        height: int,
        caption: str,
        fps: int,
        mobs_count: int = 10,
        is_god_mode: bool = False,
    ) -> None:

        self._assets_path = self._get_assets_path()
        self._mobs_count = mobs_count
        self._is_god_mode = is_god_mode

        self._sprites = pygame.sprite.Group()
        self._mobs = pygame.sprite.Group()
        self._bullets = pygame.sprite.Group()

        self._clock = pygame.time.Clock()

        self._initialize_pygame()
        self._initialize_window(width, height, caption)

        self._player = Player(
            self._window.width, self._window.height, self._load_player_img()
        )

        self._add_sprite(self._player)
        self._add_mobs()

        self._fps = fps

        self._bg = self._load_bg()
        self._font_name = pygame.font.match_font("arial")

        self._load_sounds()

    def _initialize_pygame(self) -> None:
        """Initialize pygame"""

        pygame.init()
        pygame.mixer.init()

    def _initialize_window(
        self, window_w: int, window_h: int, window_caption: str
    ) -> None:
        """Initialize window"""

        self._window = Window(window_w, window_h, window_caption)

        self._screen: pygame.Surface = self._window.get_screen()

        self._window.set_caption()

    def _play_background_music(self) -> None:
        """Play bg music"""

        music_path: str = os.path.join(
            self._assets_path, "music/neon_sign_circuit_bpm145.ogg"
        )
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.25)

    def _stop_background_music(self) -> None:
        """Stop bg music"""

        pygame.mixer.music.stop()

    def _load_sounds(self) -> None:
        """Load game sounds"""

        shoot_sound_path: str = os.path.join(self._assets_path, "music/laser.mp3")
        self._shoot_sound = pygame.mixer.Sound(shoot_sound_path)

        boom_sound_path: str = os.path.join(self._assets_path, "music/boom.wav")
        self._boom_sound = pygame.mixer.Sound(boom_sound_path)
        self._boom_sound.set_volume(0.3)

        game_over_sound_path: str = os.path.join(
            self._assets_path, "music/game_over.wav"
        )
        self._game_over_sound = pygame.mixer.Sound(game_over_sound_path)

    def _get_assets_path(self) -> str:
        """Get assets path"""

        path = os.path.dirname(__file__)
        return os.path.join(path, "../assets/")

    def _load_bg(self) -> Background:
        """Load background"""

        bg_path = os.path.join(self._assets_path, "bg/bg.jpg")

        return Background(bg_path)

    def _load_img(self, path: str, *size: Optional[tuple[int, int]]) -> pygame.Surface:
        """Helper method for loading images"""

        img = pygame.image.load(path).convert()

        if any(size):
            return pygame.transform.scale(img, size)

        return img

    def _load_player_img(self) -> pygame.Surface:
        """Load player img"""

        player_img_path = os.path.join(self._assets_path, "sprites/player.png")

        return self._load_img(player_img_path)

    def _load_bullet_img(self) -> pygame.Surface:
        """Load bullet img"""

        bullet_img_path = os.path.join(self._assets_path, "sprites/bullet.png")

        return self._load_img(bullet_img_path)

    def _load_mob_img(self) -> pygame.Surface:
        """Load mob img"""

        random_mob: int = randrange(1, 3 + 1)
        mob_img_path = os.path.join(
            self._assets_path, "sprites/mob{}.png".format(random_mob)
        )

        random_width = randrange(45, 70)
        random_height = randrange(32, 58)

        return self._load_img(mob_img_path, random_width, random_height)

    def _add_sprite(self, sprite: pygame.sprite.Sprite) -> None:
        """Add sprite to the game"""

        self._sprites.add(sprite)

    def _add_mob_sprite(self, mob: Mob) -> None:
        self._mobs.add(mob)

    def _add_mob(self) -> None:
        """Add mob to the mobs"""

        m = Mob(self._window.width, self._window.height, self._load_mob_img())

        self._add_sprite(m)
        self._add_mob_sprite(m)

    def _add_mobs(self) -> None:
        """Add mobs to the game"""

        for _ in range(self._mobs_count):
            self._add_mob()

    def _add_bullet(self, bullet: Bullet) -> None:
        """Add bullet to the game"""

        self._bullets.add(bullet)

    def _stop(self):
        """Stop the game"""

        self._stop_background_music()
        self._is_game_running = False

    def start(self) -> None:
        """Start the game"""

        self._is_game_running = True
        self._score = 0
        self._health = 100

        self._play_background_music()
        self._main_loop()

    def _spawn_bullet(self, direction: str) -> None:
        """Shoot!"""

        x = self._player.rect.left if direction == "left" else self._player.rect.right

        bullet = Bullet(x, self._player.rect.y, self._load_bullet_img())

        self._add_sprite(bullet)
        self._add_bullet(bullet)

        self._shoot_sound.play()

    def _dispatch_events(self, events: list[pygame.event.Event]):
        """Dispatch game events"""

        for event in events:
            if event.type == pygame.QUIT:
                self._stop()
                break
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_z:
                        self._spawn_bullet("left")
                    case pygame.K_x:
                        self._spawn_bullet("right")

    def _update_sprites(self) -> None:
        """Update game sprites"""

        self._sprites.update()

    def _draw_sprites(self) -> None:
        """Render all sprites"""

        self._sprites.draw(self._screen)

    def _fill_screen(self, color: tuple[int, int, int]) -> None:
        """Fill the screen with color"""

        self._screen.fill(color)

    def _flip_screen(self) -> None:
        """Flip the screen"""

        pygame.display.flip()

    def _update_screen(self) -> None:
        """Update the screen"""

        pygame.display.update()

    def _blit_bg(self) -> None:
        """Blit the bg"""

        self._bg.blit(self._screen)

    def _draw_info(self) -> None:
        """Draw game info"""

        self._draw_text(
            self._screen, f"Очки: {self._score}", 18, self._window.width / 2, 10
        )
        self._draw_health_bar(self._screen, 5, 5, self._health)

    def _render(self):
        """Render the game"""

        self._fill_screen(self.BLACK)
        self._blit_bg()
        self._draw_sprites()
        self._draw_info()
        self._flip_screen()

    def _render_game_over(self):
        """Render game over screen"""

        self._fill_screen(self.BLACK)
        self._update_screen()
        self._draw_text(
            self._screen,
            "GAME OVER",
            35,
            self._window.width / 2,
            self._window.height / 2,
            self.RED,
        )
        self._draw_text(
            self._screen,
            f"SCORE: {self._score}",
            18,
            self._window.width / 2,
            (self._window.height / 2) + 50,
            self.RED,
        )
        self._flip_screen()

    def _update(self) -> None:
        """Update the game"""

        self._update_sprites()

    def _quit_game(self) -> None:
        """Quit the game"""

        pygame.quit()

    def _check_player_collide_mobs(self) -> None:
        """Game over if player collide with mobs"""

        hits = pygame.sprite.spritecollide(
            self._player, self._mobs, True, pygame.sprite.collide_rect_ratio(0.52)
        )

        for hit in hits:
            self._health -= hit.radius * 2
            self._add_mob()

            if self._health < 0:
                self._stop()

    def _check_bullet_collide_mobs(self) -> None:
        """Kill mobs if bullet colide they"""

        hits = pygame.sprite.groupcollide(
            self._mobs, self._bullets, True, True, pygame.sprite.collide_circle
        )

        for hit in hits:
            self._score += 36 - hit.radius

            self._boom_sound.play()
            self._add_mob()

    def _draw_text(
        self,
        surface: pygame.Surface,
        text: str,
        size: int,
        x: int,
        y: int,
        color: tuple[int, int, int] = (255, 255, 255),
    ):
        """Draw text on the screen"""

        font = pygame.font.Font(self._font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def _draw_health_bar(
        self, surface: pygame.Surface, x: int, y: int, health: int = 0
    ):
        """Draw health bar"""

        if health < 0:
            health = 0

        health_bar_length = 100
        heath_bar_height = 10

        outline_rect = pygame.Rect(x, y, health_bar_length, heath_bar_height)
        fill_rect = pygame.Rect(x, y, health, heath_bar_height)

        pygame.draw.rect(surface, self.WHITE, outline_rect)
        pygame.draw.rect(surface, self.GREEN, fill_rect)
        self._draw_text(surface, f"{health}%", 18, x + (health_bar_length + 30), 0)

    def _game_over(self):
        """Game over"""

        self._render_game_over()
        self._game_over_sound.play()

    def _main_loop(self) -> None:
        """The main game loop"""

        while self._is_game_running:
            events: list[pygame.event.Event] = pygame.event.get()

            self._dispatch_events(events)
            self._update()

            self._check_bullet_collide_mobs()

            if not self._is_god_mode:
                self._check_player_collide_mobs()

            self._render()

            self._clock.tick(self._fps)

        self._game_over_sound.play()

        self._game_over()
        self._quit_game()
