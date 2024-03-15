import pygame
from game.entities.player import Player
from game.entities.enemy import Enemy
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

    def spawn(self, grid: Grid, win: pygame.Surface, enemies_dict: dict[str, list]) -> list[Enemy]:
        """
        Spawn enemies in specified zones.

        Args:
            grid: Grid object for pathfinding.
            win: Surface representing the game window.
            enemies_dict: Dictionary of the enemies that should spawn.

        Returns:
            List of spawned Enemy objects.
        """
        self.remove_all()

        enemies = []

        if enemies_dict["civilian"]:
            for area in enemies_dict["civilian"]:
                x, y = grid.get_random_node_from_zone(area).get_pos()
                enemy = Civilian((x, y), grid, win, area)
                enemies.append(enemy)

        if enemies_dict["sentinel"]:
            for areas in enemies_dict["sentinel"]:
                initial_zone = areas[0] if areas else None  # Simplified initialization of initial_zone
                if initial_zone is None:
                    x, y = grid.get_random_node().get_pos()
                else:
                    x, y = grid.get_random_node_from_zone(initial_zone).get_pos()
                enemy = Sentinel((x, y), grid, win, areas)
                enemies.append(enemy)

        if enemies_dict["guard"]:
            for areas in enemies_dict["guard"]:
                initial_zone = areas[0] if areas else None  # Simplified initialization of initial_zone
                if initial_zone is None:
                    x, y = grid.get_random_node().get_pos()
                else:
                    x, y = grid.get_random_node_from_zone(initial_zone).get_pos()
                enemy = Guard((x, y), grid, win, areas)
                enemies.append(enemy)

        number = enemies_dict["security"]
        if number != 0:
            for i in range(number):
                x, y = grid.get_random_node().get_pos()
                enemy = Security((x, y), grid, win)
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
