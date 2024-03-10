from menu.prototypes.gui_prototypes import Text
import pygame


from utils.i18n import get_translation

from utils.paths.assets_paths import FONT
from utils.constants import MENU_LEFT, MENU_GAP, TITLE_SIZE, FONT_COLOR, TEXT_VERTICAL_CORRECTION, FONT_SIZE, \
    FONT_PERCENT


class TextoSplash(Text):
    def __init__(self, screen):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        font = pygame.font.Font(FONT, size)
        pos = (pygame.display.Info().current_w / 2, pygame.display.Info().current_h - size * 1.5)
        Text.__init__(self, screen, font, (255, 255, 255), "PRESS ANY KEY TO PLAY", (0, 0))
        self.set_center(pos)



class TextoPlay(Text):
    def __init__(self, screen):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        font = pygame.font.Font(FONT, size)
        pos = (MENU_LEFT, pygame.display.Info().current_h - (size * TEXT_VERTICAL_CORRECTION) - MENU_GAP * 3)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'play'), (0, 0))
        self.set_left(pos)


class TextoConfiguration(Text):
    def __init__(self, screen):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        font = pygame.font.Font(FONT, size)
        pos = (MENU_LEFT, pygame.display.Info().current_h - (size * TEXT_VERTICAL_CORRECTION) - MENU_GAP * 2)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'settings'), (0, 0))
        self.set_left(pos)


class TextoCredits(Text):
    def __init__(self, screen):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        font = pygame.font.Font(FONT, size)
        pos = (MENU_LEFT, pygame.display.Info().current_h - (size * TEXT_VERTICAL_CORRECTION) - MENU_GAP * 1)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'credits'), (0, 0))
        self.set_left(pos)

class TextoExit(Text):
    def __init__(self, screen):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        font = pygame.font.Font(FONT, size)
        pos = (MENU_LEFT, pygame.display.Info().current_h - (size * TEXT_VERTICAL_CORRECTION) - MENU_GAP * 0)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'exit'), (0, 0))
        self.set_left(pos)


class TextoMenuTitle(Text):
    def __init__(self, screen):
        font = pygame.font.Font(FONT, TITLE_SIZE)
        Text.__init__(self, screen, font, FONT_COLOR, 'GAME TITLE',
                      (pygame.display.Info().current_w * 0.0175, pygame.display.Info().current_h * 0.2))


class TextoBackToMenu(Text):
    def __init__(self, screen):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        font = pygame.font.Font(FONT, size)
        pos = (MENU_LEFT, pygame.display.Info().current_h - (size * TEXT_VERTICAL_CORRECTION) - MENU_GAP * 0)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'return'), (0, 0))
        self.set_left(pos)



class TextoMenuMusic(Text):
    def __init__(self, screen):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        font = pygame.font.Font(FONT, size)
        pos = (MENU_LEFT, pygame.display.Info().current_h - (size * TEXT_VERTICAL_CORRECTION) - MENU_GAP * 3)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'menu music'), (0, 0))
        self.set_left(pos)


class TextoMenuController(Text):
    def __init__(self, screen):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        font = pygame.font.Font(FONT, size)
        pos = (MENU_LEFT, pygame.display.Info().current_h - (size * TEXT_VERTICAL_CORRECTION) - MENU_GAP * 2)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'controls'), (0, 0))
        self.set_left(pos)


class TextoMenuLanguages(Text):
    def __init__(self, screen):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        font = pygame.font.Font(FONT, size)
        pos = (MENU_LEFT, pygame.display.Info().current_h - (size * TEXT_VERTICAL_CORRECTION) - MENU_GAP * 1)
        Text.__init__(self, screen, font, FONT_COLOR, get_translation('en', 'language'), (0, 0))
        self.set_left(pos)
