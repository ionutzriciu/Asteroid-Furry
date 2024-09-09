# test_imports.py
import sys
import os

# Print the sys.path to ensure it includes the correct paths
print("Current Python Path:")
for path in sys.path:
    print(path)

from config.settings import *
from config.support import Scoreboard

def test_import():
    try:
        print("Settings imported successfully")
        print("Scoreboard imported successfully")
    except ImportError as e:
        print(f"Import error: {e}")

test_import()
