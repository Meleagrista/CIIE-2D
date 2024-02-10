# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                      GLOBAL VARIABLES                                         #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

# ####################################################################### #
#                             ENTITY CONSTANTS                            #
# ####################################################################### #

NPC_SIZE = 10  # Represents the size of the entity's visual representation (square).
NPC_ANGLE = 90.0  # Represents the initial angle in degrees for all enemy entities.
VIEW_OFFSET = 2.5  # Represents the offset value for the entity's directional indicator (triangle), indicating its orientation.

# ####################################################################### #
#                               MAP CONSTANTS                             #
# ####################################################################### #

GRID_SIZE = 35  # Represents the number of squares in the grid.
SQUARE_SIZE = 20  # Represents the size of each square in pixels on the grid.
MAP = 'map/map-files/map-1.txt'  # Represents the path to the file containing the map information.
GRID_SHOW = False  # Represents whether the grid lines are shown on the screen.

# ####################################################################### #
#                              PYGAME CONSTANTS                           #
# ####################################################################### #

FPS = 60  # Represents the refresh rate (frames per second) for the loop.

# ####################################################################### #
#                               MENU CONSTANTS                            #
# ####################################################################### #

MENU_FONT = 50  # Represents the font size for menu items.
CREDITS_FONT = 20  # Represents the font size for credits.
TITLE_FONT = 52  # Represents the font size for the title.
FONT_COLOR = "white"  # Represents the color of the text font.
CREDITS = (
    "Contornos Inmersivos, Interactivos e de Entretemento\n"
    "Grao en Enxenería Informática\n"
    "Universidade da Coruña\n"
    "Authors:\n"
    "Martín do Río Rico\n"
    "Yago Fernández Rego\n"
    "David García Ramallal\n"
    "Pelayo Vieites Pérez"
)  # Represents the credits information.