import pygame
import sys
from os.path import join, dirname, abspath, join, exists
import os

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS  
else:
    BASE_PATH = dirname(abspath(__file__))

sound_main_music_base = join(BASE_PATH, 'assets', 'audio', 'game_music', 'looping_music.ogg')
laser_sound_base = join(BASE_PATH, 'assets', 'audio', 'laser', 'laserfire02.ogg')
sound_explosion_base = join(BASE_PATH, 'assets', 'audio', 'explosions.flac')

# Absolute paths (for fallback)
sound_main_music_abs = r"C:\Users\riciionu\Desktop\Python related\Portofolio\GitHub Uploads\Asteroid_Furry\assets\audio\game_music\looping_music.ogg"
laser_sound_abs = r"C:\Users\riciionu\Desktop\Python related\Portofolio\GitHub Uploads\Asteroid_Furry\assets\audio\laser\laserfire02.ogg"
sound_explosion_abs = r"C:\Users\riciionu\Desktop\Python related\Portofolio\GitHub Uploads\Asteroid_Furry\assets\audio\explosions.flac"

# Function to get a valid path
def get_valid_path(base_path, abs_path):
    if exists(base_path):
        return base_path
    elif exists(abs_path):
        return abs_path
    else:
        raise FileNotFoundError("Neither base path nor absolute path exists.")

# Get valid paths for assets
sound_main_music = get_valid_path(sound_main_music_base, sound_main_music_abs)
laser_sound = get_valid_path(laser_sound_base, laser_sound_abs)
sound_explosion = get_valid_path(sound_explosion_base, sound_explosion_abs)

