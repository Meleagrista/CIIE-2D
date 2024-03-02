from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from managers.resource_manager import ResourceManager

import pygame

# TODO: Extact these into a constants file.
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        GUI SCREEN PROTOTYPE                                   #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class PantallaGUI:
    def __init__(self, menu, image_name):
        self.menu = menu
        self.image = ResourceManager.load_image(image_name)
        self.image = pygame.transform.scale(self.image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        self.elements = []
        self.click = None

    def events(self, event_list):
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                self.click = None
                for element in self.elements:
                    if element.position_in_element(event.pos):
                        self.click = element
            if event.type == MOUSEBUTTONUP:
                for element in self.elements:
                    if element.position_in_element(event.pos):
                        if element == self.click:
                            element.activate()

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect())
        for element in self.elements:
            element.draw(screen, )
