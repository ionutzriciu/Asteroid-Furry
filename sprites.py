"""
This module contains the classes for the game's main elements, including players, meteors, and lasers.
All sprite-related functionality is defined and managed here.
"""

import pygame.sprite
from settings import *
from support import *


class Player(pygame.sprite.Sprite):
    """
    Represents the player's spaceship in the game.

    Attributes:
        sprite_groups: Groups to which the player sprite belongs.
        lasers_group: Group to manage the player's laser sprites.
        energy: Player's energy bar.
    """
    def __init__(self, sprite_groups, lasers_group, energy):
        super().__init__(sprite_groups)
        self.groups = sprite_groups
        self.lasers = lasers_group
        self.energy = energy
        self.center_frame = pygame.image.load(join('data', 'images', 'space_ship', 'red', 'center.png'))
        self.left_frames = folder_importer('data', 'images', 'space_ship', 'red', 'Left')
        self.right_frames = folder_importer('data', 'images', 'space_ship', 'red', 'Right')
        self.image = image_transformer(self.center_frame, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH / 2, 700))
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 500
        self.frame_index_left = 0
        self.frame_index_right = 0
        self.laser_sound = pygame.mixer.Sound(laser_sound)

        # Shooting timer logic
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        """
        Manages the cooldown timer for shooting lasers.
        """
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        """
        Updates the player's position, animation, and shooting mechanism.

        Args:
            dt: Delta Time
        """
        keys = pygame.key.get_pressed()
        new_direction = pygame.Vector2(int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]),
                                       int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))

        if new_direction != self.direction:
            self.direction = new_direction
            self.frame_index_left = 0
            self.frame_index_right = 0

        if self.direction.x > 0:
            self.image = image_transformer(self.right_frames[self.frame_index_right], SPACE_SHIP_WIDTH,
                                           SPACE_SHIP_HEIGHT)
            self.frame_index_right = min(self.frame_index_right + 1, len(self.right_frames) - 1)
            self.frame_index_left = 0
        elif self.direction.x < 0:
            self.image = image_transformer(self.left_frames[self.frame_index_left], SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
            self.frame_index_left = min(self.frame_index_left + 1, len(self.left_frames) - 1)
            self.frame_index_right = 0
        else:
            self.image = image_transformer(self.center_frame, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
            self.frame_index_left = 0
            self.frame_index_right = 0

        self.rect.center += self.direction * self.speed * dt
        self.rect.centerx = max(self.rect.width / 2, min(WINDOW_WIDTH - self.rect.width / 2, self.rect.centerx))
        self.rect.centery = max(self.rect.height / 2, min(WINDOW_HEIGHT - self.rect.height / 2, self.rect.centery))

        if keys[pygame.K_SPACE] and self.can_shoot:
            if self.energy.energy_width == 0:
                self.can_shoot = False
            else:
                self.shoot()
                self.special_move()

        self.energy.increse_energy()
        self.laser_timer()

    def reduce_energy(self):
        """Reduces the player's energy."""
        self.energy.reduce_energy()

    def special_move(self):
        """
        Executes a special move by reducing energy and adjusting the laser cooldown duration.
        """
        self.reduce_energy()
        if self.energy.energy_width > 50:
            self.cooldown_duration = 0
        else:
            self.cooldown_duration = 400

    def shoot(self):
        """
        Shoots a laser from the player's position.
        """
        laser = Laser(self.groups, self)
        self.lasers.add(laser)
        self.laser_sound.play()
        self.can_shoot = False
        self.laser_shoot_time = pygame.time.get_ticks()


class Laser(pygame.sprite.Sprite):
    """
    Represents a laser shot by the player.

    Attributes:
        sprite_groups: Groups to which the laser sprite belongs.
        player: The player who shot the laser.
    """
    def __init__(self, sprite_groups, player):
        super().__init__(sprite_groups)
        self.groups = sprite_groups
        self.player = player
        self.initial_image = pygame.image.load(join('data', 'images', 'laser', 'Laser.png')).convert_alpha()
        self.angle = 121
        self.rotated_image = pygame.transform.rotate(self.initial_image, self.angle)
        self.image = image_transformer(self.rotated_image, LASER_WIDTH, LASER_HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)

        # Relative offset from player position
        self.offset_x = -6  # Adjust these values as needed
        self.offset_y = -30  # Adjust these values as needed

        # Set the initial position of the laser
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.player.rect.centerx + self.offset_x, self.player.rect.centery + self.offset_y)

    def update(self, dt):
        """
        Updates the position of the laser and destroys it if it moves off-screen.

        Args:
            dt: Delta time
        """
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    """
    Represents a meteor in the game.

    Attributes:
        sprite_group: Groups to which the meteor sprite belongs.
        meteors: Collection of meteor sprites.
    """
    def __init__(self, sprite_group, meteors):
        super().__init__(sprite_group)
        self.meteors = meteors
        self.groups = sprite_group
        self.meteor_frames = folder_importer('data', 'images', 'meteor')

        # Transform and set the initial image
        self.image = image_transformer(self.meteor_frames[0], METEOR_HEIGHT, METEOR_WIDTH)
        self.rect = self.image.get_rect(midbottom=(randint(50, WINDOW_WIDTH - 50), 0))
        self.mask = pygame.mask.from_surface(self.image)

        # Animation
        self.frame_index = 0
        self.animation_speed = 0.27  # Adjust animation speed as needed

        # Movement - random direction and speed
        self.direction = pygame.Vector2(random.uniform(-1, 1), 1)
        self.direction.x *= random.uniform(0.5, 1.0)
        self.speed = random.uniform(150, 300)
        self.velocity = self.direction * self.speed

    def update(self, dt):
        """
        Updates the position and animation of the meteor, and destroys it if it moves off-screen.

        Args:
            dt: Delta Time
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.meteor_frames):
            self.frame_index = 0

        current_frame = self.meteor_frames[int(self.frame_index)]
        self.image = image_transformer(current_frame, METEOR_HEIGHT, METEOR_WIDTH)

        self.rect.center += self.velocity * dt

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class AnimatedExplosion(pygame.sprite.Sprite):
    """
    Represents an animated explosion.

    Attributes:
        pos: Position where the explosion occurs.
        groups: Groups to which the explosion sprite belongs.
    """
    def __init__(self, pos, groups):
        super().__init__(groups)
        original_frames = png_image_cutter(join('data', 'images', 'explosions', '3.png'), 190, 190)
        self.frames = [image_transformer(frame, 100, 100) for frame in original_frames]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.animation_speed = 0.5

    def update(self, dt):
        """
        Updates the animation of the explosion and destroys it when the animation is complete.

        Args:
            dt: Delta time
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(center=self.rect.center)


class PlayerExplosion(AnimatedExplosion):
    """
    Represents an animated explosion for the player.

    Attributes:
        pos: Position where the explosion occurs.
        groups: Groups to which the explosion sprite belongs.
    """
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        original_frames = png_image_cutter(join('data', 'images', 'explosions', '1.png'), 196, 190)
        self.frames = [image_transformer(frame, 150, 150) for frame in original_frames]


class Health(pygame.sprite.Sprite):
    """
    Represents the health bar for the player.

    Attributes:
        groups: Groups to which the health bar sprite belongs.
    """
    def __init__(self, groups):
        super().__init__(groups)

        # Health attributes
        self.initial_width = 300
        self.width = self.initial_width
        self.height = 10
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))  # Green rectangle
        self.rect = self.image.get_rect(center=(170, 650))

        # Timer mechanics
        self.can_heal = True
        self.last_heal_time = pygame.time.get_ticks()
        self.cool_down_duration = 800

    def increase_health(self):
        """
        Increases the player's health over time based on a cooldown duration.
        """
        current_time = pygame.time.get_ticks()
        if self.can_heal and current_time >= self.last_heal_time + self.cool_down_duration:
            if self.width < self.initial_width:
                self.width += 5
                if self.width > self.initial_width:
                    self.width = self.initial_width
                self.last_heal_time = current_time
                self.update_image()

    def reduce_health(self):
        """Reduces the player's health."""
        self.width -= 10
        if self.width < 0:
            self.width = 0
        self.update_image()

    def update_image(self):
        """Updates the health bar's image and rect."""
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=self.rect.center)


