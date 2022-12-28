import pygame

from src.settings import *
from src.classes.sound import Sound
from src.classes.dot import Dot


class Pacman(pygame.sprite.Sprite, Sound):
    SPRITE_ANIMATION_SPEED = 0.3
    COOLDOWN = 1000
    start_timer = pygame.time.get_ticks()
    fruits_collection = []
    level = 1
    points = 0
    lives = 3
    speed = 2
    attack_counter = 10
    # reset current data
    current_speed = speed
    is_level_restart = False
    is_level_complete = False
    is_game_over = False
    is_pause = False
    is_dead = False
    dead_animation_counter = 0
    is_attack = False

    def __init__(self, all_spite_groups_dict):
        pygame.sprite.Sprite.__init__(self)
        self.asg = all_spite_groups_dict
        self.image = scale_image('./src/assets/images/pacman/white/5.png', 26, 26).convert()
        self.sprites_move = [pygame.image.load(f'./src/assets/images/pacman/white/{x}.png') for x in range(1, 6)]
        self.current_sprite = 0
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (BLOCK_SIZE * 14 - 14 ,BLOCK_SIZE * 16 - 14 )
        self.direction = vec(0, 0)
        self.pos = vec(self.rect.x, self.rect.y)

    def move(self):
        try:
            # ---------------------------------------------- PAUSE
            if key_pressed(pygame.K_p):
                self.is_pause = True
            # move and prevent - only if cell is empty
            if not self.is_dead :
                # ---------------------------------------------- go up
                if check_key_pressed(pygame.K_UP):
                    row = self.rect.y // BLOCK_SIZE
                    if self.direction.x == -1:
                        col = (self.rect.x + 20) // BLOCK_SIZE
                    else:
                        col = self.rect.x // BLOCK_SIZE
                    if row > 0 and Dot.food_cells[row][col] != '1':
                        self.direction.y = -1
                # ---------------------------------------------- go down
                if check_key_pressed(pygame.K_DOWN):
                    row = (self.rect.y + BLOCK_SIZE * 2) // BLOCK_SIZE
                    if self.direction.x == -1:
                        col = (self.rect.x + 20) // BLOCK_SIZE
                    else:
                        col = self.rect.x  // BLOCK_SIZE

                    if Dot.food_cells[row][col] != '1':
                        self.direction.y = 1
                # ---------------------------------------------- go left
                if check_key_pressed(pygame.K_LEFT):
                    col = (self.rect.x - BLOCK_SIZE) // BLOCK_SIZE
                    if self.direction.y == -1:
                        row = (self.rect.y + BLOCK_SIZE + 20) // BLOCK_SIZE
                    else:
                        row = (self.rect.y + BLOCK_SIZE) // BLOCK_SIZE
                    if Dot.food_cells[row][col] != '1':
                        self.direction.x = -1
                # ---------------------------------------------- go right
                if check_key_pressed(pygame.K_RIGHT):
                    col = (self.rect.x + BLOCK_SIZE) // BLOCK_SIZE
                    if self.direction.y == -1:
                        row = (self.rect.y + BLOCK_SIZE + 20) // BLOCK_SIZE
                    else:
                        row = (self.rect.y + BLOCK_SIZE) // BLOCK_SIZE
                    if Dot.food_cells[row][col] != '1':
                        self.direction.x = 1

                self.current_speed = self.speed
                self.rect.x += self.current_speed * self.direction.x
                self.rect.y += self.current_speed * self.direction.y
        except:
            pass

    def sprite_frames(self):
        # left and right animation
        if self.direction:
            self.current_sprite += self.SPRITE_ANIMATION_SPEED
            if self.current_sprite >= len(self.sprites_move):
                self.current_sprite = 1

            x_size = y_size = BLOCK_SIZE - 8  # 6
            self.image = pygame.transform.scale(self.sprites_move[int(self.current_sprite)], (x_size, y_size)).convert()

            if self.direction.y == -1:
                self.image = pygame.transform.rotate(self.image, 90)
            if self.direction.y == 1:
                self.image = pygame.transform.flip(self.image, True, False)
                self.image = pygame.transform.rotate(self.image, 90).convert()
            if self.direction.x == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            if self.direction.x == 1:
                self.image = self.image.convert()

    def check_enter_tunel(self):
        if self.direction.x == 1 and self.rect.x > S_W:
            self.rect.x = 10
        if self.direction.x == -1 and self.rect.x < 0:
            self.rect.x = S_W - 10

    def check_wall_collide(self):
        buffer = 7 # 5
        if pygame.sprite.spritecollide(self, self.asg['field'] , False, pygame.sprite.collide_mask):
            if self.direction.y == -1:
                self.rect.y += buffer
            if self.direction.y == 1:
                self.rect.y -= buffer
            if self.direction.x == -1:
                self.rect.x += buffer
            if self.direction.x == 1:
                self.rect.x -= buffer
            self.direction = vec(0, 0)
            self.current_speed = 0

    def check_dot_collide(self):
        for sprite in pygame.sprite.spritecollide(self, self.asg['dot'], True, pygame.sprite.collide_mask):
            if sprite:
                Sound.pacman_eat(self)
                self.points += 10
                if len(self.asg['dot']) == 0:
                    self.level += 1
                    self.points += 1000 * self.level
                    self.is_level_complete = True
                    self.draw_bonus_label()

    def check_dot_flash_collide(self):
        if pygame.sprite.spritecollide(self, self.asg['dot_flashing'], True, pygame.sprite.collide_mask):
            self.points += 100
            self.current_sprite = 1
            self.attack_counter = 10
            self.is_attack = True
            Sound.pacman_eat_red_dot(self)
            self.sprites_move = [pygame.image.load(f'./src/assets/images/pacman/red/{x}.png') for x in range(1, 6)]

    def check_enemy_collide(self):
        for sprite in pygame.sprite.spritecollide(self, self.asg['enemy'], False, pygame.sprite.collide_mask):
            if sprite:
                if self.is_attack: # ------------------- kill enemy
                    self.points += 150
                    sprite.kill()
                    Sound.pacman_eat_enemy(self)
                    Sound.pacman_eat_enemy_after(self)
                else: # -------------------------------- pacman dead
                    Sound.pacman_death(self)
                    for enemy in self.asg['enemy']:  # stop moving enemies
                        enemy.speed = 0
                    self.direction = vec(0, 0)
                    self.speed = 0
                    self.animation_death()
                    self.is_dead = True

    def check_bonus_collide(self):
        for sprite in pygame.sprite.spritecollide(self, self.asg['bonus'], True, pygame.sprite.collide_mask):
            if sprite:
                Sound.add_bonus_points(self)
                fruit_points = int(sprite.item_name.split('_')[2])
                self.points += fruit_points
                if sprite.item_name not in self.fruits_collection:
                    self.fruits_collection.append(sprite.item_name)

    def animation_death(self):
        if self.is_dead:
            time_now = pygame.time.get_ticks()
            if time_now - self.start_timer > 400:
                self.start_timer = time_now
                self.dead_animation_counter += 1
                if self.dead_animation_counter < 6:
                    self.image = pygame.image.load(f'./src/assets/images/pacman/death/{self.dead_animation_counter}.png')
                if self.dead_animation_counter == 6:
                    self.kill()
                    self.lives -= 1
                    if self.lives == 0: # --------------- game over
                        self.is_game_over = True
                    else:
                        self.is_level_restart = True  # call game state

    def start_attack_timer(self):
        if self.is_attack:
            time_now = pygame.time.get_ticks()
            if time_now - self.start_timer > self.COOLDOWN:
                self.start_timer = time_now
                self.attack_counter -= 1
            if self.attack_counter == 1: # alarm before stop attack
                Sound.pacman_alarm(self)
            if self.attack_counter <= 0:
                self.sprites_move = [pygame.image.load(f'./src/assets/images/pacman/white/{x}.png') for x in range(1, 6)]
                self.attack_counter = 10
                self.is_attack = False

    def draw_bonus_label(self):
        Sound.stop_all_sounds()
        Sound.bonus_music(self)
        bonus_img = pygame.image.load('./src/assets/images/backgrounds/frame.png')
        SCREEN.blit(bonus_img, [S_W // 3, S_H // 3 - 20])
        text_creator('CONGRATULATIONS', 'red', S_W // 3 + 32, S_H // 3 + 26, 26, None, './src/fonts/aAblasco.ttf')
        text_creator(f'Level {self.level - 1} - complete', 'yellow', S_W // 3 + 44, S_H // 3 + 55, 22, None,
                     './src/fonts/aAblasco.ttf')
        text_creator(f'BONUS - {(self.level - 1)  * 1000}', 'green', S_W // 3 + 80, S_H // 3 + 85, 20, None,
                     './src/fonts/aAblasco.ttf')

    def reset_current_data(self):
        self.is_level_complete = False
        self.is_game_over = False
        self.is_pause = False
        self.is_dead = False
        self.dead_animation_counter = 0
        self.attack_counter = 10
        self.is_attack = False
        self.is_level_restart = False
        self.image = scale_image('./src/assets/images/pacman/white/5.png', 26, 26)
        self.sprites_move = [pygame.image.load(f'./src/assets/images/pacman/white/{x}.png') for x in range(1, 6)]
        self.current_sprite = 0
        self.rect.center = (BLOCK_SIZE * 14 - 14, BLOCK_SIZE * 16 - 14)
        self.direction = vec(0, 0)
        self.pos = vec(self.rect.x, self.rect.y)
        self.speed = 2
        self.current_speed = self.speed

    def reset_all_data(self):
        self.fruits_collection = []
        self.level = 1
        self.points = 0
        self.lives = 3
        self.speed = 2
        self.current_speed = self.speed
        self.is_level_restart = False
        self.is_level_complete = False
        self.is_game_over = False
        self.is_pause = False
        self.is_dead = False
        self.dead_animation_counter = 0
        self.attack_counter = 10
        self.is_attack = False
        self.image = scale_image('./src/assets/images/pacman/white/5.png', 26, 26)
        self.sprites_move = [pygame.image.load(f'./src/assets/images/pacman/white/{x}.png') for x in range(1, 6)]
        self.current_sprite = 0
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (BLOCK_SIZE * 14 - 14 ,BLOCK_SIZE * 16 - 14 )
        self.direction = vec(0, 0)
        self.pos = vec(self.rect.x, self.rect.y)

    def update(self):
        self.move()
        self.sprite_frames()
        self.check_enter_tunel()
        self.check_wall_collide()
        self.check_dot_collide()
        self.check_dot_flash_collide()
        self.check_enemy_collide()
        self.check_bonus_collide()
        self.start_attack_timer()
        self.animation_death()