import pygame.mixer
from pygame import KEYDOWN, K_ESCAPE
from managers.prototypes.scene_prototype import Scene
from menu.screens import *

import time

# movement_option = Ctl.WASD

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        MENU SCENE (MENU MANAGER)                              #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#


class MenuManager(Scene):

    def __init__(self, manager, audio):
        Scene.__init__(self, manager)

        self.screen_list = []

        self.audio = audio

        self.screen_list.append(StartingScreen(self))
        self.screen_list.append(ConfigurationScreen(self))
        self.screen_list.append(CreditsScreen(self))

        self.current_screen = None
        self.show_starting_screen()

    def events(self, event_list):
        for event in event_list:
            if event.type == KEYDOWN:
                if event.has_key == K_ESCAPE:
                    self.exit()
            elif event.type == pygame.QUIT:
                self.exit()

        self.screen_list[self.current_screen].events(event_list)

    def draw(self, screen):
        self.screen_list[self.current_screen].draw(screen)

    def update(self, **kwargs):
        pass

    # ####################################################################### #
    #                               CLASS METHODS                             #
    # ####################################################################### #

    def exit(self):
        self.manager.exit()

    def run(self):
        self.audio.music_game()
        self.manager.change_scene()

    def show_starting_screen(self):
        self.current_screen = 0

    def show_configuration_screen(self):
        self.current_screen = 1

    def show_credits_screen(self):
        self.current_screen = 2

    def set_movement_option(self, option):
        self.manager.set_movement_option(option)

    def set_language(self, language):
        self.manager.set_language(language)

    @staticmethod
    def splash_screen(screen, wait_seconds):
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        splash_image = pygame.image.load(SPLASH_IMAGE)
        splash_image = pygame.transform.scale(splash_image, (screen_width, screen_height))

        screen.blit(splash_image, (0, 0))

        pygame.display.flip()

        start_time = time.time()

        running = True

        while running and time.time() - start_time < wait_seconds:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False

            pygame.time.delay(1000 // 60)
