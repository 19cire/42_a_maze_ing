#!/usr/bin/python3
# from typing import Any
import sys
import random
from maze_functoins.file_reader import read_file
from maze_functoins.color import change_color, bg_square
from maze_functoins.mazegen import build_the_grid, carve_maze
# open_wall,
# get_unvisited_neighbours,
# NORTH, EAST, SOUTH, WEST


class SizeError(Exception):
    pass


def show_maze() -> None:
    ...


def new_maze() -> None:
    ...


def say_hello() -> None:
    ...


def store_maze() -> None:
    ...


def show_menu() -> None:
    print("====MAZE GENERATOR====")
    print("1) Change color")
    print("2) new maze")
    print("3) say hello")
    print("4) store maze")
    print("5) quit")
    number = int(input("What you wanna do?"))
    if number == 1:
        show_maze()
    elif number == 2:
        new_maze()
    elif number == 3:
        say_hello()
    elif number == 4:
        store_maze()
    elif number == 5:
        print("bye!")
        exit(0)
    else:
        print("Wrong input number!")
    show_menu()


def main(config_data: dict[str, str]) -> None:
    grid = build_the_grid(
        int(config_data["WIDTH"]), int(config_data["HEIGHT"]))
    carve_maze(grid, 2, 3, random.Random())
    print(grid)
    print("=========================")
    color1 = change_color()
    symbol: str = bg_square(color1[0], color1[1], color1[2])

    TOP = 1
    BOTTOM = 4
    LEFT = 8    # oder wie auch immer dein Schema aussieht

    for x in grid:
        line1: list[str] = [symbol]
        line2: list[str] = [symbol]
        line3: list[str] = [symbol]

        for y in x:
            line1.append(symbol if y & TOP else "  ")
            line1.append(symbol)

            line2.append("  " if y & LEFT else symbol)

            line3.append(symbol if y & BOTTOM else "  ")
            line3.append(symbol)

        line2.append(symbol)
        print("".join(line1))
        print("".join(line2))
    print("".join(line3))


if __name__ == "__main__":
    config_file: str = sys.argv[1]
    config_data: dict[str, str] = read_file(config_file)
    main(config_data)
