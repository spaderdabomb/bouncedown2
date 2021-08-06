from __future__ import annotations

import arcade
import arcade.gui
from arcade.gui.ui_style import UIStyle
import threading
import locale
import time

import py_gjapi

from globals import *
from load_sprites import SpriteCache
from sound_manager import SoundManager
from Views import game_scene
from game_data import *
from Utils.gui import TextLineEdit, TextButton, Theme, TextLabel
from platforms import Platform, generate_platform_type_2

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass

locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'


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

        self._init_buttons()
        self._init_UI()

    def _init_buttons(self):
        self.ui_manager.purge_ui_elements()

        # Setup buttons
        self.back_button = SpriteCache.BACK_SETTINGS
        self.ui_manager.add_ui_element(self.back_button)

        self.achievement_button_list = []
        self.achievement_hovering_list = [False for i in range(NUM_ACHIEVEMENTS)]

        x_start = 685*RESOLUTION_SCALING
        y_start = (1080-290)*RESOLUTION_SCALING
        spacing_x = 110*RESOLUTION_SCALING
        spacing_y = 110*RESOLUTION_SCALING
        for i in range(NUM_ACHIEVEMENTS):
            x = x_start + spacing_x*(i % 6)
            y = y_start - spacing_y*(int(np.floor((i + 0.01) / 6) % 6))
            if i <= 9:
                index_str = '0'+str(i)
            else:
                index_str = str(i)
            achievement_holder_button = arcade.gui.UIImageButton(
                center_x=x,
                center_y=y,
                normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'achievement_holder.png')),
                text=' ',
                id='achievement_holder_button_' + index_str
            )
            achievement_holder_button.scale = RESOLUTION_SCALING
            self.ui_manager.add_ui_element(achievement_holder_button)
            self.achievement_button_list.append(achievement_holder_button)

    def _init_UI(self):
        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.achievements_menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'menu_achievements.png'), RESOLUTION_SCALING)
        self.achievements_menu_background.center_x = SCREEN_WIDTH / 2
        self.achievements_menu_background.center_y = SCREEN_HEIGHT / 2

        self.text_labels_list = []
        # self.achievement_labels_list = []
        # self.achievement_name_labels_list = []
        self.achievements_icon_list = []

        # Check for completed achievements
        achievements_completed = 0
        for i in range(len(GameData.data["achievements_complete"])):
            if GameData.data["achievements_complete"][i]:
                achievements_completed += 1

        # Style UILabel text
        UIStyle.default_style().set_class_attrs(
            'all_scores_button',
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.WHITE,
            font_color_press=arcade.color.WHITE,
            bg_color=(135, 21, 25),
            bg_color_hover=(135, 21, 25),
            bg_color_press=(122, 21, 24),
            border_color=(135, 21, 25),
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )

        # Create UILabel text
        text = "Completed Achievements: " + str(achievements_completed) + "/" + str(NUM_ACHIEVEMENTS)
        x = SCREEN_WIDTH / 2
        y = (1080-730)*RESOLUTION_SCALING
        self.achievements_completed_text_label = arcade.gui.UILabel(
            text,
            center_x=x,
            center_y=y,
            font_size=26,
            id='all_scores_button'
           )

        self.achievement_text_hoilder = arcade.Sprite(os.path.join(SPRITES_PATH, 'achievement_text_holder.png'), RESOLUTION_SCALING)
        self.achievement_text_hoilder.center_x = x
        self.achievement_text_hoilder.center_y = y

        # Achievement icons
        x_start = 685*RESOLUTION_SCALING
        y_start = (1080-290)*RESOLUTION_SCALING
        spacing_x = 110*RESOLUTION_SCALING
        spacing_y = 110*RESOLUTION_SCALING
        for i in range(NUM_ACHIEVEMENTS):
            x = x_start + spacing_x*(i % 6)
            y = y_start - spacing_y*(int(np.floor((i + 0.01) / 6) % 6))
            if i <= 9:
                index_str = '0'+str(i)
            else:
                index_str = str(i)
            if GameData.data['achievements_complete'][i]:
                path = os.path.join(SPRITES_PATH, "achievement_" + index_str + '.png')
            else:
                path = os.path.join(SPRITES_PATH, 'achievement_lock.png')
            achievement_icon = arcade.gui.UIImageButton(
                center_x=x,
                center_y=y,
                normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, path)),
                text=' ',
                id='achievement_icon_' + index_str
            )
            achievement_icon.scale = RESOLUTION_SCALING
            self.achievements_icon_list.append(achievement_icon)
            self.ui_manager.add_ui_element(achievement_icon)

    def on_ui_event(self, event: arcade.gui.UIEvent):
        if event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'back_button':
            self.sound_manager.play_sound(0)
            self.ui_manager.purge_ui_elements()
            start_menu_view = StartMenuView(self.window, self.sound_manager)
            self.window.show_view(start_menu_view)
        for i, button in enumerate(self.achievement_button_list):
            if button.hovered:
                pass
        for i, button in enumerate(self.achievements_icon_list):
            if button.hovered:
                pass

    def on_draw(self):
        arcade.start_render()
        self.achievements_menu_background.draw()
        self.achievement_text_hoilder.draw()


        currently_hovering = False
        for i in range(len(SpriteCache.ACHIEVEMENT_NAME_LABELS_LIST)):
            if self.achievement_hovering_list[i]:
                SpriteCache.ACHIEVEMENT_NAME_LABELS_LIST[i].draw()
                SpriteCache.ACHIEVEMENT_LABELS_LIST[i].draw()
                currently_hovering = True
            else:
                pass

        if not currently_hovering:
            self.achievements_completed_text_label.draw()


    def on_update(self, dt):
        self.sound_manager.update()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for i, button in enumerate(self.achievement_button_list):
            button_points = button.points
            if button_points[0][0] < x < button_points[1][0] and button_points[0][1] < y < button_points[3][1]:
                button.normal_texture = arcade.load_texture(os.path.join(SPRITES_PATH, 'achievement_holder_hover.png'))
                self.achievement_hovering_list[i] = True
            else:
                button.normal_texture = arcade.load_texture(os.path.join(SPRITES_PATH, 'achievement_holder.png'))
                self.achievement_hovering_list[i] = False


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

        self.my_scores_button = arcade.gui.UIImageButton(
            center_x=pos1_x,
            center_y=pos1_y,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_my_scores_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_my_scores_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_my_scores_clicked.png')),
            text='',
            id='my_scores_button'
        )
        self.my_scores_button.scale = RESOLUTION_SCALING
        self.ui_manager.add_ui_element(self.my_scores_button)

        self.best_each_button = arcade.gui.UIImageButton(
            center_x=pos2_x,
            center_y=pos1_y,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_best_each_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_best_each_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_best_each_clicked.png')),
            text='',
            id='best_each_button'
        )
        self.best_each_button.scale = RESOLUTION_SCALING
        self.ui_manager.add_ui_element(self.best_each_button)

        self.all_scores_button = arcade.gui.UIImageButton(
            center_x=pos3_x,
            center_y=pos1_y,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_all_scores_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_all_scores_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_all_scores_clicked.png')),
            text='',
            id='all_scores_button'
        )
        self.all_scores_button.scale = RESOLUTION_SCALING
        self.ui_manager.add_ui_element(self.all_scores_button)

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
        self.sound_manager.play_song(0)
        self.ui_manager = arcade.gui.UIManager(window)
        self.ui_manager.push_handlers(self.on_ui_event)

        self._setup()

    def _setup(self):
        self.ui_manager.purge_ui_elements()

        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.start_menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'bouncedown_mainmenu.png'), RESOLUTION_SCALING)
        self.start_menu_background.center_x = SCREEN_WIDTH/2
        self.start_menu_background.center_y = SCREEN_HEIGHT/2

        # Setup buttons
        self.settings_button = SpriteCache.SETTINGS_BUTTON
        self.achievements_button = SpriteCache.ACHIEVEMENTS_BUTTON
        self.highscores_button = SpriteCache.HIGHSCORES_BUTTON
        self.start_button = SpriteCache.START_BUTTON

        self.ui_manager.add_ui_element(self.settings_button)
        self.ui_manager.add_ui_element(self.achievements_button)
        self.ui_manager.add_ui_element(self.highscores_button)
        self.ui_manager.add_ui_element(self.start_button)

        x = SCREEN_WIDTH/2
        y = SCREEN_HEIGHT
        self.test_button = arcade.gui.UIImageButton(
            center_x=x,
            center_y=y,
            normal_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_play_normal.png')),
            hover_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_play_hover.png')),
            press_texture=arcade.load_texture(os.path.join(SPRITES_PATH, 'button_play_clicked.png')),
            text=' ',
            id='play_button_2'
        )
        SpriteCache.PLAY_BUTTON.scale = RESOLUTION_SCALING

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
        elif event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'play_button_2':
            print('here')

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
            width = self.loading_screen_container.width * SpriteCache.FILE_INDEX / 158 - 24 * RESOLUTION_SCALING
        height = self.loading_screen_container.height - 18*RESOLUTION_SCALING
        x = self.loading_screen_container.center_x - self.loading_screen_container.width/2 + width/2 + 6*RESOLUTION_SCALING
        y = self.loading_screen_container.center_y
        arcade.draw_rectangle_filled(x, y, width, height, self.loading_screen_container_color)

        self.loading_screen_container.draw()


    def on_update(self, dt):
        if SpriteCache.FILE_INDEX >= 1000:
            start_menu_view = AllViewsCombined(self.window, self.sound_manager)
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
        self.highscores_background.center_x = SCREEN_WIDTH / 2
        self.highscores_background.center_y = SCREEN_HEIGHT / 2

    def _init_buttons(self):
        # Setup themes
        self.button_list = []
        self.back_button = SpriteCache.BACK_SUBMIT_HIGHSCORES_BUTTON
        self.submit_score_button = SpriteCache.SUBMIT_HIGHSCORE_BUTTON
        self.button_list.append(self.back_button)
        self.button_list.append(self.submit_score_button)

        self.submit_score_button.scale = RESOLUTION_SCALING
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
        for button in self.button_list:
            button.draw()

    def on_update(self, dt):
        self.dialogue_box.update(dt)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for button in self.button_list:
            button.on_mouse_motion(x, y, dx, dy)

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

        for button in self.button_list:
            button.on_mouse_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        button_released = None
        mouse_in_button = False
        for button in self.button_list:
            if button.pressed:
                button_released, mouse_in_button = button.on_mouse_release(x, y)


