from typing import Tuple, Dict, Optional, Union
import arcade
from arcade import key
import numpy as np
import subprocess

from Utils.core import *

SHIFT_SYMBOL_DICT = {"1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(",
                     "0": ")", "`": "~", "-": "_", "=": "+", "[": "{", "]": "}", "\\": "|", ";": ":", "'": "\"",
                     ",": "<", ".": ">", "/": "?"}


class Theme:
    DEFAULT_FONT_COLOR = arcade.color.BLACK
    DEFAULT_FONT_SIZE = 24
    DEFAULT_FONT_NAME = ('Calibri', 'Arial')

    def __init__(self):
        self.button_textures: Dict[str, Optional['', arcade.Texture]] =\
            {'normal': '', 'hover': '', 'clicked': '', 'locked': '', }
        self.menu_texture = ""
        self.window_texture = ""
        self.dialogue_box_texture = ""
        self.text_box_texture = ""
        self.font_color = self.__class__.DEFAULT_FONT_COLOR
        self.font_size = self.__class__.DEFAULT_FONT_SIZE
        self.font_name = self.__class__.DEFAULT_FONT_NAME

    def add_button_textures(self, normal, hover=None, clicked=None, locked=None):
        normal_texture = arcade.load_texture(normal)
        self.button_textures['normal'] = normal_texture

        self.button_textures['hover'] = arcade.load_texture(hover) \
            if hover is not None else normal_texture
        self.button_textures['clicked'] = arcade.load_texture(clicked) \
            if clicked is not None else normal_texture
        self.button_textures['locked'] = arcade.load_texture(locked) \
            if locked is not None else normal_texture

    def add_window_texture(self, window_texture):
        self.window_texture = arcade.load_texture(window_texture)

    def add_menu_texture(self, menu_texture):
        self.menu_texture = arcade.load_texture(menu_texture)

    def add_dialogue_box_texture(self, dialogue_box_texture):
        self.dialogue_box_texture = arcade.load_texture(dialogue_box_texture)

    def add_text_box_texture(self, text_box_texture):
        self.text_box_texture = arcade.load_texture(text_box_texture)

    def set_font(self, font_size, font_color, font_name=None):
        self.font_color = font_color
        self.font_size = font_size
        self.font_name = font_name \
            if font_name is not None \
            else self.__class__.DEFAULT_FONT_NAME


class TextButton:
    """ Text-based button """
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 text: str,
                 id: str,
                 theme: Theme,
                 scale=1.0,
                 font_size=18,
                 font_face: Union[str, Tuple[str, ...]] = "Arial", font_color=None,
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.text = text
        self.id = id
        self.scale = scale
        self.pressed = False
        self.hovering = False
        self.active = True
        self.button_height = button_height
        self.theme = theme
        self.font_color = font_color
        self.width = int(self.theme.button_textures['normal'].width*self.scale)
        self.height = int(self.theme.button_textures['normal'].height*self.scale)
        self.clicked = False
        if self.theme:
            self.normal_texture = self.theme.button_textures['normal']
            self.hover_texture = self.theme.button_textures['hover']
            self.clicked_texture = self.theme.button_textures['clicked']
            self.locked_texture = self.theme.button_textures['locked']
            self.font_size = self.theme.font_size
            self.font_name = self.theme.font_name
            self.font_color = self.theme.font_color
        else:
            self.font_size = font_size
            self.font_face = font_face
            self.face_color = face_color
            self.highlight_color = highlight_color
            self.shadow_color = shadow_color
            self.font_name = font_face
        if self.font_color is None:
            self.font_color = self.face_color

    def draw_color_theme(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

    def draw_texture_theme(self):
        if self.pressed:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.clicked_texture)
        elif self.hovering:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.hover_texture)
        else:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.normal_texture)

    def draw(self):
        """ Draw the button """
        if self.theme:
            self.draw_texture_theme()
        else:
            self.draw_color_theme()

        arcade.draw_text(self.text, self.center_x, self.center_y,
                         self.font_color, font_size=self.font_size,
                         font_name=self.font_name,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def on_mouse_press(self, x, y):
        x, y = get_scaled_mouse_coordinates(x, y)

        if x > self.center_x + self.width / 2:
            return
        if x < self.center_x - self.width / 2:
            return
        if y > self.center_y + self.height / 2:
            return
        if y < self.center_y - self.height / 2:
            return

        self.on_press()

    def on_mouse_release(self, x, y):
        x, y = get_scaled_mouse_coordinates(x, y)

        if (
                x > self.center_x + self.width / 2 or
                x < self.center_x - self.width / 2 or
                y > self.center_y + self.height / 2 or
                y < self.center_y - self.height / 2
        ):
            mouse_in_button = False
        else:
            mouse_in_button = True

        if self.pressed:
            self.on_release()
            if mouse_in_button:
                self.clicked = not self.clicked

        return self, mouse_in_button

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        x, y = get_scaled_mouse_coordinates(x, y)

        left_edge = self.center_x - self.width / 2
        right_edge = self.center_x + self.width / 2
        top_edge = self.center_y + self.height / 2
        bottom_edge = self.center_y - self.height / 2
        if left_edge < x < right_edge and bottom_edge < y < top_edge:
            self.hovering = True
        else:
            self.hovering = False


class CheckBox(TextButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 text: str,
                 id: str,
                 theme: Theme):

        super().__init__(center_x, center_y, text, id, theme)

    def draw_texture_theme(self):
        if self.clicked:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.clicked_texture)
        else:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.normal_texture)



