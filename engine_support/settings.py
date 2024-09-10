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


if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS  
else:
    BASE_PATH = dirname(abspath(__file__))

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

SPACE_SHIP_HEIGHT, SPACE_SHIP_WIDTH = 135, 135
LASER_HEIGHT, LASER_WIDTH = 200, 200
METEOR_HEIGHT, METEOR_WIDTH = 100, 100

sound_main_music = r"C:\Users\riciionu\Desktop\Python related\Portofolio\GitHub Uploads\Asteroid_Furry\assets\audio\game_music\looping_music.ogg"
laser_sound = r"C:\Users\riciionu\Desktop\Python related\Portofolio\GitHub Uploads\Asteroid_Furry\assets\audio\laser\laserfire02.ogg"
sound_explosion = r"C:\Users\riciionu\Desktop\Python related\Portofolio\GitHub Uploads\Asteroid_Furry\assets\audio\explosions.flac"

