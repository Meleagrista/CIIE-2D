from managers.resource_manager import ResourceManager

import pygame

from utils.filepaths import FONT


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
    def __init__(self, screen, image_name, position):
        self.image = ResourceManager.load_image(image_name, -1)
        self.image = pygame.transform.scale(self.image, (pygame.display.Info().current_h / 10, pygame.display.Info().current_h / 10))

        ElementoGUI.__init__(self, screen, self.image.get_rect())
        
        self.set_position(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class ButtonSwitch(Button):
    def __init__(self, screen, image_name_1, image_name_2, position, initial_state):
        self.image_1 = ResourceManager.load_image(image_name_1, -1)
        self.image_1 = pygame.transform.scale(self.image_1, (pygame.display.Info().current_h / 6, pygame.display.Info().current_h / 6))
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
        self.image = font.render(text, True, color)

        ElementoGUI.__init__(self, screen, self.image.get_rect())

        self.set_position(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def activate(self):
        pass


class CreditsText:
    def __init__(self, screen):
        fuente = pygame.font.Font(FONT, 20)
        self.texts = []
        self.texts.append(Text(screen, fuente, (0, 0, 0), "Contornos Inmersivos, Interactivos e de Entretemento", (40, 100)))
        self.texts.append(Text(screen, fuente, (0, 0, 0), "Grao en Enxeneria Informatica", (40, 130)))
        self.texts.append(Text(screen, fuente, (0, 0, 0), "UDC", (40, 160)))
        self.texts.append(Text(screen, fuente, (0, 0, 0), "Authors:", (40, 190)))
        self.texts.append(Text(screen, fuente, (0, 0, 0), "- Martin do Rio Rico", (50, 220)))
        self.texts.append(Text(screen, fuente, (0, 0, 0), "- Yago Fernandez Rego", (50, 250)))
        self.texts.append(Text(screen, fuente, (0, 0, 0), "- David Garcia Ramallal:", (50, 280)))
        self.texts.append(Text(screen, fuente, (0, 0, 0), "- Pelayo Vieites Perez", (50, 310)))

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
