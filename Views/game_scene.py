from __future__ import annotations

import arcade
import arcade.gui
import collections
import os
import time
import numpy as np
import timeit

from arcade.gui.ui_style import UIStyle

from globals import *
from player import Player
from platforms import Platform, generate_platform_type
from load_sprites import SpriteCache
from game_data import GameData
from Views import menu_views
from Utils.gui import TextLabel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sound_manager import SoundManager


class GameSceneView(arcade.View):
    def __init__(self, window: arcade.Window, sound_manager: SoundManager):
        super().__init__()

        self.window = window
        self.sound_manager = sound_manager
        self.game_scene_initialized = False
        self.game_scene = True
        self.fps = FPSCounter()

        self.ui_manager = arcade.gui.UIManager(window)
        self.ui_manager.push_handlers(self.on_ui_event)
        self.physics_engine = None

        self.current_level = None
        self.score = 0
        self.platform_speed = 1.7 * RESOLUTION_SCALING
        self.starting_platform_speed = self.platform_speed
        self.leftright_platform_acceleration = 0.45
        self.player_is_small = False
        self.player_is_big = False
        self.player_has_horns = False
        self.small_big_countdown_start = 420
        self.spike_countdown_start = 420
        self.player_is_small_countdown = self.small_big_countdown_start
        self.player_is_big_countdown = self.small_big_countdown_start
        self.player_has_spikes_countdown = self.spike_countdown_start
        self.time_to_get_small_big = 60
        self.time_to_get_back_to_normal = 180
        self.player_is_bouncing = False
        self.fire_death_current_idx = 0

        self.cloud_platforms_broken = 0
        self.bouncy_platforms_touched = 0
        self.score_while_small = 0
        self.score_while_big = 0
        self.score_while_spiky = 0

        self.keyup_pressed = False
        self.keydown_pressed = False
        self.keyright_pressed = False
        self.keyleft_pressed = False
        self.keyspace_pressed = False

        self.start_spike_animation = False
        self.do_fire_death_animation = False

        self.time_elapsed = 0.0
        self.frames_elapsed = 0
        self.frames_since_platform_created = 0
        self.game_ended = False
        self.setup_complete = False

        self._setup()

    def _setup(self):
        # Player
        self.player_hitbox_vertical_scaling = 1.11
        self.player_scale = PLAYER_SCALE
        self.player_scale_initial = PLAYER_SCALE
        self.small_big_scale_constant = 1.3
        self.player = Player(os.path.join(SPRITES_PATH, 'main_character_idle.png'), self.player_scale, self)
        self.player.center_x = SCREEN_WIDTH / 2 * RESOLUTION_SCALING
        self.player.center_y = ((5 / 6) * SCREEN_HEIGHT) * RESOLUTION_SCALING
        self.player_hitbox = [[-self.player.width*0.75, int(-self.player.height*self.player_hitbox_vertical_scaling)],
                         [self.player.width*0.75, int(-self.player.height*self.player_hitbox_vertical_scaling)],
                         [self.player.width*0.75, int(-self.player.height*self.player_hitbox_vertical_scaling - 30)],
                         [-self.player.width*0.75, int(-self.player.height*self.player_hitbox_vertical_scaling - 30)]]
        self.player.hit_box = self.player_hitbox

        self.player_ghost = arcade.Sprite(os.path.join(SPRITES_PATH, 'main_character_idle.png'), self.player_scale)
        self.player_ghost.center_x = self.player.center_x
        self.player_ghost.center_y = self.player.center_y
        self.player_ghost.alpha = 0
        self.player_old_scale = self.player.scale
        self.player_ghost_hit_box_initial = np.array(self.player_ghost.hit_box)

        self.player_horns = arcade.Sprite(os.path.join(SPRITES_PATH, 'main_character_horns.png'), self.player_scale)
        self.player_horns.center_x = self.player.center_x
        self.player_horns.center_y = SCREEN_HEIGHT + 100*RESOLUTION_SCALING

        self.player_spike_death_sprite = arcade.Sprite(os.path.join(SPRITES_PATH, 'main_character_spike_death.png'), 2*self.player_scale)

        self.fire_death_animation = arcade.Sprite(os.path.join(SPRITES_PATH, 'fire_animation_0.png'), self.player_scale)
        self.fire_death_animation.center_x = SCREEN_WIDTH / 2
        self.fire_death_animation.center_y = 300
        for i in range(8):
            self.fire_death_animation.append_texture(arcade.load_texture(os.path.join(SPRITES_PATH, 'fire_animation_'+str(i+1)+'.png')))

        # Platforms
        self.platform1 = Platform(os.path.join(SPRITES_PATH, 'normal_platform.png'), PLATFORM_SCALE * RESOLUTION_SCALING, self, 1)
        self.platform1.center_x = SCREEN_WIDTH / 2
        self.platform1.center_y = ((4 / 6) * SCREEN_HEIGHT)
        self.platform1.change_y = self.starting_platform_speed

        self.platform2 = Platform(os.path.join(SPRITES_PATH, 'normal_platform.png'), PLATFORM_SCALE * RESOLUTION_SCALING, self, 1)
        self.platform2.center_x = SCREEN_WIDTH / 3
        self.platform2.center_y = ((3 / 6) * SCREEN_HEIGHT)
        self.platform2.change_y = self.starting_platform_speed

        self.platform3 = Platform(os.path.join(SPRITES_PATH, 'normal_platform.png'), 0.5 * RESOLUTION_SCALING, self, 1)
        self.platform3.center_x = (2 / 3) * SCREEN_WIDTH
        self.platform3.center_y = ((2 / 6) * SCREEN_HEIGHT)
        self.platform3.change_y = self.starting_platform_speed

        self.platform4 = Platform(os.path.join(SPRITES_PATH, 'normal_platform.png'), 0.5 * RESOLUTION_SCALING, self, 1)
        self.platform4.center_x = (1 / 4) * SCREEN_WIDTH
        self.platform4.center_y = ((1 / 6) * SCREEN_HEIGHT)
        self.platform4.change_y = self.starting_platform_speed

        self.platform_spritelist = arcade.SpriteList()
        self.platform_spritelist.extend([self.platform1, self.platform2, self.platform3, self.platform4])
        self.ice_platform_timer_list = []

        # Physics
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.platform_spritelist, GRAVITY)

        # Setup background UI
        arcade.set_background_color(arcade.color.WHITE)
        self.level_background = arcade.Sprite(os.path.join(SPRITES_PATH, 'background_playscene.png'),
                                              RESOLUTION_SCALING)
        self.level_background.center_x = SCREEN_WIDTH / 2
        self.level_background.center_y = SCREEN_HEIGHT / 2

        self.spikes = arcade.Sprite(os.path.join(SPRITES_PATH, 'spikes.png'), RESOLUTION_SCALING)
        self.spikes.center_x = SCREEN_WIDTH / 2
        self.spikes.center_y = SCREEN_HEIGHT + 80*RESOLUTION_SCALING
        self.fire = arcade.Sprite(os.path.join(SPRITES_PATH, 'fire_0.png'), RESOLUTION_SCALING)
        self.fire.center_x = SCREEN_WIDTH / 2
        self.fire.center_y = (1080-960)*RESOLUTION_SCALING
        self.bottom_bar = arcade.Sprite(os.path.join(SPRITES_PATH, 'bottom_bar.png'), RESOLUTION_SCALING)
        self.bottom_bar.center_x = SCREEN_WIDTH / 2
        self.bottom_bar.center_y = 50*RESOLUTION_SCALING
        self.sidebar_left = arcade.Sprite(os.path.join(SPRITES_PATH, 'sidebar_left.png'), RESOLUTION_SCALING)
        self.sidebar_left.center_x = 105*RESOLUTION_SCALING
        self.sidebar_left.center_y = (1080 - 555)
        self.sidebar_right = arcade.Sprite(os.path.join(SPRITES_PATH, 'sidebar_right.png'), RESOLUTION_SCALING)
        self.sidebar_right.center_x = 1814*RESOLUTION_SCALING
        self.sidebar_right.center_y = (1080 - 555)

        self.score_container = arcade.Sprite(os.path.join(SPRITES_PATH, 'score_container.png'),
                                             0.8 * RESOLUTION_SCALING)
        self.score_container.center_x = SCREEN_WIDTH / 2
        self.score_container.center_y = SCREEN_HEIGHT / 18

        # Game Over UI
        self.betterluck_label = arcade.Sprite(os.path.join(SPRITES_PATH, 'betterluck_label.png'), RESOLUTION_SCALING)
        self.betterluck_label.center_x = SCREEN_WIDTH / 2
        self.betterluck_label.center_y = SCREEN_HEIGHT / 2 + 110 * RESOLUTION_SCALING

        self.game_scene_initialized = True
        self.frames_since_game_over = 0

        # Music
        self.sound_manager.play_song(1)

    def on_ui_event(self, event: arcade.gui.UIEvent):
        if event.type == arcade.gui.UIClickable.CLICKED and event.get('ui_element').id == 'settings_button':
            pass
            # start_menu_view = start_menu.StartMenuView()
            # self.window.show_view(start_menu_view)

    def on_draw(self):
        draw_start_time = timeit.default_timer()
        arcade.start_render()

        self.level_background.draw()
        self.spikes.draw()
        self.platform_spritelist.draw()
        for platform in self.platform_spritelist:
            platform.on_draw()
            # platform.draw_hit_box(arcade.color.RED)

        # Animations
        if self.start_spike_animation:
            self.player_spike_death_sprite.draw()
        self.fire.draw()

        # Draw main sprites
        if self.player_has_horns:
            self.player_horns.draw()
        self.player.draw()
        self.player.on_draw()
        self.player_ghost.draw()
        if self.do_fire_death_animation:
            self.fire_death_animation.draw()
        # self.player_ghost.draw_hit_box(arcade.color.RED)
        # self.player.draw_hit_box(arcade.color.RED)
        self.bottom_bar.draw()
        self.sidebar_left.draw()
        self.sidebar_right.draw()

        self.score_container.draw()
        self.score_label = arcade.draw_text('Score: {0}'.format(self.score),
                                            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 18,
                                            arcade.color.WHITE,
                                            align="center", anchor_x="center", anchor_y="center",
                                            bold=True, font_size=30)

        fps = self.fps.get_fps()
        output = f"FPS: {fps:3.0f}"
        # arcade.draw_text(output, 20, SCREEN_HEIGHT - 80, arcade.color.BLACK, 16)
        self.draw_time = timeit.default_timer() - draw_start_time
        self.fps.tick()

        if self.game_ended:
            self.betterluck_label.draw()

    def generate_platform_frequency(self):
        random_generator_num = 0
        min_num_frames_before_spawn = 0
        max_num_frames_before_spawn = 0
        if self.score < 1000:
            random_generator_num = np.random.randint(1, 40)
            min_num_frames_before_spawn = 40
            max_num_frames_before_spawn = 160
        elif self.score < 2000:
            random_generator_num = np.random.randint(1, 25)
            min_num_frames_before_spawn = 25
            max_num_frames_before_spawn = 100
        elif self.score < 3000:
            random_generator_num = np.random.randint(1, 20)
            min_num_frames_before_spawn = 20
            max_num_frames_before_spawn = 90
        elif self.score < 4000:
            random_generator_num = np.random.randint(1, 15)
            min_num_frames_before_spawn = 15
            max_num_frames_before_spawn = 80
        elif self.score < 5000:
            random_generator_num = np.random.randint(1, 10)
            min_num_frames_before_spawn = 10
            max_num_frames_before_spawn = 70
        else:
            random_generator_num = np.random.randint(1, 10)
            min_num_frames_before_spawn = 10
            max_num_frames_before_spawn = 60

        return random_generator_num, min_num_frames_before_spawn, max_num_frames_before_spawn

    def _load_textures(self):
        self.fire_texture_1 = arcade.load_texture(os.path.join(SPRITES_PATH, 'fire_1.png'))
        self.fire_texture_2 = arcade.load_texture(os.path.join(SPRITES_PATH, 'fire_2.png'))
        self.fire.append_texture(self.fire_texture_1)
        self.fire.append_texture(self.fire_texture_2)

    def on_update(self, dt):
        # Load textures after setup
        if not self.setup_complete:
            self._load_textures()

        # Update main sprites
        self.spikes.update()
        self.platform_spritelist.update()
        self.bottom_bar.update()
        self.player.update()
        if self.player_has_horns:
            self.player_horns.update()
            self.player_horns.center_x = self.player.center_x
            self.player_horns.center_y = self.player.center_y + 0.8*self.player.height/2
        self.player_ghost.center_x = self.player.center_x
        self.player_ghost.center_y = self.player.center_y
        self.player_horns.scale = self.player.scale
        self.player_ghost.scale = self.player.scale
        if self.start_spike_animation:
            self.player_spike_death_sprite.update()
        if self.do_fire_death_animation:
            self.fire_death_animation.update()
        self.fire.update()

        # Scale ghost hitbox properly
        if self.player.scale < (1/2)*self.player_scale_initial:
            self.player_ghost.hit_box = (self.player_ghost_hit_box_initial * (self.player.scale + 0.06) / self.player_scale_initial).tolist()
        elif self.player.scale > (3/2)*self.player_scale_initial:
            self.player_ghost.hit_box = (self.player_ghost_hit_box_initial * (self.player.scale - 0.06) / self.player_scale_initial).tolist()
        else:
            self.player_ghost.hit_box = self.player_ghost_hit_box_initial

        # Generate platform
        random_generator_num, min_num_frames_before_spawn, max_num_frames_before_spawn = self.generate_platform_frequency()
        if (random_generator_num == 1 and self.frames_since_platform_created > min_num_frames_before_spawn) or self.frames_since_platform_created > max_num_frames_before_spawn:
            platform_type, platform_texture_name = generate_platform_type(self)
            temp_platform = Platform(os.path.join(SPRITES_PATH, platform_texture_name), 0.5 * RESOLUTION_SCALING, self,
                                     platform_type)
            temp_platform.change_y = self.platform_speed
            self.platform_spritelist.append(temp_platform)
            self.frames_since_platform_created = 0

        # Handle platform collisions
        if not self.game_ended:
            collision_list = arcade.check_for_collision_with_list(self.player, self.platform_spritelist)
            if len(collision_list) >= 1:
                temp_platform = collision_list[0]
                if self.player.change_y <= temp_platform.change_y and not temp_platform.do_ice_animation_bool:
                    self.player_is_bouncing = False
                    self.player.change_y = temp_platform.change_y
                    self.player.center_y = temp_platform.center_y + self.player.height*self.player_hitbox_vertical_scaling / 2 + 5

                    # Platform logic
                    if temp_platform.platform_type == 2 and not self.player_is_small:  # Cloud platforms
                        if not temp_platform.remove_in_2_seconds:
                            self.cloud_platforms_broken += 1
                            if self.cloud_platforms_broken > GameData.data['achievements_progress'][6]:
                                GameData.data['achievements_progress'][6] += 1
                                GameData.data['achievements_progress'][7] += 1
                                GameData.data['achievements_progress'][8] += 1
                            temp_platform.remove_after_2_seconds()
                    elif temp_platform.platform_type == 3:  # Bounce platforms
                        self.player.change_y += self.player.jump_velocity + 0.2 * temp_platform.change_y / self.starting_platform_speed
                        self.player_is_bouncing = True
                        temp_platform.do_bounce_animation()
                        self.bouncy_platforms_touched += 1
                        if self.bouncy_platforms_touched > GameData.data['achievements_progress'][9]:
                            GameData.data['achievements_progress'][9] += 1
                            GameData.data['achievements_progress'][10] += 1
                            GameData.data['achievements_progress'][11] += 1

                        # Sounds
                        if temp_platform.ready_to_play_sound:
                            if self.player_is_small:
                                self.sound_manager.play_sound(4)
                            elif self.player_is_big:
                                self.sound_manager.play_sound(3)
                            else:
                                self.sound_manager.play_sound(2)
                    elif temp_platform.platform_type == 4:  # Small platforms
                        self.player.scale -= (self.small_big_scale_constant - 1)*self.player_scale_initial / self.time_to_get_small_big
                        self.player.acceleration += (self.small_big_scale_constant-1)*self.player.acceleration_initial / self.time_to_get_small_big
                        self.player.max_speed_x += (self.small_big_scale_constant-1)*self.player.max_speed_x_initial / self.time_to_get_small_big
                        self.player.jump_velocity += (self.small_big_scale_constant+0.2-1)*self.player.jump_velocity_initial / self.time_to_get_small_big
                        if self.player.scale <= self.player_scale / self.small_big_scale_constant:
                            self.player.scale = self.player_scale / self.small_big_scale_constant
                        if self.player.acceleration >= self.player.acceleration_initial * self.small_big_scale_constant:
                            self.player.acceleration = self.player.acceleration_initial * self.small_big_scale_constant
                        if self.player.max_speed_x >= self.player.max_speed_x_initial * self.small_big_scale_constant:
                            self.player.max_speed_x = self.player.max_speed_x_initial * self.small_big_scale_constant
                        if self.player.jump_velocity >= self.player.jump_velocity_initial * (self.small_big_scale_constant + 0.2):
                            self.player.jump_velocity = self.player.jump_velocity_initial * (self.small_big_scale_constant + 0.2)

                        if self.player.scale < self.player_scale_initial:
                            self.player_is_small = True
                            self.player_is_big = False
                        elif self.player.scale > self.player_scale_initial:
                            self.player_is_small = False
                            self.player_is_big = True
                        self.player_is_small_countdown = self.small_big_countdown_start

                        # Sounds
                        if temp_platform.ready_to_play_sound:
                            self.sound_manager.play_sound(9)
                    elif temp_platform.platform_type == 5:  # Big platforms
                        self.player.scale += (self.small_big_scale_constant - 1)*self.player_scale_initial / self.time_to_get_small_big
                        self.player.acceleration -= (self.small_big_scale_constant-1)*self.player.acceleration_initial / self.time_to_get_small_big
                        self.player.max_speed_x -= (self.small_big_scale_constant-1)*self.player.max_speed_x_initial / self.time_to_get_small_big
                        self.player.jump_velocity -= (self.small_big_scale_constant+0.2-1)*self.player.jump_velocity_initial / self.time_to_get_small_big
                        if self.player.scale >= self.player_scale * self.small_big_scale_constant:
                            self.player.scale = self.player_scale * self.small_big_scale_constant
                        if self.player.acceleration <= self.player.acceleration_initial / self.small_big_scale_constant:
                            self.player.acceleration = self.player.acceleration_initial / self.small_big_scale_constant
                        if self.player.max_speed_x <= self.player.max_speed_x_initial / self.small_big_scale_constant:
                            self.player.max_speed_x = self.player.max_speed_x_initial / self.small_big_scale_constant
                        if self.player.jump_velocity <= self.player.jump_velocity_initial / (self.small_big_scale_constant + 0.2):
                            self.player.jump_velocity = self.player.jump_velocity_initial / (self.small_big_scale_constant + 0.2)

                        if self.player.scale < self.player_scale_initial:
                            self.player_is_small = True
                            self.player_is_big = False
                        elif self.player.scale > self.player_scale_initial:
                            self.player_is_small = False
                            self.player_is_big = True
                        self.player_is_small_countdown = self.small_big_countdown_start

                        # Sounds
                        if temp_platform.ready_to_play_sound:
                            self.sound_manager.play_sound(10)
                    elif temp_platform.platform_type == 6:  # Spiky platform
                        self.player_has_horns = True
                        self.player_has_spikes_countdown = self.spike_countdown_start

                        # Sounds
                        if temp_platform.ready_to_play_sound:
                            self.sound_manager.play_sound(11)
                    elif temp_platform.platform_type == 7:  # Left platforms
                        self.player.change_x -= self.leftright_platform_acceleration
                    elif temp_platform.platform_type == 8:  # Right platforms
                        self.player.change_x += self.leftright_platform_acceleration

                # Sounds
                if temp_platform.ready_to_play_sound:
                    self.sound_manager.play_sound(7)
                    temp_platform.ready_to_play_sound = False
            else:
                for platform in self.platform_spritelist:
                    platform.ready_to_play_sound = True

        # Routines for small, big and spiky splat
        if self.player_is_small:
            self.score_while_small += 1
            if self.score_while_small > GameData.data['achievements_progress'][12]:
                GameData.data['achievements_progress'][12] += 1
                GameData.data['achievements_progress'][13] += 1
                GameData.data['achievements_progress'][14] += 1
            self.player_is_small_countdown -= 1
            if self.player_is_small_countdown <= 0:
                self.player.scale += (self.small_big_scale_constant - 1) * self.player_scale_initial / self.time_to_get_back_to_normal
                self.player.acceleration -= (self.small_big_scale_constant - 1) * self.player.acceleration_initial / self.time_to_get_back_to_normal
                self.player.max_speed_x -= (self.small_big_scale_constant - 1) * self.player.max_speed_x_initial / self.time_to_get_back_to_normal
                self.player.jump_velocity -= (self.small_big_scale_constant + 0.2 - 1) * self.player.jump_velocity_initial / self.time_to_get_back_to_normal
                if self.player.scale >= self.player_scale_initial:
                    self.player.scale = self.player_scale_initial
                    self.player_is_small = False
                    self.player_is_small_countdown = self.small_big_countdown_start
                if self.player.acceleration <= self.player.acceleration_initial:
                    self.player.acceleration = self.player.acceleration_initial
                    self.player_is_small = False
                    self.player_is_small_countdown = self.small_big_countdown_start
                if self.player.max_speed_x <= self.player.max_speed_x_initial:
                    self.player.max_speed_x = self.player.max_speed_x_initial
                    self.player_is_small = False
                    self.player_is_small_countdown = self.small_big_countdown_start
                if self.player.jump_velocity <= self.player.jump_velocity_initial:
                    self.player.jump_velocity = self.player.jump_velocity_initial
                    self.player_is_small = False
                    self.player_is_small_countdown = self.small_big_countdown_start
        elif self.player_is_big:
            self.score_while_big += 1
            if self.score_while_big > GameData.data['achievements_progress'][15]:
                GameData.data['achievements_progress'][15] += 1
                GameData.data['achievements_progress'][16] += 1
                GameData.data['achievements_progress'][17] += 1
            self.player_is_big_countdown -= 1
            if self.player_is_big_countdown <= 0:
                self.player.scale -= (self.small_big_scale_constant - 1) * self.player_scale_initial / self.time_to_get_back_to_normal
                self.player.acceleration += (self.small_big_scale_constant - 1) * self.player.acceleration_initial / self.time_to_get_back_to_normal
                self.player.max_speed_x += (self.small_big_scale_constant - 1) * self.player.max_speed_x_initial / self.time_to_get_back_to_normal
                self.player.jump_velocity += (self.small_big_scale_constant + 0.2 - 1) * self.player.jump_velocity_initial / self.time_to_get_back_to_normal
                if self.player.scale <= self.player_scale_initial:
                    self.player.scale = self.player_scale_initial
                    self.player_is_big = False
                    self.player_is_big_countdown = self.small_big_countdown_start
                if self.player.acceleration >= self.player.acceleration_initial:
                    self.player.acceleration = self.player.acceleration_initial
                    self.player_is_big = False
                    self.player_is_big_countdown = self.small_big_countdown_start
                if self.player.max_speed_x >= self.player.max_speed_x_initial:
                    self.player.max_speed_x = self.player.max_speed_x_initial
                    self.player_is_big = False
                    self.player_is_big_countdown = self.small_big_countdown_start
                if self.player.jump_velocity >= self.player.jump_velocity_initial:
                    self.player.jump_velocity = self.player.jump_velocity_initial
                    self.player_is_big = False
                    self.player_is_big_countdown = self.small_big_countdown_start
        if self.player_has_horns:
            self.score_while_spiky += 1
            if self.score_while_spiky > GameData.data['achievements_progress'][18]:
                GameData.data['achievements_progress'][18] += 1
                GameData.data['achievements_progress'][19] += 1
                GameData.data['achievements_progress'][20] += 1
            self.player_has_spikes_countdown -= 1
            if self.player_has_spikes_countdown <= 0:
                self.player_has_horns = False
                self.player_has_spikes_countdown = self.spike_countdown_start

        # Speed changes
        if self.score % 100 == 0:
            for platform in self.platform_spritelist:
                platform.change_y += 0.15 * RESOLUTION_SCALING
            self.platform_speed += 0.15 * RESOLUTION_SCALING

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
            deceleration = self.player.change_x / 10
            self.player.change_x -= deceleration

        if self.player.change_y > 0 and not self.player_is_bouncing:
            self.player.change_y = 0

        # Spikes and lava
        if self.spikes.center_y < SCREEN_HEIGHT + 45*RESOLUTION_SCALING:
            self.spikes.change_y += 0.05
        elif self.spikes.center_y >= SCREEN_HEIGHT + 45*RESOLUTION_SCALING:
            self.spikes.change_y -= 0.05

        # Sprite cleanup
        for platform in self.platform_spritelist:
            if platform.center_y > SCREEN_HEIGHT * RESOLUTION_SCALING:
                self.platform_spritelist.remove(platform)

        # Lose condition
        if self.player.center_y > SCREEN_WIDTH * RESOLUTION_SCALING or self.player.center_y < 130*RESOLUTION_SCALING and not self.game_ended:
            self.sound_manager.play_sound(6)
            self.fire_death_animation.center_x = self.player.center_x
            self.fire_death_animation.center_y = 130*RESOLUTION_SCALING
            self.do_fire_death_animation = True
            self.lose_stage()
            self.game_ended = True
        collision_bool = arcade.check_for_collision(self.player_ghost, self.spikes)
        if collision_bool and not self.game_ended:
            self.sound_manager.play_sound(8)
            self.player_spike_death_sprite.center_x = self.player.center_x
            self.player_spike_death_sprite.center_y = self.player.center_y
            self.start_spike_animation = True
            self.lose_stage()
            self.game_ended = True
        for platform in self.platform_spritelist:
            if platform.platform_type == 6:
                collision_bool = arcade.check_for_collision(self.player_ghost, platform.hedgehog)
                if collision_bool and not self.game_ended:
                    self.sound_manager.play_sound(8)
                    self.player_spike_death_sprite.center_x = self.player.center_x
                    self.player_spike_death_sprite.center_y = self.player.center_y
                    self.start_spike_animation = True
                    self.lose_stage()
                    self.game_ended = True

        # End of update calls
        self.update_animation()
        self.time_elapsed += 1.0 / FRAME_RATE
        self.frames_elapsed += 1
        self.frames_since_platform_created += 1

        if not self.game_ended:
            # Achievements
            self.score += 1
            if self.score > GameData.data['highscore']:
                GameData.data['highscore'] = self.score
                GameData.data['achievements_progress'][0] = self.score
                GameData.data['achievements_progress'][1] = self.score
                GameData.data['achievements_progress'][2] = self.score

            # Marathon achievements
            GameData.data['achievements_progress'][3] += 1
            GameData.data['achievements_progress'][4] += 1
            GameData.data['achievements_progress'][5] += 1

            # Big small spikey achievements
            small_big_spiky_score = np.min([self.score_while_small, self.score_while_big, self.score_while_spiky])
            if small_big_spiky_score > GameData.data['achievements_progress'][21]:
                GameData.data['achievements_progress'][21] = small_big_spiky_score
                GameData.data['achievements_progress'][22] = small_big_spiky_score
                GameData.data['achievements_progress'][23] = small_big_spiky_score

            # Check if achievement complete
            for i in range(NUM_ACHIEVEMENTS):
                if (
                        GameData.data['achievements_progress'][i] >= GameData.data['achievements_scores'][i] and not
                        GameData.data['achievements_complete'][i]
                ):
                    GameData.data['achievements_complete'][i] = True

                    # Achievement dropdown
                    if i <= 9:
                        index_str = '0' + str(i)
                    else:
                        index_str = str(i)
                    path = os.path.join(SPRITES_PATH, 'achievement_dropdown.png')
                    path_icon = os.path.join(SPRITES_PATH, 'achievement_' + index_str + '.png')
                    achievement_dropdown = AchievementDropdown(path, RESOLUTION_SCALING)
                    achievement_icon = arcade.Sprite(path_icon, RESOLUTION_SCALING)
                    achievement_icon.center_x = (achievement_dropdown.center_x -
                                                 achievement_dropdown.width / 2 +
                                                 achievement_icon.width / 2 +
                                                 5*RESOLUTION_SCALING)
                    achievement_icon.center_y = achievement_dropdown.center_y
                    self.window.achievement_dropdown_list.append(achievement_dropdown)
                    self.window.achievement_dropdown_icon_list.append(achievement_icon)
                    self.window.achievement_dropdown_text_list.append(SpriteCache.ACHIEVEMENT_DROPDOWN_LABELS_LIST[i])

            GameData.save_data()
        else:
            self.frames_since_game_over += 1
            if self.frames_since_game_over > 120:
                if GameData.data['username'] is None:
                    submit_highscore_view = menu_views.SubmitHighscoresView(self.window, self.sound_manager, self.score)
                    self.window.show_view(submit_highscore_view)
                else:
                    GameData.add_highscore_entry(self.score)
                    GameData.save_data()
                    start_menu_view = menu_views.AllViewsCombined(self.window, self.sound_manager)
                    self.window.show_view(start_menu_view)
                    start_menu_view._setup_highscores_menu()


    def update_animation(self):
        if self.start_spike_animation:
            self.player_spike_death_sprite.scale += 0.02
            if self.player_spike_death_sprite.scale > 2.8*self.player_scale:
                self.player_spike_death_sprite.kill()

        # Fire animation
        if self.frames_elapsed % 7 == 1:
            self.fire.set_texture(self.frames_elapsed % 3)

        # Fire death animation
        if self.do_fire_death_animation and self.frames_elapsed % 5 == 0:
            self.fire_death_current_idx += 1
            if self.fire_death_current_idx < len(self.fire_death_animation.textures):
                self.fire_death_animation.set_texture(self.fire_death_current_idx)
            else:
                self.fire_death_animation.kill()
                self.do_fire_death_animation = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.jump_pressed = True
            self.player.double_jump_pressed = True
            self.keyup_pressed = True
        elif key == arcade.key.DOWN:
            self.keydown_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x += -self.player.acceleration
            self.keyleft_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
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
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.keyleft_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
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
        self.player_ghost.kill()
        self.player_horns.kill()
        self.player.remove_self()


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


class AchievementDropdown(arcade.Sprite):

    def __init__(self, file_name, scale, *args):
        super().__init__(file_name, scale)

        self.time = 0.0

        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT + self.height / 2
        self.final_y = SCREEN_HEIGHT - self.height - SCREEN_BORDER_PADDING
        self.delta_y = self.center_y - self.final_y
        self.time_to_reach_bottom = 2.0
        self.time_to_pause_end = 4.0
        self.time_to_reach_top = 6.0

        self.finished = False

        if len(args) > 0:
            self.center_y = args[0]
            self.final_y = self.center_y - self.delta_y

    def update(self):
        # Move achievement down, pause, then up
        if self.time < self.time_to_reach_bottom:
            self.center_y -= (self.center_y - self.final_y) / (self.time_to_reach_bottom * 60)
        elif self.time_to_reach_bottom < self.time < self.time_to_pause_end:
            pass
        elif self.time > self.time_to_pause_end:
            self.center_y += (self.center_y - self.final_y) / (self.time_to_reach_bottom * 60)

        if self.time > self.time_to_reach_top:
            self.finished = True

    def advance_time(self):
        self.time += 1.0 / 60.0
