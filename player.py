import pygame
from engine_support import SPACE_SHIP_HEIGHT, SPACE_SHIP_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, laser_sound, join, folder_importer, image_transformer
from laser import Laser
from abc import ABC, abstractmethod


class SpaceEntity(pygame.sprite.Sprite, ABC):
    def __init__(self, sprite_groups, health, energy):
        super().__init__(sprite_groups)
        self.health = health
        self.energy = energy
        self.direction = pygame.Vector2(0, 0)
        self.speed = 500

    @abstractmethod
    def update(self, dt):
        pass

    def reduce_health(self, amount):
        self.health.reduce(amount)

    def increase_health(self, amount):
        self.health.increase(amount)

    def reduce_energy(self, amount):
        self.energy.reduce(amount)

    def increase_energy(self, amount):
        self.energy.increase(amount)


class Movable:
    def update_position(self, rect, direction, speed, dt):
        rect.center += direction * speed * dt
        rect.centerx = max(rect.width / 2, min(WINDOW_WIDTH - rect.width / 2, rect.centerx))
        rect.centery = max(rect.height / 2, min(WINDOW_HEIGHT - rect.height / 2, rect.centery))


class Shooter:
    def __init__(self):
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        #self.laser_sound = pygame.mixer.Sound(laser_sound)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def shoot(self, groups, lasers_group, player):
        if self.can_shoot:
            laser = Laser(groups, player)
            lasers_group.add(laser)
            #self.laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()


class Player(SpaceEntity, Movable, Shooter):
    def __init__(self, sprite_groups, lasers_group, health, energy):
        SpaceEntity.__init__(self, sprite_groups, health, energy)
        Shooter.__init__(self)  
        self.groups = sprite_groups
        self.lasers = lasers_group

        self.center_frame = pygame.image.load(join('assets', 'images', 'space_ship', 'red', 'center.png'))
        self.left_frames = folder_importer('assets', 'images', 'space_ship', 'red', 'Left')
        self.right_frames = folder_importer('assets', 'images', 'space_ship', 'red', 'Right')
        self.image = image_transformer(self.center_frame, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH / 2, 700))
        self.mask = pygame.mask.from_surface(self.image)

        self.frame_index_left = 0
        self.frame_index_right = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        new_direction = pygame.Vector2(int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]),
                                       int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))

        if new_direction != self.direction:
            self.direction = new_direction
            self.frame_index_left = 0
            self.frame_index_right = 0

        self.update_image()
        self.update_position(self.rect, self.direction, self.speed, dt)

        if keys[pygame.K_SPACE] and self.can_shoot:
            if self.energy.width == 0:
                self.can_shoot = False
            else:
                self.shoot(self.groups, self.lasers, self)
                self.special_move()

        self.energy.increase(3.5)
        self.laser_timer()

    def update_image(self):
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

    def special_move(self):
        self.reduce_energy(7)
        self.cooldown_duration = 0 if self.energy.width > 50 else 400
