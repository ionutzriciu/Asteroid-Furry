import pygame
from settings import *
from support import *
from bar_health_energy import Health, Energy

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_groups, lasers_group, health, energy):
        super().__init__(sprite_groups)
        self.groups = sprite_groups
        self.lasers = lasers_group
        self.health = health  # Health bar instance
        self.energy = energy  # Energy bar instance
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
        Updates the player's position, animation, health, energy, and shooting mechanism.

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
            if self.energy.width == 0:
                self.can_shoot = False
            else:
                self.shoot()
                self.special_move()

        self.energy.increase(1)  # Passing the amount to increase energy by
        self.laser_timer()

    def reduce_health(self, amount):
        self.health.reduce(amount)  # Passing the amount to reduce health by

    def increase_health(self, amount):
        self.health.increase(amount)  # Passing the amount to increase health by

    def reduce_energy(self, amount):
        self.energy.reduce(amount)  # Passing the amount to reduce energy by

    def increase_energy(self, amount):
        self.energy.increase(amount)  # Passing the amount to increase energy by

    def special_move(self):
        self.reduce_energy(10)  # Reduces energy by a specific amount
        if self.energy.width > 50:
            self.cooldown_duration = 0
        else:
            self.cooldown_duration = 400

    def shoot(self):
        laser = Laser(self.groups, self)
        self.lasers.add(laser)
        self.laser_sound.play()
        self.can_shoot = False
        self.laser_shoot_time = pygame.time.get_ticks()

    def take_damage(self, amount):
        self.reduce_health(amount)
        if self.health.width <= 0:
            self.die()

    def die(self):
        explosion = PlayerExplosion(self.rect.center, self.groups)
        self.kill()  # Remove player from all groups, effectively "killing" the player


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
    def __init__(self, pos, groups):
        super().__init__(groups)
        original_frames = png_image_cutter(join('data', 'images', 'explosions', '1.png'), 196, 190)
        self.frames = [image_transformer(frame, 150, 150) for frame in original_frames]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.frame_index = 0
        self.animation_speed = 0.5  # Adjust this to control the speed of the animation

    def update(self, dt):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(center=self.rect.center)


class PlayerExplosion(AnimatedExplosion):
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        original_frames = png_image_cutter(join('data', 'images', 'explosions', '1.png'), 196, 190)
        self.frames = [image_transformer(frame, 150, 150) for frame in original_frames]


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
