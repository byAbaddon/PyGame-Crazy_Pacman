import pygame
from src.settings import S_W, BLOCK_SIZE, vec, choice , map_cells

class Enemy(pygame.sprite.Sprite):
    speed = 1
    is_reversed_pic = False

    def __init__(self, all_spite_groups_dict, pacman, img='./src/assets/images/enemies/5.png'):
        pygame.sprite.Sprite.__init__(self)
        self.asg = all_spite_groups_dict
        self.pacman_data = pacman
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (BLOCK_SIZE * 14 - 14 , BLOCK_SIZE * 10 - 15)
        self.direction = vec(0, -1)
        self.pos = vec(self.rect.x, self.rect.y)

    def move(self):
        self.rect.y += self.speed * self.direction.y
        self.rect.x += self.speed * self.direction.x

    def sprite_frames(self):
        # x_size = y_size = BLOCK_SIZE - 2
        # self.image  = pygame.transform.scale(self.image, (x_size, y_size))

        # left and right animation
        if self.direction.x == -1 and not self.is_reversed_pic:
            self.image = pygame.transform.flip(self.image, True, False).convert_alpha()
            self.is_reversed_pic = True
        if self.direction.x == 1 and self.is_reversed_pic:
            self.image = pygame.transform.flip(self.image, True, False).convert_alpha()
            self.is_reversed_pic = False

        # -----------------------------------player management moving
        # if check_key_pressed(pygame.K_RIGHT) and self.is_reversed_pic and self.pacman_data.rect.x > S_W // 2 :
        #     self.image = pygame.transform.flip(self.image, True, False)
        #     self.is_reversed_pic = False
        # elif check_key_pressed(pygame.K_LEFT) and not self.is_reversed_pic and self.pacman_data.rect.x <  S_W // 2 :
        #     self.image = pygame.transform.flip(self.image, True, False)
        #     self.is_reversed_pic = True

    def check_wall_collide(self):
        buffer = 1
        x = self.rect.y // BLOCK_SIZE
        y = self.rect.x // BLOCK_SIZE
        last_cell = (0,0)

        if len(self.asg['enemy']) < 6:
            random_x = -1 if self.pacman_data.rect.x < S_W // 2 else 1
        else:
            random_x = choice([-1, 1])

        if self.direction.y == -1 and map_cells[x][y] == '1' and self.direction.x == 0 and (x, y) != last_cell:
            last_cell = (x, y)
            self.rect.y += buffer
            self.direction.y = 0
            self.direction.x  =  random_x # choice([-1, 1])

        if self.direction.y == 1 and map_cells[x + 1][y] == '1' and self.direction.x == 0 and (x, y) != last_cell:
            last_cell = (x, y)
            # self.rect.y -= buffer
            self.direction.y = 0
            self.direction.x  = random_x  # choice([-1, 1])


        if self.direction.x == -1 and map_cells[x][y] == '1'and self.direction.y == 0 and (x, y) != last_cell:
            last_cell = (x, y)
            self.rect.x += buffer
            self.direction.x = 0
            self.direction.y = choice([-1, 1])

        if self.direction.x == 1 and map_cells[x][y + 1] == '1' and self.direction.y == 0 and (x, y) != last_cell:
            last_cell = (x, y)
            self.rect.x += buffer
            self.direction.x = 0
            self.direction.y =  choice([-1, 1])

        # ========================================= low FPS problem ==============================================
        # buffer = 5
        # for sprite in  pygame.sprite.spritecollide(self , self.asg['field'] ,False, pygame.sprite.collide_mask):
        #     if sprite :
        #         # - vertical
        #         if self.direction.y: # up or down sprite
        #             if self.direction.y == -1:
        #                 self.rect.y += buffer  # restore center position
        #             else:
        #                 self.rect.y -= buffer  # restore center position
        #             self.direction.y = 0 # reset y pos
        #             # - vertical random direction
        #             self.direction.x = choice([-1, 1])
        #
        #         # # - horizontal sprite
        #         elif self.direction.x:  # left or right sprite
        #             if self.direction.x == -1:
        #                 self.rect.x += buffer  # restore center position
        #             else:
        #                 self.rect.x -= buffer  # restore center position
        #             self.direction.x = 0  # reset y pos
        #             # - horizontal random direction
        #             self.direction.y = choice([-1, 1])
        # =====================================================================================

    def check_enter_tunel(self):
        if self.direction.x == 1 and  self.rect.x > S_W:
            self.rect.x = 10
        if self.direction.x == -1 and  self.rect.x < 0:
            self.rect.x = S_W - 10

    def update(self):
        self.check_wall_collide()
        self.sprite_frames()
        self.move()
        # self.check_enter_tunel()


