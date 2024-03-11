# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATHS TO FOLDERS                                       #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
from game.sprites.spritesheet import SpriteSheet

MENU_ASSETS = "assets/menu_assets/"

IMAGES_BACKGROUND = "assets/menu_assets/images/backgrounds/"
IMAGES_BUTTONS = "assets/menu_assets/images/icons/"
MUSIC_PATH = "assets/music/"
SOUNDS_PATH = "assets/sounds/"
CHARACTERS_PATH = "assets/characters_assets/characters/"
SPRITES_PATH = "assets/sprites/"

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATHS TO SPRITES                                       #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

UI_ASSETS = 'assets/ui_assets/ui-x3.png'
UI_ICONS = MENU_ASSETS + 'ui_white.png'

CHARACTER_ASSETS = 'assets/character_assets/players-red-x3.png'
ENEMY_ASSETS = 'assets/character_assets/enemies-x3.png'


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATH TO GUI ELEMENTS                                   #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

SPLASH_IMAGE = MENU_ASSETS + 'desert.jpg'
BACKGROUND_IMAGE = MENU_ASSETS + 'desert-city.png'
TITLE_IMAGE = MENU_ASSETS + 'title.png'
WASD_IMAGE = MENU_ASSETS + 'wasd.png'
ARROWS_IMAGE = MENU_ASSETS + 'arrows.png'

POPUP_IMAGE = IMAGES_BACKGROUND + 'popup_img.png'
POPUP_IMAGE_PAUSE = IMAGES_BACKGROUND + 'popup_img_pause_trans.png'
POPUP_IMAGE_DEATH = IMAGES_BACKGROUND + 'popup_img_death_trans.png'
POPUP_IMAGE_LEVEL = IMAGES_BACKGROUND + 'popup_img_level_trans.png'
POPUP_IMAGE_FINISHED = IMAGES_BACKGROUND + 'popup_img_finished_trans.png'

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATH TO MUSIC ELEMENTS                                 #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

MUSIC_FALL_FROM_GRACE = MUSIC_PATH + 'fall-from-grace.mp3'
MUSIC_MEDIEVAL = MUSIC_PATH + 'Medieval-Fantasy(chosic.com).mp3'
MUSIC_BACKGROUND = MUSIC_PATH + 'Black-Silent-Fear(chosic.com).mp3'

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATH TO FONT ELEMENTS                                  #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

FONT_PATH = "assets/fonts_assets/"
FONT = FONT_PATH + 'pixel-tactical.ttf'

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATH TO GUI BUTTONS                                    #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

buttons = SpriteSheet(MENU_ASSETS + 'ui_white.png', 10, 9, 80)

BUTTON_PLAY = buttons.get_sprite_by_number(85)
BUTTON_CONFIGURATION = buttons.get_sprite_by_number(75)
BUTTON_CREDITS = buttons.get_sprite_by_number(78)
BUTTON_EXIT = buttons.get_sprite_by_number(76)
BUTTON_BACK = buttons.get_sprite_by_number(80)
BUTTON_ARROWS = 'assets/menu_assets/arrows.png'
BUTTON_WASD = 'assets/menu_assets/wasd.png'

SWITCH_ON = buttons.get_sprite_by_number(40)
SWITCH_OFF = buttons.get_sprite_by_number(42)

flags = SpriteSheet(MENU_ASSETS + 'flags.png', 11, 5, 68)

SPAIN = flags.get_sprite_by_number(21)
UNITED_KINGDOM = flags.get_sprite_by_number(1)
FRAME = buttons.get_sprite_by_number(70)

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATH TO ICONS ELEMENTS                                 #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

KEYS_IMG = IMAGES_BUTTONS + 'key.png'

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATH TO SOUND ELEMENTS                                 #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

MOVEMENT_SOUND = SOUNDS_PATH + 'concrete-footsteps-6752.mp3'
PICK_UP_KEY_SOUND = SOUNDS_PATH + 'interface-124464.mp3'
FINISH_LEVEL_SOUND = SOUNDS_PATH + 'positive-notification-new-level-152480.mp3'
DEATH_SOUND = SOUNDS_PATH + 'piano-crash-sound-37898.mp3'
DETECTED_SOUND = SOUNDS_PATH + 'beep-warning-6387.mp3'
INCREASE_HEALTH_SOUND = SOUNDS_PATH + 'arcade-heal-48183.mp3'

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATH TO SPRITE SHEETS                                  #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

SHEET_CHARACTER = CHARACTERS_PATH + 'character_template-Sheet.png'
COORDINATES_CHARACTER = CHARACTERS_PATH + 'character_coordinates.txt'
KEYS_GREY_SHEET = SPRITES_PATH + 'Key_8_GREY_Spritesheet.png'
KEYS_SILVER_SHEET = SPRITES_PATH + 'Key_8_SILVER_Spritesheet.png'
KEYS_GOLD_SHEET = SPRITES_PATH + 'Key_8_GOLD_Spritesheet.png'
COORDINATES_KEYS = SPRITES_PATH + 'keys_coordinates.txt'
