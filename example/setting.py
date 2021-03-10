from os import path

# Pygame and Box2D
PPM = 20
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 480

# Color
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,0,255)
LIGHTGREY = (120,120,120)

# data path
IMAGE_DIR = path.join(path.dirname(__file__), "image")