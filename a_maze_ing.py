#!/usr/bin/python3
# from typing import Any
import sys
import time
from mazegen.maze_functions.generator import generate_maze
from mazegen.maze_functions.file_reader import read_file
from mazegen.maze_functions.menu import show_menu
from mazegen.maze_functions.data_validator import (check_data,
                                                   SizeError,
                                                   LessThanZeroError,
                                                   OutOfBoundsError,
                                                   PerfectError)


def main(config_data: dict[str, str], new: bool = False) -> None:
    grid: list[list[int]] = generate_maze(config_data)
    try:
        show_menu(grid, config_data)
    except ValueError as e:
        print(
            f"{e.__class__.__name__} Please choose a number between 1 - 5" +
            " and press enter!")
        show_menu(grid, config_data)


if __name__ == "__main__":
    if "--perfect" in sys.argv:
        print("PERFECT MODE IS ACTIVATED!!!")
        time.sleep(2)

    config_file: str = sys.argv[1]
    try:
        config_data: dict[str, str] = read_file(config_file)
        check_data(config_data)
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
