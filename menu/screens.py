from menu.prototypes.gui_prototypes import CreditsText
from menu.prototypes.screen_prototypes import PantallaGUI
from menu.gui_texts import *
from menu.gui_buttons import *


class StartingScreen(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, BACKGROUND_IMAGE)

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
        texto_titulo = TextoMenuTitle(self)

        self.elements.append(text_play)
        self.elements.append(text_configuration)
        self.elements.append(text_credits)
        self.elements.append(text_exit)
        self.elements.append(texto_titulo)


class ConfigurationScreen(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, BACKGROUND_IMAGE)

        switch_volumen = SwitchVolume(self)
        switch_controles = SwitchController(self)
        button_go_back = ButtonBackToMenu(self)

        self.elements.append(switch_controles)
        self.elements.append(switch_volumen)
        self.elements.append(button_go_back)

        texto_volumen = TextoMenuMusic(self)
        texto_arrows_wasd = TextoMenuController(self)
        text_go_back = TextoBackToMenu(self)

        self.elements.append(texto_volumen)
        self.elements.append(texto_arrows_wasd)
        self.elements.append(text_go_back)


class CreditsScreen(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, BACKGROUND_IMAGE)

        button_go_back = ButtonBackToMenu(self)

        self.elements.append(button_go_back)

        text_credits = CreditsText(self)
        text_go_back = TextoBackToMenu(self)

        self.elements.append(text_credits)
        self.elements.append(text_go_back)
