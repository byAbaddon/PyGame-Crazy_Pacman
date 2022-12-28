import pygame.sprite

from src.settings import *
from src.classes.background import Background
from src.classes.sound import Sound
from src.classes.table import Table
from src.classes.grid import Grid
from src.classes.field import Field
from src.classes.pacman import Pacman
from src.classes.enemy import Enemy
from src.classes.dot import Dot
from src.classes.dot_flashing import DotFlashing
from src.classes.bonus import Bonus


# ======================================================================== create Sprite groups

pacman_group = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.Group()
field_group = pygame.sprite.GroupSingle()
dot_group = pygame.sprite.Group()
dot_flashing_group = pygame.sprite.Group()
bonus_group = pygame.sprite.GroupSingle()

# # add to all_sprite_groups
all_spite_groups_dict = {'pacman' : pacman_group, 'enemy': enemy_group, 'field' : field_group , 'dot': dot_group,
                         'dot_flashing' : dot_flashing_group, 'bonus': bonus_group,
                         }

# # ======================================================================= initialize  Classes
#
pacman = Pacman(all_spite_groups_dict)

# # add to group

pacman_group.add(pacman)


# create new enemies
def enemy_creator():
    picture_enemy_color_type = f'src/assets/images/enemies/{randint(1, 7)}.png'
    enemy = Enemy(all_spite_groups_dict, pacman, picture_enemy_color_type)
    enemy_group.add(enemy)

# create dots and flashing dots and add to groups
def food_creator():
    for rows, cols  in Dot.food_cells.items():
        for col_index in range(len(cols)):
            if cols[col_index] == '0' or cols[col_index] == '2':
                row = (col_index + 1) * BLOCK_SIZE - 15
                col = rows * BLOCK_SIZE - 15
                if cols[col_index] == '2': # add flashing Dot
                    dot_flash = DotFlashing(row, col)
                    dot_flashing_group.add(dot_flash)
                else:
                    dot = Dot(row, col)
                    dot_group.add(dot)

# ==================================================================
table = Table(all_spite_groups_dict, pacman)

