from menu.prototypes.gui_prototypes import Text

import pygame

from utils.constants import FONT_SIZE, MENU_LEFT, MENU_GAP, TITLE_SIZE, FONT_COLOR
from utils.i18n import get_translation

from utils.paths.assets_paths import FONT


class TextoSplash(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, FONT_SIZE)
        pos = (pygame.display.Info().current_w / 2, pygame.display.Info().current_h - FONT_SIZE * 1.5)
        Text.__init__(self, screen, font, (255, 255, 255), "PRESS ANY KEY TO PLAY", (0, 0))
        self.set_center(pos)

    def activate(self):
        pass


class TextoPlay(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, FONT_SIZE)
        pos = (pygame.display.Info().current_w * MENU_LEFT, 0 + (FONT_SIZE * 1.5) + MENU_GAP * 0)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'play'), (0, 0))
        self.set_left(pos)

    def activate(self):
        self.screen.menu.run()


class TextoConfiguration(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, FONT_SIZE)
        pos = (pygame.display.Info().current_w * MENU_LEFT, 0 + (FONT_SIZE * 1.5) + MENU_GAP * 1)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'settings'), (0, 0))
        self.set_left(pos)

    def activate(self):
        self.screen.menu.show_configuration_screen()


class TextoCredits(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, FONT_SIZE)
        pos = (pygame.display.Info().current_w * MENU_LEFT, 0 + (FONT_SIZE * 1.5) + MENU_GAP * 2)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'credits'), (0, 0))
        self.set_left(pos)

    def activate(self):
        self.screen.menu.show_credits_screen()


class TextoExit(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, FONT_SIZE)
        pos = (pygame.display.Info().current_w * MENU_LEFT, 0 + (FONT_SIZE * 1.5) + MENU_GAP * 3)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'exit'), (0, 0))
        self.set_left(pos)

    def activate(self):
        self.screen.menu.exit()


class TextoMenuTitle(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, TITLE_SIZE)
        Text.__init__(self, screen, font, FONT_COLOR, 'GAME TITLE',
                      (pygame.display.Info().current_w * 0.05, pygame.display.Info().current_h * 0.3))

    def activate(self):
        pass


class TextoBackToMenu(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, FONT_SIZE)
        pos = (pygame.display.Info().current_w * MENU_LEFT, 0 + (FONT_SIZE * 1.5) + MENU_GAP * 0)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'return'), (0, 0))
        self.set_left(pos)

    def activate(self):
        self.screen.menu.show_starting_screen()


class TextoMenuMusic(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, FONT_SIZE)
        pos = (pygame.display.Info().current_w * MENU_LEFT, 0 + (FONT_SIZE * 1.5) + MENU_GAP * 1)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'menu music'), (0, 0))
        self.set_left(pos)


class TextoMenuController(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, FONT_SIZE)
        pos = (pygame.display.Info().current_w * MENU_LEFT, 0 + (FONT_SIZE * 1.5) + MENU_GAP * 2)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'controls'), (0, 0))
        self.set_left(pos)


class TextoMenuLanguages(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, FONT_SIZE)
        pos = (pygame.display.Info().current_w * MENU_LEFT, 0 + (FONT_SIZE * 1.5) + MENU_GAP * 3)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'language'), (0, 0))
        self.set_left(pos)
