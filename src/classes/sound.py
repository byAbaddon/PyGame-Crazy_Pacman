import pygame
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)


class Sound:
    @staticmethod
    def play_sound(sound_file, volume=0.5, loops=0):
        play = pygame.mixer.Sound(sound_file)
        play.set_volume(volume)
        play.play(loops)

    @staticmethod
    def stop_all_sounds():
        pygame.mixer.stop()

    def btn_click(self):
        self.play_sound('./src/assets/sounds/btn_one.wav')

    # Background
    def intro_music(self):
        self.play_sound('./src/assets/sounds/intro_music.mp3', 0.6, -1)

    def background_music(self):
        self.play_sound('./src/assets/sounds/background_one.mp3', 0.6, -1)

    def game_music(self):
        self.play_sound('./src/assets/sounds/game_music.mp3', 0.3, - 1)

    def game_over_music(self):
        self.play_sound('./src/assets/sounds/game_over_music.mp3', 0.5, -1)

    def get_ready_voice(self):
        self.play_sound('./src/assets/sounds/get_ready_voice.wav')

    def bonus_music(self):
        self.play_sound('./src/assets/sounds/bonus_label.wav')
    # ------------------------------------------------------
    def pacman_start(self):
        self.play_sound('./src/assets/sounds/Pacman_sound.mp3')

    def pacman_death(self):
        self.play_sound('./src/assets/sounds/Pacman_death.mp3')

    def pacman_eat(self):
        self.play_sound('./src/assets/sounds/Pacman_eat.wav', 0.9)

    def pacman_eat_red_dot(self):
        self.play_sound('./src/assets/sounds/Pacman_eat_red_dot.wav', 0.9)

    def pacman_eat_enemy(self):
        self.play_sound('./src/assets/sounds/Pacman_eat_enemy.wav', 0.5)

    def pacman_eat_enemy_after(self):
        self.play_sound('./src/assets/sounds/Pacman_eat_enemy_after.wav', 0.9)

    def pacman_alarm(self):
        self.play_sound('./src/assets/sounds/Pacman_alarm.wav', 0.9)

    def add_bonus_points(self):
        self.play_sound('./src/assets/sounds/bonus.wav')

    def add_bonus_fruit(self):
        self.play_sound('./src/assets/sounds/bonus_add.mp3')