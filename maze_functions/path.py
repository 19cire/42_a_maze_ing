from .variables import NORTH, EAST, SOUTH, WEST


def check_directions(point: int) -> list[str]:
    dir: list[str] = []
    if not point & NORTH:
        dir.append("N")
    if not point & EAST:
        dir.append("E")
    if not point & SOUTH:
        dir.append("S")
    if not point & WEST:
        dir.append("W")
    return dir


def go(direction: str,
       x: int,
       y: int,
       queue: list[tuple[int, int]],
       came_from: dict[tuple[int, int], tuple[int, int] | None]
       ) -> None:
    if direction == "N" and (x, y - 1) not in came_from:
        queue.append((x, y - 1))
        came_from[((x, y - 1))] = (x, y)

    if direction == "E" and (x + 1, y) not in came_from:
        queue.append((x + 1, y))
        came_from[((x + 1, y))] = (x, y)

    if direction == "S" and (x, y + 1) not in came_from:
        queue.append((x, y + 1))
        came_from[((x, y + 1))] = (x, y)
    if direction == "W" and (x - 1, y) not in came_from:
        queue.append((x - 1, y))
        came_from[((x - 1, y))] = (x, y)


def shortest_path(grid: list[list[int]],
                  start: tuple[int, int],
                  end: tuple[int, int]
                  ) -> list[tuple[int, int]]:
    queue: list[tuple[int, int]] = [start]
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {start:  None}

    while queue:
        x, y = queue.pop(0)
        if (x, y) == end:
            break
        directions = check_directions(grid[y][x])
        for direction in directions:
            go(direction, x, y, queue, came_from)
    path: list[tuple[int, int]] = []
    current: tuple[int, int] | None = end
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
