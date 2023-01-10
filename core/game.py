import os
import random

import pygame

from random import randrange
from time import sleep
from typing import Optional

from sprites import Bullet, Explosion, Mob, Player, Pow

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
        lives: int = 3,
    ) -> None:

        self._assets_path = self._get_assets_path()
        self._mobs_count = mobs_count
        self._is_god_mode = is_god_mode

        self._create_sprite_groups()

        self._clock = pygame.time.Clock()

        self._initialize_pygame()
        self._initialize_window(width, height, caption)

        self._load_images()

        self._player = Player(
            self._window.width, self._window.height, self._get_player_img(), lives
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

    def _create_sprite_groups(self):
        """Create sprite groups"""

        self._sprites = pygame.sprite.Group()
        self._mobs = pygame.sprite.Group()
        self._bullets = pygame.sprite.Group()
        self._powerups = pygame.sprite.Group()

    def _load_images(self):
        """Preload all images"""

        self._pow_images = self._load_power_images()

        self._preload_images = {
            "player": self._load_player_img(),
            "bullet": self._load_bullet_img(),
            "heart": self._load_heart_img(),
            "pow_gun": self._pow_images[0],
            "pow_shield": self._pow_images[1],
        }

        self._explosion_images = self._load_explosions_images()
        self._explosions = {
            "lg": self._explosion_images.get("lg"),
            "sm": self._explosion_images.get("sm"),
            "player": self._explosion_images.get("player"),
        }

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

        powerup_sound_path: str = os.path.join(self._assets_path, "music/powerup.mp3")
        self._powerup_sound = pygame.mixer.Sound(powerup_sound_path)

    def _get_assets_path(self) -> str:
        """Get assets path"""

        path = os.path.dirname(__file__)
        return os.path.join(path, "../assets/")

    def _load_bg(self) -> Background:
        """Load background"""

        bg_path = os.path.join(self._assets_path, "bg/bg.jpg")

        return Background(bg_path)

    def _load_img(self, path: str, *size: Optional[int]) -> pygame.Surface:
        """Helper method for loading images"""

        img = pygame.image.load(path).convert()
        img.set_colorkey(self.BLACK)

        if any(size):
            return pygame.transform.scale(img, size)

        return img

    def _load_sprite_img(self, filename: str, *size: Optional[int]):
        """Load sprite image"""

        img_path = os.path.join(self._assets_path, "sprites/{}".format(filename))

        return self._load_img(img_path, *size)

    def _load_player_img(self) -> pygame.Surface:
        """Load player img"""

        return self._load_sprite_img("player.png")

    def _load_bullet_img(self) -> pygame.Surface:
        """Load bullet img"""

        return self._load_sprite_img("bullet.png")

    def _load_heart_img(self) -> pygame.Surface:
        """Load heart img"""

        return self._load_sprite_img("heart.png")

    def _load_power_images(self) -> list[pygame.Surface]:
        """Load pow gun img"""

        return [
            self._load_sprite_img("pow_gun.png", 48, 28),
            self._load_sprite_img("heart.png"),
        ]

    def _load_explosions_images(self) -> dict["str", list[pygame.Surface]]:
        """Load explosions"""

        lg: list[pygame.Surface] = []
        sm: list[pygame.Surface] = []
        player: list[pygame.Surface] = []

        for explosion_i in range(8 + 1):
            filename = "regularExplosion0{}.png".format(explosion_i)
            player_filename = "sonicExplosion0{}.png".format(explosion_i)

            explosion_img_path = os.path.join(
                self._assets_path, "explosions/{}".format(filename)
            )
            player_explosion_img_path = os.path.join(
                self._assets_path, "explosions/{}".format(player_filename)
            )

            img = self._load_img(explosion_img_path)
            img.set_colorkey(self.BLACK)

            img_lg = pygame.transform.scale(img, (75, 75))
            lg.append(img_lg)

            img_sm = pygame.transform.scale(img, (32, 32))
            sm.append(img_sm)

            player_explosion_img = self._load_img(player_explosion_img_path)
            player_explosion_img.set_colorkey(self.BLACK)

            player.append(player_explosion_img)

        return {
            "lg": lg,
            "sm": sm,
            "player": player,
        }

    def _get_player_img(self) -> pygame.Surface:
        """Get player img"""

        return self._preload_images.get("player")

    def _get_bullet_img(self) -> pygame.Surface:
        """Get bullet img"""

        return self._preload_images.get("bullet")

    def _get_heart_img(self) -> pygame.Surface:
        """Get heart img"""

        return self._preload_images.get("heart")

    def _get_power_images(self) -> dict[str, pygame.Surface]:
        """Get power images"""

        return {
            "gun": self._preload_images.get("pow_gun"),
            "shield": self._preload_images.get("pow_shield"),
        }

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

    def _add_powerup(self, center: tuple[int, int]):
        pow_type = random.choice(["gun", "shield"])
        random_pow_img = self._get_power_images().get(pow_type)
        powerup = Pow(*center, random_pow_img, self._window.height, pow_type)

        self._add_sprite(powerup)
        self._powerups.add(powerup)

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

    def _shoot(self, direction: str) -> None:
        """Shoot!"""

        x = self._player.rect.left if direction == "left" else self._player.rect.right

        if self._player.is_reloaded():
            self._player.shoot()

            bullet = Bullet(x, self._player.rect.y, self._get_bullet_img())

            self._add_sprite(bullet)
            self._add_bullet(bullet)

            if self._player.is_double_shot:
                bullet_two = Bullet(
                    self._player.rect.right
                    if x == self._player.rect.left
                    else self._player.rect.left,
                    self._player.rect.y,
                    self._get_bullet_img(),
                )

                self._add_sprite(bullet_two)
                self._add_bullet(bullet_two)

                self._shoot_sound.play()

            self._shoot_sound.play()

    def _dispatch_events(self, events: list[pygame.event.Event]):
        """Dispatch game events"""

        for event in events:
            if event.type == pygame.QUIT:
                self._stop()
                break

            key_states = pygame.key.get_pressed()

            if key_states[pygame.K_z]:
                self._shoot("left")
            if key_states[pygame.K_x]:
                self._shoot("right")

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
        self._draw_lives(
            self._screen,
            self._window.width - ((30 * self._player.lives) + 10),
            5,
            self._player.lives,
        )

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

    def _blow_up(self, size: str, center: tuple[int, int]):
        """Spawn new explosion"""

        expl = Explosion(center, size, self._explosion_images)
        self._add_sprite(expl)

        return expl

    def _check_player_collide_mobs(self) -> None:
        """Game over if player collide with mobs"""

        hits: list[pygame.sprite.Sprite] = pygame.sprite.spritecollide(
            self._player, self._mobs, True, pygame.sprite.collide_rect_ratio(0.52)
        )

        for hit in hits:
            hit: Mob
            self._health -= hit.radius * 2
            self._blow_up("sm", hit.rect.center)
            self._add_mob()

            if self._health < 0:
                self._death_expl = self._blow_up("player", self._player.rect.center)

                self._player.hide()
                self._player.lives -= 1
                self._health = 100

    def _powerup_health(self):
        """Power up health"""

        self._health += random.randrange(10, 30)
        if self._health > 100:
            self._health = 100

    def _powerup_gun(self):
        """Powerup gun"""

        self._player.double_shoot()

    def _check_player_collide_powerups(self) -> None:
        """Power up player if player collide with powerups"""

        hits: list[pygame.sprite.Sprite] = pygame.sprite.spritecollide(
            self._player, self._powerups, True, pygame.sprite.collide_rect_ratio(0.52)
        )

        for hit in hits:
            hit: Pow

            if hit.type == "shield":
                self._powerup_health()
            if hit.type == "gun":
                self._powerup_gun()

            self._powerup_sound.play()

    def _check_bullet_collide_mobs(self) -> None:
        """Kill mobs if bullet colide they"""

        hits = pygame.sprite.groupcollide(
            self._mobs, self._bullets, True, True, pygame.sprite.collide_circle
        )

        for hit in hits:
            hit: Mob
            self._score += 36 - hit.radius

            self._boom_sound.play()
            self._blow_up("lg", hit.rect.center)

            if random.random() > 0.9:
                self._add_powerup(hit.rect.center)
            self._add_mob()

    def _draw_text(
        self,
        surface: pygame.Surface,
        text: str,
        size: int,
        x: int | float,
        y: int | float,
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

    def _draw_lives(self, surface: pygame.Surface, x: int, y: int, lives: int):
        for i in range(lives):
            img_rect = self._get_heart_img().get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y

            surface.blit(self._get_heart_img(), img_rect)

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

            self._check_player_collide_powerups()
            self._check_bullet_collide_mobs()

            if not self._is_god_mode:
                self._check_player_collide_mobs()

            self._render()

            self._clock.tick(self._fps)

            if (
                hasattr(self, "_death_expl")
                and self._player.lives <= 0
                and not self._death_expl.alive()
            ):
                self._stop()

        self._game_over()
        sleep(2)
        self._quit_game()
