import pygame
from src.settings import text_creator, SCREEN,  S_W, S_H, TABLE_SIZE, CLOCK, scale_image


class Table:
    def __init__(self,all_spite_groups_dict, pacman):
        self.asg = all_spite_groups_dict
        self.pacman_data = pacman
        self.height_score = 1500

    def draw_labels_and_table_data(self):
        font_size = 22
        font = './src/fonts/aAblasco.ttf'

        # label height_score
        text_creator('Top Score', 'crimson', 40, S_H - 60, font_size, None, font)
        if self.pacman_data.points >= self.height_score:
            self.height_score = self.pacman_data.points
        text_creator(f': {self.height_score}', 'crimson', 140, S_H - 60, font_size, None, font)

        # label_score
        text_creator('You Score:', 'cornflowerblue', 40, S_H - 30, 20, None, font)
        text_creator(f' {self.pacman_data.points}', 'cornflowerblue', 138, S_H - 30, font_size, None, font)


        # label lives left
        text_creator('Lives:', 'springgreen4', 280, S_H - 60, 20, None, font)
        text_creator(f'{self.pacman_data.lives}', 'springgreen4', 340, S_H - 60, font_size, None, font)

        # # label enemies current numbers
        text_creator('Enemies:', 'orange', 280, S_H - 30, 20, None, font)
        text_creator(f'{len(self.asg["enemy"])}', 'orange', 368, S_H - 30, font_size, None, font)

        # label time
        text_creator('Attack Time:', 'coral3', 440, S_H - 60, font_size, None, font)
        if self.pacman_data.attack_counter > 3:
            text_creator(f'{self.pacman_data.attack_counter}', 'white', 570, S_H - 60, font_size, None, font)
        else:
            text_creator(f'{self.pacman_data.attack_counter}', 'red', 570, S_H - 60, font_size, None, font)

        # label fruits left
        text_creator('Fruits:', 'deepskyblue4', 440, S_H - 30, font_size, None, font)
        # text_creator(f'{self.pacman_data.fruits_counter}', 'deepskyblue4', 510, S_H - 30, font_size, None, font)
        for index in range(0, len(self.pacman_data.fruits_collection)):
            fruit = f'src/assets/images/fruits/{self.pacman_data.fruits_collection[index]}.png'
            SCREEN.blit(scale_image(fruit, 15, 15),(504 + index * 18, S_H - 35))


        # label FPS
        text_creator('FPS:', 'lightskyblue4', 700, S_H - 60, font_size, None, font)
        text_creator(f'{int(CLOCK.get_fps())}', 'lightskyblue4', 745, S_H - 60, font_size, None, font)

        # label level
        text_creator('Level:', 'goldenrod4', 700, S_H - 30, font_size, None, font)
        text_creator(f'{self.pacman_data.level}', 'goldenrod4', 765, S_H - 30, font_size, None, font)

    @staticmethod
    def draw_frame():
        frame = pygame.Rect( 10 , S_H - 80, S_W - 20, 70)
        pygame.draw.rect(SCREEN, 'grey', frame, 2, -2)

    def update(self):
        self.draw_labels_and_table_data()
        self.draw_frame()




