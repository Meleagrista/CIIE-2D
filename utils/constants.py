# ####################################################################### #
#                             ENTITY CONSTANTS                            #
# ####################################################################### #

NPC_SIZE = 40  # Represents the size of the entity's visual representation (square).
NPC_ANGLE = 90.0  # Represents the initial angle in degrees for all enemy entities.
VIEW_OFFSET = 2.5  # Represents the offset value for the entity's directional indicator (triangle), indicating its orientation.
FIELD_OF_VISION = 90
REACH_OF_VISION = 5

# ####################################################################### #
#                               MAP CONSTANTS                             #
# ####################################################################### #

GRID_BACKGROUND = (0, 0, 0)
SQUARE_SIZE = 50  # Represents the size of each square in pixels on the grid.
MAP = 'game/map/files/mapa_bueno_1_bordes.csv'  # Represents the path to the file containing the map information.
TILE_MAP = 'game/map/files/mapa_bueno_1_tiles.csv'  # Represents the path to the file containing the tile map information.

FLOATING_TILES = [2, 8, 373, 374, 375, 376, 377, 1073, 1075, 1076, 1077, 1147, 1149, 1150, 1151, 1221, 1369, 1370]
GROUND_TILES = [69, 70, 71, 73, 106, 888, 889, 891, 892]
ANIMATED_TILES = [1110, 1073, 1147, 1184, 925, 858, 935, 999, 1000]
DOOR_TILES = [(i, i+1) for i in range(1443, 1466, 2)]
TILE_SCREEN = 1000
TILE_DOOR = [1295, 1296]

# ####################################################################### #
#                              PYGAME CONSTANTS                           #
# ####################################################################### #

FPS = 60  # Represents the refresh rate (frames per second) for the loop.

RED = (255, 0, 0)
PASTEL_RED = (255, 182, 193)  # This is a pastel shade of red
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# ####################################################################### #
#                               MENU CONSTANTS                            #
# ####################################################################### #

FONT_COLOR = (255, 255, 255)
TITLE_SIZE = 100
MENU_GAP = 100

TEXT_VERTICAL_CORRECTION = 1.1
BUTTON_VERTICAL_CORRECTION = 1
BUTTON_HORIZONTAL_CORRECTION = 18
MENU_LEFT = BUTTON_HORIZONTAL_CORRECTION + 80 + 18

FONT_SIZE = 60
FONT_PERCENT = 0.06


PAUSE_MENU_ID = "pause_menu"
DIE_MENU_ID = "die_menu"
LEVEL_MENU_ID = "level menu"
FINISHED_GAME_MENU_ID = "finished game menu"

# ####################################################################### #
#                               PATH CONSTANTS                            #
# ####################################################################### #

WEIGHT = 2

# ####################################################################### #
#                              PLAYER CONSTANTS                           #
# ####################################################################### #

FRICTION = 0.5
LIFE = 2
SPEED = 18
STOPPED = 0
TOTAL_MOVEMENT_SPRITES = 11
