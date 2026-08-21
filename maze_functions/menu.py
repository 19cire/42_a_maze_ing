from .show_maze import maze_viewer
from .color import change_color
from mazegen import MazeGenerator, store_maze
from maze_functions.file_reader import parse_coordinate
import random


def show_menu(maze: MazeGenerator,
              config_data: dict[str, str],
              path: bool = True,
              color: int = 42
              ) -> None:

    maze_entry: tuple[int, int] = parse_coordinate(config_data["ENTRY"])
    maze_exit: tuple[int, int] = parse_coordinate(config_data["EXIT"])

    print("====MAZE GENERATOR====")
    print("1) Change color")
    print("2) new maze")
    if path:
        print("3) hide_path")
    else:
        print("3) show_path")
    print("4) store maze")
    print("5) quit")
    number: int = int(input("What do you wanna do?"))

    try:
        if number == 1:
            color = change_color()
            maze_viewer(maze.grid,
                        maze_entry, maze_exit,
                        maze.blocked, color)

        elif number == 2:
            new_maze: MazeGenerator = MazeGenerator(
                int(config_data["WIDTH"]),
                int(config_data["HEIGHT"]),
                maze_entry,
                maze_exit,
                random.randint(0, 256),
                bool(config_data["PERFECT"]))
            new_maze.generate()
            maze = new_maze
            maze_viewer(maze.grid,
                        maze_entry,
                        maze_exit,
                        maze.blocked,
                        color)

        elif number == 3:
            if path:
                maze_viewer(maze.grid, maze_entry, maze_exit,
                            maze.blocked, color, maze.solution)
                path = False
            else:
                maze_viewer(maze.grid, maze_entry, maze_exit,
                            maze.blocked, color)
                path = True
        elif number == 4:
            store_maze(maze.grid, maze_entry, maze_exit,
                       config_data["OUTPUT_FILE"])
        elif number == 5:
            print("bye!")
            exit(0)
        else:
            print("Wrong input number!")
        show_menu(maze, config_data, path, color)
    except ValueError as e:
        print(f"{e.__class__.__name__}: Please choose a number between 1 - 5!")
        show_menu(maze, config_data, path, color)
