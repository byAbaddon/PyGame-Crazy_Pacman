import pygame.sprite
from src.settings import  Path, choice

class Bonus(pygame.sprite.Sprite):
    fruits_list = list(sorted(Path('./src/assets/images/fruits/').glob('*.png')))
    bonus_position_cord = [(345,255), (345,315), (465, 255), (465,315)]

    def __init__(self, num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.fruits_list[num])
        self.item_name = str(self.fruits_list[num]).split('/')[-1][:-4]
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (choice(self.bonus_position_cord))

