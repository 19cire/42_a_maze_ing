#!/usr/bin/python3
# from typing import Any
import sys
import random
import time
import numpy as np
from maze_functions.color import change_color
from maze_functions.show_maze import maze_viewer, clear_screen
from maze_functions.file_reader import read_file
from maze_functions.mazegen import build_the_grid, carve_maze
from maze_functions.data_validator import (check_data,
                                           SizeError,
                                           LessThanZeroError,
                                           OutOfBoundsError,
                                           PerfectError)


def new_color(grid: list[list[int]],
              entry: tuple[int],
              exit: tuple[int]
              ) -> None:
    clear_screen()
    color: int = change_color()
    maze_viewer(grid, color, entry, exit)


def new_maze() -> None:
    grid = build_the_grid
    carve_maze(grid)


def say_hello() -> None:
    print("Hello")


def store_maze(grid: list[list[int]], config_data: dict[str, str]) -> None:
    hex_grid: list[str] = []
    for line in grid:
        new_line: list[str] = []
        for row in line:
            new_line.append(hex(row)[2:])
        hex_grid.append("".join(new_line))
    with open(config_data["OUTPUT_FILE"], "w") as f:
        for line in hex_grid:
            f.write(line)
            f.write("\n")
    clear_screen()
    print("The maze is stored in maze.txt")


def show_menu(grid: list[list[int]], config_data: dict[str, str]
              ) -> None:
    print("====MAZE GENERATOR====")
    print("1) Change color")
    print("2) new maze")
    print("3) say hello")
    print("4) store maze")
    print("5) quit")
    entry: tuple[int] = int(config_data["ENTRY"][0]), int(
        config_data["ENTRY"][1])
    maze_exit: tuple[int] = int(config_data["EXIT"][0]), int(
        config_data["EXIT"][1])
    number = int(input("What you wanna do?"))
    if number == 1:
        new_color(grid, entry, maze_exit)
    elif number == 2:
        main(config_data, True)
    elif number == 3:
        say_hello()
    elif number == 4:
        store_maze(grid, config_data)
    elif number == 5:
        print("bye!")
        exit(0)
    else:
        print("Wrong input number!")
    show_menu(grid, config_data)


def main(config_data: dict[str, str], new: bool = False) -> None:
    entry: tuple[int] = int(config_data["ENTRY"][0]), int(
        config_data["ENTRY"][1])
    maze_exit: tuple[int] = int(config_data["EXIT"][0]), int(
        config_data["EXIT"][1])
    grid = build_the_grid(
        int(config_data["WIDTH"]), int(config_data["HEIGHT"]))
    if new:
        seed = np.random.randint(0, 1000)
        carve_maze(grid, 0, 0, random.Random(seed), entry, maze_exit)
    else:
        carve_maze(grid, 0, 0, random.Random(42), entry, maze_exit)
    try:
        show_menu(grid, config_data)
    except ValueError as e:
        print(f"{e.__name__.__class__} Please choose a number between 1 - 5!")
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
