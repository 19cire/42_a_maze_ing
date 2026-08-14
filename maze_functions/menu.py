from .show_maze import maze_viewer, clear_screen
from .color import change_color
from .generator import generate_maze
from .path import shortest_path


def new_color(grid: list[list[int]],
              entry: tuple[int],
              exit: tuple[int]
              ) -> int:
    clear_screen()
    color: int = change_color()
    maze_viewer(grid, entry, exit, color)


def show_path(grid: list[list[int]], entry: tuple[int, int],
              end: tuple[int, int], color: int
              ) -> None:
    path: list[tuple[int, int]] = shortest_path(grid, entry, end)
    maze_viewer(grid, entry, end, color, path)


def hide_path(grid: list[list[int]], entry: tuple[int, int],
              end: tuple[int, int], color: int
              ) -> None:
    clear_screen()
    maze_viewer(grid, entry, end, color)


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
        f.write("\n")
        f.write(f"Entry: {config_data["ENTRY"]}\n")
        f.write(f"EXIT: {config_data["EXIT"]}\n")
        f.write("The shortest path: ???\n")

    clear_screen()
    print("The maze is stored in maze.txt")


def show_menu(grid: list[list[int]],
              config_data: dict[str, str],
              path: bool | None = False
              ) -> None:

    entry: tuple[int] = int(config_data["ENTRY"][0]), int(
        config_data["ENTRY"][1])
    maze_exit: tuple[int] = int(config_data["EXIT"][0]), int(
        config_data["EXIT"][1])
    color: int = 42

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
            color = new_color(grid, entry, maze_exit)
        elif number == 2:
            grid: list[list[int]] = generate_maze(config_data, True)
        elif number == 3:
            if path:
                hide_path(grid, entry, maze_exit, color)
                path = False
            else:
                show_path(grid, entry, maze_exit, color)
                path = True
        elif number == 4:
            store_maze(grid, config_data)
        elif number == 5:
            print("bye!")
            exit(0)
        else:
            print("Wrong input number!")
        show_menu(grid, config_data, path)
    except ValueError as e:
        print(f"{e.__class__.__name__}: Please choose a number between 1 - 5!")
        show_menu(grid, config_data, path)
