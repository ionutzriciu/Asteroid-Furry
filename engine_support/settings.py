import pygame
import sys
#from random import randint
import pygame.mask
import random
from os.path import join, dirname, abspath, join
import os

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS  
else:
    BASE_PATH = dirname(abspath(__file__))

# Define relative paths to the audio files using os.path.join
sound_main_music = join(BASE_PATH, 'assets', 'audio', 'game_music', 'looping_music.ogg')
laser_sound = join(BASE_PATH, 'assets', 'audio', 'laser', 'laserfire02.ogg')
sound_explosion = join(BASE_PATH, 'assets', 'audio', 'explosions.flac')



sound_main_music = r"C:\Users\riciionu\Desktop\Python related\Portofolio\GitHub Uploads\Asteroid_Furry\assets\audio\game_music\looping_music.ogg"
laser_sound = r"C:\Users\riciionu\Desktop\Python related\Portofolio\GitHub Uploads\Asteroid_Furry\assets\audio\laser\laserfire02.ogg"
sound_explosion = r"C:\Users\riciionu\Desktop\Python related\Portofolio\GitHub Uploads\Asteroid_Furry\assets\audio\explosions.flac"




WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

SPACE_SHIP_HEIGHT, SPACE_SHIP_WIDTH = 135, 135
LASER_HEIGHT, LASER_WIDTH = 200, 200
METEOR_HEIGHT, METEOR_WIDTH = 100, 100


#Game loop constants 

SPAWN_INTERVAL_STARS = 500
MIN_SPAWN_INTERVAL = 150
SPAWN_DECREASE_RATE = 5
MAX_METEORS = 30
MAX_STARS = 20
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 50
DEFAULT_BOX_COLOR = '#8e7cc3'
BUTTON_TEXT_COLOR = (255, 255, 255)
FONT_PATH = join('assets', 'images', 'Oxanium-Bold.ttf')
BG_COLOR = (0, 0, 0)
FAQ_BG_COLOR = '#adadff'
FONT_SIZE = 40