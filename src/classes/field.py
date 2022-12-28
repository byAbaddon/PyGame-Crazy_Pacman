from src.settings import *


class Field(pygame.sprite.Sprite):
    def __init__(self, image='./src/assets/images/game_fields/gr.png'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center =(S_W // 2 + 1, S_H // 2 - 44)
