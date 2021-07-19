from __future__ import annotations

import arcade
import os
import time
import math

from globals import *
from game_data import GameData

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Views.game_scene import GameSceneView


class Player(arcade.Sprite):

    def __init__(self, file_name: str, scale: float, game_view: GameSceneView):
        super().__init__(file_name, scale)

        self.game_view = game_view

        self.setup_bool = True
        self.change_y = 0
        self.jump_velocity = 28
        self.acceleration = 0.7
        self.max_speed_x = 10

        self.current_texture = 0
        self.frame_count = 0
        self.frames_before_next_animation = 3

        # 0 - idle right
        # 1 - idle left
        self.animation_index = 0
        self.animation_list = []
        self.facing_right = True

        self.setup()

    def setup(self):
        pass

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_y > self.max_speed_x:
            self.change_y = self.max_speed_x
        elif self.change_y < -self.max_speed_x:
            self.change_y = -self.max_speed_x

    def game_scene_updates(self):
        pass

    def on_draw(self):
        pass

    def update_animation(self, delta_time: float = 1 / 60):
        pass

    def handle_new_animation(self, index: int):
        pass

    def handle_jump(self):
        self.change_y = self.jump_velocity

    def damaged(self, hp: int):
        pass