# Game State
class GameState(Sound):
    COOLDOWN = 1000  # milliseconds
    start_timer = pygame.time.get_ticks()

    def __init__(self,):
        self.state = 'intro'
        self.background_picture = None
        self.start_game_counter = 3
        self.is_music_play = False
        self.is_start_game = False
        self.is_created_enemy = False
        self.is_created_bonus = False
        self.is_game_over = False
        self.reset_current_game_data = False
        self.reset_all_data_for_new_game = False

    def game(self):

        # ----------------------------- NEW GAME  reset all data
        if self.reset_all_data_for_new_game:
            self.background_picture = None
            self.is_music_play = False
            self.start_game_counter = 3
            self.is_start_game = False
            self.is_created_enemy = False
            self.is_created_bonus = False
            self.is_game_over = False
            self.reset_current_game_data = False
            [all_spite_groups_dict[group].empty() for group in all_spite_groups_dict]
            pacman_group.add(pacman)
            pacman.reset_all_data()
            self.reset_all_data_for_new_game = False


        # ---------------------------- if level complete
        if pacman.is_level_complete:
            pygame.time.delay(3000)
            self.reset_current_game_data = True
            self.state = 'get_ready'

        # ---------------------------- pacman death replay level
        if pacman.is_level_restart:
            self.reset_current_game_data = True
            self.state = 'get_ready'

        # -----------------------------  Reset current data
        if self.reset_current_game_data:
            self.background_picture = None
            self.is_music_play = False
            self.start_game_counter = 3
            self.is_start_game = False
            self.is_game_over = False
            self.is_created_bonus = False
            enemy_group.empty()
            pacman_group.empty()
            pacman_group.add(pacman)
            pacman.reset_current_data()
            bonus_group.empty()

        # ----------------------------- start game
        if not self.is_start_game:
            Sound.stop_all_sounds()
            Sound.pacman_start(self)
            Sound.game_music(self)
            self.reset_current_game_data = False
            self.is_start_game = True

            # ------- add field
            if pacman.level < 9:
                level = pacman.level
            else:
                level = 9
            field = Field(f'./src/assets/images/game_fields/{level}.png')
            field_group.add(field)

            # ------ add dots
            if not len(dot_group):
                food_creator()  # --- add dots

        # ------------- generate enemies
        if not self.is_created_enemy: # not
            time_now = pygame.time.get_ticks()
            if time_now - self.start_timer > self.COOLDOWN + 1000:
                self.start_timer = time_now
                if len(enemy_group) < 14 + pacman.level:
                    enemy_creator()

        # ------------- generate bonus fruit
        if not self.is_created_bonus:
            if len(dot_group) == 100:
                fruit_num = pacman.level - 1
                if fruit_num > 9:
                    fruit_num = randint(0, 9)
                bonus_group.add(Bonus(fruit_num))
                Sound.add_bonus_fruit(self)
                self.is_created_bonus = True

        if pacman.is_pause:
            pacman.is_pause = False
            self.state = 'pause'

        if pacman.is_game_over:
            Sound.stop_all_sounds()
            Sound.game_over_music(self)
            self.state = 'game_over'
        # # =================================================== UPDATE
        # Grid.draw_grid(self)
        table.update()

        # #  --------------------------- draw sprite group
        field_group.draw(SCREEN)
        dot_group.draw(SCREEN)
        dot_flashing_group.draw(SCREEN)
        pacman_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        bonus_group.draw(SCREEN)

        # # --------------------------- update sprite group
        pacman_group.update()
        enemy_group.update()
        # dot_group.update()
        dot_flashing_group.update()

    def intro(self):
        if not self.is_music_play:
            Sound.intro_music(self)
            self.is_music_play = True
        font = './src/fonts/aAblasco.ttf'
        background_image('./src/assets/images/backgrounds/bg_intro.png')
        text_creator('Crazy PacMan', 'gold2', 60, 100, 70, None, './src/fonts/cute.ttf')
        text_creator('Menu - M', 'red', S_W - 230, S_H - 160, 30, None, font)
        text_creator('Credits - C', 'fuchsia', S_W - 230, S_H - 110, 30, None, font)
        text_creator('Start game - SPACE', 'deepskyblue', S_W // 3 - 6, S_H - 24, 32, None, font)
        text_creator('By Abaddon', 'orange', 10, S_H - 10, 15, None, font)
        text_creator('Copyright 2023', 'white', S_W - 125, S_H - 10, 15, None, font)

        if check_key_pressed(pygame.K_SPACE):
            Sound.btn_click(self)
            self.start_game_counter = 3
            Sound.stop_all_sounds()
            self.state = 'get_ready'
        if check_key_pressed(pygame.K_c):
            Sound.btn_click(self)
            self.state = 'credits'
        if check_key_pressed(pygame.K_m):
            Sound.btn_click(self)
            self.state = 'menu'
        exit_game()

    def menu(self):
        background_image('./src/assets/images/backgrounds/bg_menu.png')
        text_creator('Press RETURN to back...', 'bisque', S_W - 230, S_H - 12, 20, None,'./src/fonts/aAblasco.ttf')
        if check_key_pressed(pygame.K_RETURN):
            self.state = 'intro'
        exit_game()

    def credits(self):
        font = None
        size = 16
        # background_image('./src/assets/images/backgrounds/bg_EMPTY.png')
        text_creator('CREDITS', 'slateblue3', S_W // 2 - 100, 40, 50, None, './src/fonts/aAblasco.ttf', True)
        text_creator('version: 1.0.0-beta', 'cornsilk', S_W - 160, 20, 16, None, './src/fonts/aAblasco.ttf')

        text_creator('Free images:', 'brown', 110, 100, 35, None, font)
        text_creator('https://www.pngwing.com', 'cadetblue4', 130, 125, 30, None, font)

        text_creator('Free sounds:', 'brown', 110, 200, 35, None, font)
        text_creator('https://freesound.org/', 'cadetblue4', 130, 225, 30, None, font)

        text_creator('Platform 2D game:', 'brown', 110, S_H // 2, 34, None, font)
        text_creator('https://www.pygame.org', 'cadetblue4', 130, S_H // 2 + 24, 30, None, font)

        SCREEN.blit(pygame.image.load('./src/assets/images/title/pygame_logo.png'), (S_W // 4 - 50, S_H - 266))

        text_creator('Developer:', 'brown', 30, S_H - 60, 30, None, font)
        text_creator('by Abaddon', 'cadetblue4', 50, S_H - 40, 30, None, font)

        text_creator('Bug rapports:', 'brown', S_W // 2 - 90, S_H - 60, 30, None, font)
        text_creator('subtotal@abv.bg', 'cadetblue4', S_W // 2 - 70, S_H - 40, 30, None, font)

        text_creator('Copyright:', 'brown', S_W - 140, S_H - 60, 30, None, font)
        text_creator('© 2023', 'cadetblue4', S_W - 120, S_H - 40, 30, None, font)

        text_creator('Press RETURN to back...', 'bisque', S_W - 230, S_H - 12, 20, None,'./src/fonts/aAblasco.ttf')

        if check_key_pressed(pygame.K_RETURN):
            Sound.btn_click(self)
            self.state = 'intro'
        exit_game()

    def get_ready(self):
        Sound.stop_all_sounds()
        time_now = pygame.time.get_ticks()
        if time_now - self.start_timer > self.COOLDOWN:
            self.start_game_counter -= 1
            self.start_timer = time_now
        font = './src/fonts/aAblasco.ttf'
        background_image('./src/assets/images/backgrounds/bg_poster.png')
        text_creator('By Abaddon', 'orange', 10, S_H - 10, 15, None, font)
        text_creator('Copyright 2023', 'white', S_W - 125, S_H - 10, 15, None, font)
        text_creator(f'START AFTER: {self.start_game_counter}', 'purple', 215, S_H - 40, 40, None, './src/fonts/cute.ttf')

        if self.start_game_counter == 0:
            Sound.pacman_start(self)
            Sound.game_music(self)
            self.state = 'game'

    def start_pause(self):
        background_image('./src/assets/images/backgrounds/bg_pause.png')
        text_creator('PAUSE', 'red3', S_W // 2 + 60, S_H  // 2 - 30, 80, None, './src/fonts/cute.ttf')
        text_creator('Press RETURN to continue...', 'bisque', S_W - 255, S_H - 12, 20, None,'./src/fonts/aAblasco.ttf')

        if key_pressed(pygame.K_RETURN):
            self.state = 'game'

    def game_over(self):
        background_image('./src/assets/images/backgrounds/bg_game_over2.png', 4)
        text_creator('GAME OVER', 'red', S_W // 2 - 25, S_H // 2 - 150, 54, None, './src/fonts/cute.ttf')
        text_creator('Press RETURN to back...', 'bisque', S_W - 240, S_H - 12, 20, None,'./src/fonts/aAblasco.ttf')

        if key_pressed(pygame.K_RETURN):
            Sound.stop_all_sounds()
            Sound.intro_music(self)
            self.reset_all_data_for_new_game = True
            self.state = 'intro'
        exit_game()

    # ========================================= state manager ...
    def state_manager(self):
        # print(self.state)
        if self.state == 'intro':
            self.intro()
        if self.state == 'game':
            self.game()
        if self.state == 'get_ready':
            self.get_ready()
        if self.state == 'menu':
            self.menu()
        if self.state == 'credits':
            self.credits()
        if self.state == 'pause':
            self.start_pause()
        if self.state == 'game_over':
            self.game_over()



#  ================================ create new GameState
game_state = GameState()


# ============= Starting Game loop
while True:
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(FPS)
    exit_game()
