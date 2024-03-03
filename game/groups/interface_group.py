import pygame


class Interface(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._player = None

    def set_player(self, player):
        self._player = player

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
                kwargs = {'text': "Press <SPACE> to pick up the key."}
            else:
                kwargs = {'text': "You need to find the exit.", 'player': self._player}
        if self._player.in_door() and not self._player.has_key():
            kwargs = {'text': "You need to find the key."}

        for sprite in self.sprites():
            sprite.notified(**kwargs)
