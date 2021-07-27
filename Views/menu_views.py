from __future__ import annotations

import arcade
import arcade.gui
from arcade.gui.ui_style import UIStyle
import threading

import py_gjapi

from globals import *
from load_sprites import SpriteCache
from sound_manager import SoundManager
from Views import game_scene
from game_data import GameData
from Utils.gui import TextLineEdit


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass


class SettingsMenuView(arcade.View):
    def __init__(self, window: arcade.Window, sound_manager: SoundManager):
        super().__init__()

        self.window = window
        self.sound_manager = sound_manager
        self.ui_manager = arcade.gui.UIManager(window)
        self.ui_manager.push_handlers(self.on_ui_event)

        self.setup()

    def setup(self):
        self.ui_manager.purge_ui_elements()

        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.settings_menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'menu_settings.png'), RESOLUTION_SCALING)
        self.settings_menu_background.center_x = SCREEN_WIDTH/2
        self.settings_menu_background.center_y = SCREEN_HEIGHT/2

        # Setup buttons
        self.back_button = self.ui_manager.add_ui_element(SpriteCache.BACK_SETTINGS)

    def on_ui_event(self, event: arcade.gui.UIEvent):
        if event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'back_button':
            self.sound_manager.play_sound(0)
            self.ui_manager.purge_ui_elements()
            start_menu_view = StartMenuView(self.window, self.sound_manager)
            self.window.show_view(start_menu_view)

    def on_draw(self):
        arcade.start_render()
        self.settings_menu_background.draw()

    def on_update(self, dt):
        self.sound_manager.update()


class AchievementsMenuView(arcade.View):
    def __init__(self, window: arcade.Window, sound_manager: SoundManager):
        super().__init__()

        self.window = window
        self.sound_manager = sound_manager
        self.ui_manager = arcade.gui.UIManager(window)
        self.ui_manager.push_handlers(self.on_ui_event)

        self.setup()

    def setup(self):
        self.ui_manager.purge_ui_elements()

        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.achievements_menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'menu_achievements.png'), RESOLUTION_SCALING)
        self.achievements_menu_background.center_x = SCREEN_WIDTH / 2
        self.achievements_menu_background.center_y = SCREEN_HEIGHT / 2

        # Setup buttons
        self.back_button = self.ui_manager.add_ui_element(SpriteCache.BACK_SETTINGS)

    def on_ui_event(self, event: arcade.gui.UIEvent):
        if event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'back_button':
            self.sound_manager.play_sound(0)
            self.ui_manager.purge_ui_elements()
            start_menu_view = StartMenuView(self.window, self.sound_manager)
            self.window.show_view(start_menu_view)

    def on_draw(self):
        arcade.start_render()
        self.achievements_menu_background.draw()

    def on_update(self, dt):
        self.sound_manager.update()


