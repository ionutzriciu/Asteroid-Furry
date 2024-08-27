
"""
This module contains the configuration settings for the game.
All setup-related parameters and constants are defined and stored here.
"""
import pygame
from os.path import join
from os import walk
import sys
from random import randint
import pygame.mask
import time
import random
import json
from os.path import join, exists
from os.path import join, dirname, abspath
import sys


# Determine the base path for the application
if getattr(sys, 'frozen', False):
    # If the application is frozen (i.e., packaged), use the path of the executable
    BASE_PATH = sys._MEIPASS  # PyInstaller creates a temporary folder for the executable
else:
    # If not frozen, use the current directory
    BASE_PATH = dirname(abspath(__file__))

# Define window dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Define spaceship and laser dimensions
SPACE_SHIP_HEIGHT, SPACE_SHIP_WIDTH = 135, 135
LASER_HEIGHT, LASER_WIDTH = 200, 200
METEOR_HEIGHT, METEOR_WIDTH = 100, 100

# Music Files
main_menu_music = join(BASE_PATH, 'data', 'audio', 'game_music', 'boss.ogg')
laser_sound = join(BASE_PATH, 'data', 'audio', 'laser', 'laserfire02.ogg')
explosion_sound = join(BASE_PATH, 'data', 'audio', 'explosion', 'explosion.wav')

