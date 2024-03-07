# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATHS TO FOLDERS                                       #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
from game.sprites.spritesheet import SpriteSheet

MENU_ASSETS = "assets/menu_assets/"

IMAGES_BACKGROUND = "assets/images/backgrounds/"
IMAGES_BUTTONS = "assets/images/icons/"
MUSIC_PATH = "assets/music/"
SOUNDS_PATH = "assets/sounds/"
CHARACTERS_PATH = "assets/characters/"

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATH TO GUI ELEMENTS                                   #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

SPLASH_IMAGE = MENU_ASSETS + 'desert.jpg'
BACKGROUND_IMAGE = MENU_ASSETS + 'desert-city.png'

POPUP_IMAGE = IMAGES_BACKGROUND + 'popup_img.png'
POPUP_IMAGE_PAUSE = IMAGES_BACKGROUND + 'popup_img_pause.png'
POPUP_IMAGE_DEATH = IMAGES_BACKGROUND + 'popup_img_death.png'

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

buttons = SpriteSheet(MENU_ASSETS + 'ui_white.png', 10, 9, 80, 80)

BUTTON_PLAY = buttons.get_sprite_by_number(85)
BUTTON_CONFIGURATION = buttons.get_sprite_by_number(75)
BUTTON_CREDITS = buttons.get_sprite_by_number(78)
BUTTON_EXIT = buttons.get_sprite_by_number(76)
BUTTON_BACK = buttons.get_sprite_by_number(80)
BUTTON_ARROWS = buttons.get_sprite_by_number(70)
BUTTON_WASD = buttons.get_sprite_by_number(72)

SWITCH_ON = buttons.get_sprite_by_number(70)
SWITCH_OFF = buttons.get_sprite_by_number(72)

flags = SpriteSheet(MENU_ASSETS + 'flags.png', 11, 5, 68, 68)

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
DETECTED_SOUND = SOUNDS_PATH + 'sonar-ping-95840.mp3'
INCREASE_HEALTH_SOUND = SOUNDS_PATH + 'arcade-heal-48183.mp3'

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PATH TO SPRITE SHEETS                                  #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

SHEET_CHARACTER = CHARACTERS_PATH + 'character_template-Sheet.png'
COORDINATES_CHARACTER = CHARACTERS_PATH + 'character_coordinates.txt'
