from menu.prototypes.gui_prototypes import Text

import pygame

from utils.filepaths import FONT


class TextoPlay(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        Text.__init__(self, screen, fuente, (0, 0, 0), 'PLAY', (530, 55))

    def activate(self):
        self.screen.menu.run()


class TextoConfiguration(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        Text.__init__(self, screen, fuente, (0, 0, 0), 'SETTINGS', (530, 95))

    def activate(self):
        self.screen.menu.show_configuration_screen()


class TextoCredits(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        Text.__init__(self, screen, fuente, (0, 0, 0), 'CREDITS', (530, 135))

    def activate(self):
        self.screen.menu.show_credits_screen()


class TextoExit(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        Text.__init__(self, screen, fuente, (0, 0, 0), 'EXIT', (530, 175))

    def activate(self):
        self.screen.menu.exit()


class TextoMenuTitle(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 50)
        Text.__init__(self, screen, fuente, (0, 0, 0), 'GAME TITLE', (50, 100))

    def activate(self):
        pass


class TextoBackToMenu(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        Text.__init__(self, screen, fuente, (0, 0, 0), 'RETURN', (560, 160))

    def activate(self):
        self.screen.menu.show_starting_screen()


class TextoMenuMusic(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        Text.__init__(self, screen, fuente, (0, 0, 0), 'MENU MUSIC', (560, 80))


class TextoMenuController(Text):
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        Text.__init__(self, screen, fuente, (0, 0, 0), 'CONTROLS', (560, 120))
