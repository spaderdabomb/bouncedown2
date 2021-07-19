from __future__ import annotations

import arcade
import arcade.gui
import os
import time
import numpy as np

from globals import *
from player import Player
from platforms import Platform, generate_platform_type
from load_sprites import SpriteCache
from game_data import GameData

from typing import TYPE_CHECKING
from typing import Tuple
if TYPE_CHECKING:
    from sound_manager import SoundManager


class GameSceneView(arcade.View):
    def __init__(self, window: arcade.Window, sound_manager: SoundManager):
        super().__init__()

        self.window = window
        self.sound_manager = sound_manager
        self.game_scene_initialized = False
        self.game_scene = True

        self.ui_manager = arcade.gui.UIManager(window)
        self.ui_manager.push_handlers(self.on_ui_event)
        self.physics_engine = None

        self.current_level = None
        self.score = 0
        self.platform_speed = 1.7*RESOLUTION_SCALING
        self.starting_platform_speed = self.platform_speed

        self.keyup_pressed = False
        self.keydown_pressed = False
        self.keyright_pressed = False
        self.keyleft_pressed = False
        self.keyspace_pressed = False

        self.time_elapsed = 0.0
        self.frames_elapsed = 0
        self.frames_since_platform_created = 0

        self._setup()

    def _setup(self):
        # Purge UI
        self.ui_manager.purge_ui_elements()

        # Player
        self.player = Player(os.path.join(SPRITES_PATH, 'main_character_idle.png'), 0.20, self)
        # self.player = arcade.Sprite(os.path.join(SPRITES_PATH, 'main_character_idle.png'), RESOLUTION_SCALING)
        self.player.center_x = SCREEN_WIDTH/2*RESOLUTION_SCALING
        self.player.center_y = ((5/6)*SCREEN_HEIGHT)*RESOLUTION_SCALING

        # Platforms
        self.platform1 = Platform(os.path.join(SPRITES_PATH, 'normal_platform.png'), 0.5*RESOLUTION_SCALING, self, 1)
        self.platform1.center_x = SCREEN_WIDTH/2*RESOLUTION_SCALING
        self.platform1.center_y = ((4/6)*SCREEN_HEIGHT)*RESOLUTION_SCALING
        self.platform1.change_y = self.starting_platform_speed

        self.platform2 = Platform(os.path.join(SPRITES_PATH, 'normal_platform.png'), 0.5*RESOLUTION_SCALING, self, 1)
        self.platform2.center_x = SCREEN_WIDTH/4*RESOLUTION_SCALING
        self.platform2.center_y = ((3/6)*SCREEN_HEIGHT)*RESOLUTION_SCALING
        self.platform2.change_y = self.starting_platform_speed

        self.platform3 = Platform(os.path.join(SPRITES_PATH, 'normal_platform.png'), 0.5*RESOLUTION_SCALING, self, 1)
        self.platform3.center_x = (3/4)*SCREEN_WIDTH*RESOLUTION_SCALING
        self.platform3.center_y = ((2/6)*SCREEN_HEIGHT)*RESOLUTION_SCALING
        self.platform3.change_y = self.starting_platform_speed

        self.platform4 = Platform(os.path.join(SPRITES_PATH, 'normal_platform.png'), 0.5*RESOLUTION_SCALING, self, 1)
        self.platform4.center_x = (2/5)*SCREEN_WIDTH/4*RESOLUTION_SCALING
        self.platform4.center_y = ((1/6)*SCREEN_HEIGHT)*RESOLUTION_SCALING
        self.platform4.change_y = self.starting_platform_speed

        self.platform_spritelist = arcade.SpriteList()
        self.platform_spritelist.extend([self.platform1, self.platform2, self.platform3, self.platform4])
        self.ice_platform_timer_list = []

        # Physics
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.platform_spritelist, GRAVITY)

        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.level_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'menu_training_room.png'), RESOLUTION_SCALING)
        self.level_background.center_x = SCREEN_WIDTH/2
        self.level_background.center_y = SCREEN_HEIGHT/2

        self.game_scene_initialized = True


    def on_ui_event(self, event: arcade.gui.UIEvent):
        if event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'settings_button':
            pass
            # start_menu_view = start_menu.StartMenuView()
            # self.window.show_view(start_menu_view)

    def on_draw(self):
        arcade.start_render()

        self.level_background.draw()
        self.platform_spritelist.draw()

        # Draw main sprites
        self.player.draw()

        self.score_label = arcade.draw_text('Score: {0}'.format(self.score), 1690 * RESOLUTION_SCALING,
                                               (1080 - 47) * RESOLUTION_SCALING,
                                               arcade.color.WHITE,
                                               align="left", anchor_x="left", anchor_y="center",
                                               bold=True, font_size=24)

    def generate_platform_frequency(self):
        random_generator_num = 0
        min_num_frames_before_spawn = 0
        max_num_frames_before_spawn = 0
        if self.score < 1000:
            random_generator_num = np.random.randint(1, 60)
            min_num_frames_before_spawn = 50
            max_num_frames_before_spawn = 180
        elif self.score < 2000:
            random_generator_num = np.random.randint(1, 45)
            min_num_frames_before_spawn = 40
            max_num_frames_before_spawn = 160
        elif self.score < 3000:
            random_generator_num = np.random.randint(1, 40)
            min_num_frames_before_spawn = 35
            max_num_frames_before_spawn = 140
        elif self.score < 4000:
            random_generator_num = np.random.randint(1, 30)
            min_num_frames_before_spawn = 30
            max_num_frames_before_spawn = 120
        elif self.score < 5000:
            random_generator_num = np.random.randint(1, 20)
            min_num_frames_before_spawn = 20
            max_num_frames_before_spawn = 100
        else:
            random_generator_num = np.random.randint(1, 20)
            min_num_frames_before_spawn = 20
            max_num_frames_before_spawn = 80

        return random_generator_num, min_num_frames_before_spawn, max_num_frames_before_spawn

    def on_update(self, dt):
        # Update main sprites
        self.platform_spritelist.update()
        self.player.update()
        self.physics_engine.update()

        # Generate platform
        random_generator_num, min_num_frames_before_spawn, max_num_frames_before_spawn = self.generate_platform_frequency()
        if (random_generator_num == 1 and self.frames_since_platform_created > min_num_frames_before_spawn) or self.frames_since_platform_created > max_num_frames_before_spawn:
            platform_type, platform_texture_name = generate_platform_type(self)
            temp_platform = Platform(os.path.join(SPRITES_PATH, platform_texture_name), 0.5*RESOLUTION_SCALING, self, platform_type)
            temp_platform.change_y = self.platform_speed
            self.platform_spritelist.append(temp_platform)
            self.frames_since_platform_created = 0

        # Handle platform collisions
        collision_list = arcade.check_for_collision_with_list(self.player, self.platform_spritelist)
        if len(collision_list) >= 1:
            temp_platform = collision_list[0]
            if temp_platform.platform_type == 2:  # Ice platforms
                temp_platform.remove_after_2_seconds()
            elif temp_platform.platform_type == 3:  # Bounce platforms
                self.player.change_y += 20*temp_platform.change_y/self.starting_platform_speed
            elif temp_platform.platform_type == 7:  # Left platforms
                self.player.change_x -= 0.8
            elif temp_platform.platform_type == 8:  # Right platforms
                self.player.change_x += 0.8

        # Speed changes
        if self.score % 100 == 0:
            self.platform_speed += 0.15*RESOLUTION_SCALING

        # Player acceleration logic
        if self.keyleft_pressed:
            self.player.change_x += -self.player.acceleration
            if np.abs(self.player.change_x) > self.player.max_speed_x:
                self.player.change_x = -self.player.max_speed_x
        elif self.keyright_pressed:
            self.player.change_x += self.player.acceleration
            if np.abs(self.player.change_x) > self.player.max_speed_x:
                self.player.change_x = self.player.max_speed_x
        else:
            deceleration = self.player.change_x/7
            self.player.change_x -= deceleration

        # Sprite cleanup
        for platform in self.platform_spritelist:
            if platform.center_y > SCREEN_HEIGHT*RESOLUTION_SCALING:
                self.platform_spritelist.remove(platform)

        # Lose condition
        if self.player.center_y > SCREEN_WIDTH*RESOLUTION_SCALING or self.player.center_y < 0:
            self.lose_stage()

        # End of update calls
        self.time_elapsed += 1.0/FRAME_RATE
        self.frames_elapsed += 1
        self.frames_since_platform_created += 1
        self.score += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.jump_pressed = True
            self.player.double_jump_pressed = True
            self.keyup_pressed = True
        elif key == arcade.key.DOWN:
            self.keydown_pressed = True
        elif key == arcade.key.LEFT:
            self.player.change_x += -self.player.acceleration
            self.keyleft_pressed = True
        elif key == arcade.key.RIGHT:
            self.player.change_x += self.player.acceleration
            self.keyright_pressed = True
        elif key == arcade.key.SPACE:
            self.keyspace_pressed = True

        # # Pause Menu
        # if key == arcade.key.ESCAPE:
        #     pause = Pause.PauseView(self)
        #     self.window.show_view(pause)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.jump_pressed = False
            self.player.jump_key_down = False
            self.keyup_pressed = False
        elif key == arcade.key.DOWN:
            self.keydown_pressed = False
        elif key == arcade.key.LEFT:
            self.keyleft_pressed = False
        elif key == arcade.key.RIGHT:
            self.keyright_pressed = False
        elif key == arcade.key.SPACE:
            self.keyspace_pressed = False

        # Extra logic for holding down keys
        if self.keyup_pressed:
            self.player.jump_key_down = True
            self.player.double_jump_key_down = True
        if self.keydown_pressed:
            pass
        if self.keyleft_pressed:
            pass
        if self.keyright_pressed:
            pass

    def lose_stage(self):
        pass

