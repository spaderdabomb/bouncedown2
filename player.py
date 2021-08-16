from __future__ import annotations

import arcade
import os
import time
import math

from globals import *
from game_data import GameData
from load_sprites import SpriteCache

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Views.game_scene import GameSceneView


class Player(arcade.Sprite):

    def __init__(self, file_name: str, scale: float, game_view: GameSceneView):
        super().__init__(file_name, scale)

        self.game_view = game_view

        self.setup_bool = True
        self.change_y = 0
        self.jump_velocity_initial = 7*RESOLUTION_SCALING
        self.jump_velocity = self.jump_velocity_initial
        self.acceleration_initial = 0.85*RESOLUTION_SCALING
        self.acceleration = self.acceleration_initial
        self.max_speed_x_initial = 15*RESOLUTION_SCALING
        self.max_speed_x = self.max_speed_x_initial

        self.current_texture = 0
        self.frame_count = 0
        self.frames_before_next_animation = 3

        self.eyes_position = (93-34)*RESOLUTION_SCALING*PLAYER_SCALE
        self.mouth_position = (93-114)*RESOLUTION_SCALING*PLAYER_SCALE
        self.eyes_mouth_poisition_scale_factor = 1

        # 0 - idle right
        # 1 - idle left
        self.animation_index = 0
        self.animation_list = []
        self.facing_right = True

        self._setup()

    def _setup(self):
        self.eyes = arcade.Sprite(os.path.join(SPRITES_PATH, 'main_character_eyes.png'), PLAYER_SCALE)
        self.eyes.center_x = self.center_x
        self.eyes.center_y = self.center_y + self.eyes_position
        self.mouth = arcade.Sprite(os.path.join(SPRITES_PATH, 'main_character_mouth_left.png'), PLAYER_SCALE)
        self.mouth.center_x = self.center_x
        self.mouth.center_y = self.center_y + self.mouth_position

        self.mouth_texture_1 = arcade.load_texture(os.path.join(SPRITES_PATH, 'main_character_mouth_right.png'))
        self.mouth.append_texture(self.mouth_texture_1)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y -= GRAVITY

        self.eyes_position = (93-34)*RESOLUTION_SCALING*self.scale
        self.mouth_position = (93-114)*RESOLUTION_SCALING*self.scale
        self.eyes.scale = self.scale
        self.mouth.scale = self.scale
        self.eyes.center_x = self.center_x + self.change_x*self.scale*self.eyes_mouth_poisition_scale_factor
        self.eyes.center_y = self.center_y + self.eyes_position + self.change_y*self.scale*self.eyes_mouth_poisition_scale_factor + self.game_view.platform_speed / 2
        self.mouth.center_x = self.center_x - self.change_x*self.scale*self.eyes_mouth_poisition_scale_factor
        self.mouth.center_y = self.center_y + self.mouth_position - self.change_y*self.scale*self.eyes_mouth_poisition_scale_factor + self.game_view.platform_speed / 2

        if self.change_x > self.max_speed_x:
            self.change_x = self.max_speed_x
        elif self.change_x < -self.max_speed_x:
            self.change_x = -self.max_speed_x

        if self.change_x <= 0:
            self.mouth.set_texture(0)
        elif self.change_x > 0:
            self.mouth.set_texture(1)

        if self.center_x < 209*RESOLUTION_SCALING + self.width*self.scale/2 + 15*RESOLUTION_SCALING:
            self.center_x = 209*RESOLUTION_SCALING + self.width*self.scale/2 + 15*RESOLUTION_SCALING
            self.change_x = 0
        elif self.center_x > SCREEN_WIDTH - 209*RESOLUTION_SCALING - self.width*self.scale/2 - 15*RESOLUTION_SCALING:
            self.center_x = SCREEN_WIDTH - 209*RESOLUTION_SCALING - self.width*self.scale/2 - 15*RESOLUTION_SCALING
            self.change_x = 0

    def game_scene_updates(self):
        pass

    def on_draw(self):
        self.eyes.draw()
        self.mouth.draw()

    def remove_self(self):
        self.eyes.kill()
        self.mouth.kill()
        self.kill()

    def update_animation(self, delta_time: float = 1 / 60):
        pass

    def handle_new_animation(self, index: int):
        pass

    def handle_jump(self):
        self.change_y = self.jump_velocity

    def damaged(self, hp: int):
        pass