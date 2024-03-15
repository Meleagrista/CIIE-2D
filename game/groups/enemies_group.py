import pygame
from game.entities.player import Player
from game.map.grid import Grid
from game.entities.enemies.guard import Guard
from game.entities.enemies.civilian import Civilian
from game.entities.enemies.sentinel import Sentinel
from game.entities.enemies.security import Security


class Enemies(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self._player = None

    def set_player(self, player: Player) -> None:
        self._player = player

    def notified(self) -> None:
        if self._player.detected():
            for sprite in self.sprites():
                sprite.notified(self._player)

    def remove(self, enemy: Enemy = None) -> None:
        if enemy:
            enemy.kill()
        else:
            self.remove_all()

    def remove_all(self) -> None:
        if self.sprites():
            for enemy in self.sprites():
                enemy.kill()

    def spawn(self, grid: Grid, win: pygame.Surface, enemies_zones: list[list]) -> list[Enemy]:
        """
        Spawn enemies in specified zones.

        Args:
            grid: Grid object for pathfinding.
            win: Surface representing the game window.
            enemies_zones: List of zones where enemies should spawn.

        Returns:
            List of spawned Enemy objects.
        """
        self.remove_all()

        enemies = []

        for zones in enemies_zones:
            initial_zone = zones[0] if zones else None  # Simplified initialization of initial_zone
            if initial_zone is None:
                x, y = grid.get_random_node().get_pos()
            else:
                x, y = grid.get_random_node_from_zone(initial_zone).get_pos()
            enemy = Enemy((x, y), 1, 3, grid, win, zones)
            enemies.append(enemy)

        return enemies

    @staticmethod
    def introduce(enemy: Enemy, *groups: pygame.sprite.AbstractGroup) -> None:
        """
        Add an enemy to specified groups.

        Args:
            enemy: Enemy object to be added to groups.
            *groups: Variable number of groups to add the enemy to.
        """
        enemy.add(*groups)