class HighscoresMenuView(arcade.View):
    def __init__(self, window: arcade.Window, sound_manager: SoundManager):
        super().__init__()

        self.window = window
        self.sound_manager = sound_manager
        self.ui_manager = arcade.gui.UIManager(window)
        self.ui_manager.push_handlers(self.on_ui_event)

        self._init_vars()
        self._init_UI()
        self._init_buttons()

    def _init_vars(self):
        self.my_scores_active = False
        self.best_each_active = False
        self.all_time_best_active = True

        self.all_time_highscores_list = py_gjapi.GameJoltTrophy(GameData.data['username'], 'token', '633226',
                                                                '93e6356d3b7a552047844a2e250b7fb1')

        highscores = self.all_time_highscores_list.fetchScores(table_id=641423)
        self.best_each_highscores_list = []
        self.best_each_usernames_list = []
        for entry in highscores['scores']:
            self.best_each_highscores_list.append(int(entry['sort']))
            self.best_each_usernames_list.append(entry['guest'])

        highscores = self.all_time_highscores_list.fetchScores(table_id=641427)
        self.all_time_scores_list = []
        self.all_time_usernames_list = []
        for entry in highscores['scores']:
            self.all_time_scores_list.append(int(entry['sort']))
            self.all_time_usernames_list.append(entry['guest'])

    def _init_UI(self):
        # Setup background
        arcade.set_background_color(arcade.color.WHITE)
        self.highscores_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'menu_highscores.png'), RESOLUTION_SCALING)
        self.highscores_background.center_x = SCREEN_WIDTH / 2
        self.highscores_background.center_y = SCREEN_HEIGHT / 2
        self.top10_scores, self.top10_names = GameData.sort_highscores()

    def _init_buttons(self):
        self.back_button = self.ui_manager.add_ui_element(SpriteCache.BACK_SETTINGS)

        pos1_x = 698 * RESOLUTION_SCALING
        pos2_x = SCREEN_WIDTH / 2
        pos3_x = 1223 * RESOLUTION_SCALING
        pos1_y = (1080-750) * RESOLUTION_SCALING

        self.my_scores_button = self.ui_manager.add_ui_element(arcade.gui.UIImageButton(
            center_x=pos1_x,
            center_y=pos1_y,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_my_scores_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_my_scores_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_my_scores_clicked.png')),
            text='',
            id='my_scores_button'
        ))

        self.best_each_button = self.ui_manager.add_ui_element(arcade.gui.UIImageButton(
            center_x=pos2_x,
            center_y=pos1_y,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_best_each_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_best_each_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_best_each_clicked.png')),
            text='',
            id='best_each_button'
        ))

        self.all_scores_button = self.ui_manager.add_ui_element(arcade.gui.UIImageButton(
            center_x=pos3_x,
            center_y=pos1_y,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_all_scores_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_all_scores_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_all_scores_clicked.png')),
            text='',
            id='all_scores_button'
        ))


    def on_draw(self):
        arcade.start_render()
        self.highscores_background.draw()

        # Draw UI headers
        pos1_x = 680*RESOLUTION_SCALING
        pos2_x = 820*RESOLUTION_SCALING
        pos3_x = 1260*RESOLUTION_SCALING
        pos1_y = (1080-290)*RESOLUTION_SCALING
        arcade.draw_text('Rank', pos1_x, pos1_y, arcade.color.WHITE, font_size=24, align="center", anchor_x="right")
        arcade.draw_text('Username', pos2_x, pos1_y, arcade.color.WHITE, font_size=24, align="center", anchor_x="left")
        arcade.draw_text('Score', pos3_x, pos1_y, arcade.color.WHITE, font_size=24, align="center", anchor_x="right")

        # Draw scores and names
        if self.my_scores_active:
            for i in range(len(self.top10_scores)):
                score = self.top10_scores[i]
                username = self.top10_names[i]
                spacing = 40 * RESOLUTION_SCALING
                pos1_x = 680 * RESOLUTION_SCALING
                pos2_x = 820 * RESOLUTION_SCALING
                pos3_x = 1260 * RESOLUTION_SCALING
                pos1_y = (1080 - 197 - spacing - 100) * RESOLUTION_SCALING - i * spacing

                arcade.draw_text(str(i + 1) + ".", pos1_x, pos1_y, arcade.color.WHITE, font_size=22, align="center", anchor_x="right")
                arcade.draw_text(username, pos2_x, pos1_y, arcade.color.WHITE, font_size=22, align='center', anchor_x="left")
                arcade.draw_text(str(score), pos3_x, pos1_y, arcade.color.WHITE, font_size=22, align='center', anchor_x="right")
                if i >= 9: break
        elif self.best_each_active:
            for i in range(len(self.best_each_highscores_list)):
                score = self.best_each_highscores_list[i]
                username = self.best_each_usernames_list[i]
                spacing = 40 * RESOLUTION_SCALING
                pos1_x = 680 * RESOLUTION_SCALING
                pos2_x = 820 * RESOLUTION_SCALING
                pos3_x = 1260 * RESOLUTION_SCALING
                pos1_y = (1080 - 197 - spacing - 100) * RESOLUTION_SCALING - i * spacing

                arcade.draw_text(str(i + 1) + ".", pos1_x, pos1_y, arcade.color.WHITE, font_size=22, align="center", anchor_x="right")
                arcade.draw_text(username, pos2_x, pos1_y, arcade.color.WHITE, font_size=22, align="center", anchor_x="left")
                arcade.draw_text(str(score), pos3_x, pos1_y, arcade.color.WHITE, font_size=22, align="center", anchor_x="right")
                if i >= 9: break
        elif self.all_time_best_active:
            for i in range(len(self.all_time_scores_list)):
                score = self.all_time_scores_list[i]
                username = self.all_time_usernames_list[i]
                spacing = 40 * RESOLUTION_SCALING
                pos1_x = 680 * RESOLUTION_SCALING
                pos2_x = 820 * RESOLUTION_SCALING
                pos3_x = 1260 * RESOLUTION_SCALING
                pos1_y = (1080 - 197 - spacing - 100) * RESOLUTION_SCALING - i*spacing

                arcade.draw_text(str(i + 1) + ".", pos1_x, pos1_y, arcade.color.WHITE, font_size=22, align="center", anchor_x="right")
                arcade.draw_text(username, pos2_x, pos1_y, arcade.color.WHITE, font_size=22, align="center", anchor_x="left")
                arcade.draw_text(str(score), pos3_x, pos1_y, arcade.color.WHITE, font_size=22, align="center", anchor_x="right")
                if i >= 9: break

    def on_update(self, dt):
        pass

    def on_ui_event(self, event: arcade.gui.UIEvent):
        if event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'back_button':
            self.sound_manager.play_sound(0)
            self.ui_manager.purge_ui_elements()
            start_menu_view = StartMenuView(self.window, self.sound_manager)
            self.window.show_view(start_menu_view)
        elif event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'my_scores_button':
            self.my_scores_active = True
            self.best_each_active = False
            self.all_time_best_active = False
        elif event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'best_each_button':
            self.my_scores_active = False
            self.best_each_active = True
            self.all_time_best_active = False
        elif event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'all_scores_button':
            self.my_scores_active = False
            self.best_each_active = False
            self.all_time_best_active = True