class AllViewsCombined(arcade.View):
    def __init__(self, window: arcade.Window, sound_manager: SoundManager):
        super().__init__()

        self.window = window
        self.sound_manager = sound_manager
        self.sound_manager.play_song(0)
        self.ui_manager = arcade.gui.UIManager(window)

        self.current_view = 'main_menu'
        self.setup_bool = False

        self._setup()
        self._setup_start_menu()


    def _setup(self):
        # Setup class params
        self.button_list = []
        self.frames_since_platform_created = 0
        self.platform_speed = 1.7 * RESOLUTION_SCALING
        self.starting_platform_speed = self.platform_speed

        self.time_elapsed = 0.0
        self.frames_elapsed = 0
        self.frames_since_platform_created = 0

        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'bouncedown_mainmenu.png'), RESOLUTION_SCALING)
        self.menu_background.center_x = SCREEN_WIDTH / 2
        self.menu_background.center_y = SCREEN_HEIGHT / 2

        self.spikes = arcade.Sprite(os.path.join(SPRITES_PATH, 'spikes.png'), RESOLUTION_SCALING)
        self.spikes.center_x = SCREEN_WIDTH / 2
        self.spikes.center_y = SCREEN_HEIGHT + 80*RESOLUTION_SCALING
        self.fire = arcade.Sprite(os.path.join(SPRITES_PATH, 'fire_0.png'), RESOLUTION_SCALING)
        self.fire_texture_1 = arcade.load_texture(os.path.join(SPRITES_PATH, 'fire_1.png'))
        self.fire_texture_2 = arcade.load_texture(os.path.join(SPRITES_PATH, 'fire_2.png'))
        self.fire.append_texture(self.fire_texture_1)
        self.fire.append_texture(self.fire_texture_2)
        self.fire.center_x = SCREEN_WIDTH / 2
        self.fire.center_y = (1080-960)*RESOLUTION_SCALING
        self.bottom_bar = arcade.Sprite(os.path.join(SPRITES_PATH, 'bottom_bar.png'), RESOLUTION_SCALING)
        self.bottom_bar.center_x = SCREEN_WIDTH / 2
        self.bottom_bar.center_y = 50*RESOLUTION_SCALING
        self.sidebar_left = arcade.Sprite(os.path.join(SPRITES_PATH, 'sidebar_left.png'), RESOLUTION_SCALING)
        self.sidebar_left.center_x = 105*RESOLUTION_SCALING
        self.sidebar_left.center_y = SCREEN_HEIGHT / 2
        self.sidebar_right = arcade.Sprite(os.path.join(SPRITES_PATH, 'sidebar_right.png'), RESOLUTION_SCALING)
        self.sidebar_right.center_x = 1814*RESOLUTION_SCALING
        self.sidebar_right.center_y = SCREEN_HEIGHT / 2

        self.platform_spritelist = arcade.SpriteList()

        self.setup_bool = True

    def _setup_start_menu(self):
        # Setup background UI
        self.current_view = 'main_menu'

        arcade.set_background_color(arcade.color.WHITE)
        self.menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'bouncedown_mainmenu.png'), RESOLUTION_SCALING)
        self.menu_background.center_x = SCREEN_WIDTH / 2
        self.menu_background.center_y = SCREEN_HEIGHT / 2
        self.menu_button_holder = arcade.Sprite(os.path.join(SPRITES_PATH, 'main_menu_button_holder.png'), RESOLUTION_SCALING)
        self.menu_button_holder.center_x = SCREEN_WIDTH / 2
        self.menu_button_holder.center_y = (1080-580)*RESOLUTION_SCALING
        self.menu_title = arcade.Sprite(os.path.join(SPRITES_PATH, 'main_menu_title.png'), RESOLUTION_SCALING)
        self.menu_title.center_x = SCREEN_WIDTH / 2
        self.menu_title.center_y = (1080-156)*RESOLUTION_SCALING

        # Setup buttons
        self.settings_button = SpriteCache.SETTINGS_BUTTON
        self.achievements_button = SpriteCache.ACHIEVEMENTS_BUTTON
        self.highscores_button = SpriteCache.HIGHSCORES_BUTTON
        self.start_button = SpriteCache.START_BUTTON

        self.button_list = []
        self.button_list.append(self.settings_button)
        self.button_list.append(self.achievements_button)
        self.button_list.append(self.highscores_button)
        self.button_list.append(self.start_button)

    def _setup_settings_menu(self):
        self.current_view = 'settings'
        self.button_list = []
        self.menu_button_holder.kill()
        self.menu_title.kill()

        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'menu_settings.png'), RESOLUTION_SCALING)
        self.menu_background.center_x = SCREEN_WIDTH / 2
        self.menu_background.center_y = SCREEN_HEIGHT / 2

        # Setup buttons
        self.back_button = SpriteCache.BACK_SETTINGS
        self.button_list.append(self.back_button)

    def _setup_achievements_menu(self):
        self.current_view = 'achievements'
        self.button_list = []
        self.menu_button_holder.kill()
        self.menu_title.kill()

        # Setup buttons
        self.back_button = SpriteCache.BACK_SETTINGS
        self.button_list.append(self.back_button)

        self.achievement_hovering_list = [False for i in range(NUM_ACHIEVEMENTS)]
        self.achievement_button_list = SpriteCache.ACHIEVEMENT_HOLDER_BUTTON_LIST

        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'menu_achievements.png'), RESOLUTION_SCALING)
        self.menu_background.center_x = SCREEN_WIDTH / 2
        self.menu_background.center_y = SCREEN_HEIGHT / 2

        self.text_labels_list = []
        self.achievements_icon_list = []

        # Check for completed achievements
        achievements_completed = 0
        for i in range(len(GameData.data["achievements_complete"])):
            if GameData.data["achievements_complete"][i]:
                achievements_completed += 1

        # Create UILabel text
        text = "Completed Achievements: " + str(achievements_completed) + "/" + str(NUM_ACHIEVEMENTS)
        x = SCREEN_WIDTH / 2
        y = (1080-730)*RESOLUTION_SCALING
        self.achievements_completed_text_label = TextLabel(text, x, y, arcade.color.WHITE, font_size=26,
                                                           anchor_x='center', anchor_y='center', bold=True,
                                                           align='center')

        self.achievement_text_holder = arcade.Sprite(os.path.join(SPRITES_PATH, 'achievement_text_holder.png'), RESOLUTION_SCALING)
        self.achievement_text_holder.center_x = x
        self.achievement_text_holder.center_y = y

        # Achievement icons
        x_start = 685*RESOLUTION_SCALING
        y_start = (1080-290)*RESOLUTION_SCALING
        spacing_x = 110*RESOLUTION_SCALING
        spacing_y = 110*RESOLUTION_SCALING
        for i in range(NUM_ACHIEVEMENTS):
            x = x_start + spacing_x*(i % 6)
            y = y_start - spacing_y*(int(np.floor((i + 0.01) / 6) % 6))
            if i <= 9:
                index_str = '0'+str(i)
            else:
                index_str = str(i)
            if GameData.data['achievements_complete'][i]:
                path = os.path.join(SPRITES_PATH, "achievement_" + index_str + '.png')
            else:
                path = os.path.join(SPRITES_PATH, 'achievement_lock.png')

            theme = Theme()
            theme.set_font(40, arcade.color.BLACK)
            normal = os.path.join(SPRITES_PATH, path)
            theme.add_button_textures(normal, None, None, None)
            achievement_icon = TextButton(x, y, '', 'achievement_icon_' + index_str, theme)
            achievement_icon.scale = RESOLUTION_SCALING
            self.achievements_icon_list.append(achievement_icon)

    def _setup_highscores_menu(self):
        self.current_view = 'highscores'
        self.button_list = []
        self.menu_button_holder.kill()
        self.menu_title.kill()

        # Setup parameters
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

        # Setup background
        arcade.set_background_color(arcade.color.WHITE)
        self.menu_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'menu_highscores.png'), RESOLUTION_SCALING)
        self.menu_background.center_x = SCREEN_WIDTH / 2
        self.menu_background.center_y = SCREEN_HEIGHT / 2
        self.top10_scores, self.top10_names = GameData.sort_highscores()

        # Setup buttons
        self.back_button = SpriteCache.BACK_SETTINGS
        self.my_scores_button = SpriteCache.MY_SCORES_BUTTON
        self.best_each_button = SpriteCache.BEST_EACH_BUTTON
        self.all_scores_button = SpriteCache.ALL_SCORES_BUTTON

        self.button_list.append(self.back_button)
        self.button_list.append(self.my_scores_button)
        self.button_list.append(self.best_each_button)
        self.button_list.append(self.all_scores_button)

    def on_draw(self):
        arcade.start_render()
        self.menu_background.draw()
        self.platform_spritelist.draw()
        self.menu_button_holder.draw()
        self.fire.draw()
        self.bottom_bar.draw()
        self.sidebar_left.draw()
        self.sidebar_right.draw()
        self.menu_title.draw()
        self.spikes.draw()

        for button in self.button_list:
            button.draw()

        if self.current_view == 'achievements':
            self.achievement_text_holder.draw()
            hovering = False
            for i in range(len(SpriteCache.ACHIEVEMENT_NAME_LABELS_LIST)):
                if SpriteCache.ACHIEVEMENT_HOLDER_BUTTON_LIST[i].hovering:
                    SpriteCache.ACHIEVEMENT_NAME_LABELS_LIST[i].draw()
                    SpriteCache.ACHIEVEMENT_LABELS_LIST[i].draw()
                    hovering = True

            if not hovering:
                self.achievements_completed_text_label.draw()

            for achievement_holder_button in self.achievement_button_list:
                achievement_holder_button.draw()

            for achievement_icon in self.achievements_icon_list:
                achievement_icon.draw()

        if self.current_view == 'highscores':
            # Draw UI headers
            pos1_x = 680 * RESOLUTION_SCALING
            pos2_x = 820 * RESOLUTION_SCALING
            pos3_x = 1260 * RESOLUTION_SCALING
            pos1_y = (1080 - 290) * RESOLUTION_SCALING
            arcade.draw_text('Rank', pos1_x, pos1_y, arcade.color.WHITE, font_size=24, align="center", anchor_x="right")
            arcade.draw_text('Username', pos2_x, pos1_y, arcade.color.WHITE, font_size=24, align="center",
                             anchor_x="left")
            arcade.draw_text('Score', pos3_x, pos1_y, arcade.color.WHITE, font_size=24, align="center",
                             anchor_x="right")

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

                    arcade.draw_text(str(i + 1) + ".", pos1_x, pos1_y, arcade.color.WHITE, font_size=22, align="center",
                                     anchor_x="right")
                    arcade.draw_text(username, pos2_x, pos1_y, arcade.color.WHITE, font_size=22, align='center',
                                     anchor_x="left")
                    arcade.draw_text(str(score), pos3_x, pos1_y, arcade.color.WHITE, font_size=22, align='center',
                                     anchor_x="right")
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

                    arcade.draw_text(str(i + 1) + ".", pos1_x, pos1_y, arcade.color.WHITE, font_size=22, align="center",
                                     anchor_x="right")
                    arcade.draw_text(username, pos2_x, pos1_y, arcade.color.WHITE, font_size=22, align="center",
                                     anchor_x="left")
                    arcade.draw_text(str(score), pos3_x, pos1_y, arcade.color.WHITE, font_size=22, align="center",
                                     anchor_x="right")
                    if i >= 9: break
            elif self.all_time_best_active:
                for i in range(len(self.all_time_scores_list)):
                    score = self.all_time_scores_list[i]
                    username = self.all_time_usernames_list[i]
                    spacing = 40 * RESOLUTION_SCALING
                    pos1_x = 680 * RESOLUTION_SCALING
                    pos2_x = 820 * RESOLUTION_SCALING
                    pos3_x = 1260 * RESOLUTION_SCALING
                    pos1_y = (1080 - 197 - spacing - 100) * RESOLUTION_SCALING - i * spacing

                    arcade.draw_text(str(i + 1) + ".", pos1_x, pos1_y, arcade.color.WHITE, font_size=22, align="center",
                                     anchor_x="right")
                    arcade.draw_text(username, pos2_x, pos1_y, arcade.color.WHITE, font_size=22, align="center",
                                     anchor_x="left")
                    arcade.draw_text(str(score), pos3_x, pos1_y, arcade.color.WHITE, font_size=22, align="center",
                                     anchor_x="right")
                    if i >= 9: break

    def on_update(self, dt):
        self.sound_manager.update()

        # Update main sprites
        self.spikes.update()
        self.fire.update()
        self.platform_spritelist.update()
        self.bottom_bar.update()
        self.sidebar_left.update()
        self.sidebar_right.update()

        # Generate platform
        random_generator_num = np.random.randint(1, 40)
        min_num_frames_before_spawn = 40
        max_num_frames_before_spawn = 160
        if (
                (random_generator_num == 1 and self.frames_since_platform_created > min_num_frames_before_spawn) or
                (self.frames_since_platform_created > max_num_frames_before_spawn)
           ):
            platform_type, platform_texture_name = generate_platform_type_2()
            temp_platform = Platform(os.path.join(SPRITES_PATH, platform_texture_name), 0.5 * RESOLUTION_SCALING, self,
                                     platform_type)
            temp_platform.change_y = self.platform_speed
            self.platform_spritelist.append(temp_platform)
            self.frames_since_platform_created = 0

        # Spikes and lava
        if self.spikes.center_y < SCREEN_HEIGHT + 45*RESOLUTION_SCALING:
            self.spikes.change_y += 0.05
        elif self.spikes.center_y >= SCREEN_HEIGHT + 45*RESOLUTION_SCALING:
            self.spikes.change_y -= 0.05

        if not self.current_view == 'main_menu':
            self.menu_button_holder.kill()
            self.menu_title.kill()

        self.update_animation()

        for platform in self.platform_spritelist:
            if platform.center_y >= SCREEN_HEIGHT + 200*RESOLUTION_SCALING:
                platform.remove_from_sprite_lists()

        # End of update calls
        self.update_animation()
        self.time_elapsed += 1.0 / FRAME_RATE
        self.frames_elapsed += 1
        self.frames_since_platform_created += 1

    def update_animation(self):
        # Fire animation
        if self.frames_elapsed % 7 == 1:
            self.fire.set_texture(self.frames_elapsed % 3)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for button in self.button_list:
            button.on_mouse_motion(x, y, dx, dy)
        if self.current_view == 'achievements':
            for achievement_holder_button in self.achievement_button_list:
                achievement_holder_button.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for button in self.button_list:
            button.on_mouse_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        button_released = None
        mouse_in_button = False
        for button in self.button_list:
            if button.pressed:
                button_released, mouse_in_button = button.on_mouse_release(x, y)

        if mouse_in_button:
            if button_released.id == 'settings_button':
                self.sound_manager.play_sound(0)
                self._setup_settings_menu()
            elif button_released.id == 'achievements_button':
                self.sound_manager.play_sound(0)
                self._setup_achievements_menu()
            elif button_released.id == 'highscores_button':
                self.sound_manager.play_sound(0)
                self._setup_highscores_menu()
            elif button_released.id == 'start_button':
                self.sound_manager.play_sound(0)
                game_scene_view = game_scene.GameSceneView(self.window, self.sound_manager)
                self.window.show_view(game_scene_view)
            elif button_released.id == 'back_button':
                self.sound_manager.play_sound(0)
                self._setup_start_menu()
            elif button_released.id == 'my_scores_button':
                self.my_scores_active = True
                self.best_each_active = False
                self.all_time_best_active = False
            elif button_released.id == 'best_each_button':
                self.my_scores_active = False
                self.best_each_active = True
                self.all_time_best_active = False
            elif button_released.id == 'all_scores_button':
                self.my_scores_active = False
                self.best_each_active = False
                self.all_time_best_active = True