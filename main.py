import arcade

from game_data import GameData
from globals import *
from Views import menu_views
from load_sprites import SpriteCache
from sound_manager import SoundManager


def main():
    GameData(SCREEN_TITLE)
    GameData.clear_all_data_except_username()
    # GameData.clear_data()
    # GameData.save_data()
    # window = arcade.Window(int(SCREEN_WIDTH), int(SCREEN_HEIGHT), SCREEN_TITLE, resizable=True)
    window = MyAppWindow()
    sound_manager = SoundManager(window)
    loading_view = menu_views.LoadingMenuView(window, sound_manager)
    window.show_view(loading_view)
    arcade.run()

class MyAppWindow(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(int(SCREEN_WIDTH_SCALED), int(SCREEN_HEIGHT_SCALED), SCREEN_TITLE, resizable=True)

        self.achievement_dropdown_list = arcade.SpriteList()
        self.achievement_dropdown_icon_list = arcade.SpriteList()
        self.achievement_dropdown_text_list = []

    def on_resize(self, width: float, height: float):
        # It appears this currently messes up on hover events for buttons
        self.ctx.viewport = 0, 0, *self.get_framebuffer_size()
        self.ctx.projection_2d = 0, 1920, 0, 1080

    def on_draw(self):
        for holder in self.achievement_dropdown_list:
            holder.draw()
        for icon in self.achievement_dropdown_icon_list:
            icon.draw()
        for text_label in self.achievement_dropdown_text_list:
            text_label.draw()

    def on_update(self, dt):
        # Update achievements
        if len(self.achievement_dropdown_list) >= 1:
            if self.achievement_dropdown_list[0].finished:
                self.achievement_dropdown_list[0].remove_from_sprite_lists()
                self.achievement_dropdown_icon_list[0].remove_from_sprite_lists()
                self.achievement_dropdown_text_list.remove(self.achievement_dropdown_text_list[0])
            else:
                self.achievement_dropdown_list[0].update()
                self.achievement_dropdown_list[0].advance_time()

                self.achievement_dropdown_icon_list[0].center_x = (self.achievement_dropdown_list[0].center_x -
                                                                   self.achievement_dropdown_list[0].width / 2 +
                                                                   self.achievement_dropdown_icon_list[0].width / 2 +
                                                                   5*RESOLUTION_SCALING)
                self.achievement_dropdown_icon_list[0].center_y = self.achievement_dropdown_list[0].center_y
                self.achievement_dropdown_icon_list[0].update()

                self.achievement_dropdown_text_list[0].center_x = (self.achievement_dropdown_list[0].center_x +
                                                                   self.achievement_dropdown_list[0].width / 8)
                self.achievement_dropdown_text_list[0].center_y = self.achievement_dropdown_list[0].center_y


if __name__ == "__main__":
    main()