class Energy(pygame.sprite.Sprite):
    """
    Represents the energy bar for the player.

    Attributes:
        groups: Groups to which the energy bar sprite belongs.
    """
    def __init__(self, groups):
        super().__init__(groups)

        # Energy attributes
        self.initial_width = 200
        self.energy_width = self.initial_width
        self.height = 10
        self.image = pygame.Surface((self.energy_width, self.height))
        self.image.fill((0, 128, 255))  # Blue rectangle
        self.rect = self.image.get_rect(center=(170, 665))

        # Timer mechanics
        self.can_regenerate_energy = True
        self.last_regeneration = pygame.time.get_ticks()
        self.cool_down_duration = 100

    def increse_energy(self):
        """
        Increases the player's energy over time based on a cooldown duration.
        """
        current_time = pygame.time.get_ticks()
        if self.can_regenerate_energy and current_time >= self.last_regeneration + self.cool_down_duration:
            if self.energy_width < self.initial_width:
                self.energy_width += 5
                if self.energy_width > self.initial_width:
                    self.energy_width = self.initial_width
                self.last_regeneration = current_time
                self.update_image()

    def reduce_energy(self):
        """Reduces the player's energy."""
        self.energy_width -= 5
        if self.energy_width < 0:
            self.energy_width = 0
        self.update_image()

    def update_image(self):
        """Updates the energy bar's image and rect."""
        self.image = pygame.Surface((self.energy_width, self.height))
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect(center=self.rect.center)


class Stars(pygame.sprite.Sprite):
    """
    Represents a star in the background.

    Attributes:
        groups: Groups to which the star sprite belongs.
    """
    def __init__(self, groups):
        super().__init__(groups)
        self.initial_image = pygame.image.load(join('data', 'images', 'star.png')).convert_alpha()
        self.angle = 303
        self.speed = 1
        self.rotated_image = pygame.transform.rotate(self.initial_image, self.angle)
        self.image = pygame.transform.scale(self.rotated_image, (100, 100))
        self.rect = self.image.get_rect(center=(randint(0, 1280), -10))

    def update(self, dt):
        """
        Updates the position of the star and destroys it if it moves off-screen.

        Args:
            dt: Delta Time
        """
        self.rect.centery += 400 * self.speed * dt
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
