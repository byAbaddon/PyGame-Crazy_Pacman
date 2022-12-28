import pygame
from src.settings import S_W, S_H, SCREEN, BLOCK_SIZE


class Grid:
    def __init__(self):
        self.rect = ''

    def draw_grid(self):
        for x in range(0, S_W, BLOCK_SIZE):
            for y in range(0, S_H - 100, BLOCK_SIZE):
                self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, 'teal', self.rect, 1)
