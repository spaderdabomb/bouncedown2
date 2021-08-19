import arcade
import subprocess
import sys

def get_capslock_state(modifiers):
    capslock = None
    if sys.platform == "win32":
        if modifiers == 24:
            capslock = True
        else:
            capslock = False
    elif sys.platform == "darwin":
        if modifiers == 8:
            capslock = True
        else:
            capslock = False

        if subprocess.check_output('xset q | grep LED', shell=True)[65] == 50:
            capslock = False
        if subprocess.check_output('xset q | grep LED', shell=True)[65] == 51:
            capslock = True

    return capslock


# def resize_image(file_name: str, pixels_x, pixels_y, overwrite=False):
#     from PIL import Image
#
#     fname, ext = file_name.split(".")
#     size = pixels_x, pixels_y
#
#     im = Image.open(file_name)
#
#     if overwrite:
#         size = pixels_x, pixels_y
#         im_resized = im.resize(size, Image.ANTIALIAS)
#         im_resized.save(file_name, dpi=(pixels_x, pixels_y))
#     else:
#         full_path = fname + "_" + str(pixels_x) + "x" + str(pixels_y) + "." + ext
#         im_resized = im.resize(size, Image.ANTIALIAS)
#         im_resized.save(full_path, "PNG")
#
#     return size

class CounterClass():
    def __init__(self):
        self.counter = 0

    def increase_counter(self):
        self.counter += 1
        return self.counter

def get_scaled_mouse_coordinates(x, y):
    current_window = arcade.get_window()
    ctx_projection_coords = current_window.ctx.projection_2d
    projection_width = ctx_projection_coords[1] - ctx_projection_coords[0]
    projection_height = ctx_projection_coords[3] - ctx_projection_coords[2]

    window_size = current_window.get_size()
    window_width = window_size[0]
    window_height = window_size[1]

    x_scale = projection_width / window_width
    y_scale = projection_height / window_height

    x = x * x_scale
    y = y * y_scale

    return x, y

