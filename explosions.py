import pygame
from settings import *
from support import *



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

