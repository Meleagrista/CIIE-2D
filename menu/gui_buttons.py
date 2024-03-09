import pygame

from menu.prototypes.gui_prototypes import Button, ButtonSwitch
from utils.constants import MENU_GAP, BUTTON_VERTICAL_CORRECTION, BUTTON_HORIZONTAL_CORRECTION, FONT_SIZE, \
    FONT_PERCENT
from utils.enums import Controls as Ctl
from utils.paths.assets_paths import *


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        REGULAR BUTTONS                                        #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class AbstractButton(Button):
    def __init__(self, screen, button_type, button_size, button_position, action_function):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        Button.__init__(self, screen, button_type, button_size)
        pos = (BUTTON_HORIZONTAL_CORRECTION,
               pygame.display.Info().current_h - (size * BUTTON_VERTICAL_CORRECTION) - MENU_GAP * button_position)
        self.set_left(pos)
        self.action_function = action_function

    def activate(self):
        self.action_function(self.screen.menu)


class ButtonPlay(AbstractButton):
    def __init__(self, screen):
        super().__init__(screen, BUTTON_PLAY, (500, 90), 3, lambda menu: menu.run())


class ButtonConfiguration(AbstractButton):
    def __init__(self, screen):
        super().__init__(screen, BUTTON_CONFIGURATION, (500, 90), 2, lambda menu: menu.show_configuration_screen())


class ButtonCredits(AbstractButton):
    def __init__(self, screen):
        super().__init__(screen, BUTTON_CREDITS, (500, 130), 1, lambda menu: menu.show_credits_screen())


class ButtonExit(AbstractButton):
    def __init__(self, screen):
        super().__init__(screen, BUTTON_EXIT, (500, 170), 0, lambda menu: menu.exit())


class ButtonBackToMenu(AbstractButton):
    def __init__(self, screen):
        super().__init__(screen, BUTTON_BACK, (520, 200), 0, lambda menu: menu.show_starting_screen())


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        REGULAR BUTTONS                                        #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class AbstractSwitch(ButtonSwitch):
    def __init__(self, screen, image_off, image_on, button_size, button_position, initial_state, action_function):
        size = round(min(pygame.display.Info().current_w * FONT_PERCENT, FONT_SIZE))
        ButtonSwitch.__init__(self, screen, image_off, image_on, button_size, initial_state)
        self.pos = (BUTTON_HORIZONTAL_CORRECTION,
                    pygame.display.Info().current_h - (size * BUTTON_VERTICAL_CORRECTION) - MENU_GAP * button_position)
        self.set_left(self.pos)
        self.action_function = action_function

    def activate(self):
        self.action_function()


class SwitchVolume(AbstractSwitch):
    def __init__(self, screen):
        super().__init__(screen, SWITCH_ON, SWITCH_OFF, (500, 90), 3, 'Off', self.toggle_volume)
        # self.pos = (self.pos[0], self.pos[1])
        # self.set_left(self.pos)
        self.rescale(90)
        self.pos = (self.pos[0] - 9, self.pos[1])
        self.set_left(self.pos)

        self.frame = FRAME
        self.frame_rect = self.frame.get_rect()
        self.frame_rect.centery = self.pos[1]
        self.frame_rect.left = BUTTON_HORIZONTAL_CORRECTION

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.frame, self.frame_rect)

    def toggle_volume(self):
        if self.state == 'Off':
            pygame.mixer.music.set_volume(1.0)  # Max volume
            self.state = 'On'
            self.image = self.image_2
        else:
            pygame.mixer.music.set_volume(0.0)  # Mute
            self.state = 'Off'
            self.image = self.image_1

class SwitchController(AbstractSwitch):
    def __init__(self, screen):
        super().__init__(screen, BUTTON_ARROWS, BUTTON_WASD, (80, 80), 2, 'Arrows', self.toggle_controller)
        self.pos = (self.pos[0] + 15, self.pos[1])
        self.set_left(self.pos)

        self.frame = FRAME
        self.frame_rect = self.frame.get_rect()
        self.frame_rect.centery = self.pos[1]
        self.frame_rect.left = BUTTON_HORIZONTAL_CORRECTION

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.frame, self.frame_rect)

    def toggle_controller(self):
        if self.state == 'Arrows':
            self.screen.menu.set_movement_option(Ctl.WASD)
            self.state = 'WASD'
            self.image = self.image_2
        else:
            self.screen.menu.set_movement_option(Ctl.Arrows)
            self.state = 'Arrows'
            self.image = self.image_1


class SwitchLanguage(AbstractSwitch):
    def __init__(self, screen):
        super().__init__(screen, SPAIN, UNITED_KINGDOM, (500, 170), 1, 'es', self.toggle_language)
        self.pos = (self.pos[0] + 6, self.pos[1])
        self.set_left(self.pos)

        self.frame = FRAME
        self.frame_rect = self.frame.get_rect()
        self.frame_rect.centery = self.pos[1]
        self.frame_rect.left = BUTTON_HORIZONTAL_CORRECTION

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.frame, self.frame_rect)

    def toggle_language(self):
        if self.state == 'es':
            self.screen.menu.set_language('en')
            self.state = 'en'
            self.image = self.image_2
        else:
            self.screen.menu.set_language('es')
            self.state = 'es'
            self.image = self.image_1
