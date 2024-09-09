import pygame 
from support import image_transformer
from os.path import join
from settings import LASER_HEIGHT, LASER_WIDTH

class Laser(pygame.sprite.Sprite):
    def __init__(self, sprite_groups, player):
        super().__init__(sprite_groups)
        self.groups = sprite_groups
        self.player = player
        self.initial_image = pygame.image.load(join('assets', 'images', 'laser', 'Laser.png')).convert_alpha()
        self.angle = 121
        self.rotated_image = pygame.transform.rotate(self.initial_image, self.angle)
        self.image = image_transformer(self.rotated_image, LASER_WIDTH, LASER_HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)

        self.offset_x = -6  
        self.offset_y = -30  

        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.player.rect.centerx + self.offset_x, self.player.rect.centery + self.offset_y)

    def update(self, dt):
        """
         Updates the position of the laser and destroys it if it moves off-screen.
        """
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
