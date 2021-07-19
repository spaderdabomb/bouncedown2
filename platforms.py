from __future__ import annotations

import arcade
import numpy as  np

from globals import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Views.game_scene import GameSceneView


class Platform(arcade.Sprite):

    def __init__(self, file_name: str, scale: float, game_view: GameSceneView, platform_type):
        super().__init__(file_name, scale)

        self.game_view = game_view
        self.platform_type = platform_type
        self.remove_counter = 0
        self.frame_counter = 0
        self.remove_in_2_seconds = False

        self.setup()

    def setup(self):
        position_x = np.random.randint(self.width / 2,
                                       SCREEN_WIDTH * RESOLUTION_SCALING - self.width / 2)
        self.center_x = position_x
        self.center_y = 0
        self.change_y = 1.7 * RESOLUTION_SCALING

    def remove_after_2_seconds(self):
        self.remove_in_2_seconds = True

    def update(self):
        if self.remove_in_2_seconds:
            self.remove_counter += 1

        if self.remove_counter > 60:
            self.remove_from_sprite_lists()

        self.frame_counter += 1


def generate_platform_type(game_view):
    normal_platform_chance = 790
    ice_platform_chance = 30
    bounce_platform_chance = 30
    small_platform_chance = 30
    big_platform_chance = 30
    spike_platform_chance = 30
    left_platform = 30
    right_platform = 30

    platform_type = 1
    platform_texture_name = 'normal_platform.png'
    random_num = 0

    # Change spawn chances
    if -1 < game_view.score <= 100:
        random_num = np.random.randint(0, 1000)
        normal_platform_chance = 120
        ice_platform_chance = 80
        bounce_platform_chance = 30
        small_platform_chance = 30
        big_platform_chance = 30
        spike_platform_chance = 30
        left_platform = 100
        right_platform = 100
    elif 100 < game_view.score < 1800:
        random_num = np.random.randint(0, 1000)
        normal_platform_chance = 120
        ice_platform_chance = 30
        bounce_platform_chance = 100
        small_platform_chance = 30
        big_platform_chance = 30
        spike_platform_chance = 30
        left_platform = 30
        right_platform = 30

    all_platform_chances = [normal_platform_chance,
                            normal_platform_chance + ice_platform_chance,
                            normal_platform_chance + ice_platform_chance + bounce_platform_chance,
                            normal_platform_chance + ice_platform_chance + bounce_platform_chance + small_platform_chance,
                            normal_platform_chance + ice_platform_chance + bounce_platform_chance + small_platform_chance + big_platform_chance,
                            normal_platform_chance + ice_platform_chance + bounce_platform_chance + small_platform_chance + big_platform_chance + spike_platform_chance,
                            normal_platform_chance + ice_platform_chance + bounce_platform_chance + small_platform_chance + big_platform_chance + spike_platform_chance + left_platform,
                            normal_platform_chance + ice_platform_chance + bounce_platform_chance + small_platform_chance + big_platform_chance + spike_platform_chance + left_platform + right_platform]

    if 0 < random_num < all_platform_chances[0]:
        platform_type = 1
        platform_texture_name = 'normal_platform.png'
    elif all_platform_chances[0] < random_num < all_platform_chances[1]:
        platform_type = 2
        platform_texture_name = 'ice_platform.png'
    elif all_platform_chances[1] < random_num < all_platform_chances[2]:
        platform_type = 3
        platform_texture_name = 'bounce_platform.png'
    elif all_platform_chances[2] < random_num < all_platform_chances[3]:
        platform_type = 4
        platform_texture_name = 'small_platform.png'
    elif all_platform_chances[3] < random_num < all_platform_chances[4]:
        platform_type = 5
        platform_texture_name = 'big_platform.png'
    elif all_platform_chances[4] < random_num < all_platform_chances[5]:
        platform_type = 6
        platform_texture_name = 'spike_platform.png'
    elif all_platform_chances[5] < random_num < all_platform_chances[6]:
        platform_type = 7
        platform_texture_name = 'left_platform.png'
    elif all_platform_chances[6] < random_num < all_platform_chances[7]:
        platform_type = 8
        platform_texture_name = 'right_platform.png'
    else:
        temp_platform = arcade.Sprite(os.path.join(SPRITES_PATH, 'normal_platform.png'), 1.5*RESOLUTION_SCALING)

    return platform_type, platform_texture_name