class StartMenuView(arcade.View):
    def __init__(self, window: arcade.Window, sound_manager: SoundManager):
        super().__init__()

        self.window = window
        self.sound_manager = sound_manager
        self.ui_manager = arcade.gui.UIManager(window)
        self.ui_manager.push_handlers(self.on_ui_event)

        self.setup()

    def setup(self):
        self.ui_manager.purge_ui_elements()

        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.start_menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'bouncedown_mainmenu.png'), RESOLUTION_SCALING)
        self.start_menu_background.center_x = SCREEN_WIDTH/2
        self.start_menu_background.center_y = SCREEN_HEIGHT/2

        # Setup buttons
        self.settings_button = self.ui_manager.add_ui_element(SpriteCache.SETTINGS_BUTTON)
        self.achievements_button = self.ui_manager.add_ui_element(SpriteCache.ACHIEVEMENTS_BUTTON)
        self.highscores_button = self.ui_manager.add_ui_element(SpriteCache.HIGHSCORES_BUTTON)
        self.start_button = self.ui_manager.add_ui_element(SpriteCache.START_BUTTON)

    def on_ui_event(self, event: arcade.gui.UIEvent):
        if event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'settings_button':
            self.sound_manager.play_sound(0)
            self.ui_manager.purge_ui_elements()
            settings_menu_view = SettingsMenuView(self.window, self.sound_manager)
            self.window.show_view(settings_menu_view)
        elif event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'achievements_button':
            self.sound_manager.play_sound(0)
            self.ui_manager.purge_ui_elements()
            achievements_menu_view = AchievementsMenuView(self.window, self.sound_manager)
            self.window.show_view(achievements_menu_view)
        elif event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'highscores_button':
            self.sound_manager.play_sound(0)
            self.ui_manager.purge_ui_elements()
            highscores_menu_view = HighscoresMenuView(self.window, self.sound_manager)
            self.window.show_view(highscores_menu_view)
        elif event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'start_button':
            self.sound_manager.play_sound(0)
            self.ui_manager.purge_ui_elements()
            game_scene_view = game_scene.GameSceneView(self.window, self.sound_manager)
            self.window.show_view(game_scene_view)

    def on_draw(self):
        arcade.start_render()
        self.start_menu_background.draw()

    def on_update(self, dt):
        self.sound_manager.update()


