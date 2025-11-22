"""
Game Constants
Contains all constant values used throughout the game
"""

# Screen Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 32

# Game Title
GAME_TITLE = "One Piece RPG: Pre-Grand Line"

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# UI Colors
UI_BG_COLOR = (20, 30, 50)
UI_BORDER_COLOR = (100, 150, 200)
UI_TEXT_COLOR = WHITE
UI_HIGHLIGHT_COLOR = (255, 215, 0)

# Game States
STATE_MENU = "menu"
STATE_CHAR_CREATION = "character_creation"
STATE_WORLD = "world"
STATE_BATTLE = "battle"
STATE_DIALOGUE = "dialogue"
STATE_INVENTORY = "inventory"
STATE_PARTY = "party"
STATE_SAVE_LOAD = "save_load"

# Character Stats
MAX_PARTY_SIZE = 4
STARTING_LEVEL = 1
MAX_LEVEL = 100

# Base Stats
BASE_HP = 100
BASE_ATTACK = 10
BASE_DEFENSE = 8
BASE_SPEED = 10
BASE_DF_POWER = 0  # Devil Fruit Power

# Combat
MAX_BATTLE_PARTY = 4
ENEMY_GROUP_MAX = 6

# Devil Fruit Types
DF_TYPE_NONE = "none"
DF_TYPE_PARAMECIA = "paramecia"
DF_TYPE_ZOAN = "zoan"
DF_TYPE_LOGIA = "logia"

# Paths
ASSETS_PATH = "assets/"
SPRITES_PATH = ASSETS_PATH + "sprites/"
MAPS_PATH = ASSETS_PATH + "maps/"
AUDIO_PATH = ASSETS_PATH + "audio/"
FONTS_PATH = ASSETS_PATH + "fonts/"
DATA_PATH = "data/"
SAVES_PATH = "saves/"

# File Names
DEVIL_FRUITS_DATA = DATA_PATH + "devil_fruits.json"
ITEMS_DATA = DATA_PATH + "items.json"
CHARACTERS_DATA = DATA_PATH + "characters.json"
ENEMIES_DATA = DATA_PATH + "enemies.json"
QUESTS_DATA = DATA_PATH + "quests.json"
DIALOGUE_DATA = DATA_PATH + "dialogue.json"

# Movement
PLAYER_SPEED = 4

# Currencies
CURRENCY_NAME = "Berries"
STARTING_BERRIES = 1000
