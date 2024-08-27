"""
Support Functions for Image Handling

This module provides utility functions for loading and transforming images
used in the game. It includes functions to import multiple images from a
directory and to resize images to specified dimensions.

Functions:
- folder_importer(*path):
  Import and return a list of images from a directory specified by *path.

- image_transformer(image, width, height):
  Resize the given image to the specified width and height using
  smooth scaling. Return the transformed image with alpha transparency.

- png_image_cutter(sprite_sheet_path, frame_width, frame_height):
  Cut a sprite sheet into individual frames based on specified frame width
  and height. Return a list of frames.

Classes:
- Scoreboard:
  A class to manage and display the player's current score.

- HighScoresManager:
  A class to manage high scores, including loading, saving, and adding new
  high scores.

Usage Example:
--------------
To import all images from a directory and transform them:
    surfs = folder_importer('data', 'images', 'space_ship', 'red', 'Left')
    transformed_images = [image_transformer(img, 100, 100) for img in surfs]
"""

import pygame
from settings import *
from os.path import join, exists
import json
from os import walk


def folder_importer(*path):
    """
    Import and return a list of images from a directory specified by *path.

    Args:
        *path: Directory path components to load images from.

    Returns:
        List of pygame.Surface objects loaded from the specified directory.
    """
    surfs = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            image = pygame.image.load(full_path)
            surfs.append(image)
    return surfs


def image_transformer(image, width, height):
    """
    Resize the given image to the specified width and height using
    smooth scaling. Ensure the image has alpha transparency.

    Args:
        image: The pygame.Surface object to resize.
        width: The desired width of the transformed image.
        height: The desired height of the transformed image.

    Returns:
        The transformed pygame.Surface object.
    """
    # Scale the image to the desired width and height
    scaled_image = pygame.transform.smoothscale(image, (width, height))

    # Ensure the image has an alpha channel
    if scaled_image.get_alpha() is None:
        scaled_image = scaled_image.convert_alpha()
    else:
        scaled_image = scaled_image.convert_alpha()

    return scaled_image


def png_image_cutter(sprite_sheet_path, frame_width, frame_height):
    """
    Cut a sprite sheet into individual frames based on specified frame width
    and height. Return a list of frames.

    Args:
        sprite_sheet_path: Path to the sprite sheet image.
        frame_width: The width of each frame.
        frame_height: The height of each frame.

    Returns:
        List of pygame.Surface objects representing individual frames.
    """
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


class Scoreboard(pygame.sprite.Sprite):
    """
    A class to manage and display the player's current score.

    Attributes:
        groups: The sprite groups the scoreboard belongs to.
        current_score: The current score of the player.
        image: The image surface representing the score.
        rect: The rectangle defining the position and size of the image.
    """
    def __init__(self, groups):
        """
        Initialize the scoreboard with default settings.

        Args:
            groups: The sprite groups the scoreboard belongs to.
        """
        super().__init__(groups)
        self.groups = groups
        self.current_score = 0
        font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 40)  # Font style and size
        self.image = font.render(str(self.current_score), True, (255, 255, 240))
        self.rect = self.image.get_rect(center=(170, 620))

    def update_image(self):
        """
        Update the scoreboard image with the current score.
        """
        font = pygame.font.Font(join('data', 'images', 'Oxanium-Bold.ttf'), 40)
        self.image = font.render(f'Score: {self.current_score}', True, (255, 255, 240))
        self.rect = self.image.get_rect(center=(170, 620))

    def update(self, *args):
        """
        Update the scoreboard image. Called each frame.
        """
        self.update_image()

    def increase_score(self):
        """
        Increase the current score by 1.
        """
        self.current_score += 1


class HighScoresManager:
    """
    A class to manage high scores, including loading, saving, and adding new high scores.

    Attributes:
        filename: The file where high scores are stored.
        score: The current score.
        high_scores: List of high scores loaded from the file.
    """
    def __init__(self, filename='high_scores.json'):
        """
        Initialize the HighScoresManager with default settings and load high scores.

        Args:
            filename: The file where high scores are stored. Default is 'high_scores.json'.
        """
        self.filename = filename
        self.score = 0
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        """
        Load high scores from the specified file.

        Returns:
            List of high scores loaded from the file.
        """
        if exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_high_scores(self):
        """
        Save high scores to the specified file.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.high_scores, file, indent=4)

    def add_high_score(self, name, score):
        """
        Add a new high score to the list and save it.

        Args:
            name: The name of the player.
            score: The score achieved by the player.
        """
        self.high_scores.append({'name': name, 'score': score})
        self.high_scores = sorted(self.high_scores, key=lambda x: x['score'], reverse=True)[:10]
        self.save_high_scores()

    def get_high_scores(self):
        """
        Get the list of high scores.

        Returns:
            List of high scores.
        """
        return self.high_scores
