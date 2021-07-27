"""
Sprite Change Coins

This shows how you can change a sprite once it is hit, rather than eliminate it.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_change_coins
"""

import random
import arcade
import arcade.gui
from arcade.gui import UIManager
import os
from globals import *
from load_sprites import SpriteCache

from Utils.gui import TextLineEdit

import numpy as np

SPRITE_SCALING = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Change Coins"


class MyGame(arcade.Window):
    """
    Main application class.a
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.ui_manager = UIManager()
        self.setup()

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)
        self.ui_manager.purge_ui_elements()

        # self.username_line_edit = arcade.gui.UIInputBox(center_x=SCREEN_WIDTH / 2,
        #                                                 center_y=SCREEN_HEIGHT / 2,
        #                                                 width=400,
        #                                                 height=100,
        #                                                 text='hello world')
        # self.username_line_edit.cursor_index = len(self.username_line_edit.text)
        # self.ui_manager.add_ui_element(self.username_line_edit)

        self.dialogue_box = TextLineEdit(200, 200, 500, 100, background_color=(0, 0, 0, 0))
        self.dialogue_box.text_label.color = (255, 255, 255)
        self.dialogue_box.placeholder_text.color = (255, 255, 255, 100)
        self.dialogue_box.cursor_color = arcade.color.WHITE
        self.dialogue_box.placeholder_text.text = "Username"

    def on_draw(self):
        arcade.start_render()
        # self.username_line_edit.draw()
        self.dialogue_box.draw()

    def on_update(self, delta_time):
        self.dialogue_box.update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)
        self.dialogue_box.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        super().on_key_release(symbol, modifiers)
        self.dialogue_box.on_key_release(symbol, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        self.dialogue_box.on_mouse_press(x, y)



def main():
    """ Main method """
    SpriteCache()
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()