class SubmitButton(TextButton):
    def __init__(self, textbox, on_submit, x, y, width=100, height=40, text="submit", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.textbox = textbox
        self.on_submit = on_submit

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.on_submit()
            self.textbox.text_storage.text = ""
            self.textbox.text_display.text = ""


class DialogueBox:
    def __init__(self, x, y, width, height, color=None, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = False
        self.button_list = []
        self.text_list = []
        self.theme = theme
        if self.theme:
            self.texture = self.theme.dialogue_box_texture

    def on_draw(self):
        if self.active:
            if self.theme:
                arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
            else:
                arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
            for button in self.button_list:
                button.draw()
            for text in self.text_list:
                text.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_press(x, y)

    def on_mouse_release(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_release(x, y)


class TextLabel:
    def __init__(self, text, x, y, color=arcade.color.BLACK, font_size=22, anchor_x="center",
                 anchor_y="center", width: int = 0,
                 align="center",
                 font_name=('Calibri', 'Arial'),
                 bold: bool = False,
                 italic: bool = False, rotation=0):
        self.text = text
        self.center_x = x
        self.center_y = y
        self.color = color
        self.font_size = font_size
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.width = width
        self.align = align
        self.font_name = font_name
        self.bold = bold
        self.italic = italic
        self.rotation = rotation
        self.active = True

    def draw(self):
        arcade.draw_text(self.text, self.center_x, self.center_y, self.color, font_size=self.font_size,
                         anchor_x=self.anchor_x,
                         anchor_y=self.anchor_y,
                         width=self.width, align=self.align,
                         font_name=self.font_name, bold=self.bold,
                         italic=self.italic, rotation=self.rotation)


class TextDisplay:
    def __init__(self, x, y, width=300, height=40, outline_color=arcade.color.BLACK,
                 shadow_color=arcade.color.WHITE_SMOKE, highlight_color=arcade.color.WHITE, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outline_color = outline_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color
        self.highlighted = False
        self.text = ""
        self.left_text = ""
        self.right_text = ""
        self.symbol = "|"
        self.cursor_index = 0
        self.theme = theme
        if self.theme:
            self.texture = self.theme.text_box_texture
            self.font_size = self.theme.font_size
            self.font_color = self.theme.font_color
            self.font_name = self.theme.font_name
        else:
            self.texture = None
            self.font_size = 24
            self.font_color = arcade.color.BLACK
            self.font_name = ('Calibri', 'Arial')

    def draw_text(self):
        if self.highlighted:
            arcade.draw_text(self.text[:self.cursor_index] + self.symbol + self.text[self.cursor_index:],
                             self.x-self.width/2.1, self.y, self.font_color, font_size=self.font_size,
                             anchor_y="center", font_name=self.font_name)
        else:
            arcade.draw_text(self.text, self.x-self.width/2.1, self.y, self.font_color, font_size=self.font_size,
                             anchor_y="center", font_name=self.font_name)

    def color_theme_draw(self):
        if self.highlighted:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.highlight_color)
        else:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.shadow_color)
        self.draw_text()
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, self.outline_color, 2)

    def texture_theme_draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
        self.draw_text()

    def draw(self):
        if self.texture == "":
            self.color_theme_draw()
        else:
            self.texture_theme_draw()

    def on_press(self):
        self.highlighted = True

    def on_release(self):
        pass

    def check_mouse_press(self, x, y):
        if x > self.x + self.width / 2:
            self.highlighted = False
            return
        if x < self.x - self.width / 2:
            self.highlighted = False
            return
        if y > self.y + self.height / 2:
            self.highlighted = False
            return
        if y < self.y - self.height / 2:
            self.highlighted = False
            return
        self.on_press()

    def check_mouse_release(self, _x, _y):
        if self.highlighted:
            self.on_release()

    def update(self, _delta_time, text, symbol, cursor_index):
        self.text = text
        self.symbol = symbol
        self.cursor_index = cursor_index


class TextStorage:
    def __init__(self, box_width, font_size=24, theme=None):
        self.box_width = box_width
        self.font_size = font_size
        self.theme = theme
        if self.theme:
            self.font_size = self.theme.font_size
        self.char_limit = self.box_width / self.font_size
        self.text = ""
        self.cursor_index = 1
        self.cursor_symbol = "|"
        self.local_cursor_index = 0
        self.time = 0.0
        self.left_index = 0
        self.right_index = 1
        self.visible_text = ""

    def blink_cursor(self):
        seconds = self.time % 60
        if seconds > 0.1:
            if self.cursor_symbol == "_":
                self.cursor_symbol = "|"
            else:
                self.cursor_symbol = "_"
            self.time = 0.0

    def update(self, delta_time, key):
        self.time += delta_time
        # self.blink_cursor()
        if key:
            if key == arcade.key.BACKSPACE:
                if self.cursor_index < len(self.text):
                    text = self.text[:self.cursor_index-1]
                    self.text = text + self.text[self.cursor_index:]
                else:
                    self.text = self.text[:-1]
                if self.cursor_index > 0:
                    self.cursor_index -= 1
                if self.left_index > 0:
                    self.left_index -= 1
                if self.right_index > 1:
                    self.right_index -= 1
            elif key == arcade.key.LEFT:
                if self.cursor_index > 0:
                    self.cursor_index -= 1
                if 0 < self.left_index == self.cursor_index:
                    self.left_index -= 1
                    self.right_index -= 1
            elif key == arcade.key.RIGHT:
                if self.cursor_index < len(self.text):
                    self.cursor_index += 1
                if len(self.text) > self.right_index == self.cursor_index:
                    self.right_index += 1
                    self.left_index += 1
            else:
                if self.cursor_index < len(self.text):
                    self.text = self.text[:self.cursor_index] + chr(key) + self.text[self.cursor_index:]
                    self.cursor_index += 1
                    self.right_index += 1
                    if len(self.text) > self.char_limit:
                        self.left_index += 1
                else:
                    self.text += chr(key)
                    self.cursor_index += 1
                    self.right_index += 1
                    if len(self.text) >= self.char_limit:
                        self.left_index += 1
        self.visible_text = self.text[self.left_index:self.right_index]
        if self.cursor_index > self.left_index:
            self.local_cursor_index = self.cursor_index - self.left_index
        else:
            self.local_cursor_index = self.left_index
        return self.visible_text, self.cursor_symbol, self.local_cursor_index


class TextBox:
    def __init__(self, x, y, width=300, height=40, theme=None, outline_color=arcade.color.BLACK, font_size=24,
                 shadow_color=arcade.color.WHITE_SMOKE, highlight_color=arcade.color.WHITE):
        self.theme = theme
        if self.theme:
            self.text_display = TextDisplay(x, y, width, height, theme=self.theme)
            self.text_storage = TextStorage(width, theme=self.theme)
        else:
            self.text_display = TextDisplay(x, y, width, height, outline_color, shadow_color, highlight_color)
            self.text_storage = TextStorage(width, font_size)
        self.text = ""

    def draw(self):
        self.text_display.draw()

    def update(self, delta_time, key):
        if self.text_display.highlighted:
            self.text, symbol, cursor_index = self.text_storage.update(delta_time, key)
            self.text_display.update(delta_time, self.text, symbol, cursor_index)

    def check_mouse_press(self, x, y):
        self.text_display.check_mouse_press(x, y)

    def check_mouse_release(self, x, y):
        self.text_display.check_mouse_release(x, y)


class TextLineEdit:
    def __init__(self, center_x, center_y, width, height, outline_color=arcade.color.BLACK,
                 background_color=arcade.color.LIGHT_GRAY,
                 shadow_color=arcade.color.WHITE_SMOKE,
                 highlight_color=arcade.color.WHITE,
                 placeholder_text="Enter Text",
                 theme=None):
        super().__init__()

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.outline_color = outline_color
        self.background_color = background_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color

        self.text_label = TextLabel("", self.center_x, self.center_y, arcade.color.BLACK)
        self.placeholder_text = TextLabel("Enter Text", self.center_x, self.center_y, arcade.color.BLACK)
        self.placeholder_text.color = (0, 0, 0, 100)
        self.placeholder_text.italic = True

        self.left_padding = self.width / 10
        self.right_padding = self.width / 10
        self.top_padding = self.width / 10
        self.bottom_padding = self.width / 10

        self.cursor_symbol = "|"
        self.cursor_color = arcade.color.BLACK

        self._highlighted = False
        self._cursor_index = 0
        self._time = 0
        self._left_index = 0
        self._right_index = 1
        self._cursor_showing = True
        self._cursor_spacing_list = []
        self._time_before_key_repeat = 0.5
        self._time_since_key_press = 0
        self._key_repeat = False
        self._key_pressed_bool = False
        self._key_pressed = None
        self._modifiers_pressed = None
        self._caps_lock_on = False
        self._shift_pressed = False
        self._shift_last_key_pressed = False
        self._excluded_keys = [key.ENTER, key.LSHIFT, key.RSHIFT, key.RALT,
                               key.LALT, key.F1, key.F2, key.F3, key.F4, key.F5, key.F6, key.F7, key.F8, key.F9,
                               key.F10, key.F11, key.F12, key.F13, key.F14, key.F15, key.F16, key.UP, key.DOWN,
                               key.UP, key.DELETE, key.PAGEDOWN, key.PAGEUP, key.LCOMMAND, key.RCOMMAND, key.INSERT,
                               key.END, key.HOME, key.PRINT, key.SCROLLLOCK, key.PAUSE, key.TAB, key.CAPSLOCK,
                               key.ESCAPE, key.LCTRL, key.RCTRL, key.LWINDOWS, key.RWINDOWS, key.SCROLLLOCK, key.MENU]

        self.theme = theme
        if self.theme:
            self.texture = self.theme.text_box_texture
            self.font_size = self.theme.font_size
            self.font_color = self.theme.font_color
            self.font_name = self.theme.font_name
        else:
            self.texture = None
            self.font_size = 24
            self.font_color = arcade.color.BLACK
            self.font_name = ('Calibri', 'Arial')

        self.char_limit = np.floor(self.width / self.font_size)
        self.get_font_pixel_size()


    def draw(self):
        # Draw box
        if self.texture is None:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.background_color)
        else:
            pass

        # Draw text
        text_position_x = self.center_x + self.width / 2 - self.right_padding
        if self.text_label.text == "":
            text = arcade.draw_text(self.placeholder_text.text, text_position_x, self.center_y,
                                    self.placeholder_text.color,
                                    font_size=self.font_size, font_name=self.font_name,
                                    anchor_x="right", anchor_y="center")
            cursor_spacing = text.width / len(self.placeholder_text.text)
        else:
            text = arcade.draw_text(self.text_label.text, text_position_x, self.center_y, self.text_label.color,
                                    font_size=self.text_label.font_size, font_name=self.text_label.font_name,
                                    anchor_x="right", anchor_y="center")
            cursor_spacing = text.width / len(self.text_label.text)
        self.char_limit = np.floor((self.width - self.right_padding - self.left_padding) / cursor_spacing)

        # Draw Cursor
        total_character_lengths = sum(self._cursor_spacing_list[:self._cursor_index])
        cursor_position_x = self.center_x + self.width / 2 - total_character_lengths - self.right_padding
        if self._cursor_showing and self._highlighted:
            arcade.draw_text(self.cursor_symbol, cursor_position_x, self.center_y, self.cursor_color,
                             font_size=self.font_size, font_name=self.font_name, anchor_x="center", anchor_y="center")

    def update(self, delta_time):
        if self._highlighted:
            # Increase time constants if highlighted
            self._time += delta_time
            if self._key_pressed_bool and not self._shift_last_key_pressed:
                self._time_since_key_press += delta_time
            else:
                self._time_since_key_press = 0

            # Flash cursor
            if self._time*60 % 60 < 30:
                self._cursor_showing = True
            else:
                self._cursor_showing = False

            # Handle keys being held down
            if self._time_since_key_press > self._time_before_key_repeat:
                self._key_repeat = True
                if self._time_since_key_press*60 % 8 < 4:
                    self.handle_keypress_logic(self._key_pressed, self._modifiers_pressed)

        self.get_font_pixel_size()

    def handle_keypress_logic(self, key, mdifiers):
        # Handle special characters and modifiers
        key_str = str(chr(key))
        shift_modify_bool = (self._shift_pressed and key not in self._excluded_keys and
                             not key == arcade.key.DELETE and not key == arcade.key.BACKSPACE)
        if self._caps_lock_on:
            key_str = key_str.upper()
            if shift_modify_bool:
                if key_str.isalpha():
                    key_str = key_str.lower()
        elif shift_modify_bool:
            key_str = key_str.lower()
            if key_str.isalpha():
                key_str = key_str.upper()
            else:
                key_str = SHIFT_SYMBOL_DICT[key_str]

        if key == arcade.key.BACKSPACE:
            if self._cursor_index < len(self.text_label.text):
                self.text_label.text = self.text_label.text[:(len(self.text_label.text) - self._cursor_index - 1)] + \
                                       self.text_label.text[(len(self.text_label.text) - self._cursor_index):]
        elif key == arcade.key.DELETE:
            temp_text_length = len(self.text_label.text)
            start_index = len(self.text_label.text) - self._cursor_index
            stop_index = len(self.text_label.text) - self._cursor_index + 1
            if (self._cursor_index <= len(self.text_label.text)) and (not self._cursor_index == 0):
                self.text_label.text = self.text_label.text[:start_index] + self.text_label.text[stop_index:]
                self._cursor_index -= 1

        elif key == arcade.key.LEFT:
            if self._cursor_index < len(self.text_label.text):
                self._cursor_index += 1
        elif key == arcade.key.RIGHT:
            if self._cursor_index > 0:
                self._cursor_index -= 1
        elif (len(self.text_label.text) < self.char_limit) and (key not in self._excluded_keys):
            if self._cursor_index == 0:
                self.text_label.text += key_str
            elif self._cursor_index < len(self.text_label.text):
                self.text_label.text = self.text_label.text[:(len(self.text_label.text) - self._cursor_index)] + \
                                       key_str + \
                                       self.text_label.text[(len(self.text_label.text) - self._cursor_index):]
            elif self._cursor_index == len(self.text_label.text):
                self.text_label.text = key_str + self.text_label.text

    def on_key_press(self, key, modifiers):
        if self._highlighted:
            # Check modifiers
            if modifiers & arcade.key.MOD_SHIFT:
                self._shift_pressed = True
                if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                    self._shift_last_key_pressed = True
                else:
                    self._shift_last_key_pressed = False

            self._caps_lock_on = False
            if modifiers & arcade.key.MOD_CAPSLOCK:
                self._caps_lock_on = True

            # Check keys pressed
            self._key_pressed_bool = True
            self._key_pressed = key
            self._modifiers_pressed = modifiers
            self.handle_keypress_logic(key, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        if arcade.key.MOD_SHIFT:
            self._shift_pressed = False

        self._key_pressed_bool = False
        self._key_pressed = key
        self._modifiers_pressed = modifiers

    def on_mouse_press(self, x, y, button, modifiers):
        x, y = get_scaled_mouse_coordinates(x, y)

        if (self.center_x + self.width / 2 > x > self.center_x - self.width / 2 and
                self.center_y + self.height / 2 > y > self.center_y - self.height / 2):
            self._highlighted = True

            my_list = []
            for i in range(len(self._cursor_spacing_list)):
                my_list.append(sum(self._cursor_spacing_list[0:i]))

            if len(self._cursor_spacing_list) > 0:
                total_character_lengths = sum(self._cursor_spacing_list[:self._cursor_index])
                default_cursor_position = self.center_x + self.width / 2 - self.right_padding
                delta = default_cursor_position - x
                index = np.argmin(np.abs(np.array(my_list)-delta))
                self._cursor_index = index
        else:
            self._highlighted = False


    def get_font_pixel_size(self):
        self._cursor_spacing_list = [0 for i in range(len(self.text_label.text))]
        for i, character in enumerate(self.text_label.text, 0):
            text = arcade.draw_text(character, -100, self.center_y, (0, 0, 0, 0),
                             font_size=self.font_size, font_name=self.font_name, anchor_x="center", anchor_y="center")
            self._cursor_spacing_list[i] = text.width