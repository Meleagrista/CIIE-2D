from pygame import Surface

from managers.resource_manager import ResourceManager

import pygame

from utils.constants import FONT_COLOR, FONT_SIZE
from utils.paths.assets_paths import FONT
from utils.i18n import get_translation


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        GUI ELEMENT PROTOTYPE                                  #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class ElementoGUI:
    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect

    def set_position(self, position):
        (x, y) = position
        self.rect.left = x
        self.rect.bottom = y

    def set_center(self, position):
        self.rect.center = position

    def set_right(self, position):
        (x, y) = position
        self.rect.centery = y
        self.rect.right = x

    def set_left(self, position):
        (x, y) = position
        self.rect.centery = y
        self.rect.left = x

    def set_rect(self, new_rect):
        self.rect = new_rect

    def position_in_element(self, position):
        (x, y) = position
        if ((x >= self.rect.left)
                and (x <= self.rect.right)
                and (y >= self.rect.top)
                and (y <= self.rect.bottom)):
            return True
        else:
            return False

    def draw(self, screen):
        raise NotImplemented("Not implemented here.")

    def activate(self):
        raise NotImplemented("Not implemented here.")


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        GUI BUTTON PROTOTYPE                                   #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Button(ElementoGUI):
    def __init__(self, screen, image, position):
        if isinstance(image, Surface):
            self.image = image
        else:
            self.image = ResourceManager.load_image(image, -1)
            self.image = pygame.transform.scale(self.image, (pygame.display.Info().current_h / 10, pygame.display.Info().current_h / 10))

        ElementoGUI.__init__(self, screen, self.image.get_rect())

        self.set_position(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class ButtonSwitch(Button):
    def __init__(self, screen, image_name_1, image_name_2, position, initial_state):
        if isinstance(image_name_1, Surface):
            self.image_1 = image_name_1
        else:
            self.image_1 = ResourceManager.load_image(image_name_1, -1)
            self.image_1 = pygame.transform.scale(self.image_1, (pygame.display.Info().current_h / 6, pygame.display.Info().current_h / 6))
        if isinstance(image_name_2, Surface):
            self.image_2 = image_name_2
        else:
            self.image_2 = ResourceManager.load_image(image_name_2, -1)
            self.image_2 = pygame.transform.scale(self.image_2, (pygame.display.Info().current_h / 6, pygame.display.Info().current_h / 6))
        
        ElementoGUI.__init__(self, screen, self.image_1.get_rect())

        self.set_position(position)
        self.state = initial_state
        self.image = self.image_2


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        GUI TEXT PROTOTYPE                                     #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Text(ElementoGUI):
    def __init__(self, screen, font, color, text, position):
        self.color = color
        self.font = font
        self.text = text
        self.position = position

        self.image = self.font.render(self.text, True, self.color)

        ElementoGUI.__init__(self, screen, self.image.get_rect())

        self.set_position(self.position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def activate(self):
        pass

    def translate(self, language):
        new_text = get_translation(language, self.text)
        text_surface = self.font.render(new_text, True, self.color)
        old_rect = self.rect
        self.rect = text_surface.get_rect()
        self.rect.topleft = old_rect.topleft
        self.image = text_surface


class CreditsText:
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        self.texts = []
        self.texts.append(Text(screen, fuente, FONT_COLOR,
                               "Contornos Inmersivos, Interactivos y de Entretenimiento", (40, 100)))
        self.texts.append(Text(screen, fuente, FONT_COLOR,
                               "Grado en Ingenieria Informatica", (40, 130)))
        self.texts.append(Text(screen, fuente, FONT_COLOR,
                               "Universidade da Coruna, UDC", (40, 160)))
        self.texts.append(Text(screen, fuente, FONT_COLOR,
                               "Autores:", (40, 190)))
        self.texts.append(Text(screen, fuente, FONT_COLOR,
                               "     - Martin do Rio Rico", (50, 220)))
        self.texts.append(Text(screen, fuente, FONT_COLOR,
                               "     - Yago Fernandez Rego", (50, 250)))
        self.texts.append(Text(screen, fuente, FONT_COLOR,
                               "     - David Garcia Ramallal:", (50, 280)))
        self.texts.append(Text(screen, fuente, FONT_COLOR,
                               "     - Pelayo Vieites Perez", (50, 310)))

    def draw(self, screen):
        for text in self.texts:
            text.draw(screen)

    def position_in_element(self, position):
        for text in self.texts:
            if text.position_in_element(position):
                return True
        return False

    def activate(self):
        pass
