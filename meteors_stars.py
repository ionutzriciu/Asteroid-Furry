import pygame
from support import *
from settings import *

class Meteor(pygame.sprite.Sprite):
    def __init__(self, sprite_group, meteors):
        super().__init__(sprite_group)
        self.meteors = meteors
        self.groups = sprite_group

        self.meteor_frames = [image_transformer(image, METEOR_HEIGHT, METEOR_WIDTH) for image in folder_importer('assets', 'images', 'meteor')]

        self.image = self.meteor_frames[0]
        self.rect = self.image.get_rect(midbottom=(randint(50, WINDOW_WIDTH - 50), 0))
        self.mask = pygame.mask.from_surface(self.image)

        self.frame_index = 0
        self.animation_speed = 0.27

        self.direction = pygame.Vector2(random.uniform(-1, 1), 1)
        self.direction.x *= random.uniform(0.5, 1.0)
        self.speed = random.uniform(150, 300)
        self.velocity = self.direction * self.speed

    def update(self, dt):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.meteor_frames):
            self.frame_index = 0

        self.image = self.meteor_frames[int(self.frame_index)]

        self.rect.center += self.velocity * dt

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

class Stars(pygame.sprite.Sprite):
    star_image = None

    def __init__(self, groups):
        super().__init__(groups)
        
        if Stars.star_image is None:
            initial_image = pygame.image.load(join('assets', 'images', 'star.png')).convert_alpha()
            rotated_image = pygame.transform.rotate(initial_image, 303)
            Stars.star_image = pygame.transform.scale(rotated_image, (100, 100))

        self.image = Stars.star_image
        self.rect = self.image.get_rect(center=(randint(0, 1280), -10))
        self.speed = 1

    def update(self, dt):
        self.rect.centery += 400 * self.speed * dt
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

