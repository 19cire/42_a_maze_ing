import sys
from file_reader import read_file, parse_coordinate
from mazegen import MazeGenerator
from maze_functions.show_maze import maze_viewer, clear_screen
from maze_functions.menu import show_menu
from maze_functions.data_validator import (check_data,
                                           SizeError,
                                           LessThanZeroError,
                                           OutOfBoundsError,
                                           PerfectError)


def main(config_data: dict[str, str], new: bool = False) -> None:
    entry: tuple[int, int] = parse_coordinate(config_data["ENTRY"])
    end: tuple[int, int] = parse_coordinate(config_data["EXIT"])
    maze = MazeGenerator(
        int(config_data["WIDTH"]),
        int(config_data["HEIGHT"]),
        entry,
        end,
        int(config_data["SEED"]),
        config_data["PERFECT"] == "True"
    )
    maze.generate()
    maze_viewer(maze.grid, entry, end, maze.blocked)
    try:
        show_menu(maze, config_data)
    except ValueError as e:
        print(
            f"{e.__class__.__name__} Please choose a number between 1 - 5" +
            " and press enter!")
        clear_screen()
        show_menu(maze, config_data)


if __name__ == "__main__":
    if "--perfect" in sys.argv:
        print("PERFECT MODE IS ACTIVATED!!!")

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
