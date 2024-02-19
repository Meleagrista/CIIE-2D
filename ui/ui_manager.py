from utils.auxiliar import replace_accented_characters
from utils.constants import *
from utils.enums import Controls as Ctl
import os
import pygame
import pygame_menu
import time
import loop


class UIManager:
    def __init__(self, font='pixel.regular.ttf', loa_img='splash_screen_placeholder.jpeg',
                 bkg_img='desert-pixel-placeholder.png', music='fall-from-grace.mp3'):
        self.mov_opt = Ctl.WASD
        self.win_wid, self.win_hei = None, None
        self.loa_img = 'assets/' + loa_img
        self.bkg_img = 'assets/' + bkg_img
        self.font = 'assets/' + font
        self.music = 'assets/' + music

    def run(self):
        pygame.init()
        pygame.mixer.init()

        self.win_wid, self.win_hei = pygame.display.Info().current_w, pygame.display.Info().current_h

        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1)  # -1 to infinity music

        """
        Fall From Grace by Darren Curtis | https://www.darrencurtismusic.com/
        Music promoted by https://www.chosic.com/free-music/all/
        Creative Commons CC BY 3.0
        https://creativecommons.org/licenses/by/3.0/
        """

        win = pygame.display.set_mode((self.win_wid, self.win_hei), pygame.FULLSCREEN)
        self.splash_screen(win, 10)

        menu_theme = self.create_theme(MENU_FONT, TITLE_FONT, FONT_COLOR)
        menu = pygame_menu.Menu("Game Title", self.win_wid, self.win_hei, theme=menu_theme)

        menu_credits = self.write_credits(replace_accented_characters(CREDITS))

        menu_controls = pygame_menu.Menu("Settings", self.win_wid, self.win_hei, theme=menu_theme)
        menu_controls.add.selector('Player movement: ', [('WASD', 0), ('Arrows', 1)],
                                   onchange=self.change_movement_option)
        menu_controls.add.toggle_switch('Volume:', True, onchange=self.change_volume,
                                        state_color=((255, 78, 69), (183, 255, 115)), slider_thickness=10)
        # controls_menu.add.selector('Volume :', ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], onchange=change_volume)

        menu.add.button("Play", self.start)
        menu.add.button("Settings", menu_controls)
        menu.add.button("Credits", menu_credits)
        menu.add.button("Quit", pygame_menu.events.EXIT)

        menu.mainloop(win)

    def start(self):
        pygame.mixer.music.stop()
        loop.play_game(self.mov_opt)

    def change_difficulty(self):
        pass

    def splash_screen(self, win, wait_sec):
        splash_image = pygame.image.load(self.loa_img)
        splash_image = pygame.transform.scale(splash_image, (self.win_wid, self.win_hei))
        win.blit(splash_image, (0, 0))

        pygame.display.flip()
        start_time = time.time()

        running = True
        while running and time.time() - start_time < wait_sec:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    running = False

            # Limits to 60fps
            pygame.time.delay(1000 // 60)

    def create_theme(self, txt_size, ttl_size, color):
        text_font = pygame.font.Font(self.font, txt_size)
        title_font = pygame.font.Font(self.font, ttl_size)
        image = pygame.image.load(self.bkg_img)

        # Define the new size for the image, must have the same aspect ratio
        new_width = image.get_width() // (image.get_width() / self.win_hei)
        new_height = image.get_height() // (image.get_height() / self.win_hei)

        # Scale the image
        scaled_image = pygame.transform.scale(image, (new_width, new_height))
        temp_img = "assets/temp/temp_scaled_image.png"
        pygame.image.save(scaled_image, temp_img)

        base_image = pygame_menu.BaseImage(temp_img, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_CENTER)
        os.remove(temp_img)

        menu_theme = pygame_menu.Theme(background_color=base_image, title_font=title_font,
                                       title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                                       widget_font_color=color, widget_font=text_font, title_offset=(25, 25))
        return menu_theme

    def write_credits(self, labels):
        menu_theme = self.create_theme(CREDITS_FONT, TITLE_FONT, FONT_COLOR)
        menu_credits = pygame_menu.Menu("Credits", self.win_wid, self.win_hei, theme=menu_theme)

        for label in labels.split('\n'):
            menu_credits.add.label(label)
        return menu_credits

    def change_movement_option(self, value, index):
        self.mov_opt = Ctl.from_string(value)
        print(f'User selected {self.mov_opt} at index {index}')

    @staticmethod
    def change_volume(value):
        if value:
            pygame.mixer.music.set_volume(1.0)
        else:
            pygame.mixer.music.set_volume(0.0)
