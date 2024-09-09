from os.path import join, exists
import json
from os import walk
import pygame

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.groups = groups
        self.current_score = 0
        font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 40)  # Font style and size
        self.image = font.render(str(self.current_score), True, (255, 255, 240))
        self.rect = self.image.get_rect(center=(170, 620))

    def update_image(self):
        font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 40)
        self.image = font.render(f'Score: {self.current_score}', True, (255, 255, 240))
        self.rect = self.image.get_rect(center=(170, 620))

    def update(self, *args):
        self.update_image()

    def increase_score(self):
        self.current_score += 1