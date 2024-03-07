class LevelMap:
    def __init__(self, border_map_path, tile_map_path, objects_map_path):
        self.border_map_path = border_map_path
        self.tile_map_path = tile_map_path
        self.objects_map_path = objects_map_path


class LevelSpriteSheet:
    def __init__(self, path, columns, rows):
        self.path = path
        self.columns = columns
        self.rows = rows


class LevelCoordinates:
    def __init__(self, player_initial_x, player_initial_y, key_x, key_y, exit_x, exit_y):
        self.player_initial_x = player_initial_x
        self.player_initial_y = player_initial_y
        self.key_x = key_x
        self.key_y = key_y
        self.exit_x = exit_x
        self.exit_y = exit_y


class Level:
    def __init__(self, level_number, level_map, level_sprite_sheet, level_coordinates, enemies):
        self.level_number = level_number
        self.map = LevelMap(**level_map)
        self.level_sprite_sheet = LevelSpriteSheet(**level_sprite_sheet)
        self.coordinates = LevelCoordinates(**level_coordinates)
        self.enemies_zones = enemies
