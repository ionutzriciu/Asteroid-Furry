from cx_Freeze import setup, Executable
import os

base = None

# Ensure the assets are included
data_files = [
    ('data/audio/game_music', 'data/audio/game_music/boss.ogg'),
    ('data/audio/laser', 'data/audio/laser/laserfire02.ogg'),
    ('data/audio/explosion', 'data/audio/explosion/explosion.wav'),
    ('data/images/bg', 'data/images/bg/1349322.png'),
    ('data/images', 'data/images/Oxanium-Bold.ttf')
]

executables = [Executable("main.py", base=base)]

setup(
    name="Asteroid Fury",
    options={
        'build_exe': {
            'packages': ["pygame", "os", "random", "json", "time"],
            'include_files': data_files
        }
    },
    executables=executables
)
