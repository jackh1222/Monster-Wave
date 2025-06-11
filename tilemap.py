import csv
import pygame
from config import TILE_SIZE

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w=TILE_SIZE, h=TILE_SIZE):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 200, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

class TileMap:
    def __init__(self, csv_file):
        self.platforms = pygame.sprite.Group()
        with open(csv_file, newline='') as f:
            for row_idx, row in enumerate(csv.reader(f)):
                for col_idx, cell in enumerate(row):
                    if cell == '1':
                        plat = Platform(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                        self.platforms.add(plat)
