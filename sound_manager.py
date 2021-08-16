import os
import arcade
import time

from globals import *

class SoundManager():
    """ Main application class. """

    def __init__(self, window: arcade.Window):
        super().__init__()

        self.window = window

        # Variables used to manage our music. See setup() for giving them
        # values.
        self.music_list = []
        self.current_song = 0
        self.current_player = None
        self.music = None
        self.sound = None

        self.music_volume = float(GameData.data['music_on']) * 0.5
        self.sound_volume = float(GameData.data['music_on']) * 0.6

        self.setup()

    def setup(self):
        # List of music
        self.music_list = [os.path.join(AUDIO_PATH, "main_menu_music.wav"),
                           os.path.join(AUDIO_PATH, "in_game_music.wav")]

        self.sound_list = [os.path.join(AUDIO_PATH, "menu_selection_click.mp3"),
                           os.path.join(AUDIO_PATH, "big_platform_sound.wav"),
                           os.path.join(AUDIO_PATH, "bounce_platform_sound.wav"),
                           os.path.join(AUDIO_PATH, "bounce_while_big_sound.wav"),
                           os.path.join(AUDIO_PATH, "bounce_while_small_sound.wav"),
                           os.path.join(AUDIO_PATH, "cloud_platform_sound.wav"),
                           os.path.join(AUDIO_PATH, "lava_death_sound.wav"),
                           os.path.join(AUDIO_PATH, "normal_platform_sound.wav"),
                           os.path.join(AUDIO_PATH, "player_death_sound.wav"),
                           os.path.join(AUDIO_PATH, "small_platform_sound.wav"),
                           os.path.join(AUDIO_PATH, "big_platform_sound.wav"),
                           os.path.join(AUDIO_PATH, "spiky_platform_sound.wav")]

        self.current_song = 0

    def play_sound(self, index):
        self.sound = arcade.Sound(self.sound_list[index], streaming=True)
        self.sound.play(self.sound_volume)

    def play_song(self, index, new_song=True):
        # Stop what is currently playing.
        if self.music and new_song:
            self.music.stop(self.current_player)

        # Play selected song
        self.music = arcade.Sound(self.music_list[index], streaming=True)
        self.current_player = self.music.play(self.music_volume)
        time.sleep(0.01)

    def update(self):
        position = self.music.get_stream_position(self.current_player)
        if position == 0.0:
            self.play_song(0, new_song=False)

        self.current_player.volume = self.music_volume