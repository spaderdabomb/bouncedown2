import arcade
import arcade.gui
import time

from globals import *
from Utils.core import CounterClass


class SpriteCache:

    # Spritesheets

    # UI
    SETTINGS_BUTTON = None
    ACHIEVEMENTS_BUTTON = None
    HIGHSCORES_BUTTON = None
    START_BUTTON = None
    PLAY_BUTTON = None
    BACK_SETTINGS = None

    # Loading feedbakc
    FILE_INDEX = 0

    @staticmethod
    def __init__():

        a = time.time()
        SpriteCache._load_spritesheets()
        print('Spritesheet loading time:', time.time() - a)

        a = time.time()
        SpriteCache._load_textures()
        print('Textures loading time:', time.time() - a)

        a = time.time()
        SpriteCache._load_ui()
        print('UI loading time:', time.time() - a)

    @staticmethod
    def _load_spritesheets():
        index = CounterClass()

        pass

    @staticmethod
    def _load_textures():
        pass

    @staticmethod
    def _load_ui():
        x = SCREEN_WIDTH/2
        y = (1080 - 400)*RESOLUTION_SCALING
        spacing = 125*RESOLUTION_SCALING

        # Button normal/hover .pngs must be same size in order to work
        SpriteCache.SETTINGS_BUTTON = arcade.gui.UIImageButton(
            center_x=x,
            center_y=y,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_settings_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_settings_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_settings_clicked.png')),
            text=' ',
            id='settings_button'
        )

        # Button normal/hover .pngs must be same size in order to work
        SpriteCache.ACHIEVEMENTS_BUTTON = arcade.gui.UIImageButton(
            center_x=x,
            center_y=y - spacing,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_achievements_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_achievements_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_achievements_clicked.png')),
            text=' ',
            id='achievements_button'
        )

        # Button normal/hover .pngs must be same size in order to work
        SpriteCache.HIGHSCORES_BUTTON = arcade.gui.UIImageButton(
            center_x=x,
            center_y=y - spacing*2,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_highscores_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_highscores_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_highscores_clicked.png')),
            text=' ',
            id='highscores_button'
        )

        # Button normal/hover .pngs must be same size in order to work
        SpriteCache.START_BUTTON = arcade.gui.UIImageButton(
            center_x=x,
            center_y=y - 3*spacing,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_start_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_start_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_start_clicked.png')),
            text=' ',
            id='start_button'
        )

        x = SCREEN_WIDTH/2
        y = (1080 - 854)*RESOLUTION_SCALING
        SpriteCache.PLAY_BUTTON = arcade.gui.UIImageButton(
            center_x=x,
            center_y=spacing*3,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_play_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_play_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_play_clicked.png')),
            text=' ',
            id='play_button'
        )

        x = SCREEN_WIDTH/2
        y = (1080 - 400)*RESOLUTION_SCALING
        SpriteCache.BACK_SETTINGS = arcade.gui.UIImageButton(
            center_x=x,
            center_y=y - 3*spacing,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_back_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_back_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_back_clicked.png')),
            text=' ',
            id='back_button'
        )

        SpriteCache.FILE_INDEX = 200