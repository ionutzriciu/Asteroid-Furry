import pygame
from settings import *
from os.path import join, exists
import json
from os import walk


def folder_importer(*path):
    surfs = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            image = pygame.image.load(full_path)
            surfs.append(image)
    return surfs


def image_transformer(image, width, height):
    scaled_image = pygame.transform.smoothscale(image, (width, height))
    if scaled_image.get_alpha() is None:
        scaled_image = scaled_image.convert_alpha()
    else:
        scaled_image = scaled_image.convert_alpha()

    return scaled_image


def png_image_cutter(sprite_sheet_path, frame_width, frame_height):
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()
    columns = sheet_width // frame_width
    rows = sheet_height // frame_height

    frames = []
    for row in range(rows):
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height)).copy()
            frames.append(frame)

    return frames


# class Scoreboard(pygame.sprite.Sprite):
#     def __init__(self, groups):
#         super().__init__(groups)
#         self.groups = groups
#         self.current_score = 0
#         font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 40)  # Font style and size
#         self.image = font.render(str(self.current_score), True, (255, 255, 240))
#         self.rect = self.image.get_rect(center=(170, 620))

#     def update_image(self):
#         font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 40)
#         self.image = font.render(f'Score: {self.current_score}', True, (255, 255, 240))
#         self.rect = self.image.get_rect(center=(170, 620))

#     def update(self, *args):
#         self.update_image()

#     def increase_score(self):
#         self.current_score += 1



