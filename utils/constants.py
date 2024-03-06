# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                      GLOBAL VARIABLES                                         #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

# ####################################################################### #
#                             ENTITY CONSTANTS                            #
# ####################################################################### #

NPC_SIZE = 20  # Represents the size of the entity's visual representation (square).
NPC_ANGLE = 90.0  # Represents the initial angle in degrees for all enemy entities.
VIEW_OFFSET = 2.5  # Represents the offset value for the entity's directional indicator (triangle), indicating its orientation.
FIELD_OF_VISION = 60
REACH_OF_VISION = 6

# ####################################################################### #
#                               MAP CONSTANTS                             #
# ####################################################################### #

# GRID_SIZE = 35  # TODO: This must be deprecated, and use the size of the map.
GRID_BACKGROUND = (0, 0, 0)
SQUARE_SIZE = 20  # Represents the size of each square in pixels on the grid.
MAP = 'game/map/files/mapa_bueno_1_bordes.csv'  # Represents the path to the file containing the map information.
TILEMAP = 'game/map/files/mapa_bueno_1_tiles.csv'  # Represents the path to the file containing the tilemap information.
# MAP = 'game/map/files/map-100.txt'  # Represents the path to the file containing the map information.
GRID_SHOW = False  # Represents whether the grid lines are shown on the screen.

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

MENU_FONT = 50  # Represents the font size for menu items.
CREDITS_FONT = 20  # Represents the font size for credits.
TITLE_FONT = 52  # Represents the font size for the title.
FONT_COLOR = "white"  # Represents the color of the text font.
PAUSE_MENU_ID = "pause_menu"
DIE_MENU_ID = "die_menu"
CREDITS = (
    "Contornos Inmersivos, Interactivos e de Entretemento\n"
    "Grao en Enxenería Informática\n"
    "Universidade da Coruña\n"
    "Authors:\n"
    "Martín do Río Rico\n"
    "Yago Fernández Rego\n"
    "David García Ramallal\n"
    "Pelayo Vieites Pérez"
)  # Represents the credits' information.

# ####################################################################### #
#                               PATH CONSTANTS                            #
# ####################################################################### #

WEIGHT = 2

# ####################################################################### #
#                              PLAYER CONSTANTS                           #
# ####################################################################### #

FRICTION = 0.5
LIFE = 2

STOPPED = 0

TOTAL_MOVEMENT_SPRITES = 10
