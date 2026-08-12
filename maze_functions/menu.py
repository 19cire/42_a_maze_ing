from maze_functions.show_maze import maze_viewer, clear_screen
from maze_functions.color import change_color
from maze_functions.mazegen import build_the_grid, carve_maze
from a_maze_ing import main


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
    number = int(input("What do you wanna do?"))
    try:
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
    except ValueError as e:
        print(e)
        print("Wrong input! Please, enter a number beteween 1 and 5")
