import pygame

from utils.i18n import get_translation


class Interface(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._player = None
        self._language = 'en'

    def set_player(self, player):
        self._player = player

    def set_language(self, language):
        self._language = language

    def draw(self, *args, **kwargs):
        for sprite in self.sprites():
            sprite.draw(*args, **kwargs)

    def update(self, **kwargs):
        kwargs['player'] = self._player
        for sprite in self.sprites():
            sprite.update(**kwargs)

    def notified(self):
        kwargs = {'text': ""}

        if self._player.in_key():
            if not self._player.has_key():
                kwargs = {'text': get_translation(self._language, 'pick up key')}
            else:
                kwargs = {'text': get_translation(self._language, 'find exit')}
        if self._player.in_door() and not self._player.has_key():
            kwargs = {'text': get_translation(self._language, 'find key')}

        kwargs['player'] = self._player

        for sprite in self.sprites():
            sprite.notified(**kwargs)