class LoadingMenuView(arcade.View):
    def __init__(self, window: arcade.Window, sound_manager: SoundManager):
        super().__init__()

        self.window = window
        self.sound_manager = sound_manager
        self.loading_index = 0

        self.done = False

        self.setup()

    def setup(self):
        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.loading_menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'menu_loading.png'), RESOLUTION_SCALING)
        self.loading_menu_background.center_x = SCREEN_WIDTH / 2
        self.loading_menu_background.center_y = SCREEN_HEIGHT / 2

        self.loading_screen_container = arcade.Sprite(os.path.join(SPRITES_PATH, 'loading_screen_container.png'), RESOLUTION_SCALING)
        self.loading_screen_container.center_x = SCREEN_WIDTH / 2
        self.loading_screen_container.center_y = (1080-598)*RESOLUTION_SCALING
        self.loading_screen_container_color = (45, 221, 99)

        t = threading.Thread(target=self.sprite_cache)
        t.start()

    def on_draw(self):
        arcade.start_render()
        self.loading_menu_background.draw()

        if SpriteCache.FILE_INDEX == 0:
            width = 0
        else:
            width = self.loading_screen_container.width * SpriteCache.FILE_INDEX / 40 - 24 * RESOLUTION_SCALING
        height = self.loading_screen_container.height - 18*RESOLUTION_SCALING
        x = self.loading_screen_container.center_x - self.loading_screen_container.width/2 + width/2 + 6*RESOLUTION_SCALING
        y = self.loading_screen_container.center_y
        arcade.draw_rectangle_filled(x, y, width, height, self.loading_screen_container_color)

        self.loading_screen_container.draw()


    def on_update(self, dt):
        if SpriteCache.FILE_INDEX >= 200:
            start_menu_view = StartMenuView(self.window, self.sound_manager)
            self.window.show_view(start_menu_view)

    def sprite_cache(self):
        SpriteCache()


class SubmitHighscoresView(arcade.View):
    def __init__(self, window: arcade.Window, sound_manager: SoundManager, final_score: int):
        super().__init__()

        self.window = window
        self.sound_manager = sound_manager
        self.ui_manager = arcade.gui.UIManager(window)
        self.ui_manager.push_handlers(self.on_ui_event)

        self.final_score = final_score

    def on_show(self):
        self._init_UI()
        self._init_buttons()

    def _init_UI(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.highscores_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'submit_score_menu.png'), RESOLUTION_SCALING)
        self.highscores_background.center_x = SCREEN_WIDTH/2
        self.highscores_background.center_y = SCREEN_HEIGHT/2

    def _init_buttons(self):
        # Setup themes
        self.back_button = arcade.gui.UIImageButton(
            center_x=772*RESOLUTION_SCALING,
            center_y=(1080-588)*RESOLUTION_SCALING,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_back_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_back_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_back_clicked.png')),
            text=' ',
            id='back_button'
        )

        self.submit_score_button = arcade.gui.UIImageButton(
            center_x=1095*RESOLUTION_SCALING,
            center_y=(1080-588)*RESOLUTION_SCALING,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_submit_score_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_submit_score_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_submit_score_clicked.png')),
            text=' ',
            id='submit_score_button'
        )

        self.ui_manager.add_ui_element(self.back_button)
        self.ui_manager.add_ui_element(self.submit_score_button)

        x = (SCREEN_WIDTH / 2) * RESOLUTION_SCALING
        y = (1080-485)*RESOLUTION_SCALING
        width = 491*RESOLUTION_SCALING
        height = 78*RESOLUTION_SCALING
        self.dialogue_box = TextLineEdit(x, y, width, height, outline_color=arcade.color.WHITE, background_color=(0, 0, 0, 100))
        self.dialogue_box.text_label.color = (255, 255, 255)
        self.dialogue_box.placeholder_text.color = (255, 255, 255, 100)
        self.dialogue_box.cursor_color = arcade.color.WHITE
        self.dialogue_box.placeholder_text.text = "Username"

    def on_draw(self):
        arcade.start_render()
        self.highscores_background.draw()
        self.dialogue_box.draw()

    def on_update(self, dt):
        self.dialogue_box.update(dt)

    def on_ui_event(self, event: arcade.gui.UIEvent):
        if event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'back_button':
            self.sound_manager.play_sound(0)
            self.ui_manager.purge_ui_elements()
            start_menu_view = StartMenuView(self.window, self.sound_manager)
            self.window.show_view(start_menu_view)
        elif event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'submit_score_button':
            if not self.dialogue_box.text_label.text == '':
                GameData.data['username'] = self.dialogue_box.text_label.text
                GameData.add_highscore_entry(self.final_score)
                GameData.save_data()
                print(GameData.data)

                self.sound_manager.play_sound(0)
                self.ui_manager.purge_ui_elements()
                start_menu_view = HighscoresMenuView(self.window, self.sound_manager)
                self.window.show_view(start_menu_view)

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)
        self.dialogue_box.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        super().on_key_release(symbol, modifiers)
        self.dialogue_box.on_key_release(symbol, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        self.dialogue_box.on_mouse_press(x, y)

