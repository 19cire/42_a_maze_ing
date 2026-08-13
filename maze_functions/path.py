from .variables import NORTH, EAST, SOUTH, WEST


def shortest_path(grid: list[list[int]],
                  entry: tuple[int, int],
                  maze_exit: tuple[int, int]
                  ) -> list[tuple[int]]:
    # path: list[tuple[int]] = 0
    # cell: list[int, int]
    dir: list[str] = []
    x = entry[0]
    y = entry[1]
    print(grid[y][x])
    while not [x, y] == [maze_exit[0], maze_exit[1]]:
        if not grid[y][x] & EAST:
            x += 1
            dir.append("E")
    print(dir)
