import os

RESOLUTION_SCALING = 1
SCREEN_WIDTH = 1920*RESOLUTION_SCALING
SCREEN_HEIGHT = 1080*RESOLUTION_SCALING
SCREEN_BORDER_PADDING = 10*RESOLUTION_SCALING
FRAME_RATE = 60
SCREEN_TITLE = "Bouncedown 2"

GRAVITY = 0.25


FILE_PATH = os.getcwd()
SPRITES_PATH = os.path.join(FILE_PATH, 'Assets', 'Sprites')
SPRITESHEETS_PATH = os.path.join(FILE_PATH, 'Assets', 'Spritesheets')
AUDIO_PATH = os.path.join(FILE_PATH, 'Assets', 'Audio')


class Globals():
    '''
    Stores persistent data
    '''

    # Initializes data dictionary keys for saving and loading data

    @staticmethod
    def __init__(game_name):
        pass

