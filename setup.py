import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"include_files": [r"game_data.py", r"globals.py", r"load_sprites.py",
                                       r"main.py", r"platforms.py", r"player.py", "sound_manager.py", r"py_gjapi.py",
                                       r"C:\Repositories\PythonGameMaking\bouncedown_2\Assets",
                                       r"C:\Repositories\PythonGameMaking\bouncedown_2\Utils",
                                       r"C:\Repositories\PythonGameMaking\bouncedown_2\Views"],
                     "packages": ["arcade"], "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Bouncedown 2",
      version="1.1",
      description="Bouncedown in 2021",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])