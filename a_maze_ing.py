#!/usr/bin/python3
# from typing import Any
import sys
import random
from maze_functoins.file_reader import read_file
from maze_functoins.mazegen import build_the_grid, carve_maze


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
    entry: tuple[int] = int(config_data["ENTRY"][0]), int(
        config_data["ENTRY"][1])
    exit: tuple[int] = int(config_data["EXIT"][0]), int(
        config_data["EXIT"][1])
    grid = build_the_grid(
        int(config_data["WIDTH"]), int(config_data["HEIGHT"]))
    print(entry)
    print(exit)

    carve_maze(grid, 3, 3, random.Random(12), entry, exit)


if __name__ == "__main__":
    config_file: str = sys.argv[1]
    config_data: dict[str, str] = read_file(config_file)
    main(config_data)
