import pygame
from pygame import Surface

from managers.resource_manager import ResourceManager
from utils.constants import FONT_COLOR
from utils.i18n import get_translation
from utils.paths.assets_paths import FONT


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

    def set_topleft(self, position):
        (x, y) = position
        self.rect.top = y
        self.rect.left = x

    def set_topright(self, position):
        (x, y) = position
        self.rect.top = y
        self.rect.right = x

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
            self.image = pygame.transform.scale(self.image, (
                pygame.display.Info().current_h / 10, pygame.display.Info().current_h / 10))

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
            self.image_1 = pygame.transform.scale(self.image_1, (50, 50))
        if isinstance(image_name_2, Surface):
            self.image_2 = image_name_2
        else:
            self.image_2 = ResourceManager.load_image(image_name_2, -1)
            self.image_2 = pygame.transform.scale(self.image_2, (50, 50))

        ElementoGUI.__init__(self, screen, self.image_1.get_rect())

        self.set_position(position)
        self.state = initial_state
        self.image = self.image_2

    def rescale(self, size):
        self.image_1 = pygame.transform.scale(self.image_1, (size, size))
        self.image_2 = pygame.transform.scale(self.image_2, (size, size))
        self.image = pygame.transform.scale(self.image, (size, size))
        self.set_rect(self.image.get_rect())

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


class TitleElement(ElementoGUI):
    def __init__(self, screen, image, position):
        if isinstance(image, Surface):
            self.image = image
        else:
            self.image = ResourceManager.load_image(image, -1)

            # Assuming self.image is the original image surface
            original_width = self.image.get_width()
            original_height = self.image.get_height()

            # Desired width (half of the screen width in this case)
            desired_width = pygame.display.Info().current_w / 2

            # Calculate the scaling factor
            scale_factor = desired_width / original_width

            # Scale the image maintaining aspect ratio
            scaled_width = int(original_width * scale_factor)
            scaled_height = int(original_height * scale_factor)

            # Scale the image
            self.image = pygame.transform.scale(self.image, (scaled_width, scaled_height))

        ElementoGUI.__init__(self, screen, self.image.get_rect())
        self.set_topright(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def activate(self):
        pass


class CreditsText:
    def __init__(self, screen):
        self.font = pygame.font.Font(FONT, 20)
        self.screen = screen
        self.texts = []
        self.texts.append(Text(screen, self.font, FONT_COLOR,
                               get_translation('en', '1'),
                               (40, 100))
                          )
        self.texts.append(Text(screen, self.font, FONT_COLOR,
                               get_translation('en', '2'),
                               (40, 130))
                          )
        self.texts.append(Text(screen, self.font, FONT_COLOR,
                               get_translation('en', '3'),
                               (40, 160))
                          )
        self.texts.append(Text(screen, self.font, FONT_COLOR,
                               get_translation('en', '4'),
                               (40, 190))
                          )
        self.texts.append(Text(screen, self.font, FONT_COLOR,
                               get_translation('en', '5'),
                               (50, 220))
                          )
        self.texts.append(Text(screen, self.font, FONT_COLOR,
                               get_translation('en', '6'),
                               (50, 250))
                          )
        self.texts.append(Text(screen, self.font, FONT_COLOR,
                               get_translation('en', '7'),
                               (50, 280))
                          )
        self.texts.append(Text(screen, self.font, FONT_COLOR,
                               get_translation('en', '8'),
                               (50, 310))
                          )
        self.translate('en')

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

    def translate(self, language):
        # Define initial values
        translation_key = 1
        y_position = 40
        x_position = pygame.display.Info().current_w

        # Iterate through texts
        for i in range(len(self.texts)):
            # Create the text object with translated content
            new = Text(self.screen, self.font, FONT_COLOR, get_translation(language, str(translation_key)), (0, 0))
            new.set_right((x_position - 40, y_position))
            self.texts[i] = new

            # Increase translation_key and y_position for the next iteration
            translation_key += 1
            y_position += 20
