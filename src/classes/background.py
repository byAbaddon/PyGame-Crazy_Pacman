import pygame
from src.settings import SCREEN

class Background:
    def __init__(self, image=None, x=0, y=0, is_image_scaled=False):
        self.image = image
        self.x = x
        self.y = y
        self.is_image_scaled = is_image_scaled

    def create_bg(self):
        if not self.is_image_scaled:
            bg_image = pygame.image.load(self.image).convert() # convert make image fast
        else:
            bg_image = self.image.convert()
        return SCREEN.blit(bg_image, [self.x, self.y])

    def update(self):
        self.create_bg()