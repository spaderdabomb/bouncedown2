import arcade

from game_data import GameData
from globals import *
from Views import menu_views
from load_sprites import SpriteCache
from sound_manager import SoundManager


def main():
    GameData(SCREEN_TITLE)
    SpriteCache()
    GameData.data['player_level'] = 1
    GameData.data['player_xp'] = 0
    window = arcade.Window(int(SCREEN_WIDTH), int(SCREEN_HEIGHT), SCREEN_TITLE)
    sound_manager = SoundManager(window)
    loading_view = menu_views.LoadingMenuView(window, sound_manager)
    window.show_view(loading_view)
    arcade.run()


if __name__ == "__main__":
    main()
