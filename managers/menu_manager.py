from pygame import KEYDOWN, K_ESCAPE
from managers.game_scene import Scene
from menu.elements.screens import *

import time

# movement_option = Ctl.WASD

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        MENU SCENE (MENU MANAGER)                              #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#


class MenuManager(Scene):

    def __init__(self, manager):
        Scene.__init__(self, manager)

        self.screen_list = []

        self.screen_list.append(StartingScreen(self))
        self.screen_list.append(ConfigurationScreen(self))
        self.screen_list.append(CreditsScreen(self))

        self.current_screen = None
        self.show_starting_screen()

    def events(self, event_list):
        for event in event_list:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exit()
            elif event.type == pygame.QUIT:
                self.exit()

        self.screen_list[self.current_screen].events(event_list)

    def draw(self, screen):
        self.screen_list[self.current_screen].draw(screen)

    def update(self, *args):
        pass

    # ####################################################################### #
    #                               PATHFINDING                               #
    # ####################################################################### #

    def exit(self):
        self.manager.exit()

    def run(self):
        """global movement_option
        pygame.mixer.music.stop()
        game = GameManager(mov_opt=movement_option)
        game.run()"""
        pass

    def show_starting_screen(self):
        self.current_screen = 0

    def show_configuration_screen(self):
        self.current_screen = 1

    def show_credits_screen(self):
        self.current_screen = 2

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
