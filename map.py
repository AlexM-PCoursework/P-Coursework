import pygame as py

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

class Map:
    def__init__(self, filename):
        self.data[]
        with open(filename,'rt') as f:
            for line in f:
                self.data.append(line)

    self.tilewidth = len(self.data[0])
    self.tileheight = len(self.data)
    self.width = self.tilewidth * TILESIZE
    self.height = self.tileheight * TILESIZE
