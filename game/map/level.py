class LevelMap:
    """
    Represents the map files for a level.

    Attributes:
        border_map_path (str): The file path for the border map.
        tile_map_path (str): The file path for the tile map.
        objects_map_path (str): The file path for the objects map.
    """
    def __init__(self, border_map_path, tile_map_path, objects_map_path):
        self.border_map_path = border_map_path
        self.tile_map_path = tile_map_path
        self.objects_map_path = objects_map_path


class LevelSpriteSheet:
    """
    Represents the sprite sheet for a level.

    Attributes:
        path (str): The file path for the sprite sheet.
        columns (int): The number of columns in the sprite sheet.
        rows (int): The number of rows in the sprite sheet.
    """
    def __init__(self, path, columns, rows):
        self.path = path
        self.columns = columns
        self.rows = rows


class LevelCoordinates:
    """
    Represents the coordinates for important elements in a level.

    Attributes:
        player_initial_x (int): The initial x-coordinate for the player.
        player_initial_y (int): The initial y-coordinate for the player.
        exit_x (int): The x-coordinate for the level exit.
        exit_y (int): The y-coordinate for the level exit.
    """
    def __init__(self, player_initial_x, player_initial_y, exit_x, exit_y):
        self.player_initial_x = player_initial_x
        self.player_initial_y = player_initial_y
        self.exit_x = exit_x
        self.exit_y = exit_y


class Level:
    """
    Represents a level in the game.

    Attributes:
        level_number (int): The level number.
        map (LevelMap): The map for the level.
        level_sprite_sheet (LevelSpriteSheet): The sprite sheet for the level.
        coordinates (LevelCoordinates): The coordinates for important elements.
        key_zones (list): List of zones where keys can be found.
        enemies_zones (list): List of zones where enemies are located.
    """
    def __init__(self, level_number, level_map, level_sprite_sheet, level_coordinates, key_zones, enemies):
        self.level_number = level_number
        self.map = LevelMap(**level_map)
        self.level_sprite_sheet = LevelSpriteSheet(**level_sprite_sheet)
        self.coordinates = LevelCoordinates(**level_coordinates)
        self.key_zones = key_zones
        self.enemies_zones = enemies
