import pygame.sprite
from src.settings import SCREEN, S_W, S_H, BLOCK_SIZE, TABLE_SIZE, scale_image

class DotFlashing(pygame.sprite.Sprite):
    SPRITE_ANIMATION_SPEED = 0.3
    # big_dot_cord = [(30, 30), (S_W - 60, 30), (30, S_H - TABLE_SIZE - 50), (S_W - 60, S_H - TABLE_SIZE - 50)]

    def __init__(self, x, y, img='./src/assets/images/dots/red_dot.png'):
        pygame.sprite.Sprite.__init__(self)
        self.sprites_move = [pygame.image.load(f'./src/assets/images/dots/dot_sprite/{x}.png') for x in range(1, 7)]
        self.current_sprite = 0
        self.image = pygame.image.load(img)
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (x + 2, y + 3)

    def sprite_frames(self):
        self.current_sprite += self.SPRITE_ANIMATION_SPEED
        if self.current_sprite >= len(self.sprites_move):
            self.current_sprite = 1
        self.image = self.sprites_move[int(self.current_sprite)]

    def update(self):
        self.sprite_frames()

