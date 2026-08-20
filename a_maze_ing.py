# !/usr/bin/python3
# from typing import Any
import sys
import time
# from mazegen.maze_functions.generator import generate_maze
from file_reader import read_file
from mazegen import MazeGenerator
from maze_functions.show_maze import maze_viewer
from maze_functions.menu import show_menu
from maze_functions.color import change_color
from maze_functions.data_validator import (check_data,
                                                SizeError,
                                                LessThanZeroError,
                                                OutOfBoundsError,
                                                PerfectError)


def main(config_data: dict[str, str], new: bool = False) -> None:
    entry: tuple[int, int] = int(config_data["ENTRY"][0]), int(
        config_data["ENTRY"][1])
    end: tuple[int, int] = int(config_data["EXIT"][0]), int(
        config_data["EXIT"][1])
    maze = MazeGenerator(
        int(config_data["WIDTH"]),
        int(config_data["HEIGHT"]),
        entry,
        end,
        int(config_data["SEED"]),
        config_data["PERFECT"] == "True"
    )
    color = change_color()
    maze.generate()

    maze_viewer(maze.grid, entry, end, maze.blocked, color)
    show_menu(maze, config_data)

    # grid: list[list[int]] = generate_maze(config_data)
    # try:
    #     show_menu(grid, config_data)
    # except ValueError as e:
    #     print(
    #         f"{e.__class__.__name__} Please choose a number between 1 - 5" +
    #         " and press enter!")
    #     show_menu(grid, config_data)


if __name__ == "__main__":
    if "--perfect" in sys.argv:
        print("PERFECT MODE IS ACTIVATED!!!")
        time.sleep(2)

    config_file: str = sys.argv[1]
    try:
        config_data: dict[str, str] = read_file(config_file)
        check_data(config_data)
        print(config_data)
        main(config_data)
    except (SizeError,
            LessThanZeroError,
            OutOfBoundsError,
            ValueError,
            PerfectError
            ) as e:
        print(e)
    except KeyError as e:
        print(f"{e.__class__.__name__}: Check the keys in your config file." +
              f"The {e} - key is missing.")
