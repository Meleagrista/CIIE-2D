from menu.prototypes.gui_prototypes import Text

import pygame
from utils.i18n import get_translation

from utils.paths.assets_paths import FONT


class TextoSplash(Text):
    def __init__(self, screen):
        font_size = 50
        font = pygame.font.Font(FONT, font_size)
        pos = (pygame.display.Info().current_w / 2, pygame.display.Info().current_h - font_size*1.5)
        Text.__init__(self, screen, font, (255, 255, 255), "PRESS ANY KEY TO PLAY", (0, 0))
        self.set_center(pos)

    def activate(self):
        pass


class TextoPlay(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font('assets/fonts/pixel.regular.ttf', round((pygame.display.Info().current_h / 10)))
        Text.__init__(self, screen, fuente, (0, 0, 0), 'PLAY', (pygame.display.Info().current_w * 0.42, pygame.display.Info().current_h * 0.43))

    def activate(self):
        self.screen.menu.run()


class TextoConfiguration(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font('assets/fonts/pixel.regular.ttf', round((pygame.display.Info().current_h / 10)))
        Text.__init__(self, screen, fuente, (0, 0, 0), 'SETTINGS', (pygame.display.Info().current_w * 0.42, pygame.display.Info().current_h * 0.53))

    def activate(self):
        self.screen.menu.show_configuration_screen()


class TextoCredits(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font('assets/fonts/pixel.regular.ttf', round((pygame.display.Info().current_h / 10)))
        Text.__init__(self, screen, fuente, (0, 0, 0), 'CREDITS', (pygame.display.Info().current_w * 0.42, pygame.display.Info().current_h * 0.63))

    def activate(self):
        self.screen.menu.show_credits_screen()


class TextoExit(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font('assets/fonts/pixel.regular.ttf', round((pygame.display.Info().current_h / 10)))
        Text.__init__(self, screen, fuente, (0, 0, 0), 'EXIT', (pygame.display.Info().current_w * 0.42, pygame.display.Info().current_h * 0.73))

    def activate(self):
        self.screen.menu.exit()


class TextoMenuTitle(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font('assets/fonts/pixel.regular.ttf', round((pygame.display.Info().current_h / 5)))
        Text.__init__(self, screen, fuente, (0, 0, 0), 'GAME TITLE', (pygame.display.Info().current_w * 0.05, pygame.display.Info().current_h * 0.3))

    def activate(self):
        pass


class TextoBackToMenu(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font('assets/fonts/pixel.regular.ttf', round((pygame.display.Info().current_h / 10)))
        Text.__init__(self, screen, fuente, (0, 0, 0), 'RETURN', (pygame.display.Info().current_w * 0.45, pygame.display.Info().current_h * 0.80))

    def activate(self):
        self.screen.menu.show_starting_screen()


class TextoMenuMusic(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font('assets/fonts/pixel.regular.ttf', round((pygame.display.Info().current_h / 10)))
        Text.__init__(self, screen, fuente, (0, 0, 0), 'MENU MUSIC', (pygame.display.Info().current_w * 0.45, pygame.display.Info().current_h * 0.60))


class TextoMenuController(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font('assets/fonts/pixel.regular.ttf', round((pygame.display.Info().current_h / 10)))
        Text.__init__(self, screen, fuente, (0, 0, 0), 'CONTROLS', (pygame.display.Info().current_w * 0.45, pygame.display.Info().current_h * 0.40))


class TextoMenuLanguages(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        Text.__init__(self, screen, fuente, (0, 0, 0), get_translation('en', 'language'), (560, 160))
