import pygame
from settings import *
from support import *
from bar_health_energy import Health, Energy
from explosions import *
#from meteors_stars import Meteor, Stars
from laser import Laser

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


