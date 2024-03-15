import pygame

from game.entities.player import Player
from utils.i18n import get_translation


class Interface(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._player = None
        self._language = 'en'

    def set_player(self, player: Player) -> None:
        self._player = player

    def set_language(self, language: str) -> None:
        self._language = language

    def notified(self) -> None:
        kwargs = {'text': "", 'key_gone': False}
        player = self._player

        if player.in_key():
            if not player.has_key():
                kwargs['text'] = get_translation(self._language, 'pick up key')
            else:
                kwargs['text'] = get_translation(self._language, 'find exit')
        elif player.has_key() and not player.in_key():
            kwargs['key_gone'] = True
        elif player.in_door() and not player.has_key():
            kwargs['text'] = get_translation(self._language, 'find key')

        kwargs['player'] = player

        for sprite in self.sprites():
            sprite.notified(**kwargs)

    def draw(self, *args, **kwargs) -> None:
        for sprite in self.sprites():
            sprite.draw(*args, **kwargs)

    def update(self, **kwargs) -> None:
        language = kwargs.pop('language', None)
        if language is not None and not isinstance(language, str):
            raise TypeError("language must be a string")

        if language != self._language:
            self._language = language

        # Remove 'player' from kwargs if it exists
        player = kwargs.pop('player', None)

        for sprite in self.sprites():
            # Pass player directly, not as part of kwargs
            sprite.update(player=player, **kwargs)
