from pygame import MOUSEBUTTONDOWN, KEYDOWN

from menu.gui_buttons import *
from menu.gui_texts import *
from menu.prototypes.gui_prototypes import CreditsText, TitleElement
from menu.prototypes.screen_prototypes import PantallaGUI


class SplashScreen(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, SPLASH_IMAGE)

        text_splash = TextoSplash(self)

        self.all_text = []

        self.elements.append(text_splash)

    def events(self, event_list):
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                self.menu.show_starting_screen()


class StartingScreen(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, BACKGROUND_IMAGE)

        title = TitleElement(self, TITLE_IMAGE, (pygame.display.Info().current_w - 20, 20))

        self.elements.append(title)

        button_play = ButtonPlay(self)
        button_configuration = ButtonConfiguration(self)
        button_credits = ButtonCredits(self)
        button_exit = ButtonExit(self)

        self.elements.append(button_play)
        self.elements.append(button_configuration)
        self.elements.append(button_credits)
        self.elements.append(button_exit)

        text_play = TextoPlay(self)
        text_configuration = TextoConfiguration(self)
        text_credits = TextoCredits(self)
        text_exit = TextoExit(self)
        # texto_titulo = TextoMenuTitle(self)

        self.all_text = [text_play, text_configuration, text_credits, text_exit]

        self.elements.append(text_play)
        self.elements.append(text_configuration)
        self.elements.append(text_credits)
        self.elements.append(text_exit)
        # self.elements.append(texto_titulo)


class ConfigurationScreen(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, BACKGROUND_IMAGE)

        title = TitleElement(self, TITLE_IMAGE, (pygame.display.Info().current_w - 20, 20))

        self.elements.append(title)

        switch_volumen = SwitchVolume(self)
        switch_controles = SwitchController(self)
        switch_languages = SwitchLanguage(self)
        button_go_back = ButtonBackToMenu(self)

        self.elements.append(switch_controles)
        self.elements.append(switch_volumen)
        self.elements.append(switch_languages)
        self.elements.append(button_go_back)

        texto_volumen = TextoMenuMusic(self)
        texto_arrows_wasd = TextoMenuController(self)
        texto_languages = TextoMenuLanguages(self)
        text_go_back = TextoBackToMenu(self)

        self.all_text = [texto_volumen, texto_arrows_wasd, texto_languages, text_go_back]

        self.elements.append(texto_volumen)
        self.elements.append(texto_arrows_wasd)
        self.elements.append(texto_languages)
        self.elements.append(text_go_back)


class CreditsScreen(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, BACKGROUND_IMAGE)

        button_go_back = ButtonBackToMenu(self)

        self.elements.append(button_go_back)

        text_credits = CreditsText(self)
        text_go_back = TextoBackToMenu(self)

        self.all_text = [text_go_back, text_credits]

        self.elements.append(text_credits)
        self.elements.append(text_go_back)
