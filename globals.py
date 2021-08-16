import os
import locale
import pyglet
from game_data import *

locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

MONITOR_DISPLAY = pyglet.canvas.Display()
SCREEN_DISPLAY = MONITOR_DISPLAY.get_default_screen()

RESOLUTION_SCALING = 1.0
SCREEN_SCALING = 0.85*SCREEN_DISPLAY.width / 1920
SCREEN_WIDTH = 1920*RESOLUTION_SCALING
SCREEN_HEIGHT = 1080*RESOLUTION_SCALING
SCREEN_WIDTH_SCALED = SCREEN_WIDTH*SCREEN_SCALING
SCREEN_HEIGHT_SCALED = SCREEN_HEIGHT*SCREEN_SCALING
SCREEN_BORDER_PADDING = 10*RESOLUTION_SCALING
FRAME_RATE = 60
SCREEN_TITLE = "Bouncedown_2"

GRAVITY = 0.25*RESOLUTION_SCALING
PLAYER_SCALE = 0.35*RESOLUTION_SCALING
PLATFORM_SCALE = 0.5

FILE_PATH = os.getcwd()
SPRITES_PATH = os.path.join(FILE_PATH, 'Assets', 'Sprites')
SPRITESHEETS_PATH = os.path.join(FILE_PATH, 'Assets', 'Spritesheets')
AUDIO_PATH = os.path.join(FILE_PATH, 'Assets', 'Audio')

ACHIEVEMENT_TEXT = ['Score {:n}'.format(GameData.data['achievements_scores'][0])+' points',
                    'Score {:n}'.format(GameData.data['achievements_scores'][1])+' points',
                    'Score {:n}'.format(GameData.data['achievements_scores'][2])+' points',
                    'Score a total of {:n}'.format(GameData.data['achievements_scores'][3])+' points',
                    'Score a total of {:n}'.format(GameData.data['achievements_scores'][4])+' points',
                    'Score a total of {:n}'.format(GameData.data['achievements_scores'][5])+' points',
                    'Break {:n}'.format(GameData.data['achievements_scores'][6])+' cloud platforms in a single game',
                    'Break {:n}'.format(GameData.data['achievements_scores'][7])+' cloud platforms in a single game',
                    'Break {:n}'.format(GameData.data['achievements_scores'][8])+' cloud platforms in a single game',
                    'Bounce on {:n}'.format(GameData.data['achievements_scores'][9])+' bouncy platforms in a single game',
                    'Bounce on {:n}'.format(GameData.data['achievements_scores'][10])+' bouncy platforms in a single game',
                    'Bounce on {:n}'.format(GameData.data['achievements_scores'][11])+' bouncy platforms in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][12])+' points while small in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][13])+' points while small in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][14])+' points while small in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][15])+' points while small in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][16])+' points while small in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][17])+' points while small in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][18])+' points as spiky splat in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][19])+' points as spiky splat in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][20])+' points as spiky splat in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][21])+' points as small, big and spiky splat in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][22])+' points as small, big and spiky splat in a single game',
                    'Score {:n}'.format(GameData.data['achievements_scores'][23])+' points as small, big and spiky splat in a single game']

ACHIEVEMENT_NAMES = ['Crowned Splat', 'Noble Splat', 'King Splat', '5k Splat', 'Marathon Splat', 'Iron Man Splat',
                     'Angel Splat', 'Heavenly Splat', 'Keanu Reeves', 'Pogo-splat', 'Kangaroo Splat', 'Zectron Splat',
                     'Molecular Splat', 'Atomic Splat', 'Quark Splat', 'Fatty-splatty', 'Hippopoto-splat', 'Jabba the Splat',
                     'Spiky Splat', 'Horned Devil', 'El Toro Asesino', 'Mega Splat', 'Giga Splat', 'Splega Splat']

ACHIEVEMENT_DROPDOWN_NAMES = ['Crowned\nSplat', 'Noble\nSplat', 'King\nSplat', '5k\nSplat', 'Marathon\nSplat', 'Iron Man\nSplat',
                     'Angel\nSplat', 'Heavenly\nSplat', 'Keanu\nReeves', 'Pogo-\nsplat', 'Kangaroo\nSplat', 'Zectron\nSplat',
                     'Molecular\nSplat', 'Atomic\nSplat', 'Quark\nSplat', 'Fatty-\nsplatty', 'Hippopoto-\nsplat', 'Jabba\nthe Splat',
                     'Spiky\nSplat', 'Horned\nDevil', 'El Toro\nAsesino', 'Mega\nSplat', 'Giga\nSplat', 'Splega\nSplat']


class Globals():
    '''
    Stores persistent data
    '''

    # Initializes data dictionary keys for saving and loading data

    @staticmethod
    def __init__(game_name):
        pass

