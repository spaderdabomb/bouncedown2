import arcade
import arcade.gui
import time

from arcade.gui.ui_style import UIStyle

from globals import *
from Utils.core import CounterClass
from Utils.gui import TextLabel, Theme, TextButton, CheckBox


class SpriteCache:

    # Spritesheets

    # UI
    SETTINGS_BUTTON = None
    ACHIEVEMENTS_BUTTON = None
    HIGHSCORES_BUTTON = None
    START_BUTTON = None
    PLAY_BUTTON = None
    BACK_SETTINGS = None
    BACK_SUBMIT_HIGHSCORES_BUTTON = None
    MY_SCORES_BUTTON = None
    BEST_EACH_BUTTON = None
    ALL_SCORES_BUTTON = None
    SUBMIT_HIGHSCORE_BUTTON = None

    MUSIC_VOLUME_CHECKBOX = None
    SOUND_VOLUME_CHECKBOX = None
    MUSIC_VOLUME_LABEL = None
    SOUND_VOLUME_LABEL = None

    ACHIEVEMENT_NAME_LABELS_LIST = []
    ACHIEVEMENT_LABELS_LIST = []
    ACHIEVEMENT_DROPDOWN_LABELS_LIST = []
    ACHIEVEMENT_HOLDER_BUTTON_LIST = []

    # Textures
    BOUNCE_PLATFORM_UP = None
    ICE_PLATFORM = None
    MAIN_CHARACTER = None

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
        SpriteCache._load_ui_labels()
        print('UI labels loading time:', time.time() - a)

        a = time.time()
        SpriteCache._load_ui()
        print('UI buttons loading time:', time.time() - a)

    @staticmethod
    def _load_spritesheets():
        index = CounterClass()
        pass

    @staticmethod
    def _load_textures():
        for filename in os.listdir(SPRITES_PATH):
            if filename.endswith(".png"):
                cache_sprite = arcade.Sprite(os.path.join(SPRITES_PATH, filename), RESOLUTION_SCALING)
                SpriteCache.FILE_INDEX += 1

    @staticmethod
    def _load_ui_labels():
        # Achievement name text labels
        for i in range(NUM_ACHIEVEMENTS):
            # Achievement names
            x = SCREEN_WIDTH / 2
            y = (1080 - 715) * RESOLUTION_SCALING
            label = TextLabel(ACHIEVEMENT_NAMES[i], x, y, arcade.color.ORANGE, font_size=18,
                              anchor_x='center', anchor_y='center', bold=True, align='center')
            SpriteCache.ACHIEVEMENT_NAME_LABELS_LIST.append(label)
            SpriteCache.FILE_INDEX += 1

            # Achievement description text labels
            x = SCREEN_WIDTH / 2
            y = (1080 - 745) * RESOLUTION_SCALING
            text = (ACHIEVEMENT_TEXT[i] + ' ({:n}'.format(GameData.data['achievements_progress'][i]) +
                    '/' + '{:n}'.format(ACHIEVEMENT_SCORES[i]) + ')')
            label = TextLabel(text, x, y, arcade.color.WHITE, font_size=14,
                              anchor_x='center', anchor_y='center', bold=True, align='center')
            SpriteCache.ACHIEVEMENT_LABELS_LIST.append(label)
            SpriteCache.FILE_INDEX += 1

            # Achievement dropdown names
            text = ACHIEVEMENT_DROPDOWN_NAMES[i]
            x = SCREEN_WIDTH / 2 + 30*RESOLUTION_SCALING
            y = SCREEN_HEIGHT + 200*RESOLUTION_SCALING
            label = TextLabel(text, x, y, arcade.color.ORANGE, font_size=20,
                              anchor_x='center', anchor_y='center', bold=True, align='center')
            SpriteCache.ACHIEVEMENT_DROPDOWN_LABELS_LIST.append(label)
            SpriteCache.FILE_INDEX += 1

    @staticmethod
    def _load_ui():

        # Settings button
        x = SCREEN_WIDTH/2
        y = (1080 - 400)*RESOLUTION_SCALING
        spacing = 125*RESOLUTION_SCALING
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_settings_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_settings_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_settings_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.SETTINGS_BUTTON = TextButton(x, y, '', 'settings_button', theme)
        SpriteCache.FILE_INDEX += 1

        # Achievements button
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_achievements_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_achievements_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_achievements_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.ACHIEVEMENTS_BUTTON = TextButton(x, y - spacing*1, '', 'achievements_button', theme)
        SpriteCache.ACHIEVEMENTS_BUTTON.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        # Highscores button
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_highscores_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_highscores_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_highscores_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.HIGHSCORES_BUTTON = TextButton(x, y - spacing*2, '', 'highscores_button', theme)
        SpriteCache.HIGHSCORES_BUTTON.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        # Start button
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_start_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_start_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_start_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.START_BUTTON = TextButton(x, y - spacing*3, '', 'start_button', theme)
        SpriteCache.START_BUTTON.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        # Music and sound check boxes
        x = SCREEN_WIDTH / 2 + 200
        y = (1080-364)*RESOLUTION_SCALING
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, "checkmark_box_on.png")
        clicked = os.path.join(SPRITES_PATH, "checkmark_box_off.png")
        theme.add_button_textures(normal, None, clicked, None)
        SpriteCache.MUSIC_VOLUME_CHECKBOX = CheckBox(x, y, ' ', 'music_volume_checkbox', theme)
        SpriteCache.MUSIC_VOLUME_CHECKBOX.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        # Music and sound check boxes
        x = SCREEN_WIDTH / 2 + 200
        y = (1080-460)*RESOLUTION_SCALING
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, "checkmark_box_on.png")
        clicked = os.path.join(SPRITES_PATH, "checkmark_box_off.png")
        theme.add_button_textures(normal, None, clicked, None)
        SpriteCache.SOUND_VOLUME_CHECKBOX = CheckBox(x, y, ' ', 'sound_volume_checkbox', theme)
        SpriteCache.SOUND_VOLUME_CHECKBOX.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        x = SCREEN_WIDTH / 2 - 200
        y = (1080-364)*RESOLUTION_SCALING
        label = TextLabel('Music', x, y, arcade.color.WHITE, font_size=32,
                          anchor_x='center', anchor_y='center', bold=True, align='center')
        SpriteCache.MUSIC_VOLUME_LABEL = label
        SpriteCache.FILE_INDEX += 1

        x = SCREEN_WIDTH / 2 - 200
        y = (1080-460)*RESOLUTION_SCALING
        label = TextLabel('Sound', x, y, arcade.color.WHITE, font_size=32,
                          anchor_x='center', anchor_y='center', bold=True, align='center')
        SpriteCache.SOUND_VOLUME_LABEL = label
        SpriteCache.FILE_INDEX += 1

        # Back button
        x = SCREEN_WIDTH/2
        y = (1080 - 820)*RESOLUTION_SCALING
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_back_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_back_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_back_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.BACK_SETTINGS = TextButton(x, y, '', 'back_button', theme)
        SpriteCache.BACK_SETTINGS.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        # Achievement holder buttons
        x_start = 685 * RESOLUTION_SCALING
        y_start = (1080 - 290) * RESOLUTION_SCALING
        spacing_x = 110 * RESOLUTION_SCALING
        spacing_y = 110 * RESOLUTION_SCALING
        for i in range(NUM_ACHIEVEMENTS):
            x = x_start + spacing_x * (i % 6)
            y = y_start - spacing_y * (int(np.floor((i + 0.01) / 6) % 6))
            if i <= 9:
                index_str = '0' + str(i)
            else:
                index_str = str(i)
            theme = Theme()
            theme.set_font(40, arcade.color.BLACK)
            normal = os.path.join(SPRITES_PATH, 'achievement_holder.png')
            hovered = (os.path.join(SPRITES_PATH, 'achievement_holder_hover.png'))
            theme.add_button_textures(normal, hovered, None, None)
            achievement_holder_button = TextButton(x, y, '', 'achievement_holder_button_' + index_str, theme)
            achievement_holder_button.scale = RESOLUTION_SCALING
            SpriteCache.ACHIEVEMENT_HOLDER_BUTTON_LIST.append(achievement_holder_button)
            SpriteCache.FILE_INDEX += 1

        # My scores button highscores
        pos1_x = 698 * RESOLUTION_SCALING
        pos2_x = SCREEN_WIDTH / 2
        pos3_x = 1223 * RESOLUTION_SCALING
        pos1_y = (1080-750) * RESOLUTION_SCALING
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_my_scores_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_my_scores_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_my_scores_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.MY_SCORES_BUTTON = TextButton(pos1_x, pos1_y, '', 'my_scores_button', theme)
        SpriteCache.MY_SCORES_BUTTON.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        # Best each button highscores
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_best_each_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_best_each_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_best_each_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.BEST_EACH_BUTTON = TextButton(pos2_x, pos1_y, '', 'best_each_button', theme)
        SpriteCache.BEST_EACH_BUTTON.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        # All scores button highscores
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_all_scores_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_all_scores_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_all_scores_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.ALL_SCORES_BUTTON = TextButton(pos3_x, pos1_y, '', 'all_scores_button', theme)
        SpriteCache.ALL_SCORES_BUTTON.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        # Back button submit highscores
        x = 772*RESOLUTION_SCALING
        y = (1080-588)*RESOLUTION_SCALING
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_back_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_back_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_back_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.BACK_SUBMIT_HIGHSCORES_BUTTON = TextButton(x, y, '', 'back_button_submit_highscores', theme)
        SpriteCache.BACK_SUBMIT_HIGHSCORES_BUTTON.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        # Submit highscores button
        x = 1095*RESOLUTION_SCALING
        y = (1080-588)*RESOLUTION_SCALING
        theme = Theme()
        theme.set_font(40, arcade.color.BLACK)
        normal = os.path.join(SPRITES_PATH, 'button_submit_score_normal.png')
        hovered = os.path.join(SPRITES_PATH, 'button_submit_score_hover.png')
        clicked = os.path.join(SPRITES_PATH, 'button_submit_score_clicked.png')
        theme.add_button_textures(normal, hovered, clicked, None)
        SpriteCache.SUBMIT_HIGHSCORE_BUTTON = TextButton(x, y, '', 'submit_highscore_button', theme)
        SpriteCache.SUBMIT_HIGHSCORE_BUTTON.scale = RESOLUTION_SCALING
        SpriteCache.FILE_INDEX += 1

        SpriteCache.FILE_INDEX = 185